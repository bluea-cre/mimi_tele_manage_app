import os
import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox
import functools
import argparse


FUNCTIONS_DIR = "functions"
ORDER_FILE = os.path.join(FUNCTIONS_DIR, ".order")

DEBUG_LOG = False
CALL_DEEP = 0

# ANSI escape code to change text color
entry_color = "\033[94m"  # Blue color for entry
exit_color = "\033[91m"  # Red color for exit
highlight_color = [
    "\033[92m",  # Green
    "\033[93m",  # Yellow
    "\033[95m",  # Magenta
    "\033[96m",  # Cyan
    "\033[92m",  # Light Green
    "\033[93m",  # Light Yellow
    "\033[95m",  # Light Magenta
    "\033[96m",  # Light Cyan
]
reset_color = "\033[0m"  # Reset to normal color


def empty_function():
    print("Empty function\n")


def log_entry_exit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if DEBUG_LOG:
            global CALL_DEEP
            global entry_color
            global exit_color
            global highlight_color
            global reset_color
            func_color = highlight_color[CALL_DEEP % len(highlight_color)]
            indent = "    " * CALL_DEEP
            print(
                f"{indent}==> {entry_color}Entry: {func_color}{func.__name__}{reset_color} with arguments: {args}, {kwargs}"
            )
            CALL_DEEP += 1
            result = func(*args, **kwargs)
            CALL_DEEP -= 1
            indent = "    " * CALL_DEEP
            print(
                f"{indent}<== {exit_color}Exit: {func_color}{func.__name__}{reset_color} with result: {result}"
            )
        else:
            result = func(*args, **kwargs)
        return result

    return wrapper


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 1
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("tahoma", "8", "normal"),
        )
        label.pack(ipadx=1, ipady=1)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


class FunctionRunnerApp:
    @log_entry_exit
    def __init__(self, root):
        self.root = root
        self.root.title("Function Runner App")

        self.function_files = []
        self.function_rows = []

        self.edit_mode = False
        self.selected_row = None  # Track the currently focused row
        self.is_sorted_asc = (
            True  # Biến trạng thái để kiểm tra thứ tự sắp xếp (tăng dần hoặc giảm dần)
        )

        self.create_widgets()
        self.load_functions()

    @log_entry_exit
    def create_widgets(self):
        # Add main_frame to wrap all UI with margins
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        control_frame = ttk.Frame(main_frame)  # Change parent to main_frame
        control_frame.pack(pady=10)

        self.btn_check_all = ttk.Button(
            control_frame, text="Check/Uncheck All", command=self.toggle_all
        )
        self.btn_check_all.grid(row=0, column=0, padx=5)

        self.btn_run_all = ttk.Button(
            control_frame, text="Run All", command=self.run_all
        )
        self.btn_run_all.grid(row=0, column=1, padx=5)

        self.edit_save_button = ttk.Button(
            control_frame, text="Edit", command=self.toggle_edit_mode
        )
        self.edit_save_button.grid(row=0, column=2, padx=5)
        self.edit_tooltip = Tooltip(
            self.edit_save_button, "Edit function names and order"
        )

        self.btn_add_function = ttk.Button(
            control_frame, text="Add New Function", command=self.add_new_function
        )
        self.btn_add_function.grid(row=0, column=3, padx=5)

        # New row for move buttons
        move_frame = ttk.Frame(main_frame)  # Change parent to main_frame
        move_frame.pack(pady=5)

        self.btn_move_up = ttk.Button(
            move_frame, text="↑", width=6, command=self.move_up
        )
        self.btn_move_up.grid(row=0, column=0, padx=1)
        self.btn_move_down = ttk.Button(
            move_frame, text="↓", width=6, command=self.move_down
        )
        self.btn_move_down.grid(row=0, column=1, padx=1)
        self.btn_move_top = ttk.Button(
            move_frame, text="⇈", width=6, command=self.move_top
        )
        self.btn_move_top.grid(row=0, column=2, padx=1)
        self.btn_move_bottom = ttk.Button(
            move_frame, text="⇊", width=6, command=self.move_bottom
        )
        self.btn_move_bottom.grid(row=0, column=3, padx=1)
        self.btn_sort_alpha = ttk.Button(
            move_frame, text="Alphabet Sort", command=self.sort_alphabet
        )
        self.btn_sort_alpha.grid(row=0, column=4, padx=5)

        self.move_buttons = [
            self.btn_move_up,
            self.btn_move_down,
            self.btn_move_top,
            self.btn_move_bottom,
            self.btn_sort_alpha,
        ]
        for btn in self.move_buttons:
            btn.state(["disabled"])  # Initially disabled

        self.functions_frame = ttk.Frame(main_frame)  # Change parent to main_frame
        self.functions_frame.pack(pady=10, fill="x")
        # Configure column weight for function name entry to expand
        self.functions_frame.columnconfigure(2, weight=1)

    @log_entry_exit
    def load_functions(self):
        if not os.path.exists(FUNCTIONS_DIR):
            os.makedirs(FUNCTIONS_DIR)
        all_files = [f for f in os.listdir(FUNCTIONS_DIR) if f.endswith(".py")]
        if os.path.exists(ORDER_FILE):
            with open(ORDER_FILE, "r") as f:
                ordered_files = [line.strip() for line in f if line.strip()]
            self.function_files = [f for f in ordered_files if f in all_files]
            for f in all_files:
                if f not in self.function_files:
                    self.function_files.append(f)
        else:
            self.function_files = sorted(all_files)
        self.reload_order()

    @log_entry_exit
    def add_function_row(self, idx, filename):
        frame = ttk.Frame(self.functions_frame)
        frame.pack(fill="x", pady=2)
        frame.columnconfigure(2, weight=1)

        var = tk.BooleanVar()
        chk = ttk.Checkbutton(frame, variable=var)
        chk.grid(row=0, column=0, padx=10)
        chk.bind("<Button-1>", lambda e, r=idx - 1: self.select_row(r))

        lbl_idx = ttk.Label(frame, text=f"No.{idx:03}")
        lbl_idx.grid(row=0, column=1, padx=10)

        name_var = tk.StringVar(value=filename)
        entry_name = ttk.Entry(frame, textvariable=name_var, state="readonly")
        entry_name.grid(row=0, column=2, padx=10, sticky="ew")
        entry_name.bind(
            "<FocusIn>", lambda e, r=idx - 1: self.select_row(r)
        )  # Update row index

        btn_run = ttk.Button(
            frame,
            text="Run",
            command=lambda nv=name_var, r=idx - 1: (
                self.select_row(r),
                self.run_function(nv.get()),
            )[-1],
        )
        btn_run.grid(row=0, column=3, padx=10)

        self.function_rows.append(
            {
                "frame": frame,
                "check_var": var,
                "filename": filename,
                "name_var": name_var,
                "entry": entry_name,
                "run_button": btn_run,
                "label_idx": lbl_idx,
            }
        )

    @log_entry_exit
    def select_row(self, row_idx):
        if row_idx < len(self.function_rows):
            self.selected_row = row_idx
            for idx, row in enumerate(self.function_rows):
                bg = "#d9d9d9" if idx == row_idx else "white"
                row["entry"].config(background=bg)
                row["frame"].config(
                    style="Highlighted.TFrame" if idx == row_idx else "TFrame"
                )

    @log_entry_exit
    def toggle_all(self):
        current_state = all(row["check_var"].get() for row in self.function_rows)
        for row in self.function_rows:
            row["check_var"].set(not current_state)

    @log_entry_exit
    def run_all(self):
        for row in self.function_rows:
            if row["check_var"].get():
                self.run_function(row["name_var"].get())

    @log_entry_exit
    def run_function(self, filename):
        filepath = os.path.join(FUNCTIONS_DIR, filename)
        spec = importlib.util.spec_from_file_location("module.name", filepath)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                module.main()
            else:
                print(f"{filename} has no main() function.")
        except Exception as e:
            print(f"Failed to run {filename}: {e}")

    @log_entry_exit
    def add_new_function(self):
        existing_numbers = [
            int(f.split("_")[-1].split(".")[0])
            for f in self.function_files
            if f.startswith("function_")
            and f.endswith(".py")
            and f.split("_")[-1].split(".")[0].isdigit()
        ]
        next_number = max(existing_numbers, default=0) + 1
        new_filename = f"function_{next_number:03}.py"
        new_filepath = os.path.join(FUNCTIONS_DIR, new_filename)
        with open(new_filepath, "w") as f:
            f.write(
                f'def main():\n    print("Running new function: File name: {new_filename}")\n'
            )
        self.function_files.append(new_filename)
        self.reload_order()

    @log_entry_exit
    def move_up(self):
        if self.selected_row is not None and self.selected_row > 0:
            idx = self.selected_row
            self.function_files[idx], self.function_files[idx - 1] = (
                self.function_files[idx - 1],
                self.function_files[idx],
            )
            self.selected_row -= 1
            self.reload_order()

    @log_entry_exit
    def move_down(self):
        if (
            self.selected_row is not None
            and self.selected_row < len(self.function_files) - 1
        ):
            idx = self.selected_row
            self.function_files[idx], self.function_files[idx + 1] = (
                self.function_files[idx + 1],
                self.function_files[idx],
            )
            self.selected_row += 1
            self.reload_order()

    @log_entry_exit
    def move_top(self):
        if self.selected_row is not None and self.selected_row > 0:
            filename = self.function_files.pop(self.selected_row)
            self.function_files.insert(0, filename)
            self.selected_row = 0
            self.reload_order()

    @log_entry_exit
    def move_bottom(self):
        if (
            self.selected_row is not None
            and self.selected_row < len(self.function_files) - 1
        ):
            filename = self.function_files.pop(self.selected_row)
            self.function_files.append(filename)
            self.selected_row = len(self.function_files) - 1
            self.reload_order()

    @log_entry_exit
    def sort_alphabet(self):
        if messagebox.askyesno("Sort by Alphabet", "Bạn có chắc muốn sắp xếp?"):
            # Kiểm tra xem danh sách hiện tại đã được sắp xếp theo thứ tự tăng dần hay chưa
            if self.is_sorted_asc:
                self.function_files.sort(reverse=True)  # Sắp xếp giảm dần
                self.is_sorted_asc = False  # Cập nhật trạng thái sắp xếp
            else:
                self.function_files.sort()  # Sắp xếp tăng dần
                self.is_sorted_asc = True  # Cập nhật trạng thái sắp xếp
            self.reload_order()

    @log_entry_exit
    def reload_order(self):
        # Configure style for highlighted frame
        style = ttk.Style()
        style.configure("Highlighted.TFrame", background="#d9d9d9")
        style.configure("TFrame", background="white")

        for idx, filename in enumerate(self.function_files, start=1):
            if idx - 1 < len(self.function_rows):
                row = self.function_rows[idx - 1]
                row["filename"] = filename
                row["name_var"].set(filename)
                row["label_idx"].config(text=f"No.{idx:03}")
                row["entry"].config(state="normal" if self.edit_mode else "readonly")
                row["run_button"].config(
                    command=lambda nv=row["name_var"], r=idx - 1: (
                        self.select_row(r),
                        self.run_function(nv.get()),
                    )[-1]
                )
                row["check_var"].set(row["check_var"].get())
            else:
                self.add_function_row(idx, filename)

        for idx in range(len(self.function_files), len(self.function_rows)):
            self.function_rows[idx]["frame"].pack_forget()

        self.function_rows = self.function_rows[: len(self.function_files)]

        # Update move buttons state
        for btn in self.move_buttons:
            btn.state(["!disabled"] if self.edit_mode else ["disabled"])

        # Highlight selected row
        self.select_row(self.selected_row if self.selected_row is not None else -1)

    @log_entry_exit
    def toggle_edit_mode(self):
        if hasattr(self, "edit_tooltip") and self.edit_tooltip.tipwindow:
            self.edit_tooltip.hide_tip()
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.edit_save_button.config(text="Save")
        else:
            self.edit_save_button.config(text="Edit")
            self.save_order_and_names()
        self.reload_order()

    @log_entry_exit
    def save_order_and_names(self):
        new_function_files = []
        for row in self.function_rows:
            new_name = (
                row["name_var"].get().replace(" ", "_")
            )  # Replace spaces with "_"
            if not new_name.endswith(".py"):
                new_name += ".py"
            old_name = row["filename"]
            old_path = os.path.join(FUNCTIONS_DIR, old_name)
            new_path = os.path.join(FUNCTIONS_DIR, new_name)
            if old_name != new_name:
                os.rename(old_path, new_path)
                print(f"Renamed {old_name} → {new_name}")
                row["filename"] = new_name
            new_function_files.append(new_name)
        self.function_files = new_function_files
        with open(ORDER_FILE, "w") as f:
            for filename in self.function_files:
                f.write(filename + "\n")
        print("Functions saved:", self.function_files)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    DEBUG_LOG = args.debug

    try:
        root = tk.Tk()
        app = FunctionRunnerApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Application failed to start: {e}")
