
__version__ = '0.3.0'  # 2023-03-31

import os,pathlib
from . ts import TimeSeries, CyclicalTimeSeries, NullTimeSeries
from . import datum
from . import random
from . import trends
from . import util


Datum  = datum.Datum


# Dataset0D = cls.Dataset0D
#
#
# dirREPO  = pathlib.Path( __file__ ).parent.parent
# dirDATA  = os.path.join( dirREPO, 'Data' )





