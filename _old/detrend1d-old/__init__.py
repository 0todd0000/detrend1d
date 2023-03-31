
__version__ = '0.2.1'  # 2023-02-10

import os,pathlib
from . metadata import Metadata
from . import cls
from . import models
from . import rand


Dataset0D = cls.Dataset0D


dirREPO  = pathlib.Path( __file__ ).parent.parent
dirDATA  = os.path.join( dirREPO, 'Data' )





