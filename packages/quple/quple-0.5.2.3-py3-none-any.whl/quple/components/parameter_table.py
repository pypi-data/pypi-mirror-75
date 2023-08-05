from typing import (Any, Callable, cast, Dict, FrozenSet, Iterable, Iterator,
                    List, Optional, overload, Sequence, Set, Tuple, Type,
                    TYPE_CHECKING, TypeVar, Union)    

import re
import sympy as sp
import numpy as np

class ParameterTable():
    def __init__(self, params: Union[str, List[str], List[sp.Symbol]]=None):
        self._parameters = {}
        if params:
            self.append(params)
    
    @property
    def parameters(self) -> Dict:
        return self._parameters
    
    def count_params(self) -> int:
        count = 0
        for name in self._parameters:
            if isinstance(self._parameters[name], np.ndarray):
                count += self._parameters[name].shape[0]
            else:
                count += 1
        return count
    
    def count_symbols(self) -> int:
        return len(self._parameters)
    
    def pop(self, symbol:str):
        self._parameters.pop(symbol, None)
    
    def __getitem__(self, key):
        return self._parameters[key]
    
    def __len__(self):
        return len(self._parameters)
    
    def __contains__(self, item):
        return item in self._parameters
        
    def append_array(self, symbol:str, size:int):
        self._parameters[symbol] = sp.symarray(symbol, size)
        
    def keys(self):
        return self._parameters.keys()
    
    def values(self):
        return self._parameters.values()
    
    def append(self, parameters: Union[str, List[str], sp.Symbol, List[sp.Symbol]] ):
        if isinstance(parameters, list):
            if all(isinstance(param, str) for param in parameters):
                self._parameters.update(ParameterTable._create_param_key_values(parameters))
            elif all(isinstance(param, sp.Symbol) for param in parameters):
                self._parameters.update({param.name: param for param in parameters})
            else:
                raise ValueError('inconsistent list of parameters passed: {}'.format(parameters))
        elif isinstance(parameters, str):
            self.append([parameters])
        elif isinstance(parameters, sp.Symbol):
            self._parameters.update({parameters.name: parameters})
        else:
            raise TypeError('unsupported parameter type : {}'.format(type(parameters)))
    
    @staticmethod
    def _create_param_key_values(parameters:List[str]) -> Dict:
        return {param: sp.Symbol(param) for param in parameters}
    
    
        