# read version from installed package
from importlib.metadata import version
from .dcdcpy import DataConnector

__version__ = version("dcdcpy")
