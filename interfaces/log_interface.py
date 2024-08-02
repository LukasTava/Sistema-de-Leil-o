import tkinter as tk
from tkinter import scrolledtext

class LogInterface:
    def __init__(self, root):
        self.root = root

        self.frame_log = tk.LabelFrame(self.root, text="Log")
        self.frame_log.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.log_text = scrolledtext.ScrolledText(self.frame_log, width=80, height=20)
        self.log_text.grid(row=0, column=0, padx=10, pady=10)

    def log_mensagem(self, mensagem):
        self.log_text.insert(tk.END, mensagem + '\n')
        self.log_text.see(tk.END)
