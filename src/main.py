from tkinter import *
import customtkinter as ctk

import time
from datetime import datetime

import os
import sys

import math

#
# SETUP
#
ctk.set_appearance_mode("dark")
window = ctk.CTk()
#window.attributes('-fullscreen', True) #update later
window.geometry("320x240")
window.configure(bg='black')

#
# VARIABLES
#
running = True
min_ratio = 360 / 60
hour_ratio = 360 / 12

# close window
def close(event):
    global running
    running = False

window.bind('<Escape>', close)
canvas = ctk.CTkCanvas(window, width=200, height=212, bg='black')

timelabel = Label(window, text="", font=("NovaMono", 20), bg="black", fg="white")
datelabel = Label(window, text="", font=("Bahnschrift", 15), bg="black", fg="white")

datelabel.pack()
timelabel.pack()
canvas.pack()

#canvas setup
Path = os.path.abspath(__file__)
Path = Path[:len(Path)-11] + "imgs/clock.png"

img = PhotoImage(file = Path)
canvas.create_image((100, 106), image=img)



def UpdateTime():
    if running == False:
        exit(1)

    now = datetime.now()

    #change time
    timelabel.configure(text=now.strftime("%H:%M:%S"))
    datelabel.configure(text=now.strftime("%A, %e %B"))

    #change analog clock value
    canvas.delete("all")
    canvas.create_image((100, 106), image=img)
    
    hour_angle = hour_ratio * now.hour
    min_angle = min_ratio * now.minute

    hour_x = round(math.sin(hour_angle) * 80)
    hour_y = round(math.cos(hour_angle) * 80)
    
    min_x = round(math.sin(min_angle) * 40)
    min_y = round(math.cos(min_angle) * 40)

    if now.hour > 6:
        hour_x = 100 - hour_x
    else:
        hour_x = 100 + hour_x

    if 3 < now.hour < 6:
        hour_y = 106 - hour_y
    else:
        hour_y = 100 + hour_y

    if now.minute > 30:
        min_x = 100 - min_x
    else:
        min_x = 100 + min_x

    if 15 < now.minute < 30:
        min_y = 106 - min_y
    else:
        min_y = 100 + min_y

    canvas.create_line(100, 106, hour_x, hour_y, fill="white", width=5)
    canvas.create_line(100, 106, min_x, min_y, fill="white", width=5)

    window.after(1000, UpdateTime)

UpdateTime()

window.mainloop()