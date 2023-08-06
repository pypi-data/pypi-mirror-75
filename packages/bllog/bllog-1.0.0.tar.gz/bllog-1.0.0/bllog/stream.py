# Output stream for logger

import abc
import copy
import os
import sys

import colorama
import termcolor
from log_symbols import LogSymbols

from bllog.log_classes import LogMessage, LogLevel
from bllog.fomat import LogFormatter

default_console_format = LogFormatter('[{symbol}] {date_time:%Y-%m-%d %H:%M:%S.%f} {thread_id} [{level}]: {message}')
default_file_format = LogFormatter('{date_time:%Y-%m-%d %H:%M:%S.%f} {thread_id} [{level}]: {message}')


class LogStream(abc.ABC):

    def __init__(self):
        self.set_default_format()
        self.is_open = False
        self.level = LogLevel.TRACE

    def set_level(self, lvl: LogLevel):
        self.level = lvl

    def set_formatter(self, fmt: LogFormatter):
        self.formatter = fmt

    @abc.abstractmethod
    def set_default_format(self):
        pass

    @abc.abstractmethod
    def init(self):
        """Initialize the stream here. Ex: setup color, open file, rotate, etc"""
        pass

    @abc.abstractmethod
    def destroy(self):
        """Close the stream. Note that this is not always called, the interpreter can crash on
        force closed"""
        pass

    def open(self):
        if not self.is_open:
            self.init()
            self.is_open = True

    def close(self):
        if self.is_open:
            self.destroy()
            self.is_open = False

    def log(self, msg: LogMessage):
        if not self.is_open:
            self.open()

        if msg.level.value >= self.level.value:
            self.write_log(msg)

    @abc.abstractmethod
    def write_log(self, msg: LogMessage):
        """Write log message to output"""
        pass


class ConsoleStream(LogStream):

    def __init__(self):
        super().__init__()
        self.line_color = False

    def set_default_format(self):
        self.formatter = copy.copy(default_console_format)

    def init(self):
        pass

    def destroy(self):
        """Do nothing :D"""
        pass

    def write_log(self, msg: LogMessage):
        p_message = self.formatter.format(msg)

        if self.line_color:
            p_message = color(p_message, msg.level)

        sys.stdout.write(p_message)
        sys.stdout.write(os.linesep)
        sys.stdout.flush()

    def enable_line_color(self, enabled: bool):
        self.line_color = enabled
        if enabled:
            colorama.init()


class FileStream(LogStream):

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

        self.check_file()

    def set_default_format(self):
        self.formatter = copy.copy(default_file_format)

    def init(self):
        self.fd = open(self.file_name, 'wt')

    def destroy(self):
        self.fd.close()

    def write_log(self, msg: LogMessage):
        p_message = self.formatter.format(msg)
        self.fd.write(p_message)
        self.fd.write('\n')
        self.fd.flush()

    def check_file(self):
        """Truncate file if it already exists"""
        if os.path.exists(self.file_name):
            os.remove(self.file_name)


class StreamBuilder:
    def __init__(self):
        self.proto = None

    def console(self):
        self.proto = ConsoleStream()
        return self

    def named_file(self, file_name: str):
        self.proto = FileStream(file_name)
        return self

    def color_line(self):
        self.proto.enable_line_color(True)
        return self

    def level(self, lvl: LogLevel):
        self.proto.set_level(lvl)
        return self

    def format_level_color(self):
        self.proto.formatter.format_string = self.proto.formatter.format_string.replace('{level}', '{color_level}')
        return self

    def format_symbol_color(self):
        self.proto.formatter.format_string = self.proto.formatter.format_string.replace('{symbol}', '{color_symbol}')
        return self

    def build(self):
        return self.proto


color_map = {
    LogLevel.TRACE: lambda s: termcolor.colored(s, 'grey'),
    LogLevel.DEBUG: lambda s: termcolor.colored(s, 'white'),
    LogLevel.INFO: lambda s: termcolor.colored(s, 'green'),
    LogLevel.WARNING: lambda s: termcolor.colored(s, 'yellow'),
    LogLevel.ERROR: lambda s: termcolor.colored(s, 'red'),
    LogLevel.FATAL: lambda s: termcolor.colored(s, 'red', 'on_white')
}


def color(msg: str, lvl: LogLevel):
    return color_map[lvl](msg)
