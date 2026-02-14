import darkdetect
from ui.Sidebar import SidebarFrame

def getTheme():
    return "Dark" if darkdetect.theme() == "Dark" else "Light"

def getBG(theme):
    settings = getUiSettings()
    return settings["DarkBackground"] if theme == "Dark" else settings["LightBackground"]

def getUiSettings():
    return {
       "LightBackground" : "#DFDFDF",
       "LightForeground" : "#FFFFFF",

       "DarkBackground"  : "#1A1919",
       "DarkForeground"  : "#FFFFFF"
    }

print("- ui package loaded -")