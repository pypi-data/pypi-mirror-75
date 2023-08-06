from functools import reduce
import numpy as np
import sympy as sp

from quple.components.interaction_graphs import cyclic

def self_product(x: np.ndarray) -> float:
    """
    Define a function map from R^n to R.

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    coeff = x[0] if len(x) == 1 else reduce(lambda m, n: m * n, x)  
    return coeff
    
def modified_cosine_product(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    cos_x = [sp.cos(x_i) for x_i in x]
    coeff = cos_x[0] if len(x) == 1 else reduce(lambda m, n: m * n, cos_x)  
    return coeff

def cosine_product(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    cos_x = [sp.cos(sp.pi*(x_i+1)/2) for x_i in x]
    coeff = cos_x[0] if len(x) == 1 else reduce(lambda m, n: m * n, cos_x)  
    return coeff

def sine_cosine_alternate_product(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    mix_x = [sp.cos(sp.pi*x[i]) if i%2 else sp.sin(sp.pi*x[i]) for i in range(len(x))]
    coeff = cos_x[0] if len(x) == 1 else reduce(lambda m, n: m * n, mix_x)  
    return coeff

def modified_sine_cosine_alternate_product(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    mix_x = [sp.cos(x[i]) if i%2 else sp.sin(sp.pi*x[i]) for i in range(len(x))]
    coeff = cos_x[0] if len(x) == 1 else reduce(lambda m, n: m * n, mix_x)  
    return coeff

def distance_measure(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    if len(x) == 1:
        coeff = x[0]
    elif len(x) == 2:
        coeff = (x[0] - x[1])/2
    else:
        pairs = cyclic(len(x))
        y = [x[a]-x[b] for a,b in pairs]
        coeff = reduce(lambda m, n: m * n, y)/2**len(pairs)  
    return coeff


def distance_measure(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    if len(x) == 1:
        coeff = x[0]
    elif len(x) == 2:
        coeff = (x[0] - x[1])/2
    else:
        pairs = cyclic(len(x))
        y = [x[a]-x[b] for a,b in pairs]
        coeff = reduce(lambda m, n: m * n, y)/2**len(pairs)  
    return coeff

def one_norm_distance(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    if len(x) == 1:
        coeff = x[0]
    elif len(x) == 2:
        coeff = np.abs(x[0] - x[1])
    else:
        pairs = cyclic(len(x))
        y = [np.abs(x[a]-x[b]) for a,b in pairs]
        coeff = reduce(lambda m, n: m + n, y)/(2*len(pairs))
    return coeff

def two_norm_distance(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    if len(x) == 1:
        coeff = x[0]
    elif len(x) == 2:
        coeff = np.abs(x[0] - x[1])
    else:
        pairs = cyclic(len(x))
        y = [(x[a] - x[b])**2 for a,b in pairs]
        coeff = (reduce(lambda m, n: m + n, y)**(1/2))/np.sqrt(len(pairs))
    return coeff

def arithmetic_mean(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    coeff = x[0] if len(x) == 1 else reduce(lambda m, n: m + n, x)/len(x) 
    return coeff    
    
def second_moment(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    square_x = [x_i**2 for x_i in x]
    coeff = x[0] if len(x) == 1 else (reduce(lambda m, n: m + n, square_x)/len(x))**0.5*2-1
    return coeff   

def third_moment(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    cube_x = [x_i**3 for x_i in x]
    coeff = x[0] if len(x) == 1 else (abs(reduce(lambda m, n: m + n, cube_x))/len(x))**(1/3.0)*2-1
    return coeff 
                                          
def exponential_squared_sum(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    square_x = [x_i**2 for x_i in x]
    coeff = x[0] if len(x) == 1 else (np.e**(reduce(lambda m, n: m + n, square_x)/len(x))*2)/np.e-1
    return coeff         

def exponential_cube_sum(x: np.ndarray) -> float:
    """
    Linear map: f(x) =

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    cube_x = [x_i**3 for x_i in x]
    coeff = x[0] if len(x) == 1 else (np.e**(reduce(lambda m, n: m + n, cube_x)/len(x))*2)/np.e-1
    return coeff     