# The main logger implementation
import threading
from datetime import datetime

from bllog.log_classes import LogMessage, LogLevel
from bllog.stream import LogStream



class Logger:

    def __init__(self, name: str = ''):
        self.streams = []
        self.name = name
        self.closed = False

    def add_stream(self, stream: LogStream):
        self.streams.append(stream)
        stream.open()

    def log(self, msg: LogMessage):
        if self.closed:
            raise IOError('Logger already closed')

        msg.name = self.name
        for stream in self.streams:
            stream: LogStream = stream
            stream.log(msg)

    def close(self):
        for s in self.streams:
            s.close()
        self.closed = True

    def __del__(self):
        self.close()

    def make_log(self, lvl: LogLevel, msg: str):
        lm = LogMessage(msg, lvl, threading.get_ident(), datetime.now())
        self.log(lm)

    def trace(self, msg: str):
        self.make_log(LogLevel.TRACE, msg)

    def debug(self, msg: str):
        self.make_log(LogLevel.DEBUG, msg)

    def info(self, msg: str):
        self.make_log(LogLevel.INFO, msg)

    def warning(self, msg: str):
        self.make_log(LogLevel.WARNING, msg)

    def error(self, msg: str):
        self.make_log(LogLevel.ERROR, msg)

    def fatal(self, msg: str):
        self.make_log(LogLevel.FATAL, msg)

class LoggerFactory:

    def __init__(self):
        self.streams = []

    def get_logger(self, name: str):
        lg = LoggerBuilder().name(name).streams(self.streams).build()


class LoggerBuilder:

    def __init__(self):
        self.m_streams = []
        self.m_name = ''

    def streams(self, streams):
        for s in streams:
            self.m_streams.append(s)
        return self

    def name(self, name: str):
        self.m_name = name
        return self

    def build(self) -> Logger:
        log = Logger(self.m_name)
        log.streams = self.m_streams

        return log
