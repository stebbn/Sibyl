import csv

dataLoc   = "../data.csv"
data_dict = {
    # student data defines the keys for its dictionary.
    "StudentData": ["id", "first_name", "last_name", "program_code", "year", "gender"],
    
    "CollegeData": {
        "CCS": {
            "name": "College of Computer Studies",
            "programs": ["BSCS", "BSIT", "BSIS"]
        },
        "COET": {
            "name": "College of Engineering and Technology",
            "programs": ["BSCE", "BSME", "BSEE", "BSECE", "BSChE", "BSCpE", "BSCerE", "BSMetE"]
        },
        "CSM": {
            "name": "College of Science and Mathematics",
            "programs": ["BSBio", "BSChem", "BSMath", "BSPhys", "BSStat"]
        },
        "CASS": {
            "name": "College of Arts and Social Sciences",
            "programs": ["BAPsych", "BSPsych", "BAELS", "BALCS", "BAFil", "BAHis", "BAPoS", "BASoc"]
        },
        "CEBA": {
            "name": "College of Economics, Business and Accountancy",
            "programs": ["BSA", "BSBA-MM", "BSBA-Econ", "BSHM"]
        },
        "CED": {
            "name": "College of Education",
            "programs": ["BEEd", "BSEd-Sci", "BSEd-Math", "BTVTEd", "BTLEd"]
        },
        "CHS": {
            "name": "College of Health Sciences",
            "programs": ["BSN"]
        }
    },

    "ProgramNames": {
        # CCS
        "BSCS": "Bachelor of Science in Computer Science",
        "BSIT": "Bachelor of Science in Information Technology",
        "BSIS": "Bachelor of Science in Information Systems",
        # COET
        "BSCE": "Bachelor of Science in Civil Engineering",
        "BSME": "Bachelor of Science in Mechanical Engineering",
        "BSEE": "Bachelor of Science in Electrical Engineering",
        "BSECE": "Bachelor of Science in Electronics and Communications Engineering",
        "BSChE": "Bachelor of Science in Chemical Engineering",
        "BSCpE": "Bachelor of Science in Computer Engineering",
        "BSCerE": "Bachelor of Science in Ceramic Engineering",
        "BSMetE": "Bachelor of Science in Metallurgical Engineering",
        # CSM
        "BSBio": "Bachelor of Science in Biology",
        "BSChem": "Bachelor of Science in Chemistry",
        "BSMath": "Bachelor of Science in Mathematics",
        "BSPhys": "Bachelor of Science in Physics",
        "BSStat": "Bachelor of Science in Statistics",
        # CASS
        "BAELS": "Bachelor of Arts in English Language Studies",
        "BALCS": "Bachelor of Arts in Literary and Cultural Studies",
        "BSPsych": "Bachelor of Science in Psychology",
        "BAFil": "Bachelor of Arts in Filipino",
        # CED
        "BTVTEd": "Bachelor of Technical-Vocational Teacher Education",
        "BTLEd": "Bachelor of Technology and Livelihood Education",
        # CHS
        "BSN": "Bachelor of Science in Nursing"
    }
}

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
    data = 1

def FindData():
    data = 1

def FindUser():
    data = 1
