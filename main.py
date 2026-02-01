import tkinter
import sv_ttk
import darkdetect
import pywinstyles

from datetime import datetime

import sys
import csv

from tkinter import ttk

root = tkinter.Tk()

window_width = 600
window_height = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

def onButtonPress():
    with open('./data/data.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ')
        spamwriter.writerow(['gi pindot'] + ['|'] + [datetime.now().strftime("%H:%M:%S")])
    print("Data written!")

button = ttk.Button(root, text="dark mode test", command=onButtonPress)
button.pack()

sv_ttk.set_theme(darkdetect.theme())
sv_ttk.set_theme("dark")

def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

apply_theme_to_titlebar(root)
root.mainloop()