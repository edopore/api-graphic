from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from api import *

def inicio():
    raiz = Tk()
    raiz.title("API MikroTik")
    raiz.iconbitmap("media/MikroTik.ico")
    raiz.resizable(False, False)

    frameimagen = Frame(raiz)
    frameimagen.grid(row=0)

    host = StringVar()
    username = StringVar()
    password = StringVar()

    imagen = PhotoImage(file="media/logoIsanet.gif")
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

    botonconectar = Button(miframe, text="Conectar", command=lambda: getdata(host, username, password, raiz))
    botonconectar.grid(column=0, row=4, padx=5, pady=5)
    botonsalir = Button(miframe, text="Salir", command=lambda: salir(raiz))
    botonsalir.grid(column=1, row=4, padx=5, pady=5)

    raiz.mainloop()

def archivo():
    ventana = Tk()
    ventana.withdraw()
    ventana.filename = filedialog.askopenfilename(initialdir="/Documents", title="Select file", filetypes=(("excel files", "*.xlsx"), ("all files", "*.*")))
    print(ventana.filename)
    return ventana.filename

def disconect(conect,window):
    disconnect(conect)
    window.destroy()
    inicio()

def salir(window):
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
        MainWindow(app, conect)

def MainWindow(app, conect):
    MainMenu = Tk()
    MainMenu.geometry("500x500")
    blogout = Button(MainMenu,text="Cerrar Sesión",command=lambda: disconect(conect, MainMenu))
    blogout.grid()
