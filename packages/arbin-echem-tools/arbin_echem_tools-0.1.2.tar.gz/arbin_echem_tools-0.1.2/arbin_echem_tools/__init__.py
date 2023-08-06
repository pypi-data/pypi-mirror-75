"""Top-level package for Arbin Electrochemical Tools."""
import arbin_echem_tools._version

__author__ = """Vincent Wu"""
__email__ = 'vincentwu@ucsb.edu'
__version__ = __version__ = arbin_echem_tools._version.__version__
from arbin_echem_tools.parse import (readArbin, toDataframe, extractEchem, 
extractCycleEchem, generateSummary, generateEchemSummary, plotEchem)

