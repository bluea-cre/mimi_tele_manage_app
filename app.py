import tkinter as tk
from typing import Optional
from gui.ui import UI
from function_manager import FunctionManager
from file_handler import FileHandler
from gui.utils.tooltip import Tooltip
from utils.log_util import *


class FunctionRunnerApp:
    """Main application class for the Function Runner GUI."""

    @log_entry_exit
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Function Runner App")
        self.edit_mode: bool = False
        self.selected_row: Optional[int] = None
        self.is_sorted_asc: bool = True
        self.function_manager = FunctionManager(self)
        self.ui = UI(root, self)
        self.load_window_size()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.function_manager.load_functions()

    @log_entry_exit
    def load_window_size(self) -> None:
        """Load and apply window size."""
        width, height = FileHandler.load_window_size()
        self.root.geometry(f"{width}x{height}")

    @log_entry_exit
    def on_close(self) -> None:
        """Handle window close event."""
        FileHandler.save_window_size(self.root.winfo_width(), self.root.winfo_height())
        self.function_manager.save_order_and_names()
        self.root.destroy()

    @log_entry_exit
    def select_row(self, row_idx: int) -> None:
        """Highlight the selected row."""
        if row_idx < len(self.function_manager.function_rows):
            self.selected_row = row_idx
            for idx, row in enumerate(self.function_manager.function_rows):
                bg = "#d9d9d9" if idx == row_idx else "white"
                row["entry"].config(background=bg)
                row["frame"].config(
                    style="Highlighted.TFrame" if idx == row_idx else "TFrame"
                )

    @log_entry_exit
    def toggle_edit_mode(self) -> None:
        """Toggle edit mode and update UI."""
        if (
            hasattr(self.ui.edit_save_button, "tipwindow")
            and self.ui.edit_save_button.tipwindow
        ):
            Tooltip.hide_tip(self.ui.edit_save_button)
        self.edit_mode = not self.edit_mode
        self.ui.edit_save_button.config(text="Save" if self.edit_mode else "Edit")
        if not self.edit_mode:
            self.function_manager.save_order_and_names()
        self.ui.reload_order()

    @log_entry_exit
    def on_sort_option_selected(self, event) -> None:
        """Handle sort option selection."""
        selected_option = self.ui.move_buttons[-1].get()
        LOGI(f"Selected option {selected_option}")
        if selected_option == "Sort Alphabet":
            self.function_manager.sort_alphabet()
        elif selected_option == "Move Checked to Top":
            self.function_manager.move_checked_to_top()
