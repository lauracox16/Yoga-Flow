"""Welcome to the world of software dev, (or DevOps or Cloud Engineering or Automation, etc. etc)
    here is a long complicated way to do something simple.

    Provided is a link to what you should expect in the software world
    https://www.youtube.com/watch?v=dQw4w9WgXcQ

    IMPORTANT
        make sure you're in the Yoga-Flow dir when running program
        also install requirements via `pip3 install -r requirements.txt`

    tips:
        - use vscode, and extensions pylint/Python Docstring Generator
        - write notes in markdown always
"""

from datetime import datetime
import os
from PIL import ImageTk, Image
import PIL.Image
import sys
import time
from tkinter import *
import tkinter as tk
import json
from io import BytesIO

import requests
from PIL import ImageTk, Image
import PIL.Image


class yoga_master:
    """yoga app start

    Returns:
        None: nothing
    """
    running = False
    _images = []
    # so if the images aren't included, you can bring down at runtime into memory
    _image_cache = {
        "pose_illustrations": {
            "high_poses": {
                "chair.png": "todo"
            },
            "low_poses": {
                "dog.jpg": "todo"
            },
            "leet_poses": {
                "yoga_master.jpg": "https://images.i.thechive.com/__c29b08d7193a0b43a0d38b12316f52bb_width-600.jpeg"
            }
        },
        "error": "https://www.freeiconspng.com/thumbs/error-icon/error-icon-32.png"
    }

    def __init__(self):
        """start of function
        """
        self.counter = 0

        self.root = tk.Tk()
        self.root.title('Yoga Flow Generator')

        canvas = tk.Canvas(self.root, height=700, width=700, bg = '#FA8072')
        canvas.pack()

        self.frame = tk.Frame(self.root, bg='white')
        self.frame.place(relwidth=0.8, relheight=0.8, relx = 0.09, rely=0.07)

        self.panel = tk.Label(self.frame, bg='white',  width=500, height=500)

        self.panel.pack()
        self.panel.place(x=30, y=30)

        illustrationButton = tk.Button(self.frame, 
                                        relief=FLAT, 
                                        text='NEXT POSITION',
                                        bg="#FFC3B3", 
                                        fg='#595858', 
                                        width=30, 
                                        font='avory 10 bold', 
                                        command=self.next_img )
        illustrationButton.pack()

        # show the first image
        self.next_img()

        # Customizing buttons
        self.label = tk.Label(self.frame, 
                            relief = FLAT, 
                            text='00:00', 
                            fg='#FFC3B3', 
                            bg='white', 
                            font='avory 25 bold'
        )
        
        self.start = tk.Button(self.frame, 
                            relief = FLAT, 
                            text='START', 
                            fg='#595858', 
                            bg='#FFC3B3', 
                            width=5, 
                            font='avory 8 bold', 
                            command=lambda: self.Start())

        self.stop = tk.Button(self.frame, 
                            relief = FLAT, 
                            text='STOP', 
                            fg='#595858', 
                            bg='#FFC3B3', 
                            width=5, 
                            font='avory 8 bold', 
                            state='disabled', 
                            command= self.Stop)

        self.reset = tk.Button(self.frame, 
                            relief = FLAT, 
                            text='RESET', 
                            fg='#595858', 
                            bg='#FFC3B3', 
                            width=5, 
                            font='avory 8 bold', 
                            state='disabled', 
                            command=lambda: self.Reset())
        
        self.label.pack()
        self.label.place(x=30, y=480)
        
        self.start.pack()
        self.stop.pack()
        self.reset.pack()
        
        self.start.place(x=5, y=530)
        self.stop.place(x=52, y=530)
        self.reset.place(x=99, y=530)

        self.root.mainloop()

    @property
    def images(self):
        """Returns list of filepaths to images

        Returns:
            list: see above
        """
        if not self._images:
            for filepath, _, files in list(os.walk('pose_illustrations')):
                for img in files:
                    self._images.append(filepath.replace('\\','/') + '/' + img)
            self._images = iter(self._images)
        
        return self._images

    def next_img(self):
        """um.... read title?
        """
        try:
            img_filepath = next(self.images)  # gets next image from iterator
        except StopIteration:
            # TODO: Cheeky way of doing loop of images, this is lazy
            self._images = []
            img_filepath = next(self.images)

        self.root.title('NOW DO THE [' + img_filepath.split('/')[-1].split('.')[0] + ']')

        # load and display image
        try:
            img = PIL.Image.open(img_filepath)
        except FileNotFoundError:
            # try and grab file from online, else display error
            img = self._pull_from_online(img_filepath)
            img = PIL.Image.open(img)

        img = ImageTk.PhotoImage(img)
        self.panel.img = img
        self.panel['image'] = img

    def _pull_from_online(self, filepath):
        """Pull from online, if not exists

        Args:
            filepath (str): path to file

        Returns:
            io.BytesIO: basically just bytes of file
        """
        
        # drill down in dict, based on filepath
        # see online_backup.json
        folder = filepath.split('/')[1]
        img_file = filepath.split('/')[2]
        try:
            img = self._image_cache['pose_illustrations'][folder][img_file]
        except KeyError:
            # lazy 
            if isinstance(self._image_cache['error'], BytesIO):
                return self._image_cache['error']
            else:
                buffer = BytesIO()
                raw_file = requests.get(self._image_cache['error']).content
                buffer.write(raw_file)
                buffer.seek(0)
                # for cache
                self._image_cache['error'] = buffer
                return self._image_cache['error']
        
        # if we already have pulled image, return it
        if isinstance(img, BytesIO):
            return img
        # else img == url link

        buffer = BytesIO()
        try:
            raw_file = requests.get(img).content
        except: # too lazy to find error exception
            if isinstance(self._image_cache['error'], BytesIO):
                return self._image_cache['error']
            else:
                raw_file = requests.get(self._image_cache['error']).content

        buffer.write(raw_file)
        buffer.seek(0)
        # for cache
        self._image_cache['pose_illustrations'][folder][img_file] = buffer

        return buffer

    def counter_label(self):
        """Creating a min:sec stop watch
        """
        def count():
            if self.running:
                # Initial delay exists, so need to counter this
                if self.counter == 0:
                    display = '00:00'
                else:
                    tt = datetime.fromtimestamp(self.counter)
                    string = tt.strftime('%M:%S')
                    display = string

                self.label['text'] = display

                self.label.after(1000, count)    # Delays by 1000ms (1 second) and calls count function again.
                self.counter += 1

        # Triggering the counter
        count()

    def Start(self):
        """Start function of the stopwatch
        """
        self.running = True
        self.counter_label()
        self.start['state'] = 'disabled'
        self.stop['state'] = 'normal'
        self.reset['state'] = 'normal'

    def Stop(self):
        """Stop function of the stopwatch
        """
        self.start['state'] = 'normal'
        self.stop['state'] = 'disabled'
        self.reset['state'] = 'normal'
        self.running = False

    def Reset(self):
        """Reset function of the stopwatch
        """
        self.counter = 0

        # If reset is pressed after pressing stop
        if self.running == False:
            self.reset['state'] = 'disabled'
            self.label['text'] = '00:00'

        # If reset is pressed while the stopwatch is running
        else:
            self.label['text'] = '00:00'

yoga_master()
