__version__ = '0.1.0'

import pickle


def to_file(obj, filename):
    with open(filename, 'wb') as fp:
        pickle.dump(obj, fp)


def from_file(filename):
    with open(filename, 'rb') as fp:
        return pickle.load(fp)
