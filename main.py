# main.py
import tkinter as tk
from gui import DeadlockSimulatorApp

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Deadlock Detection & Prevention Simulator")
    root.geometry("800x600")
    
    app = DeadlockSimulatorApp(root)
    app.pack(fill="both", expand=True)
    
    root.mainloop()
