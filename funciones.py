from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from api import *


def start():
    raiz = Tk()
    raiz.title("API ISANET")
    raiz.iconbitmap("media/MikroTik.ico")
    raiz.resizable(False, False)

    frameroot = Frame(raiz)
    frameroot.pack()

    frameimagen = Frame(frameroot)
    frameimagen.pack()

    host = StringVar()
    username = StringVar()
    password = StringVar()

    image = PhotoImage(file="media/logoIsanet.gif")
    Label(frameimagen, image=image).pack()

    miframe = Frame(frameroot, width=650, height=350)
    miframe.pack()

    Label(miframe, text="Host: ").grid(column=0, row=1, padx=5, pady=5, sticky='e')

    host = Entry(miframe, textvariable=host)
    host.focus()
    host.grid(column=1, row=1, padx=5, pady=5)

    lusername = Label(miframe, text="Username: ")
    lusername.grid(column=0, row=2, padx=5, pady=5, sticky='e')
    username = Entry(miframe, textvariable=username)
    username.grid(column=1, row=2, padx=5, pady=5)

    lpassword = Label(miframe, text="Password: ")
    lpassword.grid(column=0, row=3, padx=5, pady=5, sticky='e')
    password = Entry(miframe, textvariable=password, show='x')
    password.grid(column=1, row=3, padx=5, pady=5)

    bconectar = Button(miframe, text="Conectar", command=lambda: getdata(host, username, password, raiz))
    bconectar.grid(column=0, row=4, padx=5, pady=5)
    bsalir = Button(miframe, text="Salir", command=lambda: out(raiz))
    bsalir.grid(column=1, row=4, padx=5, pady=5)

    raiz.protocol('WM_DELETE_WINDOW', lambda: out(raiz))
    raiz.bind('<Escape>', lambda e: out(raiz))
    raiz.bind('<Return>', lambda e: getdata(host, username, password, raiz))
    raiz.mainloop()


def file():
    ventana = Tk()
    ventana.withdraw()
    ventana.filename = filedialog.askopenfilename(initialdir="/Documents", title="Select file",
                                                  filetypes=(("excel files", "*.xlsx"), ("all files", "*.*")))
    print(ventana.filename)
    return ventana.filename


def disconect(conect, window):
    disconnect(conect)
    window.destroy()
    start()


def out(window):
    cerrar = messagebox.askyesno(title="Salir", message="¿Está seguro que desea salir?")
    if cerrar:
        window.destroy()


def getdata(host, username, password, window):
    host = host.get()
    username = username.get()
    password = password.get()
    if not (host and username and password):
        messagebox.showerror(title="Error", message='¡¡Ingrese los datos!!')
    else:
        app, conect = connect(host, username, password)
        window.destroy()
        mainwindow(app, conect)


def activatewindow(app, dirip=""):
    if dirip:
        ip = dirip.get()
        activar(app, ip)
        print("Activar usuario " + ip)
    else:
        ips = file()
        print("Activar Usuarios " + ips)


def deactivatewindow(app, dirip=""):
    if dirip:
        ip = dirip.get()
        print("Desactivar usuario " + ip)
    else:
        ips = file()
        print("Desactivar Usuarios " + ips)
    return ips


def mainwindow(app, conect):
    mainmenu = Tk()
    mainframe = Frame(mainmenu)
    mainframe.pack()

    option = IntVar()
    option.set(1)
    selec(option, mainframe, app)

    Radiobutton(mainframe, text="Activar usuarios", variable=option, value=1, command=lambda: selec(option, mainframe, app)).grid(row=0, column=0, padx=5, pady=5)
    Radiobutton(mainframe, text="Desactivar usuarios", variable=option, value=2, command=lambda: selec(option, mainframe, app)).grid(row=0, column=1, padx=5, pady=5)
    Button(mainframe, text="Cerrar Sesión", command=lambda: disconect(conect, mainmenu)).grid(padx=5, pady=5)


def selec(option, frame, app):
    dirip = StringVar()
    Label(frame, text="Dirección IP: ").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    Entry(frame, textvariable=dirip).grid(row=1, column=1, padx=5, pady=5)
    if option.get() == 1:
        Button(frame, text="Activar usuario", width="15", command=lambda: activatewindow(app, dirip)).grid(row=2, column=0, padx=5, pady=5)
        Button(frame, text="Activar usuarios desde archivo", command=lambda: activatewindow(app)).grid(row=2, column=1, padx=5, pady=5)
    else:
        Button(frame, text="Desactivar usuario", width="15", command=lambda: deactivatewindow(app, dirip)).grid(row=2, column=0, padx=5, pady=5)
        Button(frame, text="Activar usuarios desde archivo", command=lambda: deactivatewindow(app)).grid(row=2, column=1, padx=5, pady=5)
