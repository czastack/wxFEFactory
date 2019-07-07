from .view import *
from .aui import *
from .bars import *
from .containers import *
from .controls import *
from .datacontrols import *
from .frames import *
from .menu import *


def __getattr__(name):
    module = __import__('%s.%s' % (__name__, name), fromlist=[name])
    globals()[name] = module
    return module
