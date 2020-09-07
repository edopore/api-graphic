from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from api import *


def start():
    raiz = Tk()
    raiz.title("API ISANET")
    raiz.iconbitmap("media/LogoIsanet.ico")
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


def mainwindow(app, conect, host, user):
    mainmenu = Tk()
    mainmenu.geometry("500x250")
    mainmenu.title("API ISANET: " + user + "@" + host)
    mainmenu.iconbitmap("media/LogoIsanet.ico")
    mainmenu.resizable(False, False)
    mainmenu.protocol('WM_DELETE_WINDOW', lambda: disconect(conect, mainmenu))

    optionframe = Frame(mainmenu)
    optionframe.pack()

    mainframe = Frame(mainmenu)
    mainframe.pack()

    logoutframe = Frame(mainmenu)
    logoutframe.pack()

    option = IntVar()
    option.set(1)
    selec(option, mainframe, app)

    Radiobutton(mainframe, text="Activar usuarios", variable=option,
                value=1, command=lambda: selec(option, mainframe, app)).grid(row=0, column=0, padx=5, pady=5)
    Radiobutton(mainframe, text="Desactivar usuarios", variable=option,
                value=2, command=lambda: selec(option, mainframe, app)).grid(row=0, column=1, padx=5, pady=5)
    Button(logoutframe, text="Cerrar Sesión", command=lambda: disconect(conect, mainmenu)).grid(row=0, padx=5, pady=5)


def treestatus(opcode, app):
    ips = filewindow()

    window = Tk()
    window.iconbitmap("media/LogoIsanet.ico")
    Label(window, text='Estado Usuarios').pack(fill=X)
    tree = ttk.Treeview(window, selectmode='browse')
    vsb = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')

    tree["columns"] = ("one", "two", "three")
    tree.column("#0", width=50, minwidth=50)
    tree.column("one", width=80, minwidth=80)
    tree.column("two", width=80, minwidth=80)
    tree.column("three", width=80, minwidth=80)

    tree.heading("#0", text="#")
    tree.heading("one", text="ID")
    tree.heading("two", text="Dirección IP")
    tree.heading("three", text="Disabled")

    tree.pack(side=TOP, fill=X)
    #Button(window, text="Cerrar", command=window.destroy).pack()

    if ips:
        file = pd.read_excel(ips)
        ip = file['DIRECCION IP']
        print(len(ip))
        i = 0
        if opcode == 1:
            window.title("API ISANET: Activar")
            for dire in ip:
                _id, en = activar(app, dire)
                tree.insert("", i, text=str(i+1), values=(_id, dire, en))
                i += 1
        elif opcode == 2:
            window.title("API ISANET: Desactivar")
            for dire in ip:
                _id, en = desactivar(app, dire)
                tree.insert("", i, text=str(i+1), values=(_id, dire, en))
                i += 1
    else:
        window.destroy()


def filewindow():
    window = Tk()
    window.withdraw()
    window.filename = filedialog.askopenfilename(initialdir="/Documents", title="Select file",
                                                 filetypes=(("excel files", "*.xlsx"), ("all files", "*.*")))
    window.destroy()
    return window.filename


def disconect(conect, window):
    if messagebox.askyesno(title="Cerrar Sesión", message="¿Está seguro que desea cerrar sesión?"):
        disconnect(conect)
        window.destroy()
        start()


def out(window):
    if messagebox.askyesno(title="Salir", message="¿Está seguro que desea salir?"):
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


def activate(app, opcode, dirip=""):
    if opcode == 1:
        if dirip:
            activar(app, dirip)
            messagebox.showinfo(title="Activar usuario", message=dirip + " Activada")
        else:
            messagebox.showerror(title="Error", message='¡¡Ingrese los datos!!')
    elif opcode == 2:
        treestatus(opcode-1, app)


def deactivate(app, opcode, dirip=""):
    if opcode == 1:
        if dirip:
            desactivar(app, dirip)
            messagebox.showinfo(title="Desactivar usuario", message=dirip + " Desactivada")
        else:
            messagebox.showerror(title="Error", message='¡¡Ingrese los datos!!')
    elif opcode == 2:
        treestatus(opcode, app)


def selec(option, frame, app):
    dirip = StringVar()
    Label(frame, text="Dirección IP: ").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    dirip = Entry(frame, textvariable=dirip)
    dirip.focus()
    dirip.grid(row=1, column=1, padx=5, pady=5)

    if option.get() == 1:
        Button(frame, text="Activar usuario", width="15",
               command=lambda: activate(app, 1, dirip.get())).grid(row=2, column=0, padx=5, pady=5)
        Button(frame, text="Activar usuarios desde archivo", width="25",
               command=lambda: activate(app, 2)).grid(row=2, column=1, padx=5, pady=5)
    else:
        Button(frame, text="Desactivar usuario", width="15",
               command=lambda: deactivate(app, 1, dirip.get())).grid(row=2, column=0, padx=5, pady=5)
        Button(frame, text="Desactivar usuarios desde archivo", width="25",
               command=lambda: deactivate(app, 2)).grid(row=2, column=1, padx=5, pady=5)
