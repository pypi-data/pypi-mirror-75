from typing import List
import copy
import cirq
import quple
import sympy as sp


def replace_symbol_in_op(op, old_symbol:sp.Symbol, new_symbol:sp.Symbol) -> None:
    """Replace the symbol in a parameterised gate with a new symbol."""
    if isinstance(op, cirq.EigenGate):
        if old_symbol in op.exponent.free_symbols:
            op._exponent = op.exponent.subs(old_symbol, new_symbol)

    if isinstance(op, cirq.FSimGate):
        if isinstance(op.theta, sympy.Basic):
            if old_symbol in op.theta.free_symbols:
                op._theta = op.theta.subs(old_symbol, new_symbol)
        if isinstance(op.phi, sympy.Basic):
            if old_symbol in op.phi.free_symbols:
                op._phi = op.phi.subs(old_symbol, new_symbol)

    if isinstance(op, cirq.PhasedXPowGate):
        if isinstance(op.exponent, sympy.Basic):
            if old_symbol in op.exponent.free_symbols:
                op._exponent = op.exponent.subs(old_symbol, new_symbol)
        if isinstance(op.phase_exponent, sympy.Basic):
            if old_symbol in op.phase_exponent.free_symbols:
                op._phase_exponent = op.phase_exponent.subs(old_symbol, new_symbol)
                
def pqc_symbol_map(circuit:cirq.Circuit, symbols_map) -> cirq.Circuit:
    new_circuit = copy.deepcopy(circuit)
    for moment in new_circuit:
        for op in moment:
            if cirq.is_parameterized(op):
                symbols_in_op = quple.symbols_in_op(op.gate)
                for sym in symbols_in_op:
                    replace_symbol_in_op(op.gate, sym, symbols_map[sym])
    return new_circuit



def merge_pqc(circuits:List[cirq.Circuit], symbol:str='θ') -> cirq.Circuit:
    symbol_size = 0
    if not all(isinstance(circuit, cirq.Circuit) for circuit in circuits):
        raise ValueError('Circuits to be merged must be intances of cirq.Circuit object')
    for circuit in circuits:
        symbol_size += len(quple.get_circuit_symbols_in_order(circuit))
    all_symbols = sp.symarray(symbol, symbol_size)
    qubits = set()
    for circuit in circuits:
        qubits |= set(quple.get_circuit_qubits(circuit))
    qubits = sorted(list(qubits))
    merged_circuit = quple.QuantumCircuit(qubits)
    for circuit in circuits:
        old_symbols = quple.get_circuit_symbols_in_order(circuit)
        new_symbols = all_symbols[:len(old_symbols)]
        all_symbols = all_symbols[len(old_symbols):]
        symbols_map = {old:new for old, new in zip(old_symbols, new_symbols)}
        merged_circuit.append(pqc_symbol_map(circuit, symbols_map))
    return merged_circuit
                        
                        