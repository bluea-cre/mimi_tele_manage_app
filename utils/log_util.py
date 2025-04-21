import functools
import logging
import datetime
import os


from cfg.constants import LOG_FILE


# Define public API
__all__ = [
    "set_entry_log",
    "log_entry_exit",
    "set_log_level",
    "get_log_level",
    "get_level_name",
    "loglevel_s2i",
    "entrylog_s2i",
    "LOGF",
    "LOGE",
    "LOGW",
    "LOGI",
    "LOGD",
    "LOGV",
]


# Log levels
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
VERBOSE = 5
VERB = VERBOSE
NOTSET = 0
ENTRY_EXIT = -1

# Private global configuration (only for this file)
_gLogLevel = INFO
_gEntryExitLog = False
_gCallDepth = 0


# Setup basic file logging
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=DEBUG,
    format="%(asctime)s %(message)s [%(filename)s:%(lineno)d = %(funcName)s()]",
    encoding="utf-8",
)


def set_log_level(level):
    """
    Set the global minimum log level.
    """
    global _gLogLevel
    _gLogLevel = level


def get_log_level():
    """
    Get the global minimum log level.
    """
    return _gLogLevel


def get_level_name(level):
    """
    Return the string representation of a log level.
    """
    if level == FATAL:
        return "FATAL"
    elif level == ERROR:
        return "ERROR"
    elif level == WARN:
        return "WARNL"  # all 5 characters for align
    elif level == INFO:
        return "INFOL"  # all 5 characters for align
    elif level == DEBUG:
        return "DEBUG"
    elif level == VERBOSE:
        return "VERBO"
    elif level == ENTRY_EXIT:
        return "EELOG"
    else:
        return "NOSET"


def loglevel_s2i(level_str):
    """
    Convert string to internal log level constant.
    """
    if level_str is None:
        return INFO  # Default is INFO if not specified

    level_str = level_str.upper() if isinstance(level_str, str) else "INFO"

    if level_str in ("FATAL", "CRITICAL"):
        return FATAL
    elif level_str in ("ERROR", "ERR"):
        return ERROR
    elif level_str in ("WARNING", "WARN"):
        return WARN
    elif level_str == "INFO":
        return INFO
    elif level_str in ("DEBUG", "DBG"):
        return DEBUG
    elif level_str in ("VERBOSE", "VERB"):
        return VERBOSE
    elif level_str in ("ENTRY_EXIT", "EE"):
        return ENTRY_EXIT
    else:
        return INFO  # Default if invalid


def set_entry_log(enable: bool):
    """
    Enable or disable entry-exit logging.
    """
    global _gEntryExitLog
    _gEntryExitLog = enable


def entrylog_s2i(entrylog_str):
    """
    Convert string to entry exit log config.
    """
    if entrylog_str is None:
        return False  # Default is Disable

    entrylog_str = entrylog_str.upper() if isinstance(entrylog_str, str) else "False"

    if entrylog_str in (
        "1",
        "Yes",
        "yes",
        "Y",
        "y",
        "Enable",
        "enable",
        "True",
        "true",
        "T",
        "t",
    ):
        return True
    else:
        return False


def log(*args, level=INFO):
    """
    General log function: outputs to both console and file if level is sufficient.
    This function can now handle any number of arguments.
    """
    if level >= _gLogLevel:
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level_name = get_level_name(level)

        # Convert all arguments to strings, ensuring that even complex types are captured
        message = " ".join([str(arg) for arg in args])

        formatted_message = f"[{level_name}] {message}"

        # Print to console
        print(formatted_message)

        # Log to file
        logging.log(logging.INFO, formatted_message, stacklevel=3)


def logee(message, level=ENTRY_EXIT):
    """
    Log function for Entry-Exit log only.
    """
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level_name = get_level_name(level)
    formatted_message = f"[{level_name}] {message}"

    # Log to file
    logging.log(logging.INFO, formatted_message, stacklevel=5)


# Predefined short log functions for each level
def LOGF(*args):
    log(*args, level=FATAL)


def LOGE(*args):
    log(*args, level=ERROR)


def LOGW(*args):
    log(*args, level=WARN)


def LOGI(*args):
    log(*args, level=INFO)


def LOGD(*args):
    log(*args, level=DEBUG)


def LOGV(*args):
    log(*args, level=VERBOSE)


# Colors for terminal output
entry_color = "\033[94m"  # Blue for entry
exit_color = "\033[91m"  # Red for exit
highlight_colors = [
    "\033[92m",  # Green
    "\033[93m",  # Yellow
    "\033[95m",  # Magenta
    "\033[96m",  # Cyan
    "\033[92m",  # Light Green
    "\033[93m",  # Light Yellow
    "\033[95m",  # Light Magenta
    "\033[96m",  # Light Cyan
]
reset_color = "\033[0m"  # Reset color


def log_entry_exit(func):
    """
    Decorator to automatically log function entry and exit with arguments and return value.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if _gEntryExitLog:
            global _gCallDepth
            func_color = highlight_colors[_gCallDepth % len(highlight_colors)]
            indent = "    " * _gCallDepth

            # Log function entry
            console_entry_message = f"{indent}==> {entry_color}Entry: {func_color}{func.__name__}{reset_color}():"  # with args: {args}, kwargs: {kwargs}"
            print(console_entry_message)

            file_entry_message = f"{indent}==> Entry: {func.__name__}():"  # with args: {args}, kwargs: {kwargs}"
            logee(file_entry_message)

            _gCallDepth += 1
            result = func(*args, **kwargs)
            _gCallDepth -= 1

            indent = "    " * _gCallDepth

            # Log function exit
            console_exit_message = f"{indent}<== {exit_color}Exit: {func_color}{func.__name__}{reset_color}():"  # returning: {result}"
            print(console_exit_message)

            file_exit_message = (
                f"{indent}<== Exit: {func.__name__}():"  # returning: {result}"
            )
            logee(file_exit_message)
        else:
            result = func(*args, **kwargs)
        return result

    return wrapper
