import csv
import json

from pathlib import Path

def prettyPrint(msg):
    print("[DATA]:", msg)

BASE_DIR = Path(__file__).resolve().parent

json_path = BASE_DIR.parent / "data" / "directory.json"
data_path = BASE_DIR.parent / "data" / "data.csv"

dataFormat = ["id_no", "first_name", "last_name", "program_code", "year", "gender"]

try:
    with open(json_path, 'r') as f:
        data_dict = json.load(f)
except FileNotFoundError as e:
    prettyPrint(f"{e}")
except Exception as e:
    prettyPrint(f"An unexpected error occurred: {e}")
    raise Exception("Unable to Load Data!")

def get_college_by_program(program_code : str):
    program_code = program_code.upper()

    print(program_code)

    for i, info in data_dict["CollegeData"].items():
        if program_code in info["programs"]:
            return info["name"]
    return "invalid program code"

def WriteData():
    data = 1

def EditData():
    data = 2

def GetData():
    database = {}
   
    try:
        with open(data_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=dataFormat)

            for row in reader:
                student_id = row['id_no']
                database[student_id] = [
                    row['first_name'],
                    row['last_name'],
                    row['program_code'],
                    row['year'],
                    row['gender']
                ]
        return database
    except FileNotFoundError:
        prettyPrint(f"{data_path} not found.")
        return {}

currentData = GetData()

def getDictData(): return currentData

def FindData():
    data = 1

def FindUser():
    data = 1

def GetFormat(): return dataFormat