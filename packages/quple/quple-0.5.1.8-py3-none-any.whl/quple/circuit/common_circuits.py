from quple import QuantumCircuit

def construct_bell_circuit():
    cq = QuantumCircuit(2)
    cq.H(0)
    cq.CNOT((0,1))
    return cq

bell_circuit = construct_bell_circuit()
