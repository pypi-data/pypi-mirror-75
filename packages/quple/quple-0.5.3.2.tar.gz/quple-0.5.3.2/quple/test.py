import numpy as np
import tensorflow as tf

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

import quple
from quple.data_encoding.first_order_expansion import FirstOrderExpansion
from quple.data_encoding.second_order_expansion import SecondOrderExpansion
from quple.data_encoding.encoding_maps import self_product, cosine_product, modified_cosine_product, distance_measure, arithmetic_mean, second_moment
from quple.data_encoding.encoding_maps import sine_cosine_alternate_product, exponential_squared_sum, exponential_cube_sum
from quple.components.data_preparation import prepare_train_val_test
from quple.classifiers.variational_quantum_classifier import VQC
from quple.trial_wavefunction.efficient_su2 import EfficientSU2
from quple.trial_wavefunction.real_amplitudes import RealAmplitudes
from quple.trial_wavefunction.excitation_preserving import ExcitationPreserving
from quple.classifiers.vqc_logger import VQCLogger

# prepare training data
data = np.load('data/hmumu_twojet_0719.npy')
x = data[:,:-1]
y = data[:,-1]
n_qubit = 5
n_event = 1000
trials = 10
batch_size = 64
epochs = 100
preprocessors = [PCA(n_components=n_qubit), StandardScaler(), MinMaxScaler((-1,1))]

first_order_expansion = FirstOrderExpansion(feature_dimension=n_qubit, copies=2)
second_order_expansion_0 = SecondOrderExpansion(feature_dimension=n_qubit, copies=2, entangle_strategy='linear', encoding_map=self_product)
second_order_expansion_1 = SecondOrderExpansion(feature_dimension=n_qubit, copies=2, entangle_strategy='linear', encoding_map=cosine_product)
second_order_expansion_2 = SecondOrderExpansion(feature_dimension=n_qubit, copies=2, entangle_strategy='linear', encoding_map=distance_measure)
second_order_expansion_3 = SecondOrderExpansion(feature_dimension=n_qubit, copies=2, entangle_strategy='linear', encoding_map=arithmetic_mean)
second_order_expansion_4 = SecondOrderExpansion(feature_dimension=n_qubit, copies=2, entangle_strategy='linear', encoding_map=second_moment)
excitation_preserving = ExcitationPreserving(n_qubit=n_qubit, copies=2)
efficient_su2 = EfficientSU2(n_qubit=n_qubit, copies=2)
real_amplitudes = RealAmplitudes(n_qubit=n_qubit, copies=2)

vqc_sets = [VQC(first_order_expansion, real_amplitudes, metrics=['binary_accuracy','AUC']),
			VQC(first_order_expansion, efficient_su2, metrics=['binary_accuracy','AUC']),
			VQC(first_order_expansion, excitation_preserving, metrics=['binary_accuracy','AUC']),
			VQC(second_order_expansion_0, efficient_su2, metrics=['binary_accuracy','AUC']),
			VQC(second_order_expansion_1, efficient_su2, metrics=['binary_accuracy','AUC']),
			VQC(second_order_expansion_2, efficient_su2, metrics=['binary_accuracy','AUC']),
			VQC(second_order_expansion_3, efficient_su2, metrics=['binary_accuracy','AUC']),
			VQC(second_order_expansion_4, efficient_su2, metrics=['binary_accuracy','AUC'])]

from pdb import set_trace
set_trace()
for vqc in vqc_sets:
	logger = VQCLogger()
	x_train, x_val, x_test, y_train, y_val, y_test = prepare_train_val_test(x, y, train_size=n_event, val_size=n_event, test_size=n_event, preprocessors=preprocessors)
	vqc.run(x_train, y_train, x_val, y_val, x_test, y_test, batch_size=batch_size, epochs=epochs, callbacks=[logger])