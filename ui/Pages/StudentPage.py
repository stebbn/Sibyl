import modules.Data as data

from tkinter import ttk

def prettyPrint(msg : str): 
    print("[STUDENT]:", msg)

fields = ["ID Number", "First Name", "Last Name", "Program Code", "Year Level", "Gender"]

class StudentPageFrame(ttk.Frame):
    def __init__(self, master, controller):
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
        entry.bind("<<ComboboxSelected>>", lambda e: self.focus())
        entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.entries[5] = entry

        ttk.Button(
            self.form_container, 
            text="Save Student Record", 
            style="Accent.TButton",
            command=self.save_data
        ).grid(row=len(fields), column=0, columnspan=2, pady=10)

        self.WarnLabel = ttk.Label(
                    self.form_container, 
                    text="",
                    foreground= "#B92905"
                )
        self.WarnLabel.grid(row=len(fields)+1, column=0, columnspan=2, pady=0)

    def save_data(self):
      self.WarnLabel.config(text="")

      format = data.GetFormat()
      to_pack = {}

      for i, data_item in enumerate(format):
          inputted = self.entries[i].get().strip()
          verified, msg = data.VerifyFormat(data_item, inputted, fields[i])
          # msg contains corrected format

          if inputted and verified == True:
            to_pack[i] = msg
          elif verified != True:
              self.WarnLabel.config(text=msg)
              return
          else: 
              to_pack[i] = None
              # useless rn lo

      data.AddData(to_pack)

class EditTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
       
    def setup_ui(self):
        self.form_container = ttk.Frame(self)
        self.form_container.place(relx=0.5, rely=0.51, anchor="center")

        self.SearchEntry = ttk.Entry(self.form_container, width=30)
        self.SearchEntry.grid(row=3, column=0, padx=10, pady=10, sticky="w")
       
        self.CurrentButton = ttk.Button(
                            self.form_container, 
                            text="Select Id", 
                            style="Accent.TButton",
                            command=self.search_id
                        )
        self.CurrentButton.grid(row=4, column=0, columnspan=2, pady=10)
        self.WarnLabel = False

    def warn(self, msg : str):
        if not self.WarnLabel:
                self.WarnLabel = ttk.Label(
                self.form_container, 
                text=msg,
                foreground= "#B92905"
            )
                self.WarnLabel.grid(row=self.CurrentButton.grid_info()["row"]+1, column=0, columnspan=2, pady=0)
        else:
            self.WarnLabel.config(text=msg)
            self.WarnLabel.grid(row=self.CurrentButton.grid_info()["row"]+1, column=0, columnspan=2, pady=0)

    def search_id(self): 
        search = data.FindData(self.SearchEntry.get())
        if search:
            return True
        else:
            self.warn("ID Not Found.")



    def edit_id(): return True

class SearchTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Search Registry").pack(pady=20)