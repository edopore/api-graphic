from api import *
'''
print("Inicio")
app, conect = connect()

queue = obtenerqueue(app)
queue

arp = obtenerarp(app)
arp

disconnect(conect)

strin = ""
print(bool(strin))
if strin:
    print("entra")

'''
print("Inicio")
app, conect = connect()
desactivar(app)
disconnect(conect)

