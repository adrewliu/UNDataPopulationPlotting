import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os.path
from tkinter import messagebox
from business import Business


class PlotWindow(tk.Toplevel):
    '''
    this class plots the price trend or bar chart depending on the user choice
    '''

    def __init__(self, master, fct, *args):
        self.master = master
        super().__init__(master)
        #self.rent = rent
        plt.clf()
        self.fig = plt.figure(figsize=(8, 7))
        #plt.clf()
        fct(*args)
        #plt.show()
        #plt.clf()
        #plt.cla()
        #plt.close()
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()
        #plt.show()

        #plt.plot()
        #self.closePlot()
'''
    def closePlot(self):
        plt.cla()
        plt.close(self.fig)
'''



