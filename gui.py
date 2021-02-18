from datetime import datetime
import os
from PIL import ImageTk, Image
import PIL.Image
import sys
import time
from tkinter import *
from tkinter import ttk as ttk
import tkinter as tk
import tkinter
import json
from io import BytesIO

import requests
from PIL import ImageTk, Image
import PIL.Image


counter = 0
running = False

root = tk.Tk()
root.title('Yoga Flow Generator')

canvas = tk.Canvas(root, height=700, width=700, bg = '#FA8072')
canvas.pack()

frame = tk.Frame(root, bg='white')
frame.place(relwidth=0.8, relheight=0.8, relx = 0.09, rely=0.07)

# Creating the pop up window

# Adding images to GUI
base = "pose_illustrations/leet_poses/yoga_master.jpg"

#buffer = BytesIO()
#base = requests.get('URL').content
#buffer.write(b'')
#buffer.seek(0)

img = ImageTk.PhotoImage(PIL.Image.open(base))

panel = tk.Label(frame, bg='white', image = img, width=500, height=500)

panel.pack()
panel.place(x=30, y=30)


_images = []
for filepath, _, files in list(os.walk('pose_illustrations')):
    for img in files:
        _images.append(filepath.replace('\\','/') + '/' + img)

images = iter(_images)


def next_img():
    global images
    
    try:
        img = next(images)  # gets next image from iterator
    except StopIteration:
        #return  # if no more images, nothing happens
        images = iter(_images)
        img = next(images)
    except FileNotFoundError:
        # online
        return

    root.title('NOW DO THE [' + img.split('/')[-1].split('.')[0] + ']')
    # load and display image
    img = PIL.Image.open(img)
    img = ImageTk.PhotoImage(img)
    panel.img = img
    panel['image'] = img


# Creating a min:sec stop watch
def counter_label(label):
    def count():
        if running:
            global counter

            # Initial delay exists, so need to counter this
            if counter == 0:
                display = '00:00'
            else:
                tt = datetime.fromtimestamp(counter)
                string = tt.strftime('%M:%S')
                display = string

            label['text'] = display

            label.after(1000, count)    # Delays by 1000ms (1 second) and calls count function again.
            counter += 1

    # Triggering the counter
    count()


# Start function of the stopwatch
def Start(label):
    global running
    running = True
    counter_label(label)
    start['state'] = 'disabled'
    stop['state'] = 'normal'
    reset['state'] = 'normal'


# Stop function of the stopwatch
def Stop():
    global running
    start['state'] = 'normal'
    stop['state'] = 'disabled'
    reset['state'] = 'normal'
    running = False


# Reset function of the stopwatch
def Reset(label):
    global counter
    counter = 0

    # If reset is pressed after pressing stop
    if running == False:
        reset['state'] = 'disabled'
        label['text'] = '00:00'

    # If reset is pressed while the stopwatch is running
    else:
        label['text'] = '00:00'


if __name__ == "__main__":


    # Pulling the illustrations from poselist.py
    #pose_pics = list(os.walk('pose_illustrations')[1:])

    illustrationButton = tk.Button(frame, relief=FLAT, text='NEXT POSITION',bg="#FFC3B3", fg='#595858', width=30, font='avory 10 bold', command=next_img)
    illustrationButton.pack()

    # show the first image
    next_img()

    
    # Customizing buttons
    label = tk.Label(frame, relief = FLAT, text='00:00', fg='#FFC3B3', bg='white', font='avory 25 bold')
    start = tk.Button(frame, relief = FLAT, text='START', fg='#595858', bg='#FFC3B3', width=5, font='avory 8 bold', command=lambda:Start(label))
    stop = tk.Button(frame, relief = FLAT, text='STOP', fg='#595858', bg='#FFC3B3', width=5, font='avory 8 bold', state='disabled', command=Stop)
    reset = tk.Button(frame, relief = FLAT, text='RESET', fg='#595858', bg='#FFC3B3', width=5, font='avory 8 bold', state='disabled', command=lambda:Reset(label))
    label.pack()
    start.pack()
    stop.pack()
    reset.pack()
    label.place(x=30, y=480)
    start.place(x=5, y=530)
    stop.place(x=52, y=530)
    reset.place(x=99, y=530)

    root.mainloop()
