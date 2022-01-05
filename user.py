import socket
#from socket import *
from business import Business
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
import re
from gui import PlotWindow
import json
import pickle


client_socket = socket.socket()
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
port = 2048


class App(Frame):
    def __init__(self, master=None):
        self.b = Business()
        Frame.__init__(self, master)

        print("INSTRUCTIONS:\n1. Wait for server to choose client to connect to (will be prompted of connection)\n"
              "2. Select a country "
              )
        self.grid()
        #self.master.title("Client")
        self.conn = False
        self.clientID = 0

        for r in range(4):
            self.master.rowconfigure(r, weight=1)
        for c in range(2):
            self.master.columnconfigure(c)

        topFrame = tk.Frame(master)
        topFrame.grid(row=0, column=0, rowspan=3)
        BottomFrame = tk.Frame(master, bg="blue")
        BottomFrame.grid(row=4, column=0)
        SideFrame = tk.Frame(master, bg="green")
        SideFrame.grid(column=1, row=0, rowspan=4)

        countryNums = [str(i) + " " + str(self.b.individual_country_list[i]) for i in range(len(self.b.individual_country_list))]
        self.OPTIONS = countryNums
        self.variable = StringVar(master)
        self.variable.set(self.OPTIONS[0])
        #print("OPTIONS", self.OPTIONS)
        self.w = OptionMenu(topFrame, self.variable, *self.OPTIONS)
        self.w.config(width=100, bg="BLACK")
        self.w.grid(column=3, row=3)

        b2 = Button(SideFrame, text="Disconnect", command=self.disconnect)
        b2.grid(row=0, column=0, padx=5, pady=5)
        b3 = Button(SideFrame, text="Send", command=self.send_ID)
        b3.grid(row=2, column=0, padx=5, pady=5)

        client_socket.connect((host, port))
        self.conn = True
        self.ID = ''
        print("Connected to: ", host, " ", port)
        connected = "Client: " + str(client_socket.getsockname())
        client_socket.send(connected.encode())
        #self.receive_msg()

    def send_ID(self):
        country = self.variable.get()
        self.ID = ''.join(c for c in country if c.isdigit())
        cJson = self.b.getJson(int(self.ID))
        #print(type(cJson), cJson)
        print(self.ID)
        self.send_data(int(self.ID))
        PlotWindow(self.master, self.b.getJson, int(self.ID))

    def disconnect(self):
        if self.conn:
            client_socket.close()
            self.conn = False
        else:
            print("you are already disconnected")

    def receive_json(self):
        print("\nPreparing to receive", client_socket.recv(1024))
        decoded_data = client_socket.recv(1024)
        print("sup", pickle.loads(decoded_data))
        decoded_data = pickle.loads(decoded_data)
        print("hello", decoded_data)
        cont = "Do you want to continue? (y/n)"
        c = input(cont)
        if c.lower == 'y':
            pass
        elif c.lower == 'n':
            raise SystemExit

    def send_data(self, message):
        try:
            client_socket.send(str(message).encode('utf-8'))
            self.receive_json()
        except:
            print("message didn't send")
            pass

    def clear_plot(self):
        plt.close("Figure 1")


root = Tk()
app = App(root)
app.mainloop()

