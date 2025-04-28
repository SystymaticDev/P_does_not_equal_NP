import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import time
import random
from itertools import product
import torch

MAX_VARIABLES = 20  # Limit the number of variables to prevent excessive computation

# Function to simulate SAT solving using PyTorch
def is_satisfiable(clauses, assignment):
    assignment_tensor = torch.tensor(assignment, dtype=torch.bool).to('cuda')
    for clause in clauses:
        clause_tensor = torch.tensor(clause, dtype=torch.int).to('cuda')
        if not torch.any(assignment_tensor[clause_tensor.abs() - 1] == (clause_tensor > 0)):
            return False
    return True

def brute_force_sat(clauses, num_vars, progress_callback):
    total_assignments = 2 ** num_vars
    for count, assignment in enumerate(product([False, True], repeat=num_vars), 1):
        if is_satisfiable(clauses, assignment):
            return True
        if count % (total_assignments // 100) == 0:  # Update progress every 1%
            progress_callback(count / total_assignments * 100)
    return False

# Main Application Class
class ComplexitySuiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Complexity Suite")
        self.root.geometry("800x600")
        self.apply_dark_mode()

        # Notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Tabs
        self.create_fine_grained_tab()
        self.create_average_case_tab()
        self.create_class_separations_tab()
        self.create_results_tab()

        # Console Output Log
        self.console_output = scrolledtext.ScrolledText(root, height=10, state='disabled', bg='#1e1e1e', fg='light cyan', font=('Consolas', 10))
        self.console_output.pack(fill='both', expand=True)

    def apply_dark_mode(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='#2e2e2e', foreground='light cyan', fieldbackground='#2e2e2e', font=('Consolas', 10))
        style.configure('TButton', background='#3e3e3e', foreground='light cyan')
        style.configure('TLabel', background='#2e2e2e', foreground='light cyan')
        style.configure('TEntry', fieldbackground='#3e3e3e', foreground='light cyan')
        style.configure('TNotebook', background='#2e2e2e')
        style.configure('TNotebook.Tab', background='#3e3e3e', foreground='light cyan')
        style.configure('TFrame', background='#2e2e2e')
        style.configure('TProgressbar', background='light cyan')

    def log_to_console(self, message):
        self.console_output.config(state='normal')
        self.console_output.insert(tk.END, message + '\n')
        self.console_output.yview(tk.END)
        self.console_output.config(state='disabled')

    def create_fine_grained_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Fine-Grained Complexity")

        ttk.Label(frame, text="Number of Variables (Max {}):".format(MAX_VARIABLES)).pack(pady=5)
        self.num_vars_entry = ttk.Entry(frame)
        self.num_vars_entry.pack(pady=5)

        self.sat_progress = ttk.Progressbar(frame, orient='horizontal', length=400, mode='determinate')
        self.sat_progress.pack(pady=5)

        ttk.Button(frame, text="Run SAT Solver", command=self.run_sat_solver).pack(pady=5)

    def run_sat_solver(self):
        try:
            num_vars = int(self.num_vars_entry.get())
            if num_vars <= 0 or num_vars > MAX_VARIABLES:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive integer for the number of variables (max {}).".format(MAX_VARIABLES))
            return

        clauses = [[random.randint(1, num_vars) * random.choice([-1, 1]) for _ in range(3)] for _ in range(num_vars * 4)]

        def progress_callback(progress):
            self.sat_progress['value'] = progress
            self.root.update_idletasks()

        def task():
            start_time = time.time()
            self.log_to_console(f"Running SAT solver with {num_vars} variables...")
            result = brute_force_sat(clauses, num_vars, progress_callback)
            end_time = time.time()
            self.log_to_console(f"SAT Result: {'Satisfiable' if result else 'Unsatisfiable'}, Time Taken: {end_time - start_time:.2f} seconds")
        
        threading.Thread(target=task).start()

    # Other methods omitted for brevity...

if __name__ == "__main__":
    root = tk.Tk()
    app = ComplexitySuiteApp(root)
    root.mainloop()