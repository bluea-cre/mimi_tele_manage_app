import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Optional
from gui.utils.tooltip import Tooltip
from gui.frame import CustomFrame
from cfg.constants import SORT_OPTIONS
from utils.log_util import *


class UI:
    """Manages the creation and updating of UI components."""

    def __init__(self, root: tk.Tk, app: "FunctionRunnerApp"):  # type: ignore
        self.root = root
        self.app = app
        self.functions_frame: Optional[CustomFrame] = None
        self.functions_canvas: Optional[tk.Canvas] = None
        self.move_buttons: list = []
        self.edit_save_button: Optional[ttk.Button] = None
        self.background_frame: Optional[CustomFrame] = None
        self._is_background_light = True
        self.create_widgets()

    def create_widgets(self) -> None:
        """Create and arrange all UI widgets."""
        # Create main container frames
        self.background_frame = CustomFrame(self.root, background="white")
        self.background_frame.pack(padx=0, pady=0, fill="both", expand=True)
        main_frame = CustomFrame(self.background_frame, background="white")
        main_frame.pack(padx=(40, 5), pady=(5, 20), fill="both", expand=True)

        # Configure main_frame as a grid
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)  # Row 2 (functions_frame) expands

        # Create UI sections
        self._create_first_row(main_frame)
        self._create_second_row(main_frame)
        self._create_functions_frame(main_frame)

    def _create_first_row(self, main_frame: CustomFrame) -> None:
        """Create the first row with Add New Function and Edit buttons."""
        first_row_frame = CustomFrame(main_frame, background="white")
        first_row_frame.grid(row=0, column=0, pady=10)
        control_frame = CustomFrame(first_row_frame, background="white")
        control_frame.grid(row=0, column=0)

        # Add New Function button
        btn_add_function = ttk.Button(
            control_frame,
            text="Add New Function",
            command=self.app.function_manager.add_new_function,
        )
        btn_add_function.grid(row=0, column=0, padx=5)

        # Edit/Save button
        self.edit_save_button = ttk.Button(
            control_frame,
            text="Edit",
            command=self.app.toggle_edit_mode,
        )
        self.edit_save_button.grid(row=0, column=1, padx=5)
        Tooltip(self.edit_save_button, "Edit function names and order")

    def _create_second_row(self, main_frame: CustomFrame) -> None:
        """Create the second row with Check/Uncheck, Run All, and move buttons."""
        second_row_frame = CustomFrame(main_frame, background="white")
        second_row_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        second_row_frame.grid_columnconfigure(0, weight=0)
        second_row_frame.grid_columnconfigure(1, weight=1)
        second_row_frame.grid_columnconfigure(2, weight=0)

        # Check/Uncheck All button
        btn_check_all = ttk.Button(
            second_row_frame,
            text="Check/Uncheck All",
            command=self.app.function_manager.toggle_all,
        )
        btn_check_all.grid(row=0, column=0, padx=(10, 10), sticky="w")

        # Run All button
        btn_run_all = ttk.Button(
            second_row_frame,
            text="Run All",
            command=self.app.function_manager.run_all,
        )
        btn_run_all.grid(row=0, column=2, padx=(10, 34), sticky="e")

        # Move buttons and sort combobox
        self._create_move_controls(second_row_frame)

    def _create_move_controls(self, parent: CustomFrame) -> None:
        """Create move buttons and sort combobox in a subframe."""
        move_frame = CustomFrame(parent, background="white")
        move_frame.grid(row=0, column=1, padx=(10, 10))

        # Move buttons
        buttons = [
            ("↑", self.app.function_manager.move_up, 1),
            ("↓", self.app.function_manager.move_down, 2),
            ("⇈", self.app.function_manager.move_top, 3),
            ("⇊", self.app.function_manager.move_bottom, 4),
        ]
        self.move_buttons = []
        for text, command, column in buttons:
            btn = ttk.Button(move_frame, text=text, width=6, command=command)
            btn.grid(row=0, column=column, padx=1, sticky="ew")
            self.move_buttons.append(btn)

        # Sort combobox
        sort_combobox = ttk.Combobox(
            move_frame, values=SORT_OPTIONS, state="readonly", width=20
        )
        sort_combobox.grid(row=0, column=6, padx=5)
        sort_combobox.bind("<<ComboboxSelected>>", self.app.on_sort_option_selected)
        sort_combobox.set("Select a sort option")
        Tooltip(sort_combobox, "Sort by option")
        self.move_buttons.append(sort_combobox)

        # Disable move buttons initially
        for btn in self.move_buttons:
            btn.state(["disabled"])

    def _create_functions_frame(self, main_frame: CustomFrame) -> None:
        """Create the scrollable frame for function rows, fixed after row 2."""
        # Outer frame to hold canvas and scrollbar
        functions_outer_frame = CustomFrame(main_frame, background="white")
        functions_outer_frame.grid(row=2, column=0, sticky="nsew", pady=0)
        functions_outer_frame.grid_rowconfigure(0, weight=1)
        functions_outer_frame.grid_columnconfigure(0, weight=1)

        # Canvas for scrolling
        self.functions_canvas = tk.Canvas(
            functions_outer_frame, highlightthickness=0, background="white"
        )
        self.functions_canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        functions_scrollbar = ttk.Scrollbar(
            functions_outer_frame,
            orient="vertical",
            command=self.functions_canvas.yview,
        )
        functions_scrollbar.grid(row=0, column=1, sticky="ns", padx=(2, 2), pady=(1, 0))
        self.functions_canvas.configure(yscrollcommand=functions_scrollbar.set)

        # Inner frame for function rows
        self.functions_frame = CustomFrame(self.functions_canvas, background="white")
        # Create window with fixed anchor at northwest
        canvas_window_id = self.functions_canvas.create_window(
            (0, 0), window=self.functions_frame, anchor="nw", tags="functions_frame"
        )
        self.functions_frame.columnconfigure(2, weight=1)

        # Update scroll region and window size
        def update_scroll_region(event=None):
            self.functions_canvas.configure(
                scrollregion=self.functions_canvas.bbox("all")
            )

        # Configure canvas resizing
        def on_canvas_configure(event):
            # Update the width of the canvas window to match canvas width
            self.functions_canvas.itemconfig(canvas_window_id, width=event.width)
            # Ensure the window stays anchored at (0,0)
            self.functions_canvas.coords(canvas_window_id, 0, 0)
            # Update scroll region
            update_scroll_region()

        # Bind configure events
        self.functions_canvas.bind("<Configure>", on_canvas_configure)
        self.functions_frame.bind("<Configure>", update_scroll_region)

        # Mouse wheel scrolling
        def on_mouse_wheel(event):
            if self.functions_canvas.winfo_viewable():
                # Only scroll if there is content to scroll
                bbox = self.functions_canvas.bbox("all")
                if bbox and bbox[3] > self.functions_canvas.winfo_height():
                    self.functions_canvas.yview_scroll(
                        int(-1 * (event.delta / 120)), "units"
                    )

        main_frame.bind_all("<MouseWheel>", on_mouse_wheel)

        # Initialize scroll region
        self.functions_canvas.after(100, update_scroll_region)

    def create_function_row(
        self, idx: int, filename: str, run_function: Callable, select_row: Callable
    ) -> Dict:
        """Create a single function row in the UI."""
        frame = CustomFrame(self.functions_frame, background="white")
        frame.pack(fill="x", pady=2)
        frame.columnconfigure(2, weight=1)

        var = tk.BooleanVar()
        chk = ttk.Checkbutton(frame, variable=var)
        chk.grid(row=0, column=0, padx=10)
        chk.bind("<Button-1>", lambda e, r=idx - 1: select_row(r))

        lbl_idx = ttk.Label(frame, text=f"No.{idx:03}")
        lbl_idx.grid(row=0, column=1, padx=10)

        name_var = tk.StringVar(value=filename)
        entry_name = ttk.Entry(frame, textvariable=name_var, state="readonly")
        entry_name.grid(row=0, column=2, padx=10, sticky="ew")
        entry_name.bind("<FocusIn>", lambda e, r=idx - 1: select_row(r))

        btn_run = ttk.Button(
            frame,
            text="Run",
            command=lambda: (select_row(idx - 1), run_function(name_var.get())),
        )
        btn_run.grid(row=0, column=3, padx=10)

        return {
            "frame": frame,
            "check_var": var,
            "filename": filename,
            "name_var": name_var,
            "entry": entry_name,
            "run_button": btn_run,
            "label_idx": lbl_idx,
        }

    def update_scrollregion(self) -> None:
        """Update the scroll region of the canvas."""
        self.functions_canvas.configure(scrollregion=self.functions_canvas.bbox("all"))

    def reload_order(self) -> None:
        """Update UI to reflect current row order."""
        style = ttk.Style()
        style.configure("Highlighted.TFrame", background="#d9d9d9")
        style.configure("TFrame", background="white")

        for row in self.app.function_manager.function_rows:
            row["frame"].pack_forget()

        for idx, row in enumerate(self.app.function_manager.function_rows, start=1):
            row["filename"] = row["name_var"].get()
            row["label_idx"].config(text=f"No.{idx:03}")
            row["entry"].config(
                textvariable=row["name_var"],
                state="normal" if self.app.edit_mode else "readonly",
            )
            row["frame"].children["!checkbutton"].config(variable=row["check_var"])
            row["run_button"].config(
                command=lambda nv=row["name_var"], r=idx - 1: (
                    self.app.select_row(r),
                    self.app.function_manager.run_function(nv.get()),
                )
            )
            row["frame"].pack(fill="x", pady=2)

        while len(self.functions_frame.winfo_children()) > len(
            self.app.function_manager.function_rows
        ):
            self.functions_frame.winfo_children()[-1].pack_forget()

        for btn in self.move_buttons:
            btn.state(["!disabled"] if self.app.edit_mode else ["disabled"])

        self.app.select_row(
            self.app.selected_row if self.app.selected_row is not None else -1
        )
        self.update_scrollregion()
