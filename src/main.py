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

footer = Label(window, text="RPiClock, very useless clock that just tells time", font=("NovaMono", 10), bg="black", fg="white")

datelabel.pack()
timelabel.pack()
canvas.pack()
footer.pack()

#canvas setup
Path = os.path.abspath(__file__)
Path = Path[:len(Path)-11] + "imgs/clock.png"

img = PhotoImage(file = Path)
canvas.create_image((100, 106), image=img)

def Update():
    if running == False:
        exit(1)

    now = datetime.now()

    #change time
    timelabel.configure(text=now.strftime("%H:%M:%S"))
    datelabel.configure(text=now.strftime("%A, %e %B"))

    #change analog clock value
    canvas.delete("all")
    canvas.create_image((100, 106), image=img)
    
    add_x = [100, 100, -100, -100]
    add_y = [-106, 106, 106, -106]
    for i in range(6, 25, 6):
        if now.hour <= i: 
            hour_angle = (hour_ratio * now.hour) - (90 * (i / 6 - 1))
            hour_x = abs(add_x[int(i / 6) - 1] + round(math.sin(hour_angle) * 40))
            hour_y = abs(add_y[int(i / 6) - 1] + round(math.cos(hour_angle) * 40))



    for i in range(15, 61, 15):
        if now.minute <= i: 
            min_angle = (min_ratio * now.minute) - (90 * (i / 15 - 1))
            min_x = abs(add_x[int(i / 15) - 1] + round(math.sin(min_angle) * 80))
            min_y = abs(add_y[int(i / 15) - 1] + round(math.cos(min_angle) * 80))

    canvas.create_line(100, 106, hour_x, hour_y, fill="white", width=5)
    canvas.create_line(100, 106, min_x, min_y, fill="white", width=5)

    window.after(1000, Update)

Update()

window.mainloop()
