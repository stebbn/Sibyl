import tkinter as tk
import tkinter.font as tkFont

import sv_ttk
import darkdetect
import pywinstyles

import sys
import traceback

from tkinter import ttk
from ui import SidebarFrame
from ui.Pages import CollegeFinderFrame, StudentPageFrame, DataPageFrame

def prettyPrint(msg : str): 
    print("[Main]:", msg)

class Sibyl_App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.withdraw()

        self.title("Sibyl - Student Information System")
        self.setup_geometry(900, 500)
        self.minsize(900, 500)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

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

        # always make last or it wont apply all
        self.apply_theme()

        style = ttk.Style()
        style.configure("Sidebar.TFrame", 
                        background="#1A1919" if darkdetect.theme() else "#CCCCCC", 
                        borderwidth=0, 
                        highlightthickness=3
                        ) 
        style.configure("Sidebar2.TFrame",background="#1A1919" if darkdetect.theme() else "#CCCCCC",) 
        
        style.configure('TCombobox', selectbackground=None, selectforeground=None)
        style.configure("TNotebook", tabposition="n")
        style.configure('TButton', font=('Bahnschrift SemiLight', 10))

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

    def setup_geometry(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - width / 2)
        center_y = int(screen_height/2 - height / 2)
        self.geometry(f'{width}x{height}+{center_x}+{center_y}')
  
    def apply_theme(self):
        sv_ttk.set_theme(darkdetect.theme())

        self.is_dark = sv_ttk.get_theme() == "dark"
        version = sys.getwindowsversion()
        color = "#1A1919" if darkdetect.theme() else "#CCCCCC"

        if version.major == 10 and version.build >= 22000:
            pywinstyles.change_header_color(self, color)
        elif version.major == 10:
            pywinstyles.apply_style(self, "dark" if self.is_dark else "normal")
            self.wm_attributes("-alpha", 0.99)
            self.wm_attributes("-alpha", 1)

if __name__ == "__main__":
    app = Sibyl_App()
    app.mainloop()