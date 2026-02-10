import tkinter as tk
from tkinter import ttk
from modules.Data import get_college_by_program

class CollegeFinderFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="Card.TFrame")
      
        self.txt = ttk.Entry(self)
        self.txt.pack(pady=5)

        self.btn = ttk.Button(self, text="Find College", command=self.read_input)
        self.btn.pack(pady=5)

        self.lbl = ttk.Label(self, text="")
        self.lbl.pack(pady=5)

    def read_input(self):
        program = self.txt.get()
        college = get_college_by_program(program)
        self.lbl.config(text=f"{college}")