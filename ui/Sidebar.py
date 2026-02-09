import tkinter as tk
from tkinter import ttk

class SidebarFrame(ttk.Frame):
    def __init__(self, master, on_nav_click):
       
        super().__init__(master, style="Card.TFrame") 
        
        self.on_nav_click = on_nav_click
        
        title_lbl = ttk.Label(self, text="SIBYL", font=("Segoe UI Semibold", 18))
        title_lbl.pack(pady=20, padx=20)

        self.student_btn = ttk.Button(
            self, 
            text="Students", 
            command=lambda: self.on_nav_click("students")
        )
        self.student_btn.pack(fill="x", padx=10, pady=5)

        self.college_btn = ttk.Button(
            self, 
            text="Colleges", 
            command=lambda: self.on_nav_click("colleges")
        )
        self.college_btn.pack(fill="x", padx=10, pady=5)

        spacer = ttk.Label(self, text="")
        spacer.pack(expand=True)

        self.info_lbl = ttk.Label(self, text="sum placeholder aura farm text idk", font=("Segoe UI", 5))
        self.info_lbl.pack(pady=10)