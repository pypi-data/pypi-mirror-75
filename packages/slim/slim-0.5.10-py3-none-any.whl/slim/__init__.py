from slim.base.types.doc import ApplicationDocInfo
from slim.ext.decorator import D
from .base.app import Application, CORSOptions
from .base.permission import ALL_PERMISSION, EMPTY_PERMISSION, A
from .utils.json_ex import json_ex_dumps, json_ex_default
from . import base
from . import support
from . import utils

__version__ = '0.5.10'
