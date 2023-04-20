
__version__ = '0.1.0'  # 2023-04-20


from . dv import TimeSeries, CyclicalTimeSeries, NullTimeSeries
from . dv.datum import *
from . gen import RandomTimeSeriesGenerator, RandomCyclicalTimeSeriesGenerator
from . randdurn import RandomDuration
from . trends import *
from . rand1d import GaussianRandomFieldGenerator
from . import util


import os
dirCSV = os.path.join( os.path.dirname( __file__ ), 'csv' )


