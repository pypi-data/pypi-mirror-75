'''Set environment variable telling scikit-glpk where libary lives.'''

import os

def glpk_set_env(libpath):
    '''Set "GLPK_LIB_PATH" environment variable.'''
    os.environ["GLPK_LIB_PATH"] = libpath
