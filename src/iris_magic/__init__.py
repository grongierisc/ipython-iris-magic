"""An iris magic"""
__version__ = '0.0.1'

from .iris_magic import IrisMagic

def load_ipython_extension(ipython):
    ipython.register_magics(IrisMagic)