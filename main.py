import tkinter as tk
import tkinter.font as tkFont

import sys
import traceback
import sv_ttk
import pywinstyles

from tkinter import ttk
from ui import SidebarFrame, getBG, getTheme, setup_geometry, apply_theme
from ui.Pages import CollegeFinderFrame, StudentPageFrame, DataPageFrame

def prettyPrint(msg : str): 
    print("[Main]:", msg)

width, height = 900, 500

class Sibyl_App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.withdraw()

        self.title("Sibyl - Student Information System")

        setup_geometry(self, width, height)
        self.minsize(width, height)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.Theme = getTheme()

        apply_theme(self)

        style = ttk.Style()
        style.configure("Sidebar.TFrame", 
                        background=getBG(self.Theme), 
                        borderwidth=0, 
                        highlightthickness=3
                        ) 
        style.configure("Sidebar2.TFrame",background=getBG(self.Theme),) 
        
        style.configure('TCombobox', selectbackground=None, selectforeground=None)
        style.configure("TNotebook", tabposition="n")
        style.configure('TButton', font=('Bahnschrift SemiLight', 10))

        self.sidebar = SidebarFrame(self, on_nav_click=self.switch_page)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0)

        self.PageContainer = ttk.Frame(self)
        self.PageContainer.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)   

        self.ui_pages = {
            "College"  : CollegeFinderFrame,
            "Students" : StudentPageFrame,
            "Data"     : DataPageFrame
        }

        self.PageClass   = None
        self.CurrentPage = ""
        self.StarterPage = "Students"

        bigfont = tkFont.Font(family="Helvetica",size=20)
        self.option_add("*TCombobox*Listbox*Font", bigfont)

        self.switch_page(self.StarterPage)
        self.sidebar.UpdateSelected(self.StarterPage)

        self.deiconify()

    def switch_page(self, page_name : str):
        try:
            page_class = self.ui_pages.get(page_name)
            last_page  = self.CurrentPage

            if page_class and self.CurrentPage != page_name:

                for widget in self.PageContainer.winfo_children():
                   widget.destroy()

                self.PageClass = None
                self.PageClass = page_class(self.PageContainer, controller = self)
                self.PageClass.pack(fill="both", expand=True)

                self.CurrentPage = page_name
                
                prettyPrint(f"Switched to {page_name}")
            else:
                prettyPrint(f"Unable to switch to {page_name} | last page: {last_page}")
                
        except Exception as e:
            prettyPrint(f"invalid ui page: {page_name} | {e} | {traceback.format_exc()}")

if __name__ == "__main__":
    app = Sibyl_App()
    app.mainloop()