import csv
import json
import re

from pathlib import Path

def prettyPrint(msg):
    print("[DATA]:", msg)

BASE_DIR = Path(__file__).resolve().parent

json_path = BASE_DIR.parent / "data" / "directory.json"
data_path = BASE_DIR.parent / "data" / "data.csv"

dataFormat = ["id_no", "first_name", "last_name", "program_code", "year", "gender"]
database   = False

try:
    with open(json_path, 'r') as f:
        data_dict = json.load(f)
except FileNotFoundError as e:
    prettyPrint(f"{e}")
except Exception as e:
    prettyPrint(f"An unexpected error occurred: {e}")
    raise Exception("Unable to Load Data!")

def format_college_prog(code : str):
    prettyPrint("program code:" + code)

    for i,v in data_dict["ProgramNames"].items():
        if i.upper() == code.upper():
            return i
        
    return False

def get_college_by_program(program_code : str):
    program_code = format_college_prog(program_code)

    if not program_code: return "invalid program code"

    for i, info in data_dict["CollegeData"].items():
        if program_code in info["programs"]:
            return info["name"]
    return "program not found in a college (?)"

def AddData(data_table):
    try:
        with open(data_path, mode='a', newline='', encoding='utf-8') as f:
            if f.tell() != 0: #check if empty
                pass 
                
            writer = csv.DictWriter(f, fieldnames=dataFormat)
            
            row_to_save = {
                'id_no': data_table[0],
                'first_name': data_table[1],
                'last_name': data_table[2],
                'program_code': data_table[3],
                'year': data_table[4],
                'gender': data_table[5]
            }
            
            writer.writerow(row_to_save)
            prettyPrint(f"successfully wrote {data_table[0]}'s data")
            UpdateData()
            return True
    except Exception as e:
        print(f"Error: {e}")

def EditData():
    data = 2

def FindData(id):
    return False

def FindUser():
    data = 1

def UpdateData():
    database = {}
    try:
        with open(data_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=dataFormat)
            for row in reader:
                student_id = row['id_no']

                database[student_id] = {
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "prog_code": row['program_code'],
                    "year": row['year'],
                    "gender": row['gender']
                }
        return database
    except FileNotFoundError:
        prettyPrint(f"{data_path} not found.")
        return {}

def GetData():
    if not database:
        UpdateData()
        return database
    else:
        return database
    
def GetFormat(): return dataFormat

def VerifyFormat(data_type, user_input, name):
    if not user_input or not user_input.strip():
        return [False, f"{name} is required."]

    if data_type == dataFormat[0]:
        if not re.match(r"^\d{4}-\d{4}$", user_input):
            return [False, "Use format: 0000-0000"]
            
        year_part = user_input.split("-")[0]
        if 2000 <= int(year_part) <= 2026:
            return [True, user_input]
        else:
            return [False, "ID Year must be between 2000 and 2026."]

    elif data_type == dataFormat[1] or data_type == dataFormat[2]:
        if all(x.isalpha() or x.isspace() for x in user_input):
            return [True, user_input.title()]
        return [False, f"{name} Letters and spaces only"]
    
    elif data_type == dataFormat[3]:
        formatted = format_college_prog(user_input)
        print(formatted)
        if not formatted:
            return [False, f"{name} is an invalid program."]
        return [True, formatted]

    elif data_type == dataFormat[4]:
        if user_input.isdigit() and 1 <= int(user_input) <= 5:
            return [True, user_input]
        return [False, f"{name} Must be between 1-5"]

    return [True, user_input]