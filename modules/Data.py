import csv
import json
import re
import time

from pathlib import Path

def prettyPrint(msg):
    print("[DATA]:", msg)

BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR.parent / "data" / "directory.json"
data_path = BASE_DIR.parent / "data" / "data.csv"

dataFormat = ["id_no", "first_name", "last_name", "program_code", "year", "gender"]
database = {}

try:
    with open(json_path, 'r') as f:
        data_dict = json.load(f)
except Exception as e:
    prettyPrint(f"Critical Error: {e}")
    raise SystemExit("Unable to Load Directory Data.")

#-----------------------------utils---------------------------------#

def format_college_prog(code: str) -> bool | str:
    for i in data_dict.get("ProgramNames", {}):
        if i.upper() == code.strip().upper():
            return i
    return False

def get_college_by_program(program_code: str) -> str:
    program_code = format_college_prog(program_code)
    if not program_code: 
        return "invalid program code"

    for name, info in data_dict.get("CollegeData", {}).items():
        if program_code in info.get("programs", []):
            return info.get("name", name)
    return "program not found in a college"

def pack_data(table) -> dict:
    return {
        table[0]: {
            'first_name': table[1],
            'last_name': table[2],
            'program_code': table[3],
            'year': table[4],
            'gender': table[5]
        }
    }

def pack_data_csv(table) -> dict:
    return dict(zip(dataFormat, table))

def get_file_parent(): return BASE_DIR.parent

#-------------------------------------------------------------------#

def AddData(data_table) -> bool:
    global database

    try:
        needs_newline = False
        if data_path.exists() and data_path.stat().st_size > 0:
            with open(data_path, 'rb+') as f_check:
                f_check.seek(-1, 2)
                if f_check.read(1) != b'\n':
                    needs_newline = True

        with open(data_path, mode='a', newline='', encoding='utf-8') as f:
            if needs_newline: 
                f.write('\n')
            writer = csv.DictWriter(f, fieldnames=dataFormat)
            writer.writerow(pack_data_csv(data_table))
            
        database.update(pack_data(data_table))
        prettyPrint(f"Successfully added {data_table[0]}")
        return True
    except Exception as e:
        prettyPrint(f"Add Error: {e}")
        return False
    
def EditData(id : str, new_data_table : dict) -> bool:
    global database
    current_data = GetData()

    if id not in current_data:
        return False

    del current_data[id]
    current_data.update(pack_data(new_data_table))
 
    try:
        with open(data_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=dataFormat)
            writer.writeheader()
            for sid, info in current_data.items():
                row = {'id_no': sid, **info}
                writer.writerow(row)
        
        database = current_data
        prettyPrint(f"Edited {id} | {new_data_table}")
        return True
    except Exception as e:
        prettyPrint(f"Edit Error: {e}")
        return False

def FindData(student_id : str) -> bool | dict:
    all_students = GetData() 
    if student_id in all_students:
        return {student_id: all_students[student_id]}
    return False

def UpdateData() -> dict:
    global database
    loaded_data = {}

    runStart = time.perf_counter()

    try:
        if not data_path.exists():
            return {}
        with open(data_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                loaded_data[row['id_no']] = {
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "program_code": row['program_code'],
                    "year": row['year'],
                    "gender": row['gender']
                }
        database = loaded_data
        prettyPrint("Data successfully synced")
    except Exception as e:
        prettyPrint(f"Sync Error: {e}")
        database = {"bum alert" : 
                    {
                    "first_name": "something",
                    "last_name": "failed",
                    "program_code": "the",
                    "year": "loading",
                    "gender": "so pls get good"
                    }
                }
    runEnd = time.perf_counter()
    prettyPrint(f"took {runEnd - runStart} seconds for data laod.")

    return database

def DeleteData(student_id : str) -> bool:
    global database
    current_data = GetData()

    if student_id not in current_data:
        return False

    del current_data[student_id]

    try:
        with open(data_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=dataFormat)
            writer.writeheader()
            for sid, info in current_data.items():
                row = {'id_no': sid, **info}
                writer.writerow(row)

        database = current_data
        prettyPrint(f"Deleted {student_id}")
        return True
    except Exception as e:
        prettyPrint(f"Delete Error: {e} | Data remains the same.")
        return False

def GetData() -> dict:
    global database
    return database if database else UpdateData()

# might change this to a util module
def VerifyFormat(data_type : str, user_input : str, name : str) -> list[bool, str]:
    val = user_input.strip()
    if not val:
        return [False, f"{name} is required."]

    if data_type == dataFormat[0]:
        if FindData(val): 
            return [False, "ID already exists."]
        if not re.match(r"^\d{4}-\d{4}$", val):
            return [False, "Format: 0000-0000"]
        year = int(val.split("-")[0])
        if 2000 <= year <= 2026:
            return [True, val]
        return [False, "Year must be 2000-2026"]

    elif data_type in (dataFormat[1], dataFormat[2]):
        if all(x.isalpha() or x.isspace() for x in val):
            return [True, val.title()]
        return [False, "Letters only"]
    
    elif data_type == dataFormat[3]:
        fmt = format_college_prog(val)
        return [True, fmt] if fmt else [False, "Invalid program"]

    elif data_type == dataFormat[4]:
        if val.isdigit() and 1 <= int(val) <= 5:
            return [True, val]
        return [False, "Range: 1-5"]

    return [True, val]

def GetFormat(): return dataFormat

UpdateData()