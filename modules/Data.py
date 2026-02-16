import csv
import json
import re
import time

from pathlib import Path
from typing import Literal

def prettyPrint(msg):
    print("[DATA]:", msg)

BASE_DIR = Path(__file__).resolve().parent

colleges_path = BASE_DIR.parent / "data" / "colleges.csv"
programs_path = BASE_DIR.parent / "data" / "programs.csv"
data_path     = BASE_DIR.parent / "data" / "data.csv"

dataFormat = {
    "Student" : ["id_no", "first_name", "last_name", "program_code", "year", "gender"],
    "College" : ["college_code","college_name"],
    "Program" : ["program_code","program_name","college_code"]
}

college_data  = {}
program_data  = {}
student_data  = {}

#-----------------------------utils---------------------------------#

def format_college_prog(code: str) -> bool | str:
    for i in program_data:
        if i.upper() == code.strip().upper():
            return i
    return False

def get_college_by_program(program_code: str) -> str:
    program_code = format_college_prog(program_code)
    if not program_code: 
        return "invalid program code"

    college_code = program_data[program_code].get("college")
    return college_data.get(college_code, "College Not Found")

def VerifyFormat(data_type : str, user_input : str, name : str) -> list[bool, str]:
    val = user_input.strip()
    student_format = dataFormat["Student"]

    if not val:
        return [False, f"{name} is required."]

    if data_type == student_format[0]:
        if FindStudentData(val): 
            return [False, "ID already exists."]
        if not re.match(r"^\d{4}-\d{4}$", val):
            return [False, "Format: 0000-0000"]
        year = int(val.split("-")[0])
        if 2000 <= year <= 2026:
            return [True, val]
        return [False, "Year must be 2000-2026"]

    elif data_type in (student_format[1], student_format[2]):
        if all(x.isalpha() or x.isspace() for x in val):
            return [True, val.title()]
        return [False, "Letters only"]
    
    elif data_type == student_format[3]:
        fmt = format_college_prog(val)
        return [True, fmt] if fmt else [False, "Invalid program"]

    elif data_type == student_format[4]:
        if val.isdigit() and 1 <= int(val) <= 5:
            return [True, val]
        return [False, "Range: 1-5"]

    return [True, val]

def LoadCSV(file_path: Path, callback) -> dict:
    try:
        if not file_path.exists():
            prettyPrint(f"Warning: {file_path.name} not found.")
            return {}
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return callback(reader)
    except Exception as e:
        prettyPrint(f"Load Error [{file_path.name}]: {e}")
        return {"actual bum x3"}

def SaveCSV(type_key: Literal["Student", "College", "Program"], data_dict: dict) -> bool:
    paths = {"Student": data_path, "College": colleges_path, "Program": programs_path}
    
    try:
        with open(paths[type_key], mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=dataFormat[type_key])
            writer.writeheader()
            
            for key, info in data_dict.items():
                primary_key = dataFormat[type_key][0]
                row = {primary_key: key, **info}
                writer.writerow(row)
        return True
    except Exception as e:
        prettyPrint(f"Save Error [{type_key}]: {e}")
        return False

# ------------------------- main data funcs --------------------------------- #

def SyncAll():
    global student_data, college_data, program_data
    
    start = time.perf_counter()

    def student_cb(reader):
        return {row['id_no']: {k: row[k] for k in dataFormat["Student"][1:]} for row in reader}
    student_data = LoadCSV(data_path, student_cb)

    college_data = LoadCSV(colleges_path, lambda r: {row['college_code']: row['college_name'] for row in r})

    def program_cb(reader):
        return {row['program_code']: {"name": row['program_name'], "college": row['college_code']} for row in reader}
    program_data = LoadCSV(programs_path, program_cb)

    end = time.perf_counter()
    prettyPrint(f"Total load took {end - start:.4f} seconds.")

def SaveData(type: Literal["Student", "College", "Program"], data_dict: dict) -> bool:
    paths = {"Student": data_path, "College": colleges_path, "Program": programs_path}
    
    try:
        with open(paths[type], mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=dataFormat[type])
            writer.writeheader()
            
            for key, info in data_dict.items():
                primary_key = dataFormat[type][0]
              
                if type == "College":
                    row = {primary_key: key, "college_name": info}
                elif type == "Program":
                    row = {primary_key: key, "program_name": info["name"], "college_code": info["college"]}
                else:
                    row = {primary_key: key, **info}
                    
                writer.writerow(row)
        return True
    except Exception as e:
        prettyPrint(f"Unable to save [{type}]: {e}")
        return False
    
# Add datas ------------------------------------------------------------------------

def AddStudent(data_list) -> bool:
    global student_data
    sid = data_list[0]
   
    student_data[sid] = {
        'first_name': data_list[1],
        'last_name': data_list[2],
        'program_code': data_list[3],
        'year': data_list[4],
        'gender': data_list[5]
    }
    
    prettyPrint(f"Adding Student: {sid}")
    return SaveData("Student", student_data)

def AddCollege(data_list) -> bool:
    global college_data
    code = data_list[0].upper()
   
    college_data[code] = data_list[1]
    
    prettyPrint(f"Adding College: {code}")
    return SaveData("College", college_data)

def AddProgram(data_list) -> bool:
    global program_data
    p_code = data_list[0].upper()
    
    program_data[p_code] = {
        "name": data_list[1],
        "college": data_list[2].upper()
    }
    
    prettyPrint(f"Adding Program: {p_code}")
    return SaveData("Program", program_data)

# Edit datas -----------------------------------------------------------------------

def EditStudent(sid: str, new_data_list) -> bool:
    global student_data
    if sid not in student_data: return False

    student_data[sid] = {
        'first_name': new_data_list[1],
        'last_name': new_data_list[2],
        'program_code': new_data_list[3],
        'year': new_data_list[4],
        'gender': new_data_list[5]
    }
    return SaveData("Student", student_data)

def EditCollege(code: str, new_name: str) -> bool:
    global college_data
    code = code.upper()
    if code not in college_data: return False

    college_data[code] = new_name
    return SaveData("College", college_data)

def EditProgram(p_code: str, new_data_list) -> bool:
    global program_data
    p_code = p_code.upper()
    if p_code not in program_data: return False

    program_data[p_code] = {
        "name": new_data_list[1],
        "college": new_data_list[2].upper()
    }
    return SaveData("Program", program_data)

# Delete datas ---------------------------------------------------------------------

def DeleteStudent(sid: str) -> bool:
    global student_data
    if sid in student_data:
        del student_data[sid]
        return SaveData("Student", student_data)
    return False

def DeleteCollege(code: str) -> bool:
    global college_data
    code = code.upper()
    if code in college_data:
        del college_data[code]
        return SaveData("College", college_data)
    return False

def DeleteProgram(p_code: str) -> bool:
    global program_data
    p_code = p_code.upper()
    if p_code in program_data:
        del program_data[p_code]
        return SaveData("Program", program_data)
    return False

# ------------------------- retrieve stuff ----------------------------------------- #

def FindStudentData(student_id : str) -> bool | dict:
    all_students = student_data
    if student_id in all_students:
        return {student_id: all_students[student_id]}
    return False

def GetFormat(type : Literal["Student", "College", "Program"]) -> dict : return dataFormat[type]
def get_file_parent(): return BASE_DIR.parent

SyncAll()