import tkinter as tk
from tkinter import ttk

class StudentPageFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="Card.TFrame")
    
        self.lbl = ttk.Label(self, text="yokoso soul society washoii", font=30)
        self.lbl.pack(pady=10)
