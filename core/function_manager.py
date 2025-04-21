import importlib.util
import os
from typing import List, Dict, Optional
from tkinter import messagebox
from cfg.constants import FUNCTIONS_DIR
from utils.log_util import *


class FunctionManager:
    """Manages function loading, execution, and sorting."""

    @log_entry_exit
    def __init__(self, app: "FunctionRunnerApp"): # type: ignore
        self.app = app
        self.function_rows: List[Dict] = []

    @log_entry_exit
    def load_functions(self) -> None:
        """Load functions from files and populate rows."""
        from core.file_handler import FileHandler

        ordered_files = FileHandler.load_function_files()
        self.function_rows = []
        for idx, filename in enumerate(ordered_files, start=1):
            self.add_function_row(idx, filename)
        from core.file_handler import FileHandler

        FileHandler.update_order_file(self.function_rows)
        self.app.ui.reload_order()

    @log_entry_exit
    def add_function_row(self, idx: int, filename: str) -> None:
        """Add a new function row to the UI."""
        row = self.app.ui.create_function_row(
            idx, filename, self.run_function, self.app.select_row
        )
        self.function_rows.append(row)

    @log_entry_exit
    def run_function(self, filename: str) -> None:
        """Run a function from a specified file."""
        filepath = os.path.join(FUNCTIONS_DIR, filename)
        spec = importlib.util.spec_from_file_location("module.name", filepath)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                module.main()
            else:
                LOGW(f"{filename} has no main() function.")
        except Exception as e:
            LOGF(f"Failed to run {filename}: {e}")

    @log_entry_exit
    def run_all(self) -> None:
        """Run all checked functions."""
        for row in self.function_rows:
            if row["check_var"].get():
                self.run_function(row["name_var"].get())

    @log_entry_exit
    def toggle_all(self) -> None:
        """Toggle check state of all function rows."""
        current_state = all(row["check_var"].get() for row in self.function_rows)
        for row in self.function_rows:
            row["check_var"].set(not current_state)

    @log_entry_exit
    def add_new_function(self) -> None:
        """Create a new function file and add it to the UI."""
        next_number = len(self.function_rows) + 1
        new_filename = f"function_{next_number:03}.py"
        new_filepath = os.path.join(FUNCTIONS_DIR, new_filename)
        with open(new_filepath, "w") as f:
            f.write(
                f'from utils.log_util import *\n\n\ndef main():\n    LOGI("Running new function: File name: {new_filename}")\n'
            )
        self.add_function_row(len(self.function_rows) + 1, new_filename)
        self.app.ui.reload_order()
        self.app.ui.update_scrollregion()

    @log_entry_exit
    def swap_content(self, row1_idx: int, row2_idx: int) -> None:
        """Swap content between two rows."""
        fields_to_swap = ["filename", "name_var", "check_var"]
        for field in fields_to_swap:
            self.function_rows[row1_idx][field], self.function_rows[row2_idx][field] = (
                self.function_rows[row2_idx][field],
                self.function_rows[row1_idx][field],
            )

    @log_entry_exit
    def move_up(self) -> None:
        """Move the selected row up."""
        if self.app.selected_row is not None and self.app.selected_row > 0:
            self.swap_content(self.app.selected_row, self.app.selected_row - 1)
            self.app.selected_row -= 1
            self.app.ui.reload_order()

    @log_entry_exit
    def move_down(self) -> None:
        """Move the selected row down."""
        if (
            self.app.selected_row is not None
            and self.app.selected_row < len(self.function_rows) - 1
        ):
            self.swap_content(self.app.selected_row, self.app.selected_row + 1)
            self.app.selected_row += 1
            self.app.ui.reload_order()

    @log_entry_exit
    def move_top(self) -> None:
        """Move the selected row to the top."""
        if self.app.selected_row is not None and self.app.selected_row > 0:
            idx = self.app.selected_row
            for i in range(idx, 0, -1):
                self.swap_content(i, i - 1)
            self.app.selected_row = 0
            self.app.ui.reload_order()

    @log_entry_exit
    def move_bottom(self) -> None:
        """Move the selected row to the bottom."""
        if (
            self.app.selected_row is not None
            and self.app.selected_row < len(self.function_rows) - 1
        ):
            idx = self.app.selected_row
            for i in range(idx, len(self.function_rows) - 1):
                self.swap_content(i, i + 1)
            self.app.selected_row = len(self.function_rows) - 1
            self.app.ui.reload_order()

    @log_entry_exit
    def sort_alphabet(self) -> None:
        """Sort rows alphabetically."""
        if messagebox.askyesno("Sort by Alphabet", "Are you sure you want to sort?"):
            content_list = [
                {
                    "filename": row["filename"],
                    "name_var": row["name_var"],
                    "check_var": row["check_var"],
                    "original_idx": i,
                }
                for i, row in enumerate(self.function_rows)
            ]
            content_list.sort(
                key=lambda x: x["name_var"].get(), reverse=not self.app.is_sorted_asc
            )
            self.app.is_sorted_asc = not self.app.is_sorted_asc

            selected_content = (
                self.function_rows[self.app.selected_row]["name_var"].get()
                if self.app.selected_row is not None
                else None
            )

            for i, content in enumerate(content_list):
                self.function_rows[i]["filename"] = content["filename"]
                self.function_rows[i]["name_var"] = content["name_var"]
                self.function_rows[i]["check_var"] = content["check_var"]

            if selected_content:
                for i, row in enumerate(self.function_rows):
                    if row["name_var"].get() == selected_content:
                        self.app.selected_row = i
                        break

            self.app.ui.reload_order()

    @log_entry_exit
    def move_checked_to_top(self) -> None:
        """Move checked rows to the top."""
        content_list = [
            {
                "filename": row["filename"],
                "name_var": row["name_var"],
                "check_var": row["check_var"],
                "is_checked": row["check_var"].get(),
                "original_idx": i,
            }
            for i, row in enumerate(self.function_rows)
        ]
        checked_content = [c for c in content_list if c["is_checked"]]
        unchecked_content = [c for c in content_list if not c["is_checked"]]

        selected_content = (
            self.function_rows[self.app.selected_row]["name_var"].get()
            if self.app.selected_row is not None
            else None
        )

        new_content = checked_content + unchecked_content
        for i, content in enumerate(new_content):
            self.function_rows[i]["filename"] = content["filename"]
            self.function_rows[i]["name_var"] = content["name_var"]
            self.function_rows[i]["check_var"] = content["check_var"]

        if selected_content:
            for i, row in enumerate(self.function_rows):
                if row["name_var"].get() == selected_content:
                    self.app.selected_row = i
                    break

        self.app.ui.reload_order()

    @log_entry_exit
    def save_order_and_names(self) -> None:
        """Save function order and rename files as needed."""
        from core.file_handler import FileHandler

        for row in self.function_rows:
            new_name = row["name_var"].get().replace(" ", "_")
            if not new_name.endswith(".py"):
                new_name += ".py"
            old_name = row["filename"]
            old_path = os.path.join(FUNCTIONS_DIR, old_name)
            new_path = os.path.join(FUNCTIONS_DIR, new_name)
            if old_name != new_name:
                os.rename(old_path, new_path)
                LOGI(f"Renamed {old_name} → {new_name}")
                row["filename"] = new_name
        FileHandler.update_order_file(self.function_rows)
        LOGI("Functions saved:", [row["filename"] for row in self.function_rows])
