import tkinter as tk
import modules.Data as data
from tkinter import ttk

def prettyPrint(msg : str): 
    print("[DATA_REG]:", msg)

class DataPageFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, style="Card.TFrame")
        
        self.controller = controller
        self.CurrentSort = "#0"
        self.ReverseSort = False

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit Student", command=self.edit_student)
        self.context_menu.add_command(label="Delete Student", command=self.delete_student)

        search_frame = ttk.Frame(self)
        search_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side="left", padx=5)

        self.search_field = ttk.Combobox(search_frame, state="readonly", width=15)
        self.search_field['values'] = ("All Fields", "ID No.", "First Name", "Last Name", "Program", "Year", "Gender")
        self.search_field.set("All Fields")
        self.search_field.pack(side="left", padx=5)

        search_path = data.get_file_parent() / "ui" / "Assets" / "search.png"
        self.search_image = tk.PhotoImage(file=search_path).subsample(35,35)

        ttk.Button(
            search_frame, 
            command=self.update_list, 
            image=self.search_image
        ).pack(side="left", padx=10)
        
        tree_container = ttk.Frame(self)
        tree_container.pack(side="top", fill="both", expand=True)

        columns = ("first_name", "last_name", "program_code", "year", "gender")
        self.tree = ttk.Treeview(tree_container, columns=columns, height=12)
        
        self.tree.tag_configure("program_error", foreground="#FF6B6B")

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

        self.scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        self.scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.info_frame = ttk.LabelFrame(self, text=" Student Details ", padding=15)
        self.info_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        self.display_box = tk.Text(
            self.info_frame, 
            height=15, 
            font=("Bahnschrift SemiLight", 10),
            relief="flat",
            state="disabled",
            padx=2,
            pady=1
        )
        self.display_box.pack(fill="x")
        self.display_box.tag_configure("header", font=("Bahnschrift", 10, "bold"))

        self.show_info()

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        id = item["text"]
        value = item["values"]

        college = data.get_college_by_program(value[2])
       
        self.display_box.config(state="normal")
        self.display_box.delete("1.0", tk.END)

        self.display_box.insert(tk.END, "ID NUMBER:        ", "header")
        self.display_box.insert(tk.END, f"{id}\n")
        
        self.display_box.insert(tk.END, "FULL NAME:        ", "header")
        self.display_box.insert(tk.END, f"{value[1]}, {value[0]}\n")
        
        self.display_box.insert(tk.END, "ACADEMICS:       ", "header")
        self.display_box.insert(tk.END, f"{data.program_data[value[2]]['name']} (Year {value[3]})" if value[2] in data.program_data else "Invalid Program Code")

        self.display_box.insert(tk.END, "\nCOLLEGE:             ", "header")
        self.display_box.insert(tk.END, f"{college if college != 'invalid program code' else '-'}")
        
        self.display_box.insert(tk.END, "\nGENDER:              ", "header")
        self.display_box.insert(tk.END, f"{value[4]}")

        self.display_box.config(state="disabled")

    def update_list(self, *args):
        search_term = self.search_var.get()
        self.show_info(search_term)

    def show_info(self, search_query=""):
        for item in self.tree.get_children():
            self.tree.delete(item)

        student_records = data.student_data
        search_query = search_query.lower()
        field_filter = self.search_field.get()
        
        for student_id, value in student_records.items():
            field_map = {
                "ID No.": student_id,
                "First Name": value.get('first_name', ''),
                "Last Name": value.get('last_name', ''),
                "Program": value.get('program_code', ''),
                "Year": value.get('year', ''),
                "Gender": value.get('gender', '')
            }

            if field_filter == "All Fields":
                target_text = f"{student_id} {' '.join(str(v) for v in value.values())}".lower()
            else:
                target_text = str(field_map.get(field_filter, "")).lower()
            
            if not search_query or search_query in target_text:
                display_values = (
                    value.get("first_name", ""), 
                    value.get("last_name", ""), 
                    value.get("program_code", ""),
                    value.get("year", ""), 
                    value.get("gender", "")  
                )
                
                if data.get_college_by_program(value.get("program_code", "")) == "invalid program code":
                    self.tree.insert("", "end", text=student_id, values=display_values, tags=("program_error",))
                else:
                    self.tree.insert("", "end", text=student_id, values=display_values)

        self.sort_column(self.CurrentSort, self.ReverseSort)

    def show_context_menu(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            self.tree.focus(item_id)
            self.context_menu.post(event.x_root, event.y_root)

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
            data_list.sort(key=lambda t: int(t[0].split('-')[0]) if '-' in t[0] else int(t[0]), reverse=reverse)
        except ValueError:
            data_list.sort(key=lambda t: t[0].lower(), reverse=reverse)

        for index, (val, k) in enumerate(data_list):
            self.tree.move(k, "", index)

        arrow = " ▼" if reverse else " ▲"
        new_text = self.tree.heading(col)["text"] + arrow
        self.tree.heading(col, text=new_text, command=lambda: self.sort_column(col, not reverse))
        self.CurrentSort = col
        self.ReverseSort = reverse

    def edit_student(self):
        selected = self.tree.selection()
        if selected:
            student_id = self.tree.item(selected[0])["text"]
            self.controller.sidebar.handle_click(None, "Students")
            self.controller.PageClass.notebook.select(1)
            self.controller.PageClass.tab_edit.search_id(student_id)
        else: prettyPrint("did not select anything")

    def delete_student(self):
        selected = self.tree.selection()
        if selected:
            student_id = self.tree.item(selected[0])["text"]
            if data.DeleteStudent(student_id): self.show_info()
        else: prettyPrint("did not select anything")