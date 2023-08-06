from typing import List, Union, Optional, Callable, Sequence, Tuple

from quple import ParameterisedCircuit

class ExcitationPreserving(ParameterisedCircuit):
    '''Excitation preserving trial wavefunction

    '''    
    def __init__(self, n_qubit: int, copies: int=2, 
                 entanglement_gate:str='RISWAP',
                 entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None,
                 parameter_symbol:str='θ', name:str='ExcitationPreserving', *args, **kwargs):
        
        allowed_blocks = ['RISWAP', 'FSim']
        if entanglement_gate not in allowed_blocks:
            raise ValueError('Unsupported gate operation {}, choose one of '
                             '{}'.format(entanglement_gate, allowed_blocks))
 
        super().__init__(n_qubit=n_qubit, copies=copies,
                         rotation_blocks='RZ',
                         entanglement_blocks=entanglement_gate,
                         entangle_strategy=entangle_strategy,
                         parameter_symbol=parameter_symbol,
                         name=name,
                         flatten_circuit=False,
                         *args, **kwargs)