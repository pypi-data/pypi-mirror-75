from os.path import abspath, join, split
from pandas import read_csv

def get_path(f):
    return split(abspath(f))[0]

def loaddata(module, file_name):
    return read_csv(join(get_path(module), file_name), compression='bz2')
