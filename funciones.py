from tkinter import filedialog
from tkinter import messagebox
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


def filewindow():
    ventana = Tk()
    ventana.withdraw()
    ventana.filename = filedialog.askopenfilename(initialdir="/Documents", title="Select file",
                                                  filetypes=(("excel files", "*.xlsx"), ("all files", "*.*")))
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
        mainwindow(app, conect, host, username)


def activatewindow(app, opcode, dirip=""):
    if opcode == 1:
        print(opcode)
        ip = dirip.get()
        if ip:
            activar(app, ip)
            messagebox.showinfo(title="Activar usuario", message=ip+" Activada")
        else:
            messagebox.showinfo(title="Error", message='¡¡Ingrese los datos!!')
    elif opcode == 2:
        print(opcode)
        ips = filewindow()
        print(type(ips))
        activarfile(ips, app)
        print("Activar Usuarios " + ips)


def deactivatewindow(app, opcode, dirip=""):
    if opcode == 1:
        print(opcode)
        ip = dirip.get()
        if ip:
            desactivar(app, ip)
            messagebox.showerror(title="Desactivar usuario", message=ip + " Desactivada")
        else:
            messagebox.showerror(title="Error", message='¡¡Ingrese los datos!!')
    elif opcode == 2:
        print(opcode)
        ips = filewindow()
        print(type(ips))
        desactivarfile(ips, app)
        print("Activar Usuarios " + ips)


def mainwindow(app, conect, host, user):
    mainmenu = Tk()
    mainmenu.geometry("500x250")
    mainmenu.title("API ISANET:"+user+"@"+host)
    mainmenu.iconbitmap("media/MikroTik.ico")
    mainmenu.resizable(False, False)

    optionframe = Frame(mainmenu)
    optionframe.pack()

    mainframe = Frame(mainmenu)
    mainframe.pack()

    logoutframe = Frame(mainmenu)
    logoutframe.pack()

    option = IntVar()
    option.set(1)
    selec(option, mainframe, app)

    Radiobutton(mainframe, text="Activar usuarios", variable=option, value=1, command=lambda: selec(option, mainframe, app)).grid(row=0, column=0, padx=5, pady=5)
    Radiobutton(mainframe, text="Desactivar usuarios", variable=option, value=2, command=lambda: selec(option, mainframe, app)).grid(row=0, column=1, padx=5, pady=5)
    Button(logoutframe, text="Cerrar Sesión", command=lambda: disconect(conect, mainmenu)).grid(row=0, padx=5, pady=5)


def selec(option, frame, app):
    dirip = StringVar()
    Label(frame, text="Dirección IP: ").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    dirip = Entry(frame, textvariable=dirip).grid(row=1, column=1, padx=5, pady=5)
    if option.get() == 1:
        Button(frame, text="Activar usuario", width="15", command=lambda: activatewindow(app, 1, dirip)).grid(row=2, column=0, padx=5, pady=5)
        Button(frame, text="Activar usuarios desde archivo", width="25", command=lambda: activatewindow(app, 2)).grid(row=2, column=1, padx=5, pady=5)
    else:
        Button(frame, text="Desactivar usuario", width="15", command=lambda: deactivatewindow(app, 1, dirip)).grid(row=2, column=0, padx=5, pady=5)
        Button(frame, text="Desactivar usuarios desde archivo", width="25", command=lambda: deactivatewindow(app, 2)).grid(row=2, column=1, padx=5, pady=5)
