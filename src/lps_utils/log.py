import enum
import datetime
import time

import inspect


class DebugLevel(enum.Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    EXCEPTION = 3
    ERROR = 4
    DISABLED = 5

    def __str__(self):
        colored_tags = [
            "\033[1;34m  [DEBUG]  \033[1;39m ",
            "\033[1;32m  [INFO]   \033[1;39m ",
            "\033[1;33m [WARNING] \033[1;39m ",
            "\033[1;35m[EXCEPTION]\033[1;39m ",
            "\033[1;31m  [ERROR]  \033[1;39m ",
            ""
        ]
        return colored_tags[self.value]


    def print(self, message: str) -> None:
        if self.value < DebugConfig.level.value:
            return

        frame = inspect.currentframe()
        caller_frame = frame.f_back
        filename = caller_frame.f_code.co_filename
        lineno = caller_frame.f_lineno
        func_name = caller_frame.f_code.co_name
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        print(f"[{current_time}] {self} {func_name} ({filename}:{lineno}): {message}")

class DebugConfig():
    level = DebugLevel.DEBUG

def debug(message: str) -> None:
    DebugLevel.DEBUG.print(message)

def info(message: str) -> None:
    DebugLevel.INFO.print(message)

def warning(message: str) -> None:
    DebugLevel.WARNING.print(message)
    
def exception(message: str) -> None:
    DebugLevel.EXCEPTION.print(message)
    
def error(message: str) -> None:
    DebugLevel.ERROR.print(message)

def set_debug_log_level() -> None:
    DebugConfig.level = DebugLevel.DEBUG
def set_info_log_level() -> None:
    DebugConfig.level = DebugLevel.INFO
def set_warning_log_level() -> None:
    DebugConfig.level = DebugLevel.WARNING
def set_exception_log_level() -> None:
    DebugConfig.level = DebugLevel.EXCEPTION
def set_error_log_level() -> None:
    DebugConfig.level = DebugLevel.ERROR

def disable_log() -> None:
    DebugConfig.level = DebugLevel.WARNING