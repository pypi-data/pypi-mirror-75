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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create console handler 
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

from pdb import set_trace


class VQC(tf.keras.Sequential):
    def __init__(self, encoding_circuit:'cirq.Circuit', variational_circuit:'cirq.Circuit', 
                 optimizer:Optional[Union[str,tf.keras.optimizers.Optimizer]]=None, 
                 differentiator:Optional[tfq.differentiators.Differentiator]=None,
                 loss='categorical_crossentropy', 
                 activation='sigmoid',
                 metrics=['categorical_accuracy'],
                 random_state:int=None,
                 name:str=None, *arg, **args):
        
        self.encoding_circuit = encoding_circuit
        self.variational_circuit = variational_circuit
        self.differentiator = differentiator        
        self.activation = activation        
        self.random_state = random_state
        layers = self._get_vqc_layers()
        super(VQC, self).__init__(layers, name)
        optimizer = optimizer or tf.keras.optimizers.Adam()       
        self.compile(loss=loss, optimizer=optimizer, metrics=metrics)

    @property
    def encoding_circuit(self):
        return self._encoding_circuit
    
    @encoding_circuit.setter
    def encoding_circuit(self, val):
        feature_dimension = len(quple.get_circuit_symbols(val))
        if not feature_dimension:
            raise ValueError('Encoding circuit must be a parameterised circuit with '
                             'number of parameters matching the feature dimension')
        self._encoding_circuit = val
        if isinstance(val, quple.QuantumCircuit):
            if val.expr_map is not None:
                feature_dimension = len(quple.symbols_in_expr_map(val.expr_map))
        self._feature_dimension = feature_dimension
        logger.info('Registered encoding circuit with feature dimension: {}'.format(feature_dimension))
        
    @property
    def num_parameters(self) -> int:
        return self.num_parameters
    
    @property
    def feature_dimension(self) -> int:
        return self._feature_dimension
    
    @property
    def variational_circuit(self):
        return self._variational_circuit
    
    @variational_circuit.setter
    def variational_circuit(self, val):
        num_parameters = len(quple.get_circuit_symbols(val))
        if not num_parameters:
            raise ValueError('Variational circuit must be a parameterised circuit which'
                             ' the parameters are to be optimized by the optimizer.')
        self._variational_circuit = val
        self._readout = [cirq.Z(qubit) for qubit in quple.get_circuit_qubits(val)]
        self._num_parameters = num_parameters
        logger.info('Registered variational circuit with number of parameters: {}'.format(num_parameters))
        
    # n_qubit
    
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
        self._differentiator = val
    
    @property
    def activation(self):
        return self._activation
    
    @activation.setter
    def activation(self, val):
        if isinstance(val, six.string_types):
            val = tf.keras.activations.get(val)
        self._activation = val
        
    def _get_vqc_layers(self):
        
        input_layer = tf.keras.layers.Input(shape=(), dtype=tf.string)
        pqc_layer = tfq.layers.PQC(self.variational_circuit,
                                   self.readout,
                                   initializer=tf.keras.initializers.RandomUniform(0, 2 * 
                                   np.pi, seed=self.random_state),
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
        return tfq.convert_to_tensor(self.encoding_circuit.resolve_parameters(x))
        
    def fit(self, x, y,
            batch_size:Optional[int]=None,
            epochs:int=1, 
            validation_data=None,
            *args, **kwargs):
        if isinstance(x, np.ndarray):
            x = self.convert_to_tensor(x)
        if validation_data and isinstance(validation_data, tuple):
            if isinstance(validation_data[0], np.ndarray):
                x_val = self.convert_to_tensor(validation_data[0])
                validation_data = (x_val, validation_data[1])
        
        return super(VQC, self).fit(x, y,
                             batch_size=batch_size,
                             epochs=epochs,
                             validation_data=validation_data,
                             *args, **kwargs)
    
    def evaluate(self, x, y, *args, **kwargs):
        if isinstance(x, np.ndarray):
            x = self.convert_to_tensor(x)
        return super(VQC, self).evaluate(x, y, *args, **kwargs)
    
    def predict(self, x, *args, **kwargs):
        if isinstance(x, np.ndarray):
            x = self.convert_to_tensor(x)
        return super(VQC, self).predict(x, *args, **kwargs)    
    
    def roc_curve(self, x, y):
        y_true = y
        y_score = self.predict(x)
        from sklearn.metrics import roc_curve
        return roc_curve(y_true, y_score)
        