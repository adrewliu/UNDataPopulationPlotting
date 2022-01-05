import socket
import threading
import time
from queue import Queue
from business import Business
import json
import tkinter as tk
import matplotlib.pyplot as plt

thread_count = 2
connection_jobs = [1, 2]
queue = Queue()
all_connections = []
all_address = []
b = Business()


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        port = 2048
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)

            all_connections.append(conn)
            all_address.append(address)
            print("Connection has been established :" + address[0] + " " + str(port))
            print("COMMANDS:\n" + "show all ---------------- display all countries and clients connected to server\n" + "choice ID# ------------- select the number in front of country\n"
                  + "client ID#--------------------- returns the json for the client that selected the country\n" + "quit ---------------------- exit current client when called in send target function\n" + "exit  ------------------------------- exits the program\n")

        except:
            print("Error accepting connections")



def start_shell():

    cmd = str(input('shell> '))
    if cmd.lower() == 'exit':
        print("ending program")
        raise SystemExit
    while cmd.lower != 'quit':
        if cmd.lower() == 'show all':
            showCountries()
            create_client_list()
            list_connections()
            cmd = str(input('shell> '))
        elif 'choice' in cmd.lower():
            ID = get_country(cmd)
            print(b.getJson, ID)
        elif 'client' in cmd.lower():
            conn = get_target(cmd)
            if conn is None:
                send_target_commands(conn)
        else:
            if cmd.lower() == 'exit':
                raise SystemExit
            send_target_commands(cmd)
            print("Command not recognized")
        receive_client_input(conn)


def showCountries():
    countries = []
    for i in range(len(b.individual_country_list)):
        id_country = str(i) + " " + str(b.individual_country_list[i])
        print(id_country)


def create_client_list():
    client_string = ""
    for c, conn in enumerate(all_connections):
        try:
            temp = str(c) + "   " + str(all_address[c][0]) + "   " + str(all_address[c][1]) + "\n"
            client_string = client_string + temp
        except:
            print("Clients could not be retrieved....")
    print("-------------Clients--------------\n" + client_string)


def list_connections():

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            data = conn.recv(1024)
            print(data)
        except:

            del all_connections[i]
            del all_address[i]
            continue

    start_shell()


def get_country(cmd):
    try:
        countryID = cmd.replace('choice ', '')
        countryID = int(countryID)
        print("You have selected", b.individual_country_list[countryID])
        print(b.getJson(countryID))
    except:
        print("invalid countryID")


def get_target(cmd):
    try:
        shellID = cmd.replace('client ', '')
        shellID = int(shellID)
        conn = all_connections[shellID]
        print("Now connected to: " + str(all_address[shellID]))
        #print(str(all_address[shellID][0]) + ">", end="")
        receive_client_input(conn)
        return conn

    except:
        print("Selection not valid")
        return None


def send_target_commands(conn):
    while True:
        try:
            print("Press 'Enter' key if not connected to client to retype shell command or 'quit' to exit current client")
            cmd = str(input('shell>>'))
            if cmd.lower() == 'quit':
                goodbye = "goodbye"
                print(goodbye)
                conn.send(goodbye.encode())
                start_shell()
            if len(str.encode(cmd)) > 0:
                conn.send(cmd.encode())
                client_response = str(conn.recv(1024), "utf-8")
                print(client_response, '\n', end="")
                if client_response == 'exit':
                    start_shell()
                else:
                    send_target_commands(conn)
            else:
                start_shell()
        except:
            print("Error sending commands")
            start_shell()
            break


def receive_client_input(conn):
    client_selection = conn.recv(1024)
    c_id = client_selection.decode()
    print("this is c id", c_id, int(c_id))
    country_json = b.getJson(int(client_selection))
    print(country_json)
    conn.send(country_json.encode())
    start_shell()


def create_threads():
    for _ in range(thread_count):
        t = threading.Thread(target=get_queue)
        t.daemon = True
        t.start()


def get_queue():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_shell()

        queue.task_done()


def create_queue():
    for x in connection_jobs:
        queue.put(x)

    queue.join()


create_threads()
create_queue()

