import sys
import argparse
from utils.log_util import *


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the application.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Function Runner Application")
    parser.add_argument(
        "-ll",
        "--loglevel",
        type=str,
        default=None,
        help="Set log level: DEBUG, INFO, WARN, ERROR, VERBOSE, FATAL",
        choices=[
            "DEBUG",
            "INFO",
            "WARN",
            "ERROR",
            "VERBOSE",
            "FATAL",
        ],  # Optional: restrict choices
    )
    parser.add_argument(
        "-ee",
        "--entrylog",
        type=str,
        default=None,
        help="Enable entry/exit log: 1, Yes, yes, Y, y, Enable, enable, True, true, T, t",
    )

    try:
        return parser.parse_args()
    except argparse.ArgumentError as e:
        LOGE(f"Error parsing arguments: {e}")
        sys.exit(1)


def configure_logging(args: argparse.Namespace) -> None:
    """
    Configure logging based on command-line arguments.

    Args:
        args (argparse.Namespace): Parsed arguments.
    """
    log_level = loglevel_s2i(args.loglevel)
    set_log_level(log_level)
    entry_log = entrylog_s2i(args.entrylog)
    set_entry_log(entry_log)
    LOGI(f"Logging configured with log level: {log_level}")
    LOGI(f"Entry/Exit logging configured: {'Enabled' if entry_log else 'Disabled'}")
