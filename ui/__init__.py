import sys
import darkdetect
import sv_ttk
import pywinstyles

from ui.Sidebar import SidebarFrame

def getTheme():
    return "Dark" if darkdetect.theme() == "Dark" else "Light"

def getBG(theme):
    settings = getUiSettings()
    return settings["DarkBackground"] if theme == "Dark" else settings["LightBackground"]

def getUiSettings():
    return {
       "LightBackground" : "#ECECEC",
       "LightForeground" : "#FFFFFF",

       "DarkBackground"  : "#1A1919",
       "DarkForeground"  : "#FFFFFF"
    }

def setup_geometry(self, width, height):
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    center_x = int(screen_width/2 - width / 2)
    center_y = int(screen_height/2 - height / 2)
    self.geometry(f'{width}x{height}+{center_x}+{center_y}')
  
def apply_theme(self, theme=None):
    theme = theme if theme else getTheme()

    sv_ttk.set_theme(theme)

    self.is_dark = sv_ttk.get_theme() == "dark"
    version = sys.getwindowsversion()
    color = getBG(theme)

    if version.major == 10 and version.build >= 22000:
        pywinstyles.change_header_color(self, color)
    elif version.major == 10:
        pywinstyles.apply_style(self, "dark" if self.is_dark else "normal")
        self.wm_attributes("-alpha", 0.99)
        self.wm_attributes("-alpha", 1)

print("- ui package loaded -")