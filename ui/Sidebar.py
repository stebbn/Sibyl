import tkinter as tk
from tkinter import ttk

def prettyPrint(msg : str): 
    print("[SIDEBAR]:", msg)

class SidebarFrame(ttk.Frame):
    def __init__(self, master, on_nav_click):
       
        super().__init__(master, style="Card.TFrame") 
        
        self.on_nav_click = on_nav_click
        self.nav_buttons = {}
        self.current_button = None

        self.CreateButton("Students", "Students")
        self.CreateButton("Colleges", "College")
        self.CreateButton("Data Registry", "Data")

        spacer = ttk.Label(self, text="")
        spacer.pack(expand=True)

        self.info_lbl = ttk.Label(self, text="v1", font=("Segoe UI", 5))
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
        btn.pack(fill="x", padx=10, pady=5)
        self.nav_buttons[call_name] = btn

    def handle_click(self, btn:ttk.Button, page_name):
        self.UpdateSelected(page_name)
        self.on_nav_click(page_name)


        