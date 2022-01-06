import socket
from business import Business
import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import *


client_socket = socket.socket()
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
port = 2048
conn = False


class DialogWindow(tk.Toplevel):

    def __init__(self, master, business, b):
        global conn
        self.business = business
        self.b = b
        self.conn = conn
        tk.Toplevel.__init__(self, master)

        canvas = tk.Canvas(self, height=500, width=500, background='#2C5881')
        canvas.pack()

        self.grab_set()
        self.focus_set()
        self.transient(master)

        self.frame = tk.Frame(self, background='#81F0F7', border=5)
        self.frame.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.8)

        self.countries = business
        self.country = ''
        self.num = ''
        countryNums = [str(i) + " " + str(self.countries[i]) for i in
                       range(len(self.countries))]
        self.OPTIONS = countryNums
        self.variable = StringVar(master)
        self.variable.set(self.OPTIONS[0])
        self.w = OptionMenu(self.frame, self.variable, *self.OPTIONS)
        self.w.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.2)
        self.w.config(width=100, bg="WHITE")

        self.disconnectButton = tk.Button(self.frame, text='Disconnect', command=self.disconnect, font=("Palatino Linotype", 15, 'bold'))
        self.disconnectButton.pack(side='bottom', fill='both')

        self.plotButton = tk.Button(self.frame, text='Okay',
                                    command=self.setNum,
                                    font=("Palatino Linotype", 15, 'bold'))
        self.plotButton.pack(side='bottom', fill='both')

    def send_ID(self):
        country = self.variable.get()
        #print(country)
        self.country = ''.join(char for char in country if not char.isdigit())
        print("Country selected", self.country)
        ID = ''.join(c for c in country if c.isdigit())
        #cJson = self.b.getJson(ID)
        #print(type(cJson), cJson)
        self.send_data(ID)

    def disconnect(self):
        if not self.conn:
            self.conn = False
            client_socket.close()
        else:
            print("you are already disconnected")

    def receive_json(self):
        print("Preparing to receive")
        #json_length = client_socket.recv(1024).decode()
        #print(json_length)
        #j_length = int(json_length)
        #print(j_length)
        js = b''
        tmp = client_socket.recv(10248)
        #print(len(tmp), tmp)
        #j_length = len(tmp)
        js += tmp
        print("Received Json: ", str(js))

    def send_data(self, countryID):
        print("CountryID: ", countryID)
        client_socket.send(countryID.encode())
        self.receive_json()

    def setNum(self):
        self.num = self.variable.get()
        self.num = ''.join(c for c in self.num if c.isdigit())
        self.destroy()

    def getNum(self):
        return self.num


class PlotWindow(tk.Toplevel):
    '''
    this class plots the price trend or bar chart depending on the user choice
    '''

    def __init__(self, master, fct, *args):
        global conn
        self.master = master
        super().__init__(master)
        fig = plt.figure(figsize=(8, 7))
        fct(*args)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()


class App(tk.Tk):
    def __init__(self):
        global conn
        self.business = Business()
        super().__init__()

        self.clientID = 0

        self.canvas = tk.Canvas(self, height=700, width=700)
        self.canvas.pack()
        frame = tk.Frame(self.canvas, background='#2C5881', border=5)
        frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        b = tk.Button(frame, text="Country Menu", command=self.displayDialog)
        b.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.2)
        b.config(font=("Palatino Linotype", 20, 'bold'))

        client_socket.connect((host, port))
        conn = True
        self.ID = ''
        print("Connected to: ", host, " ", port)
        print("INSTRUCTIONS:\nSelect a country ")
        print("Countries: ", self.business.individual_country_list)


    def displayDialog(self):
        while conn is True:
            dWin = DialogWindow(self, self.business.individual_country_list, self.business)
            self.wait_window(dWin)
            dWin.send_ID()
            choice = dWin.getNum()
            if len(choice) == 0:
                print("\nWindows have all been closed. Goodbye!")
                raise SystemExit
            PlotWindow(self, self.business.getJson, choice)


mainWin = App()
mainWin.mainloop()

