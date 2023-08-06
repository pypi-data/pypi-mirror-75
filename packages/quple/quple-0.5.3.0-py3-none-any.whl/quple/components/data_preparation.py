import numpy as np
from sklearn.model_selection import train_test_split

def _validate_train_val_test_sizes(train_size, val_size, test_size):
    sizes = [train_size, val_size, test_size]
    dtypes = [np.asarray(size).dtype.kind for size in sizes]
    if all(size==None for size in sizes):
        # set default ratios
        train_size = 0.7
        test_size = 0.15
        train_size = 0.15
    elif all(dtype == 'f' for dtype in dtypes):
        sizes_sum = np.sum(sizes)
        if sizes_sum < 0 or sizes_sum > 1:
            raise ValueError(
            'The sum of train_size, test_size and train_size = {}, '
            'should be within (0,1)'.format(sizes_sum))
    elif not all(dtype == 'i' for dtype in dtypes):
        raise ValueError('train_size={}, val_size={}, test_size={} must '
                         'be all integers, all floats or all None'.format(
                             train_size, val_size, test_size))
        
    return tuple(sizes)
    

def train_val_test_split(x:np.ndarray, y:np.ndarray, train_size=None, val_size=None,
                           test_size=None, shuffle=True, random_state=None):
    train_size, val_size, test_size = _validate_train_val_test_sizes(train_size, val_size, test_size)
    x_train, x_val, y_train, y_val = train_test_split(x, y, train_size=train_size, test_size=val_size+test_size,
                                                      shuffle=shuffle, random_state=random_state)
    if np.asarray(val_size).dtype.kind == 'f' and np.asarray(test_size).dtype.kind == 'f':
        normalizer = 1/(val_size+test_size)
        val_size *=normalizer
        test_size *=normalizer
    x_val, x_test, y_val, y_test = train_test_split(x_val, y_val, train_size=val_size,
                                                    test_size=test_size, shuffle=False,
                                                    random_state=random_state)
    return x_train, x_val, x_test, y_train, y_val, y_test

def prepare_train_val_test(x:np.ndarray, y:np.ndarray, train_size=None, val_size=None,
                           test_size=None, preprocessors=None, shuffle=True, random_state=None):
    
    x_train, x_val, x_test, y_train, y_val, y_test = \
    train_val_test_split(x, y, train_size, val_size, test_size, shuffle, random_state)
    
    if preprocessors:
        import sklearn
        for preprocessor in preprocessors:
            if not isinstance(preprocessor, sklearn.base.TransformerMixin):
                raise ValueError('Data preprocessor must be an instance of '
                                 'sklearn.base.TransformerMixin')
            transformer = preprocessor.fit(x_train)
            x_train = transformer.transform(x_train)
            x_val = transformer.transform(x_val)
            x_test = transformer.transform(x_test)
                                           
    return x_train, x_val, x_test, y_train, y_val, y_test  