"""
Logging module with different debug levels and colored output.

This module defines a set of debug levels and functions to print messages with contextual
information. The output includes the timestamp, function name, filename, and line number from where
the log function is called.

Usage:
- See example/log_test.py.
"""
import enum
import datetime

import inspect


class DebugLevel(enum.Enum):
    """ Enum class for different debug levels. """
    DEBUG = 0
    INFO = 1
    WARNING = 2
    EXCEPTION = 3
    ERROR = 4
    DISABLED = 5

    def __str__(self):
        """ Return a string representation of the debug level with color tags."""
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
        """
        Print a message with contextual information if this debug level is enabled.

        Args:
            message (str): The message to print.
        """
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
    """ Configuration class to set the global debug level. """
    level = DebugLevel.DEBUG


def debug(message: str) -> None:
    """ Print a debug level message
    Args:
        message (str): The message to print.
    """
    DebugLevel.DEBUG.print(message)

def info(message: str) -> None:
    """ Print an info level message
    Args:
        message (str): The message to print.
    """
    DebugLevel.INFO.print(message)

def warning(message: str) -> None:
    """ Print a warning level message
    Args:
        message (str): The message to print.
    """
    DebugLevel.WARNING.print(message)

def exception(message: str) -> None:
    """ Print an exception level message
    Args:
        message (str): The message to print.
    """
    DebugLevel.EXCEPTION.print(message)

def error(message: str) -> None:
    """ Print an error level message
    Args:
        message (str): The message to print.
    """
    DebugLevel.ERROR.print(message)

def set_debug_log_level() -> None:
    """ Set the global debug level to DEBUG. """
    DebugConfig.level = DebugLevel.DEBUG

def set_info_log_level() -> None:
    """ Set the global debug level to INFO. """
    DebugConfig.level = DebugLevel.INFO

def set_warning_log_level() -> None:
    """ Set the global debug level to WARNING. """
    DebugConfig.level = DebugLevel.WARNING

def set_exception_log_level() -> None:
    """ Set the global debug level to EXCEPTION. """
    DebugConfig.level = DebugLevel.EXCEPTION

def set_error_log_level() -> None:
    """ Set the global debug level to ERROR. """
    DebugConfig.level = DebugLevel.ERROR

def disable_log() -> None:
    """ Disable logging by setting the global debug level to DISABLED. """
    DebugConfig.level = DebugLevel.DISABLED
