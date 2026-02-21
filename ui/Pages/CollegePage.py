import tkinter as tk
import modules.Data as data

from tkinter import ttk
from modules.ui_utils import setup_geometry, apply_theme, getTheme, processImage

def prettyPrint(msg : str): 
    print("[COLLEGE_PAGE]:", msg)

def sort_column(self, col, reverse):
    for c in self.tree["columns"]:
        current_text = self.tree.heading(c)["text"].replace(" ▲", "").replace(" ▼", "")
        self.tree.heading(c, text=current_text)
    
    id_text = self.tree.heading("code")["text"].replace(" ▲", "").replace(" ▼", "")
    self.tree.heading("code", text=id_text)

    data_list = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

    try:
        data_list.sort(key=lambda t: int(t[0].split('-')[0]) if '-' in t[0] else int(t[0]), reverse=reverse)
    except ValueError:
        data_list.sort(key=lambda t: t[0].lower(), reverse=reverse)

    for index, (val, k) in enumerate(data_list):
        self.tree.move(k, "", index)

    arrow = " ▼" if reverse else " ▲"
    new_text = self.tree.heading(col)["text"] + arrow
    self.tree.heading(col, text=new_text, command=lambda: sort_column(self, col, not reverse)) # might be a problem

    self.CurrentSort = col
    self.ReverseSort = reverse

class CollegeFinderFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.pack(expand=True, fill="both")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_colleges = CollegeTab(self.notebook)
        self.tab_programs = ProgramTab(self.notebook)

        self.notebook.add(self.tab_colleges, text="Colleges")
        self.notebook.add(self.tab_programs, text="Programs")

class CollegeTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh())

        self.CurrentSort = "code"
        self.ReverseSort = False

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(header, text="College Registry", font=("", 12, "bold")).pack(side="left")

        search_ent = ttk.Entry(header, textvariable=self.search_var, width=25)
        search_ent.pack(side="right", padx=10)

        ttk.Label(header, text="Search:").pack(side="right")

        search_path = data.get_file_parent() / "ui" / "Assets" / "add.png"
        self.add_image = processImage(search_path,15,15,dark_mode_invert=True)

        ttk.Button(header, width=2, image=self.add_image, command=lambda: self.open_editor()).pack(side="left", padx=10)

        self.tree = ttk.Treeview(self, columns=("code", "name"), show="headings")
        
        self.tree.heading("code", text="College Code", command=lambda: sort_column(self, "code", False))
        self.tree.heading("name", text="Name", command=lambda: sort_column(self, "name", False))

        self.tree.column("code", width=120, anchor="center", stretch=tk.NO)
        self.tree.column("name", width=400, anchor="w", stretch=tk.YES)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Edit College", command=self.edit_selected)
        self.menu.add_command(label="Delete College", command=self.delete_selected)
        self.tree.bind("<Button-3>", self.show_menu)

    def refresh(self):
        query = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())

        if not data.college_data: prettyPrint("college data not available"); return

        for code, name in data.college_data.items():
            if query in code.lower() or query in name.lower():
                self.tree.insert("", "end", values=(code, name))

        sort_column(self, self.CurrentSort, self.ReverseSort)

    def show_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu.post(event.x_root, event.y_root)

    def edit_selected(self):
        values = self.tree.item(self.tree.selection()[0])['values']
        self.open_editor(values)

    def delete_selected(self):
        code = self.tree.item(self.tree.selection()[0])['values'][0]
        if data.DeleteCollege(code): self.refresh()

    def open_editor(self, info=None):
        EditorWindow(self, "College", info)

class ProgramTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh())

        self.CurrentSort = "code"
        self.ReverseSort = False

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(header, text="Program Registry", font=("", 12, "bold")).pack(side="left")

        search_ent = ttk.Entry(header, textvariable=self.search_var, width=25)
        search_ent.pack(side="right", padx=10)

        ttk.Label(header, text="Search:").pack(side="right")

        search_path = data.get_file_parent() / "ui" / "Assets" / "add.png"
        self.add_image = processImage(search_path,15,15,dark_mode_invert=True)

        ttk.Button(header, width=2, image=self.add_image, command=lambda: self.open_editor()).pack(side="left", padx=10)

        self.tree = ttk.Treeview(self, columns=("code", "name", "college"), show="headings")

        self.tree.heading("code", text="Program Code", command=lambda: sort_column(self, "code", False))
        self.tree.heading("name", text="Name", command=lambda: sort_column(self, "name", False))
        self.tree.heading("college", text="College", command=lambda: sort_column(self, "college", False))

        self.tree.column("code", width=100, anchor="center", stretch=tk.NO)
        self.tree.column("name", width=450, anchor="w", stretch=tk.YES)
        self.tree.column("college", width=100, anchor="center", stretch=tk.NO)

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Edit Program", command=self.edit_selected)
        self.menu.add_command(label="Delete Program", command=self.delete_selected)

        self.tree.bind("<Button-3>", self.show_menu)

    def refresh(self):
        query = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())

        if not data.program_data: prettyPrint("program data not available"); return

        for code, info in data.program_data.items():
           
            if any(query in str(v).lower() for v in [code, info['name'], info['college']]):
                self.tree.insert("", "end", values=(code, info['name'], info['college']))

        sort_column(self, self.CurrentSort, self.ReverseSort)

    def show_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu.post(event.x_root, event.y_root)

    def edit_selected(self):
        values = self.tree.item(self.tree.selection()[0])['values']
        self.open_editor(values)

    def delete_selected(self):
        code = self.tree.item(self.tree.selection()[0])['values'][0]
        if data.DeleteProgram(code): self.refresh()

    def open_editor(self, info=None):
        EditorWindow(self, "Program", info)

class EditorWindow(tk.Toplevel):
    def __init__(self, parent, mode, info=None):
        super().__init__(parent)

        self.parent = parent
        self.mode = mode
        self.info = info

        self.title(f"{'Edit' if info else 'Add'} {mode}")

        self.width = 400
        self.height = 230

        self.setup_geometry()
        apply_theme(self, getTheme())
        self.setup_ui()

    def setup_geometry(self):
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(self.width,self.height)

        setup_geometry(self, self.width, self.height)

    def setup_ui(self):
        f = ttk.Frame(self, padding=20)
        f.pack(expand=True, fill="both")

        ttk.Label(f, text=f"{self.mode} Code:").pack(pady=5)
        self.ent_code = ttk.Entry(f)
        self.ent_code.pack(fill="x")

        if self.info:
            self.ent_code.insert(0, self.info[0])
            self.ent_code.config(state="disabled")

        ttk.Label(f, text="Name:").pack(pady=5)
        self.ent_name = ttk.Entry(f)
        self.ent_name.pack(fill="x")

        if self.info: self.ent_name.insert(0, self.info[1])

        if self.mode == "Program":
            
            self.height += 60
            self.setup_geometry()

            ttk.Label(f, text="College:").pack(pady=5)
            self.cb_college = ttk.Combobox(f, values=list(data.college_data.keys()), state="readonly")
            self.cb_college.pack(fill="x")
            if self.info: self.cb_college.set(self.info[2])

        ttk.Button(f, text="Save Data", style="Accent.TButton", command=self.save).pack(pady=20)

    def save(self):
        code = self.ent_code.get().strip()
        name = self.ent_name.get().strip()
        
        prettyPrint(f"attempt to {'Edit' if self.info else 'Add'}: {self.mode}")

        if self.mode == "College":
            if self.info: data.EditCollege(code, name)
            else: data.AddCollege([code, name])
        else:
            college = self.cb_college.get()
            if self.info: data.EditProgram(code, [name, college])
            else: data.AddProgram([code, name, college])

        self.parent.refresh()
        self.destroy()