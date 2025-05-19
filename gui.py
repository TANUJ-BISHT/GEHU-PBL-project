import tkinter as tk
from tkinter import messagebox
from banker import is_safe_state

class DeadlockSimulatorApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.process_count = tk.IntVar()
        self.resource_count = tk.IntVar()

        self.matrix_inputs = []  # stores allocation and max inputs
        self.available_inputs = []

        self.init_screen = None
        self.matrix_screen = None

        self.create_init_screen()

    def handle_next(self):
        p = self.process_count.get()
        r = self.resource_count.get()

        if p <= 0 or r <= 0:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return

        self.init_screen.destroy()
        self.create_matrix_input_screen(p, r)

    def create_init_screen(self):
        self.init_screen = tk.Frame(self)
        self.init_screen.pack(fill="both", expand=True)

        tk.Label(self.init_screen, text="Deadlock Simulator",
                 font=("Helvetica", 20)).pack(pady=20)

        form = tk.Frame(self.init_screen)
        form.pack(pady=10)

        tk.Label(form, text="Number of Processes:").grid(
            row=0, column=0, padx=10, pady=5)
        tk.Entry(form, textvariable=self.process_count).grid(row=0, column=1)

        tk.Label(form, text="Number of Resources:").grid(
            row=1, column=0, padx=10, pady=5)
        tk.Entry(form, textvariable=self.resource_count).grid(row=1, column=1)

        tk.Button(self.init_screen, text="Next",
                  command=self.handle_next).pack(pady=20)

    def create_matrix_input_screen(self, p, r):
        self.matrix_screen = tk.Frame(self)
        self.matrix_screen.pack(fill="both", expand=True)

        tk.Label(self.matrix_screen, text="Enter Allocation and Max Matrices", font=(
            "Helvetica", 16)).pack(pady=10)

        table_frame = tk.Frame(self.matrix_screen)
        table_frame.pack()

        self.matrix_inputs = []

        for i in range(p):
            row = []
            for j in range(r):
                alloc = tk.Entry(table_frame, width=5)
                alloc.grid(row=i+1, column=j)
                row.append(alloc)
            row.append(tk.Label(table_frame, text="|"))
            for j in range(r):
                maxx = tk.Entry(table_frame, width=5)
                maxx.grid(row=i+1, column=j+r+1)
                row.append(maxx)
            self.matrix_inputs.append(row)

        tk.Label(table_frame, text="Allocation").grid(
            row=0, column=0, columnspan=r)
        tk.Label(table_frame, text="|").grid(row=0, column=r)
        tk.Label(table_frame, text="Max").grid(row=0, column=r+1, columnspan=r)

        # Available resources input
        tk.Label(self.matrix_screen, text="Available Resources:").pack(pady=10)
        avail_frame = tk.Frame(self.matrix_screen)
        avail_frame.pack()

        self.available_inputs = []
        for j in range(r):
            entry = tk.Entry(avail_frame, width=5)
            entry.grid(row=0, column=j)
            self.available_inputs.append(entry)

        # Submit + Reset buttons
        tk.Button(self.matrix_screen, text="Run Banker's Algorithm",
                command=self.collect_data).pack(pady=10)

        reset_button = tk.Button(self.master, text="Reset", command=self.reset_ui)
        reset_button.pack(pady=5)

    def reset_ui(self):
        for row in self.matrix_inputs:
            for widget in row:
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)

        for entry in self.available_inputs:
            entry.delete(0, tk.END)

    def collect_data(self):
        
        try:
            allocation = []
            max_matrix = []
            for row in self.matrix_inputs:
                alloc_row = [int(cell.get())
                            for cell in row[:self.resource_count.get()]]
                max_row = [int(cell.get())
                        for cell in row[self.resource_count.get()+1:]]
                allocation.append(alloc_row)
                max_matrix.append(max_row)

            available = [int(entry.get()) for entry in self.available_inputs]

            # Run Banker’s Algorithm here
            safe, sequence = is_safe_state(allocation, max_matrix, available)

            if not safe:
                # Build Request Matrix = Need
                request = []
                for i in range(len(max_matrix)):
                    request.append([max_matrix[i][j] - allocation[i][j] for j in range(len(available))])

            if safe:
                messagebox.showinfo(
                    "Safe State", f"System is in a safe state.\nSafe Sequence: {sequence}")
            else:
                messagebox.showerror(
                    "Deadlock Detected", "System is in an unsafe state (deadlock possible).")

        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter only integer values.")