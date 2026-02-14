import tkinter as tk
from tkinter import ttk

import modules.Data as data

def prettyPrint(msg : str): 
    print("[SIDEBAR]:", msg)

class SidebarFrame(ttk.Frame):
    def __init__(self, master, on_nav_click):
       
        super().__init__(master, style="Sidebar.TFrame") 
        
        self.on_nav_click = on_nav_click
        self.nav_buttons = {}
        self.current_button = None

        logo_path = data.get_file_parent() / "ui" / "Assets" / "Logo.png"
        self.IconImage = tk.PhotoImage(file=logo_path).subsample(10, 10)

        self.logo_lbl = ttk.Label(self, image=self.IconImage, 
            background=ttk.Style().lookup("Sidebar.TFrame", "background"),  )
        self.logo_lbl.pack(pady=30)

        self.CreateButton("Students", "Students")
        self.CreateButton("Colleges", "College")
        self.CreateButton("Data Registry", "Data")

        spacer = ttk.Label(self, text="", background=ttk.Style().lookup("Sidebar.TFrame", "background"))
        spacer.pack(expand=True)

        self.info_lbl = ttk.Label(self, text="To create and manage.", font=("Bahnschrift SemiLight", 7, "italic"), background=ttk.Style().lookup("Sidebar.TFrame", "background"))
        self.info_lbl.pack(pady=10)

        self.UpdateSelected = self.SelectedUpdated
        # event to call from main when new selected / force select

    def SelectedUpdated(self, new : str):
        oldButton : ttk.Button = self.current_button
        theButton : ttk.Button = self.nav_buttons.get(new)

        self.current_button = theButton

        if oldButton:
            oldButton.config(style="TButton")

        if theButton:
            theButton.config(style="Accent.TButton")
        else:
            prettyPrint(f"invalid button update {new}")
            prettyPrint(self.nav_buttons)

    def CreateButton(self, name : str, call_name : str):
        btn = ttk.Button(
            self, 
            text=name,
            command=lambda: self.handle_click(btn,call_name)
        )
        btn.pack(fill="x", padx=10, pady=20)
        self.nav_buttons[call_name] = btn

    def handle_click(self, btn:ttk.Button, page_name):
        self.UpdateSelected(page_name)
        self.on_nav_click(page_name)


        