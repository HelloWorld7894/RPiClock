from tkinter import *
import customtkinter as ctk

import time
from datetime import datetime

import os
import sys
import RPi.GPIO as GPIO
import pyautogui

import math

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

def MoveMouse(channel): #just to wake up the waveshare screen
    pyautogui.moveTo(100, 100)
    pyautogui.moveTo(150, 150)
    pyautogui.moveTo(100, 100)

#
# SETUP
#
ctk.set_appearance_mode("dark")
window = ctk.CTk()
window.attributes('-fullscreen', True)
window.configure(bg='black')
window.bind('<Escape>', close)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(37, GPIO.RISING, callback=MoveMouse)

#
# RUN
#
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
canvas.create_image((100, 100), image=img)

def Update():
    if running == False:
        exit(1)

    now = datetime.now()
    Hour = now.hour if now.hour <= 12 else now.hour - 12 #formatting to 12-hour format

    #change time
    timelabel.configure(text=now.strftime("%H:%M:%S"))
    datelabel.configure(text=now.strftime("%A, %e %B"))

    #change analog clock value
    canvas.delete("all")
    canvas.create_image((100, 100), image=img)

    #hours
    canvas.create_line(100, 100, 100+40*math.sin(math.radians(Hour*hour_ratio)), 100-40*math.cos(math.radians(Hour*hour_ratio)), fill="white", width=5)
    
    #minutes
    canvas.create_line(100, 100, 100+80*math.sin(math.radians(now.minute*min_ratio)), 100-80*math.cos(math.radians(now.minute*min_ratio)), fill="white", width=5)

    #seconds
    canvas.create_line(100, 100, 100+80*math.sin(math.radians(now.second*min_ratio)), 100-80*math.cos(math.radians(now.second*min_ratio)), fill="white", width=2)

    window.after(1000, Update)

Update()

window.mainloop()
