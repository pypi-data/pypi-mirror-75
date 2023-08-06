from typing import Optional, Sequence, List, Dict, Union
from abc import ABC
import logging

import numpy as np
import six

import tensorflow as tf
import tensorflow_quantum as tfq

import cirq
import quple
from quple import ParameterisedCircuit

from pdb import set_trace


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

class DefaultDict(dict):
    def __missing__(self, key):
        return key

class VQC(tf.keras.Sequential):
    def __init__(self, encoding_circuit:'cirq.Circuit', variational_circuit:'cirq.Circuit', 
                 optimizer:Optional[Union[str,tf.keras.optimizers.Optimizer]]='adam', 
                 differentiator:Optional[tfq.differentiators.Differentiator]=None,
                 loss='binary_crossentropy', 
                 activation='sigmoid',
                 metrics=['binary_accuracy'],
                 random_state:int=None,
                 name:str=None, *arg, **args):
        super(VQC, self).__init__()
        self._attributes = DefaultDict({})
        if random_state:
            tf.random.set_seed(random_state)
        self.encoding_circuit = encoding_circuit
        self.variational_circuit = variational_circuit
        circuit_qubits = quple.get_circuit_qubits(variational_circuit)
        self._attributes['qubits'] = circuit_qubits
        self._attributes['n_qubit'] = len(circuit_qubits)
        self.differentiator = differentiator        
        self.activation = activation        
        self.random_state = random_state
        layers = self._get_vqc_layers()
        super(VQC, self).__init__(layers, name)
        self.compile(loss=loss, optimizer=optimizer, metrics=metrics)
        
    def compile(self, optimizer='adam', loss='binary_crossentropy', metrics=['binary_accuracy'], *args, **kwargs):
        super(VQC, self).compile(optimizer, loss, metrics, *args, **kwargs)
        self._attributes['optimizer'] = self.optimizer._name if hasattr(self.optimizer, '_name') \
                                        else self.optimizer.__name__
        self._attributes['metrics'] = [metric._name if hasattr(metric, '_name')\
                                       else metric.__name__ for metric in self.metrics]
        self._attributes['loss'] = [loss.name if hasattr(loss, 'name') \
                                    else loss.__name__ for loss in self.loss_functions]
        
    @property
    def attributes(self):
        return self._attributes

    @property
    def encoding_circuit(self):
        return self._encoding_circuit
    
    @encoding_circuit.setter
    def encoding_circuit(self, val):
        feature_dimension = len(quple.get_circuit_unflattened_symbols(val))
        if not feature_dimension:
            raise ValueError('Encoding circuit must be a parameterised circuit with '
                             'number of parameters matching the feature dimension')
        self._check_circuit_qubits()
        self._encoding_circuit = val
        self._attributes['feature_dimension'] = feature_dimension
        self._attributes['encoding_circuit'] = val.name if isinstance(val, quple.QuantumCircuit) else ''
        self._attributes['encoding_map'] = val.encoding_map.__name__ if isinstance(val, quple.EncodingCircuit) else ''
        logger.info('Registered encoding circuit with feature dimension: {}'.format(feature_dimension))
    
    @property
    def qubits(self):
        return self.attributes['qubits']
    
    @property
    def n_qubit(self) -> int:
        return self.attributes['n_qubit']
        
    @property
    def symbols(self) -> List[str]:
        return self.attributes['symbols']
    
    @property
    def num_parameters(self) -> int:
        return self.attributes['num_parameters']
    
    @property
    def feature_dimension(self) -> int:
        return self.attributes['feature_dimension']
    
    @property
    def variational_circuit(self):
        return self._variational_circuit
    
    @variational_circuit.setter
    def variational_circuit(self, val):
        from pdb import set_trace
        circuit_parameters = quple.get_circuit_symbols(val)
        num_parameters = len(circuit_parameters)
        if not num_parameters:
            raise ValueError('Variational circuit must be a parameterised circuit which'
                             ' the parameters are to be optimized by the optimizer.')
        self._check_circuit_qubits()
        self._variational_circuit = val
        self._readout = [cirq.Z(qubit) for qubit in quple.get_circuit_qubits(val)]
        self._attributes['circuit_parameters'] = circuit_parameters
        self._attributes['num_parameters'] = num_parameters
        self._attributes['variational_circuit'] = val.name if isinstance(val, quple.QuantumCircuit) else ''
        logger.info('Registered variational circuit with number of parameters: {}'.format(num_parameters))
        
    def _check_circuit_qubits(self):
        # make sure both encoding and variational circuits are initialized
        if self.__dict__.get('_encoding_circuit', None) and \
        self.__dict__.get('_variational_circuit', None):
            encoding_circuit_qubits = quple.get_circuit_qubits(self.encoding_circuit)
            variational_circuit_qubits = quple.get_circuit_qubits(self.variational_circuit)
            if set(encoding_circuit_qubits) != set(variational_circuit_qubits):
                raise ValueError('encoding circuit and variational circuit must'
                                 ' have the same qubit layout')
    
    @property
    def readout(self):
        return self._readout
    
    @property
    def differentiator(self):
        return self._differentiator
    
    @differentiator.setter
    def differentiator(self, val):
        if (val != None) and (not isinstance(val, tfq.differentiators.Differentiator)):
            raise ValueError('Only tensorflow quantum differentiator is allowed')
        self._attributes['differentiator'] = val.__name__ if val else ''
        self._differentiator = val
    
    @property
    def activation(self):
        return self._activation
    
    @activation.setter
    def activation(self, val):
        if isinstance(val, six.string_types):
            val = tf.keras.activations.get(val)
        self._attributes['activation'] = val.__name__ if val else ''
        self._activation = val
        
    def _get_vqc_layers(self):
        
        input_layer = tf.keras.layers.Input(shape=(), dtype=tf.string)
        pqc_layer = tfq.layers.PQC(self.variational_circuit,
                                   self.readout,
                                   differentiator=self.differentiator)
        output_layer = tf.keras.layers.Dense(1, activation=self.activation)
        
        return [input_layer, pqc_layer, output_layer]
    def _reset_layers(self):
        self._layers = None
        for layer in self._get_vqc_layers():
            self.add(layer)
        
    def _check_data(self, x):
        if isinstance(x, np.ndarray):
            num_dim = x.ndim
            if x.ndim != 2:
                raise ValueError('Data in numpy array format must be of dimension 2')
            num_var = x.shape[1]
            if num_var != self.feature_dimension:
                raise ValueError('Data has feature dimension {} but the encoding'
                ' circuit has feature dimension {}'.format(num_var, self.feature_dimension))
    
    def convert_to_tensor(self, x:np.ndarray):
        self._check_data(x)
        logger.info('Converting circuits to tensors...')
        return tfq.convert_to_tensor(self.encoding_circuit.resolve_parameters(x))
    
    def run(self, x_train, y_train, x_val, y_val, 
            x_test, y_test, 
            batch_size:Optional[int]=None,
            epochs:int=1, callbacks=None,
            roc_curve=True):
        self._attributes['train_size'] = len(x_train)
        self._attributes['val_size'] = len(x_val)
        self._attributes['test_size'] = len(x_test)
        self._attributes['batch_size'] = batch_size
        self._attributes['epochs'] = epochs   
        self.fit(x_train, y_train, batch_size, epochs,
                 validation_data=(x_val, y_val),
                 callbacks=callbacks)
        if isinstance(x_test, np.ndarray):
            x_test = self.convert_to_tensor(x_test)        
        self.evaluate(x_test, y_test, callbacks=callbacks) 
        if roc_curve:
            self.roc_curve(x_test, y_test, callbacks=callbacks)
        for callback in callbacks:
            if isinstance(callback, quple.VQCLogger):
                callback.reset_logger()
    def fit(self, x, y,
            batch_size:Optional[int]=None,
            epochs:int=1, 
            validation_data=None,
            *args, **kwargs):
        self._attributes['train_size'] = len(x)
        if isinstance(x, np.ndarray):
            x = self.convert_to_tensor(x)
        if validation_data and isinstance(validation_data, tuple):
            self._attributes['val_size'] = len(validation_data[0])
            if isinstance(validation_data[0], np.ndarray):
                x_val = self.convert_to_tensor(validation_data[0])
                validation_data = (x_val, validation_data[1])
        self._attributes['batch_size'] = batch_size
        self._attributes['epochs'] = epochs
        return super(VQC, self).fit(x, y,
                             batch_size=batch_size,
                             epochs=epochs,
                             validation_data=validation_data,
                             *args, **kwargs)
    
    def evaluate(self, x, y, *args, **kwargs):
        self._attributes['test_size'] = len(x)
        if isinstance(x, np.ndarray):
            x = self.convert_to_tensor(x)
        return super(VQC, self).evaluate(x, y, *args, **kwargs)
    
    def predict(self, x, *args, **kwargs):
        self._attributes['predict_size'] = len(x)
        if isinstance(x, np.ndarray):
            x = self.convert_to_tensor(x)
        return super(VQC, self).predict(x, *args, **kwargs)    
    
    def roc_curve(self, x, y, callbacks=None):
        y_true = y
        y_score = self.predict(x)
        from sklearn.metrics import roc_curve, auc
        fpr, tpr, thresholds = roc_curve(y_true, y_score)
        roc_auc = auc(fpr, tpr)
        for callback in callbacks:
            if isinstance(callback, quple.VQCLogger):
                callback.log_roc_curve(fpr, tpr, roc_auc)
        return fpr, tpr, thresholds, roc_auc
        