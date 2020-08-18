from funciones import *
from tkinter import *

raiz = Tk()
raiz.title("API MikroTik")
raiz.iconbitmap("mikrotik.ico")
raiz.resizable(False, False)
frameimagen = Frame(raiz)
frameimagen.grid(row=0)

host = StringVar()
username = StringVar()
password = StringVar()

imagen = PhotoImage(file="logoisanet.gif")
Label(frameimagen, image=imagen).pack()

miframe = Frame(raiz, width=650, height=350)
miframe.grid(row=1, pady=5)

Label(miframe, text="Host: ").grid(column=0, row=1, padx=5, pady=5, sticky='e')

host = Entry(miframe, textvariable=host)
host.grid(column=1, row=1, padx=5, pady=5)

lusername = Label(miframe, text="Username: ")
lusername.grid(column=0, row=2, padx=5, pady=5, sticky='e')
username = Entry(miframe, textvariable=username)
username.grid(column=1, row=2, padx=5, pady=5)

lpassword = Label(miframe, text="Password: ")
lpassword.grid(column=0, row=3, padx=5, pady=5, sticky='e')
password = Entry(miframe, textvariable=password, show='x')
password.grid(column=1, row=3, padx=5, pady=5)

botonconectar = Button(miframe, text="Conectar", command=lambda: getdata(host, username, password))
botonconectar.grid(column=0, row=4, padx=5, pady=5)
botonsalir = Button(miframe, text="Salir", command=salir)
botonsalir.grid(column=1, row=4, padx=5, pady=5)


raiz.mainloop()
