from asyncio import AbstractEventLoop
from enum import Enum
from inspect import iscoroutinefunction

from structlog import get_logger

from macrobase.exceptions import HookException

log = get_logger('macrobase')


class HookNames(Enum):
    before_start = 'before_start'
    after_stop = 'after_stop'
