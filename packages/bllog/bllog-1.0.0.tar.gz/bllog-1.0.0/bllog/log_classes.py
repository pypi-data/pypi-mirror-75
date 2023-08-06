import platform
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    TRACE = 1
    DEBUG = 2
    INFO = 3
    WARNING = 4
    ERROR = 5
    FATAL = 6


class LogMessage:
    """A log message to be written to the streams"""

    def __init__(self, message: str, lvl: LogLevel, tid: int, date_time: datetime):
        self.date_time: datetime = date_time
        self.thread_id = tid
        self.name = ""
        self.level = lvl
        self.message = message
        self.ex = None

    pass

_MAIN = {
    'info': 'ℹ',
    'success': '✔',
    'warning': '⚠',
    'error': '✖'
}

_FALLBACKS = {
    'info': '¡',
    'success': 'v',
    'warning': '!!',
    'error': '×'
}


def is_supported():
    """Check whether operating system supports main symbols or not.

    Returns
    -------
    boolean
        Whether operating system supports main symbols or not
    """

    os_arch = platform.system()

    if os_arch != 'Windows':
        return True

    return False


_SYMBOLS = _MAIN if is_supported() else _FALLBACKS


class LogSymbols(Enum):
    INFO = _SYMBOLS['info']
    SUCCESS =_SYMBOLS['success']
    WARNING = _SYMBOLS['warning']
    ERROR = _SYMBOLS['error']
