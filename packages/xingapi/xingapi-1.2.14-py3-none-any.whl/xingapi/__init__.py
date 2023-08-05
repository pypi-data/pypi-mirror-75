__version__ = '1.2.14'

import sys
if sys.platform != 'win32':
    raise Exception('xingapi requires 32bit working environment')

from xingapi.api.res import Res
from xingapi.api.log import Logger
from xingapi.api.xasession import Session
from xingapi.api.xaquery import Query
from xingapi.api.xareal import Real, RealManager

from xingapi.app.vanila import App