import tkinter as tk
import modules.Data as data

from tkinter import ttk
from modules.ui_utils import processImage

def prettyPrint(msg : str): 
    print("[SIDEBAR]:", msg)

class SidebarFrame(ttk.Frame):
    def __init__(self, master, on_nav_click):
       
        super().__init__(master, style="Sidebar.TFrame") 
        
        self.on_nav_click = on_nav_click
        self.nav_buttons = {}
        self.current_button = None

        asset_path = data.get_file_parent() / "ui" / "Assets"
    
        self.IconImage      = processImage(asset_path / "Logo.png", 120,120)

        self.StudentImage   = processImage(asset_path / "student.png", 26,26, dark_mode_invert=True)
        self.DatabaseImage  = processImage(asset_path / "database.png", 26,26, dark_mode_invert=True)
        self.CollegeImage   = processImage(asset_path / "college.png", 26,26, dark_mode_invert=True)

        self.logo_lbl = ttk.Label(self, image=self.IconImage, 
            background=ttk.Style().lookup("Sidebar.TFrame", "background"),  )
        self.logo_lbl.pack(pady=30)

        self.CreateButton("Students", "Students", self.StudentImage)
        self.CreateButton("Colleges", "College", self.CollegeImage)
        self.CreateButton("Data Registry", "Data", self.DatabaseImage)

        spacer = ttk.Label(self, text="", background=ttk.Style().lookup("Sidebar.TFrame", "background"))
        spacer.pack(expand=True)

        self.info_lbl = ttk.Label(self, text="To create and manage.", font=("Bahnschrift SemiLight", 7, "italic"), background=ttk.Style().lookup("Sidebar.TFrame", "background"))
        self.info_lbl.pack(pady=10)

        self.UpdateSelected = self.SelectedUpdated

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

    def CreateButton(self, name : str, call_name : str, image_path = None):
       
        btn = ttk.Button(
            self, 
            text=f"   {name}",
            image=image_path if image_path else None,
            command=lambda: self.handle_click(btn,call_name)
        )
       
        btn.pack(fill="x", padx=10, pady=20)
        self.nav_buttons[call_name] = btn

    def handle_click(self, btn:ttk.Button, page_name):
        self.UpdateSelected(page_name)
        self.on_nav_click(page_name)


        