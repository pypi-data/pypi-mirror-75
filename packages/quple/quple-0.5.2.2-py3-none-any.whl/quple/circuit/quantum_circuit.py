from abc import ABC, abstractmethod
import itertools
from typing import (Any, Callable, cast, Dict, FrozenSet, Iterable, Iterator,
                    List, Optional, overload, Sequence, Set, Tuple, Type,
                    TYPE_CHECKING, TypeVar, Union)
import re
import numpy as np 
from pdb import set_trace
import sympy

import cirq   
from cirq import  devices, GridQubit 
from cirq.circuits import InsertStrategy

import quple
from quple.circuit.qubit_register import QubitRegister
from quple.components.parameter_table import ParameterTable


# InsertStrategy.EARLIEST, InsertStrategy.NEW, InsertStrategy.INLINE and InsertStrategy.NEW_THEN_INLINE

kGateMapping = {
        "H": cirq.H, # Hadamard gate
        "I": cirq.I,  # one-qubit Identity gate
        "S": cirq.S, # Clifford S gate
        "T": cirq.T, # non-Clifford T gate
        'X': cirq.X, # Pauli-X gate
        "Y": cirq.Y, # Pauli-Y gate
        "Z": cirq.Z, # Pauli-Z gate
        "PauliX": cirq.X, # Pauli-X gate
        "PauliY": cirq.Y, # Pauli-Y gate
        "PauliZ": cirq.Z, # Pauli-Z gate
        "CX": cirq.CX, # Controlled-NOT gate
        "CNOT": cirq.CNOT, # Controlled-NOT gate
        "CZ": cirq.CZ, # Controlled-Z gate
        "XX": cirq.XX, # tensor product of two X gates
        "YY": cirq.YY, # tensor product of two Y gates
        "ZZ": cirq.ZZ, # tensor product of two Z gates
        "RX": cirq.rx, # rotation along X axis
        "RY": cirq.ry, # rotation along Y axis
        "RZ": cirq.rz, # rotation along Z axis
        "CCNOT": cirq.CCNOT, # Toffoli gate
        "CCX": cirq.CCX, # Toffoli gate
        "Toffoli": cirq.TOFFOLI, # Toffoli gate
        "SWAP": cirq.SWAP, # SWAP gate
        "CSWAP": cirq.CSWAP, # Controlled SWAP gate
        "ISWAP": cirq.ISWAP, # ISWAP gate
        "RISWAP": cirq.riswap, #Rotation ISWAP gate (X⊗X + Y⊗Y)
        "FSim": cirq.FSimGate, # Fermionic simulation gate
        "Fredkin": cirq.FREDKIN, # Controlled SWAP gate
    }


class QuantumCircuit(cirq.Circuit):
    def __init__(self, n_qubit:Union[int, Sequence[GridQubit]]=0, name:str=None,
                insert_strategy:InsertStrategy=None) -> None:
        super().__init__()
        self._name = 'qc' or name
        self._qr = QubitRegister(n_qubit)
        self._parameter_table = ParameterTable()
        self._insert_strategy = insert_strategy or InsertStrategy.INLINE
        self._expr_map = None
        
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def n_qubit(self) -> int:
        return self._qr.size
    

    @n_qubit.setter
    def n_qubit(self, value:int):
        self._qr = QubitRegister(value)
    
    @property
    def circuit(self):
        return self
    
    @property
    def parameter_table(self):
        return self._parameter_table
    
    @property
    def qr(self):
        return self._qr

    @property
    def qubits(self):
        return self._qr.qubits
    
    @property
    def insert_strategy(self):
        return self._insert_strategy

    @property
    def diagram(self):
        print(self)
    
    @property
    def expr_map(self):
        return self._expr_map
    
    @staticmethod
    def _parse_gate_operation(gate_name:str):
        if gate_name in kGateMapping:
            return kGateMapping[gate_name]
        else:
            raise KeyError("Unknown gate operation {}".format(gate_name))

    @property
    def symbols(self):
        return quple.get_circuit_symbols(self)  

    def apply_gate_operation(self, operation:[str, cirq.Gate], qubit_expr):
        if isinstance(operation, str):
            operation = QuantumCircuit._parse_gate_operation(operation)
        qubit_sequence = self.qr.get(qubit_expr)
        strategy = self.insert_strategy
        if all(isinstance(qubits, GridQubit) for qubits in qubit_sequence):
            self.append([operation(qubit) for qubit in qubit_sequence], strategy=strategy)
        elif all(isinstance(qubits, tuple) for qubits in qubit_sequence):
            self.append([operation(*qubits) for qubits in qubit_sequence], strategy=strategy)
        else:
            raise ValueError('Inconsistent qubit representation: {}'.format(qubit_sequence))
            
    def get_param_resolver(self, param_values: Dict):
        return cirq.ParamResolver(param_values)

    def S(self, qubit_expr):
        '''Clifford-S gate
        '''
        self.apply_gate_operation(cirq.ops.S, qubit_expr)

    def T(self, qubit_expr):
        '''Non-Clifford-T gate
        '''
        self.apply_gate_operation(cirq.ops.T, qubit_expr)


    def H(self, qubit_expr):
        '''Hadamard gate
        '''
        self.apply_gate_operation(cirq.ops.H, qubit_expr)
    
    def RX(self, theta:Union[int, float], qubit_expr):
        self.apply_gate_operation(cirq.ops.rx(theta), qubit_expr)

    def RY(self, theta:Union[int, float], qubit_expr):
        self.apply_gate_operation(cirq.ops.ry(theta), qubit_expr)

    def RZ(self, theta:Union[int, float], qubit_expr):
        self.apply_gate_operation(cirq.ops.rz(theta), qubit_expr)                
    
    def SWAP(self, qubit_expr):
        '''SWAP gate
        '''
        self.apply_gate_operation(cirq.ops.SWAP, qubit_expr)
    

    def PauliX(self, qubit_expr):
        self.apply_gate_operation(cirq.X, qubit_expr)
        
    def PauliY(self, qubit_expr):
        self.apply_gate_operation(cirq.Y, qubit_expr)

    def PauliZ(self, qubit_expr):
        self.apply_gate_operation(cirq.Z, qubit_expr)
        

    def CNOT(self, qubit_expr):
        '''Controlled NOT gate
        '''
        self.apply_gate_operation(cirq.ops.CNOT, qubit_expr)
    
    def Toffoli(self, qubit_expr):
        '''Toffoli gate
        '''
        self.apply_gate_operation(cirq.ops.TOFFOLI, qubit_expr)

    def PhaseShift(self, phi, qubit_expr):
        '''PhaseShit gate
        Perform PhaseShift gate operation
        '''
        self.apply_gate_operation(cirq.ZPowGate(exponent=phi / np.pi), qubit_expr)
            
    def CX(self, qubit_expr):
        '''Equivalent to CNOT gate
        Perform controlled-X gate operation
        '''
        self.apply_gate_operation(cirq.ops.CX, qubit_expr)
  
    def CZ(self, qubit_expr):
        '''Controlled-Z gate
        Perform controlled-X gate operation
        '''
        self.apply_gate_operation(cirq.ops.CZ, qubit_expr)
        
    def clear(self) -> None:
        '''
        clear the content of the circuit
        '''
        self._moments = []
        self._parameter_table = ParameterTable()
        
    def _entangled_qubit_pairing(self, qubits: Sequence[int], 
        *args, **kwargs) -> List[Tuple[int]]:
        '''determines how qubits are paired in the entanglement operation
        can be overridden
        Args:
            qubits: qubits to be entangled
        Return:
            list of pair of qubit indices for entanglement
        Example:
        >>> cq = EntanglementCircuit(n_qubit=5)
        >>> cq._entangled_qubit_pairing((1,3,4)) #entangle qubits 1, 3 and 4
        [(1,3), (3,4)]
        '''
        pairing_indices = [(qubits[i], qubits[i+1]) for i in range(len(qubits)-1)]
        
        return pairing_indices
    
    def entangle(self, qubits:Sequence[int],
                 inverse:bool=False,
                 gate:cirq.Gate=cirq.ops.CNOT):
        '''entangle qubits in a quantum cirquit
        Args:
            qubits: qubits to be entangled
            inverse: reverse the order of operation
            gate: gate operation that entangles the qubits
        Example:
        >>> cq = QuantumCircuit(n_qubit=5)
        >>> cq.entangle((1,2))
        >>> cq.entangle((0,3,4))
                       ┌──┐
            (0, 0): ─────@────────
                         │
            (1, 0): ────@┼────────
                        ││
            (2, 0): ────X┼────────
                         │
            (3, 0): ─────X────@───
                              │
            (4, 0): ──────────X───
                       └──┘
        '''
        
        pairing_indices = self._entangled_qubit_pairing(qubits)
        qubit_pairs = self.qr.get(pairing_indices)
        if inverse:
            qubit_pairs = qubit_pairs[::-1]
        self.append([gate(*qpair) for qpair in qubit_pairs])  
    def measure(self, qubit_idx: int, key=None):
        qubit = self.qr.get(qubit_idx)[0]
        self.append(cirq.measure(qubit, key=key))
    
    def assign(self, circuit:'cirq.Circuit'):
        self._moments = circuit._moments
    
    @classmethod
    def from_cirq(cls, circuit:cirq.Circuit):
        qubits = quple.get_circuit_qubits(circuit)
        symbols = quple.get_circuit_symbols(circuit)
        cq = cls(qubits)
        cq._parameter_table.append(symbols)
        cq.append(circuit)
        return cq
    
    def new_layer(self, name:str=None, *args, **kwargs):
        '''New circuit layer
        Create a circuit block that is a new instance of the current circuit type
        '''
        return self.__class__(self.n_qubit, name=name, *args, **kwargs)
    
    @property
    def parameters(self):
        return self.symbols
    
    def get_parameter_resolver(self, vals:np.ndarray) -> Union['cirq.ParamResolver',List['cirq.ParamResolver']]:
        ndim = vals.ndim
        if ndim == 1:
            vals = vals.reshape(-1,vals.size)
        elif ndim != 2:
            raise ValueError('values to resolve must be a numpy array of dimension 1 or 2')
            
        resolver = cirq.ListSweep([cirq.ParamResolver({param:value for param, value in 
                                   np.column_stack((self.parameters,val))}) for val in vals])
        if self.expr_map:
            resolver = cirq.ListSweep([self.expr_map.transform_params(params) for params in resolver])
        
        if ndim == 1:
            resolver = resolver[0]
            
        return resolver

    def resolve_parameters(self, vals:np.ndarray)-> Union['cirq.Circuit', List['cirq.Circuit']]:
        ndim = vals.ndim
        param_resolver = self.get_parameter_resolver(vals)
        if ndim == 1:
            return cirq.protocols.resolve_parameters(self, param_resolver)
        elif ndim == 2:
            return [cirq.protocols.resolve_parameters(self, params) for params in param_resolver]
        else:
            return None
    def flatten(self):
        # get flattened circuit and corresponding expr_map
        cq_flat, expr_map = cirq.flatten(self)
        self.assign(cq_flat)
        self._expr_map = expr_map    
            