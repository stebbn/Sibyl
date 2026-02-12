import tkinter as tk
import modules.Data as data

from tkinter import ttk

def prettyPrint(msg : str): 
    print("[DATA_REG]:", msg)

class DataPageFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, style="Card.TFrame")
        
        self.CurrentSort = "#0"
        self.ReverseSort = False

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit Student", command=self.edit_student)
        self.context_menu.add_command(label="Delete Student", command=self.delete_student)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_list) 
        
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True)

        columns = ("first_name", "last_name", "program_code", "year", "gender")
        self.tree = ttk.Treeview(self, columns=columns, height=15)
        
        self.tree.heading("#0", text="ID No.", command=lambda: self.sort_column("#0", False))
        self.tree.column("#0", width=100)
        
        col_names = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "program_code": "Program Code",
            "year": "Year",
            "gender": "Gender"
        }
        
        for col, name in col_names.items():
            self.tree.heading(col, text=name, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=100, anchor="center")

        self.tree.column("first_name", width=120, anchor="w")
        self.tree.column("last_name", width=120, anchor="w")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.bind("<Button-3>", self.show_context_menu)

        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        self.scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.show_info()

    def update_list(self, *args):
        search_term = self.search_var.get()
        self.show_info(search_term)

    def show_context_menu(self, event):
        item_id = self.tree.identify_row(event.y)
        
        if item_id:
            self.tree.selection_set(item_id)
            self.tree.focus(item_id)
          
            self.context_menu.post(event.x_root, event.y_root)

    def show_info(self, search_query=""):
        for item in self.tree.get_children():
            self.tree.delete(item)

        student_records = data.GetData()
        search_query = search_query.lower()
        
        for student_id, value in student_records.items():
            full_text = f"{student_id} {value.get('first_name')} {value.get('last_name')} {value.get('program_code')} {value.get('year')} {value.get('gender')}".lower()
            
            if not search_query or search_query in full_text:
                display_values = (
                    value.get("first_name", ""), 
                    value.get("last_name", ""), 
                    value.get("program_code", ""),
                    value.get("year", ""), 
                    value.get("gender", "")  
                )
                self.tree.insert(parent="", index="end", text=student_id, values=display_values)

        self.sort_column(self.CurrentSort, self.ReverseSort)

    def sort_column(self, col, reverse):
        for c in self.tree["columns"]:
            current_text = self.tree.heading(c)["text"].replace(" ▲", "").replace(" ▼", "")
            self.tree.heading(c, text=current_text)
       
        id_text = self.tree.heading("#0")["text"].replace(" ▲", "").replace(" ▼", "")
        self.tree.heading("#0", text=id_text)

        if col == "#0":
            data_list = [(self.tree.item(k)["text"], k) for k in self.tree.get_children("")]
        else:
            data_list = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

        try:
            data_list.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            data_list.sort(key=lambda t: t[0].lower(), reverse=reverse)

        for index, (val, k) in enumerate(data_list):
            self.tree.move(k, "", index)

        arrow = " ▼" if reverse else " ▲"
        new_text = self.tree.heading(col)["text"] + arrow
        
        self.tree.heading(col, text=new_text, command=lambda: self.sort_column(col, not reverse))

        self.CurrentSort = col
        self.ReverseSort = reverse

        prettyPrint(f"Sorted {col} | Reverse: {reverse}")

    def edit_student(self):
        selected = self.tree.selection()
        if selected:
            student_id = self.tree.item(selected[0])["text"]
            prettyPrint(f"edit edit {student_id}")
        else: prettyPrint("no selection for edit")

    def delete_student(self):
        selected = self.tree.selection()
        if selected:
            student_id = self.tree.item(selected[0])["text"]
            prettyPrint(f"delete delete {student_id}")
        else: prettyPrint("no selection for delete")
