from tkinter import *
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import business
from business import Business
import sqlite3
import json
import os.path
import socket


class UI(tk.Tk):
    def __init__(self, fileName):
        self.b = Business()
        super().__init__()

        self.canvas = tk.Canvas(self, height=200, width=200)
        self.canvas.pack()

        frame = tk.Frame(self.canvas, background='#2C5881', border=5)
        frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        self.OPTIONS = self.b.individual_country_list
        self.variable = StringVar(self.master)
        self.variable.set(self.OPTIONS[0])

        print("OPTIONS", self.OPTIONS)
        w = OptionMenu(frame, self.variable, *self.OPTIONS)
        w.config(width=100, bg="BLACK")
        w.grid(column=3, row=3)

        button = Button(frame, text="OK", command=self.displayDialog)
        button.place(relx=0.05, rely=0.6, relwidth=0.4, relheight=0.2)
        button.config(font=("Palatino Linotype", 20, 'bold'))

        for file in fileName:
            if not os.path.exists(file) or not os.path.isfile(file):
                tk.messagebox.showwarning("Error", "Cannot open this file\n(%s)" % file)

    def displayDialog(self):
        dWin = DialogWindow(self, self.b.individual_country_list)
        self.wait_window(dWin)
        selection = dWin.getSelection()
        plt.show(self.b.getJson(selection))


class DialogWindow(tk.Toplevel):
    def __init__(self, master, b):
        self.b = b
        tk.Toplevel.__init__(self, master)

        self.grab_set()
        self.focus_set()
        self.transient(master)

        self.country = ""

    def setSelection(self):
        self.country = self.variable.get()
        print(self.country)
        self.destroy()

    def getSelection(self):
        return self.country


file = ['UNData.db']
mainWin = UI(file)
mainWin.mainloop()
