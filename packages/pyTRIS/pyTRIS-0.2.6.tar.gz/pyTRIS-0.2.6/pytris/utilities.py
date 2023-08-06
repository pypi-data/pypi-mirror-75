from functools import wraps


def requires_pandas(func):
    @wraps(func)
    def inner(*args, **kwargs):
        import pandas as pd
        
        if pd.__version__.startswith('0'):
            from pandas.io.json import json_normalize
        else:
            from pandas import json_normalize

        func.__globals__['pd'] = pd
        func.__globals__['json_normalize'] = json_normalize
        
        return func(*args, **kwargs)
    return inner
