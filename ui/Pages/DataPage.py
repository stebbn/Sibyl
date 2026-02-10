import tkinter as tk
import modules.Data as data

from tkinter import ttk

class DataPageFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="Card.TFrame")
    
        columns = ("first_name", "last_name", "prog_code", "year", "gender")
        self.tree = ttk.Treeview(self, columns=columns, height=15)
     
        self.tree.heading("#0", text="ID No.")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("prog_code", text="Program Code")
        self.tree.heading("year", text="Year")
        self.tree.heading("gender", text="Gender")

        self.tree.column("#0", width=100) 
        self.tree.column("first_name", width=120, anchor="w")
        self.tree.column("last_name", width=120, anchor="w")
        self.tree.column("prog_code", width=100, anchor="center")
        self.tree.column("year", width=80, anchor="center")
        self.tree.column("gender", width=80, anchor="center")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        self.scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.ShowInformation()

    def ShowInformation(self):
        for student_id, value in data.getDictData().items():
       
            display_values = (
                value[0], 
                value[1], 
                value[2],
                value[3], 
                value[4]  
            )
            self.tree.insert(parent="", index="end", text=student_id, values=display_values)