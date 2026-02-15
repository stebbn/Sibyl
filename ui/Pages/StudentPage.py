import modules.Data as data

from tkinter import ttk

def prettyPrint(msg : str): 
    print("[STUDENT]:", msg)

fields = ["ID Number", "First Name", "Last Name", "Program Code", "Year Level", "Gender"]

def save_data(self, isEdit=False):
    self.warn("")
    data_format = data.GetFormat("Student")
    to_pack = []

    for i, data_item in enumerate(data_format):
        if isEdit and i == 0:
            to_pack.append(self.data_id)
            continue
        else:
            inputted = self.entries[i].get().strip()
            
        verified, msg = data.VerifyFormat(data_item, inputted, fields[i])

        if verified:
            to_pack.append(msg)
        else:
            self.warn(msg)
            return

    if isEdit:
        data.EditStudent(self.data_id, to_pack)
        self.warn("Succesfully edited.", "#18C421")
    else:
        data.AddStudent(to_pack)
        self.warn("Succesfully added.", "#18C421")

class StudentPageFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.pack(expand=True, fill="both") 

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_insert = InsertTab(self.notebook)
        self.tab_edit = EditTab(self.notebook)

        self.notebook.add(self.tab_insert, text="Insert New Student")
        self.notebook.add(self.tab_edit, text="Edit Information")

class InsertTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
        self.WarnLabel = False

        self.warn("")

    def setup_ui(self):
        self.form_container = ttk.Frame(self)
        self.form_container.place(relx=0.5, rely=0.51, anchor="center")

        self.entries = {}

        for i, field in enumerate(fields):
           if field == "Gender": 
                continue 
           
           ttk.Label(self.form_container, text=field + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")
           entry = ttk.Entry(self.form_container, width=30)
           entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
           self.entries[i] = entry

        ttk.Label(self.form_container, text=fields[5] + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        
        GenderOptions = ["Male", "Female", "Non-Binary"]

        entry = ttk.Combobox(self.form_container, values=GenderOptions, state="readonly", justify="center")
        self.entries[5] = entry
        entry.bind("<<ComboboxSelected>>", lambda e: self.focus())
        entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.CurrentButton = ttk.Button(
                self.form_container, 
                text="Save Student Record", 
                style="Accent.TButton",
                command=lambda:save_data(self)
            )
        self.CurrentButton.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def warn(self, msg : str, color="#B92905"):
        if not self.WarnLabel:
                self.WarnLabel = ttk.Label(
                self.form_container, 
                text=msg,
                foreground= color
            )
                self.WarnLabel.grid(row=self.CurrentButton.grid_info()["row"]+1, column=0, columnspan=2, pady=0)
        else:
            self.WarnLabel.config(text=msg, foreground=color)
            self.WarnLabel.grid(row=self.CurrentButton.grid_info()["row"]+1, column=0, columnspan=2, pady=0)

class EditTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
    
        self.warn("")

    def setup_ui(self):
        self.form_container = ttk.Frame(self)
        self.form_container.place(relx=0.5, rely=0.51, anchor="center")

        self.WarnLabel = False

        self.open_search()

    def warn(self, msg : str, color="#B92905"):
        if not self.WarnLabel:
                self.WarnLabel = ttk.Label(
                self.form_container, 
                text=msg,
                foreground= color
            )
                self.WarnLabel.grid(row=self.CurrentButton.grid_info()["row"]+1, column=0, columnspan=2, pady=0)
        else:
            self.WarnLabel.config(text=msg, foreground=color)
            self.WarnLabel.grid(row=self.CurrentButton.grid_info()["row"]+1, column=0, columnspan=2, pady=0)

    def clear_container(self):
        for widget in self.form_container.winfo_children():
                   widget.destroy()

        self.WarnLabel = False

    def open_search(self):
        self.clear_container()

        self.SearchEntry = ttk.Entry(self.form_container, width=30)
        self.SearchEntry.grid(row=3, column=0, padx=10, pady=10, sticky="w")
       
        self.CurrentButton = ttk.Button(
                            self.form_container, 
                            text="Select ID", 
                            style="Accent.TButton",
                            command=self.search_id
                        )
        self.CurrentButton.grid(row=4, column=0, pady=10)
        self.warn("")

    def search_id(self, id=None): 
        search = data.FindStudentData(id or self.SearchEntry.get())
        if search:
            self.open_edit(search)
        else:
            self.warn("ID Not Found.")

    def open_edit(self, student_data: dict):
        self.data_id = next(iter(student_data))
        data_content = student_data[self.data_id]
        data_format = data.GetFormat("Student")
        
        self.clear_container()
        self.entries = {}

        ttk.Label(self.form_container, text=f"Editing ID: {self.data_id}", font=("", 12, "bold")).grid(row=0, column=0, pady=20)

        for i, field in enumerate(fields[1:5], start=1):
            ttk.Label(self.form_container, text=field + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(self.form_container, width=30)
            entry.insert(0, data_content[data_format[i]])
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            self.entries[i] = entry

        ttk.Label(self.form_container, text="Gender:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        
        gender_options = ["Male", "Female", "Non-Binary"]

        combo = ttk.Combobox(self.form_container, values=gender_options, state="readonly", justify="center")
        combo.set(data_content[data_format[5]])
        combo.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        combo.bind("<<ComboboxSelected>>", lambda e: self.focus())

        self.entries[5] = combo

        self.CurrentButton = ttk.Button(
            self.form_container, 
            text="Update Student Record", 
            style="Accent.TButton",
            command=lambda: save_data(self, True)
        )
        self.CurrentButton.grid(row=6, column=0, padx=10, pady=5, sticky="e")

        ttk.Button(
            self.form_container, 
            text="Cancel / Back to Search", 
            command=self.open_search
        ).grid(row=6, column=1, padx=10, pady=5, sticky="w")

        self.warn("")