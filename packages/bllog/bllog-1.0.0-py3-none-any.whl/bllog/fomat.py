# Log message formatting
import termcolor

from bllog.log_classes import LogLevel, LogSymbols
from bllog.logger import LogMessage

# '{date_time:%Y-%m-%d %H:%M:%S.%f} {thread_id} [{level}]: {message}'
class LogFormatter():

    # TODO Document format
    def __init__(self, fmt: str):
        self.parse_format(fmt)
        self.format_string = fmt

    def parse_format(self, fmt: str):

        self.parse_date(fmt)

        pass

    def format(self, msg: LogMessage):
        r_msg = self.format_string

        r_msg = r_msg.replace('{thread_id}', str(msg.thread_id))
        r_msg = r_msg.replace('{level}', msg.level.name)
        r_msg = r_msg.replace('{message}', msg.message)
        r_msg = r_msg.replace('{name}', msg.name)
        r_msg = r_msg.replace('{symbol}', symbol_map[msg.level])
        r_msg = r_msg.replace('{color_symbol}', color_symbol_map[msg.level])
        r_msg = r_msg.replace('{color_level}', color_level_map[msg.level])

        if self.has_date:
            start = r_msg.find('{date_time')
            end = find_endpos(r_msg, start)
            r_msg = r_msg[:start ] + msg.date_time.strftime(self.date_fmt_str) + r_msg[end + 1:]

        return r_msg

    def parse_date(self, fmt: str):
        try:
            loc = fmt.index('{date_time')
            endpos = find_endpos(fmt, loc)

            date_string = fmt[loc + 1: endpos]
            if ':' in date_string:
                date_format = date_string[date_string.find(':') + 1:]
            else:
                date_format = '%Y-%m-%d %H:%M:%S.%f'
            self.has_date = True
            self.date_fmt_str = date_format

        except ValueError:
            # Not found
            self.has_date = False
            self.date_fmt_str = ''


def find_endpos(msg: str, start: int):
    """Finds the closing } for a open one"""
    lvl = 0
    for i in range(start + 1, len(msg) - 1):
        char = msg[i]
        if char == '{':
            lvl += 1
        elif char == '}':
            if lvl > 0:
                lvl -= 1
            else:
                return i
    raise ValueError('No closing } found')

symbol_map = {
    LogLevel.TRACE: ' ',
    LogLevel.DEBUG: ' ',
    LogLevel.INFO: LogSymbols.INFO.value,
    LogLevel.WARNING: LogSymbols.WARNING.value,
    LogLevel.ERROR: LogSymbols.ERROR.value,
    LogLevel.FATAL: LogSymbols.ERROR.value,
}

color_symbol_map = {
    LogLevel.TRACE: ' ',
    LogLevel.DEBUG: ' ',
    LogLevel.INFO: termcolor.colored(LogSymbols.INFO.value, 'green'),
    LogLevel.WARNING: termcolor.colored(LogSymbols.WARNING.value, 'yellow'),
    LogLevel.ERROR: termcolor.colored(LogSymbols.ERROR.value, 'red'),
    LogLevel.FATAL: termcolor.colored(LogSymbols.ERROR.value, 'red'),
}

color_level_map = {
    LogLevel.TRACE: termcolor.colored('TRACE', 'grey'),
    LogLevel.DEBUG: termcolor.colored('DEBUG', 'white'),
    LogLevel.INFO:  termcolor.colored('INFO', 'green'),
    LogLevel.WARNING: termcolor.colored('WARNING', 'yellow'),
    LogLevel.ERROR: termcolor.colored('ERROR', 'red'),
    LogLevel.FATAL: termcolor.colored('FATAL', 'red', 'on_white'),
}


