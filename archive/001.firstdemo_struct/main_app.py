try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:
    print("Error: tkinter module is not installed in your Python environment.")
    print("Please install it or use a different environment that has tkinter available.")
    exit(1)

class FunctionRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Function Runner App")

        self.functions = [
            ("Function 1", self.func1),
            ("Function 2", self.func2),
            ("Function 3", self.func3),
            ("Function 4", self.func4),
        ]

        self.check_vars = []

        self.create_widgets()

    def create_widgets(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        self.check_all_var = tk.BooleanVar()

        btn_check_all = ttk.Button(control_frame, text="Check/Uncheck All", command=self.toggle_all)
        btn_check_all.grid(row=0, column=0, padx=5)

        btn_run_all = ttk.Button(control_frame, text="Run All", command=self.run_all)
        btn_run_all.grid(row=0, column=1, padx=5)

        self.functions_frame = ttk.Frame(self.root)
        self.functions_frame.pack(pady=10)

        for idx, (func_name, func_callback) in enumerate(self.functions, start=1):
            self.add_function_row(idx, func_name, func_callback)

    def add_function_row(self, idx, func_name, func_callback):
        frame = ttk.Frame(self.functions_frame)
        frame.pack(fill='x', pady=2)

        var = tk.BooleanVar()
        chk = ttk.Checkbutton(frame, variable=var)
        chk.grid(row=0, column=0, padx=5)

        lbl_idx = ttk.Label(frame, text=f"No.{idx:03}")
        lbl_idx.grid(row=0, column=1, padx=5)

        lbl_name = ttk.Label(frame, text=func_name)
        lbl_name.grid(row=0, column=2, padx=5)

        btn_run = ttk.Button(frame, text="Run", command=lambda cb=func_callback: cb())
        btn_run.grid(row=0, column=3, padx=5)

        self.check_vars.append((var, func_callback))

    def toggle_all(self):
        new_state = not self.check_all_var.get()
        self.check_all_var.set(new_state)
        for var, _ in self.check_vars:
            var.set(new_state)

    def run_all(self):
        for var, callback in self.check_vars:
            if var.get():
                callback()

    # Dummy function implementations
    def func1(self):
        print("Running Function 1")

    def func2(self):
        print("Running Function 2")

    def func3(self):
        print("Running Function 3")

    def func4(self):
        print("Running Function 4")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = FunctionRunnerApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Application failed to start: {e}")
