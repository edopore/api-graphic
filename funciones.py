from tkinter import filedialog
from tkinter import *
from api import *

def archivo():
    ventana = Tk()
    ventana.filename = filedialog.askopenfilename(initialdir="/Documents",
                                                  title="Select file",
                                                  filetypes=(("excel files", "*.xlsx"),
                                                             ("all files", "*.*")))
    print(ventana.filename)
    return ventana.filename


def saludo():
    print("Hola, ¿Cómo vas veve?")


def getdata(host, username, password):
    host = host.get()
    username = username.get()
    password = password.get()
    if not (host and username and password):
        print('¡¡Ingrese los datos!!')
    else:
        connect(host, username, password)

def salir():
    print('cosa1')
