import sys
import os
import tkinter as tk
from core.app import FunctionRunnerApp  # Absolute import
from utils.log_util import LOGI
from utils.cli_util import *


def main() -> None:
    """
    Main entry point for the Function Runner App.
    """
    LOGI(
        "<====================================== Starting Function Runner App ======================================>"
    )

    # Parse command-line arguments
    args = parse_arguments()

    # Configure logging
    configure_logging(args)

    LOGI("Application configuration completed. Launching GUI...")

    try:
        root = tk.Tk()
        app = FunctionRunnerApp(root)
        root.mainloop()
    except Exception as e:
        LOGI(f"Application failed to start: {e}")
    finally:
        LOGI(
            "<====================================== Closing Function Runner App ======================================>"
        )


if __name__ == "__main__":
    main()
