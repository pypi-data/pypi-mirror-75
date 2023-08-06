import cirq
import numpy as np
import sympy as sp
from itertools import combinations
from sympy import default_sort_key

import quple

#reference: https://github.com/tensorflow/quantum/blob/v0.3.0/tensorflow_quantum/python/util.py
def symbols_in_op(op):
    """Returns the set of symbols in a parameterized gate."""
    if isinstance(op, cirq.EigenGate):
        return op.exponent.free_symbols

    if isinstance(op, cirq.FSimGate):
        ret = set()
        if isinstance(op.theta, sp.Basic):
            ret |= op.theta.free_symbols
        if isinstance(op.phi, sp.Basic):
            ret |= op.phi.free_symbols
        return ret

    if isinstance(op, cirq.PhasedXPowGate):
        ret = set()
        if isinstance(op.exponent, sp.Basic):
            ret |= op.exponent.free_symbols
        if isinstance(op.phase_exponent, sp.Basic):
            ret |= op.phase_exponent.free_symbols
        return ret

    raise ValueError("Attempted to scan for symbols in circuit with unsupported"
                     " ops inside. Expected op found in tfq.get_supported_gates"
                     " but found: ".format(str(op)))
    
def symbols_in_expr_map(expr_map, to_str=False):
    all_symbols = set()
    for expr in expr_map:
        if isinstance(expr, sp.Basic):
            all_symbols |= expr.free_symbols
    if to_str:
        return sorted([str(x) for x in all_symbols])
    return sorted(list(all_symbols), key=default_sort_key)

def get_circuit_unflattened_symbols(circuit:'quple.QuantumCircuit', to_str=True):
    if isinstance(circuit, quple.QuantumCircuit):
        expr_map = circuit.expr_map
        if expr_map is not None:
            symbols = quple.symbols_in_expr_map(expr_map, to_str=to_str)
    else:
        symbols = quple.get_circuit_symbols(circuit)
    return symbols


#reference: https://github.com/tensorflow/quantum/blob/v0.3.0/tensorflow_quantum/python/util.py
def get_circuit_symbols(circuit, to_str=True):
    all_symbols = set()
    for moment in circuit:
        for op in moment:
            if cirq.is_parameterized(op):
                all_symbols |= symbols_in_op(op.gate)
    if to_str:
        return sorted([str(x) for x in all_symbols])
    return sorted(list(all_symbols), key=default_sort_key)

def get_circuit_qubits(circuit):
    all_qubits = set()
    for moment in circuit:
        for op in moment:
            all_qubits |= set(op._qubits)
    return sorted(list(all_qubits))

def get_circuit_symbols_in_order(circuit):
    all_symbols = set()
    symbols_in_order = []
    for moment in circuit:
        for op in moment:
            if cirq.is_parameterized(op):
                new_symbols = symbols_in_op(op.gate)
                symbols_in_order += (new_symbols - all_symbols)
                all_symbols |= symbols_in_op(op.gate)
    return symbols_in_order

def sample_final_states(circuit, samples=1, data=None):
    import tensorflow_quantum as tfq
    layer = tfq.layers.State()
    symbols = get_circuit_symbols(circuit)
    if symbols:
        if not data:
            data = np.random.rand(samples, len(symbols))*2*np.pi
        tensor_final_states = layer(circuit, symbol_names=symbols, symbol_values=data)
    else:
        tensor_final_states = layer([circuit]*samples)
    final_states = [tensor_state.numpy() for tensor_state in tensor_final_states]
    return final_states

def sample_density_matrices(circuit, samples=1, data=None):
    final_states = sample_final_states(circuit, samples, data=data)
    density_matrices = [cirq.density_matrix_from_state_vector(fs) for fs in final_states] 
    return density_matrices


def sample_fidelities(circuit, samples=1, data=None):
    sample_states_1 = sample_final_states(circuit, samples, data=data)
    sample_states_2 = sample_final_states(circuit, samples, data=data)
    fidelities = []
    for s1, s2 in zip(sample_states_1, sample_states_2):
        fidelities.append(cirq.fidelity(s1, s2))
    return fidelities

def circuit_fidelity_pdf(circuit, samples=3000, bins=100, data=None):
    data = np.array(sample_fidelities(circuit, samples, data=data))
    pdf = np.histogram(data, bins=bins, range=(0,1), density=True)
    return pdf

def Haar_pdf(samples=3000, bins=100):
    data = np.linspace(0., 1., samples)
    pdf = np.histogram(data, bins=bins, range=(0.,1.), density=True)
    return pdf

def circuit_fidelity_plot(circuit, samples=3000, bins=100, data=None, KL=True):      
    import matplotlib.pyplot as plt
    data_pqc = np.array(sample_fidelities(circuit, samples, data=data))
    daa_Haar = np.linspace(0., 1., samples)
    plt.hist(daa_Haar, bins=bins, range=(0.,1.), alpha=0.5, density=True, label='Haar')
    plt.hist(data_pqc, bins=bins, range=(0.,1.), alpha=0.5, density=True, label='PQC')
    plt.legend()
    plt.xlabel('Fidelity')
    plt.ylabel('Probability')
    if KL:
        import scipy as sp
        pdf_pqc = np.histogram(data_pqc, bins=bins, range=(0.,1.), density=True)
        pdf_Haar = np.histogram(daa_Haar, bins=bins, range=(0.,1.), density=True)
        Kullback_Leibler_divergence = sp.stats.entropy(pdf_pqc[0], pdf_Haar[0])
        plt.title('$D_{KL}=$'+str(Kullback_Leibler_divergence))
    return plt

def circuit_expressibility_measure(circuit, samples = 3000, bins=100, data=None, relative=False):
    import scipy as sp
    pdf_pqc = circuit_fidelity_pdf(circuit, samples, bins, data=data)
    pdf_Haar = Haar_pdf(samples, bins)
    Kullback_Leibler_divergence = sp.stats.entropy(pdf_pqc[0], pdf_Haar[0])
    expressibility = Kullback_Leibler_divergence
    if relative:
        expressibility_idle_circuit = (2**circuit.n_qubit-1)*(np.log(bins))
        expressibility = -np.log(expressibility/expressibility_idle_circuit)
    return expressibility

def Meyer_Wallach_measure(state):
    state = np.array(state)
    size = state.shape[0]
    n = int(np.log2(size))
    Q = 0.
    
    def linear_mapping(b:int, j:int) -> np.ndarray:
        keep_indices = [i for i in range(size) if b == ((i & (1 << j))!=0)]
        return state[keep_indices]
    
    def distance(u:np.ndarray, v:np.ndarray) -> float:
        return np.sum(np.abs(np.outer(u,v) - np.outer(v,u))**2)/2
    
    for k in range(n):
        iota_0k = linear_mapping(0, k)
        iota_1k = linear_mapping(1, k)
        Q += distance(iota_0k, iota_1k)
    Q = (4/n)*Q
    return Q
    
        
def circuit_entangling_measure(circuit, samples=200, data=None):
    final_states = sample_final_states(circuit, samples, data=data)
    mw_measures = [Meyer_Wallach_measure(fs) for fs in final_states]
    return np.mean(mw_measures)


def circuit_von_neumann_entropy(circuit, samples=200, data=None):
    density_matrices = sample_density_matrices(circuit, samples, data=data)
    von_neumann_entropy = [cirq.von_neumann_entropy(dm) for dm in density_matrices]
    return np.mean(von_neumann_entropy)
    
    
def gradient_variance_test(circuits, op, symbol=None):
    import tensorflow_quantum as tfq
    import tensorflow as tf
    """Compute the variance of a batch of expectations w.r.t. op on each circuit that 
    contains `symbol`."""
    resolved_circuits = []
    # Resolve irrelevant symbols:
    for circuit in circuits: 
        symbols = get_circuit_symbols(circuit)
        if not len(symbols) > 0:
            raise ValueError('No symbols found in circuit')
        if not symbol:
            symbol = symbols[0]
            symbols = symbols[1:]
        else:
            symbols.remove(symbol)
        resolver = cirq.ParamResolver({s:np.random.uniform() * 2.0 * np.pi for s in symbols})
        resolved_circuits.append(cirq.protocols.resolve_parameters(circuit, resolver))

    # Setup a simple layer to batch compute the expectation gradients.
    expectation = tfq.layers.Expectation()

    # Prep the inputs as tensors
    circuit_tensor = tfq.convert_to_tensor(resolved_circuits)
    n_circuits = len(resolved_circuits)
    values_tensor = tf.convert_to_tensor(
        np.random.uniform(0, 2 * np.pi, (n_circuits, 1)).astype(np.float32))

    # Use TensorFlow GradientTape to track gradients.
    with tf.GradientTape() as g:
        g.watch(values_tensor)
        forward = expectation(circuit_tensor,
                              operators=op,
                              symbol_names=[symbol],
                              symbol_values=values_tensor)

    # Return variance of gradients across all circuits.
    grads = g.gradient(forward, values_tensor)
    grad_var = tf.math.reduce_std(grads, axis=0)
    return grad_var.numpy()[0]

