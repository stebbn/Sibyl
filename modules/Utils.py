import sys
import darkdetect
import sv_ttk
import pywinstyles

from PIL import Image, ImageTk, ImageOps

def processImage(file_loc, w, h, dark_mode_invert = False) -> ImageTk.Image:
    og_img = Image.open(file_loc)

    if dark_mode_invert and getTheme() == "Light":
        
        r, g, b, a = og_img.split()
        rgb_img = Image.merge('RGB', (r, g, b))
        inverted_rgb = ImageOps.invert(rgb_img)
       
        r2, g2, b2 = inverted_rgb.split()
        og_img = Image.merge('RGBA', (r2, g2, b2, a))

    aliased_image = og_img.resize((w, h), Image.Resampling.LANCZOS)

    photo_image = ImageTk.PhotoImage(aliased_image)
    return photo_image

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