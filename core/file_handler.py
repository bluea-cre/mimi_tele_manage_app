import json
import os
from typing import List, Dict
from cfg.constants import ORDER_FILE, WINDOW_SIZE_FILE, DEFAULT_WINDOW_SIZE, FUNCTIONS_DIR
from utils.log_util import *


class FileHandler:
    """Handles file operations for function order and window size."""

    @staticmethod
    @log_entry_exit
    def update_order_file(function_rows: List[Dict]) -> None:
        """Update the .order file with the current function order."""
        with open(ORDER_FILE, "w") as f:
            for row in function_rows:
                f.write(row["filename"] + "\n")
        LOGI("Updated order file")

    @staticmethod
    @log_entry_exit
    def load_window_size() -> tuple[int, int]:
        """Load window size from file or return default."""
        try:
            with open(WINDOW_SIZE_FILE, "r") as f:
                size_data = json.load(f)
                return size_data.get(
                    "width", DEFAULT_WINDOW_SIZE["width"]
                ), size_data.get("height", DEFAULT_WINDOW_SIZE["height"])
        except FileNotFoundError:
            return DEFAULT_WINDOW_SIZE["width"], DEFAULT_WINDOW_SIZE["height"]

    @staticmethod
    @log_entry_exit
    def save_window_size(width: int, height: int) -> None:
        """Save window size to file."""
        size_data = {"width": width, "height": height}
        with open(WINDOW_SIZE_FILE, "w") as f:
            json.dump(size_data, f)
        LOGI("Saved window size")

    @staticmethod
    @log_entry_exit
    def load_function_files() -> List[str]:
        """Load and order function files from the functions directory."""
        if not os.path.exists(FUNCTIONS_DIR):
            os.makedirs(FUNCTIONS_DIR)
        all_files = [f for f in os.listdir(FUNCTIONS_DIR) if f.endswith(".py")]
        ordered_files = []
        if os.path.exists(ORDER_FILE):
            with open(ORDER_FILE, "r") as f:
                ordered_files = [line.strip() for line in f if line.strip()]
            ordered_files = [f for f in ordered_files if f in all_files]
            for f in all_files:
                if f not in ordered_files:
                    ordered_files.append(f)
        else:
            ordered_files = sorted(all_files)
        return ordered_files
