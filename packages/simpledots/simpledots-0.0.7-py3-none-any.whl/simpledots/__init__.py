'''
__init__.py: base file for simpledots
Lincoln Ombelets, 2020
'''

__version__ = '0.0.7'
__author__  = '''Lincoln Ombelets'''
__email__   = 'lombelets@caltech.edu'

import os
os.environ['MKL_NUM_THREADS'] = '4'
os.environ['OMP_NUM_THREADS'] = '4'

from .simpledots import WBImage, DotImage, show_two_ims, coloc
from .utils import fetch_image
del simpledots