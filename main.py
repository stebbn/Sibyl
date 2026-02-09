import tkinter as tk
from tkinter import ttk
import sv_ttk
import darkdetect
import pywinstyles
import sys

from modules.Data import get_college_by_program
from ui import SidebarFrame

class SibylApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sibyl")
        self.setup_geometry(800, 500)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.sidebar = SidebarFrame(self, on_nav_click="")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.setup_main_content()

        # always make last or it wont apply all
        sv_ttk.set_theme(darkdetect.theme())
        self.apply_theme_to_titlebar()

    def setup_geometry(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - width / 2)
        center_y = int(screen_height/2 - height / 2)
        self.geometry(f'{width}x{height}+{center_x}+{center_y}')

    def setup_main_content(self):
        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        self.txt = ttk.Entry(self.container)
        self.txt.pack(pady=5)

        self.btn = ttk.Button(self.container, text="Find College", command=self.read_input)
        self.btn.pack(pady=5)

        self.lbl = ttk.Label(self.container, text="Enter Program Code (e.g., BSCS)")
        self.lbl.pack(pady=5)

    def read_input(self):
        program = self.txt.get()
        college = get_college_by_program(program)
        self.lbl.config(text=f"College: {college}")

    def apply_theme_to_titlebar(self):
        version = sys.getwindowsversion()
        is_dark = sv_ttk.get_theme() == "dark"
        color = "#1c1c1c" if is_dark else "#141313"

        if version.major == 10 and version.build >= 22000:
            pywinstyles.change_header_color(self, color)
        elif version.major == 10:
            pywinstyles.apply_style(self, "dark" if is_dark else "normal")
            self.wm_attributes("-alpha", 0.99)
            self.wm_attributes("-alpha", 1)

if __name__ == "__main__":
    app = SibylApp()
    app.mainloop()