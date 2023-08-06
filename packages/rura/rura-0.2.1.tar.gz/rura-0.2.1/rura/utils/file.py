import pandas as pd
import numpy as np
import json


def read_file(path, ext, options={}):
    if ext == 'feather':
        return pd.read_feather(path, **options)
    elif ext == 'csv':
        return pd.read_csv(path, **options)
    elif ext == 'npy':
        try:
            return np.load(path, **options)
        except ValueError:
            return np.load(path, allow_pickle=True, **options)
    elif ext == 'txt':
        with open(path) as f:
            return f.read()
    elif ext == 'json':
        with open(path) as f:
            return json.load(f)
    else:
        raise NotImplementedError


# TODO - Stop computing the final path within here
def save_file(path, ext, data):
    if ext == 'feather':
        data.to_feather(path)
    elif ext == 'csv':
        data.to_csv(path, index=False)
    elif ext == 'npy':
        np.save(path, data)
    elif ext == 'txt':
        with open(path, 'w') as f:
            f.write(data)
    elif ext == 'json':
        with open(path, 'w') as f:
            json.dump(data, f)
    else:
        raise NotImplementedError
