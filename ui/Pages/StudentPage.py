import tkinter as tk
import modules.Data as data

from tkinter import ttk

def prettyPrint(msg : str): 
    print("[STUDENT]:", msg)

class StudentPageFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        style = ttk.Style()
        style.configure("TNotebook", tabposition="n")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_insert = InsertTab(self.notebook)
        self.tab_edit = EditTab(self.notebook)
        self.tab_search = SearchTab(self.notebook)

        self.notebook.add(self.tab_insert, text="Insert New Student")
        self.notebook.add(self.tab_edit, text="Edit Information")
        self.notebook.add(self.tab_search, text="Search Registry")

class InsertTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()

    def setup_ui(self):
        form_container = ttk.Frame(self)
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        self.fields = ["ID Number", "First Name", "Last Name", "Program Code", "Year Level"]
        self.entries = {}

        for i, field in enumerate(self.fields):
            ttk.Label(form_container, text=field + ":").grid(row=i, column=0, padx=10, pady=10, sticky="e")
            entry = ttk.Entry(form_container, width=30)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            self.entries[i] = entry

        ttk.Button(
            form_container, 
            text="Save Student Record", 
            style="Accent.TButton",
            command=self.save_data
        ).grid(row=len(self.fields), column=0, columnspan=2, pady=20)

        self.TextLabel = ttk.Label(
            form_container, 
            text="",
            foreground= "#B92905"
        )
        self.TextLabel.grid(row=len(self.fields)+1, column=0, columnspan=2, pady=0)

    def verify_format(): return True

    def save_data(self):
      format = data.GetFormat()
      to_pack = {}

      print(self.entries)

      for i, data_item in enumerate(format):
          inputted = self.entries[i]
          verified = self.verify_format(inputted)

          if inputted and verified == True:
            to_pack[i] = inputted
          elif verified != True:
              self.TextLabel.config(text=verified)
              break
          else: 
              to_pack[i] = None

class EditTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Edit Student Registry").pack(pady=20)

class SearchTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Search Registry").pack(pady=20)