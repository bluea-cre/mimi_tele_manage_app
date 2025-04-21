import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import argparse
import tkinter as tk
from utils.log_util import (
    LOGI,
    loglevel_s2i,
    set_log_level,
    entrylog_s2i,
    set_entry_log,
)
from core.app import FunctionRunnerApp  # Absolute import
from utils.log_util import *


@log_entry_exit
def main():
    """Main entry point for the Function Runner App."""
    LOGI(
        "<====================================== Start Function Runner App ======================================>"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--loglevel",
        type=str,
        default=None,
        help="Set log level: DEBUG, INFO, WARN, ERROR, VERBOSE, FATAL",
    )
    parser.add_argument(
        "--entrylog",
        type=str,
        default=None,
        help="Enable entry exit log: 1, Yes, yes, Y, y, Enable, enable, True, true, T, t",
    )
    args = parser.parse_args()

    log_level = loglevel_s2i(args.loglevel)
    set_log_level(log_level)
    entry_log = entrylog_s2i(args.entrylog)
    set_entry_log(entry_log)

    LOGI(f"Example log line")

    try:
        root = tk.Tk()
        app = FunctionRunnerApp(root)
        root.mainloop()
    except Exception as e:
        LOGI(f"Application failed to start: {e}")

    LOGI(
        "<====================================== Close Function Runner App ======================================>"
    )


if __name__ == "__main__":
    main()
