import tkinter as tk
from interfaces.interface import Interface

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()