import routeros_api
import pandas as pd


def connect(host, username, password):
    connection = routeros_api.RouterOsApiPool(host, username=username, password=password, port=8740, plaintext_login=True)
    api = connection.get_api()
    print('Conexión Establecida')
    return api, connection


def disconnect(connection):
    print("Desconexión Exitosa")
    return connection.disconnect()


def obtenerqueue(api):
    list_queues = api.get_resource('/queue/simple')
    lista = list_queues.get()
    queue = []
    for i in lista:
        queue.append(i)
    return lista


def obtenerarp(api, interface=''):
    list_queues = api.get_resource('/ip/arp')
    if interface == '':
        lista = list_queues.get()
    else:
        lista = list_queues.get(interface=interface)
    arp = []
    for i in lista:
        arp.append(i)
    return arp


def desactivarfile(file, app):
    print(file)
    file = pd.read_excel(file)
    ip = file['DIRECCION IP']
    print(len(ip))
    for dire in ip:
        print(dire)
        desactivar(app, dire)
    return


def activarfile(file, app):
    print(file)
    file = pd.read_excel(file)
    ip = file['DIRECCION IP']
    print(len(ip))
    for dire in ip:
        print(dire)
        activar(app, dire)
    return


def activar(app, address):
    list_address = app.get_resource('/ip/arp')  # Obtiene Datos de la tabla ARP
    _id = list_address.get(address=address)[0]['id']
    list_address.set(id=_id, address=address, disabled='false')
    enable = list_address.get(address=address)[0]['disabled']
    return _id, enable


def desactivar(app, address):
    list_address = app.get_resource('/ip/arp')  # Obtiene Datos de la tabla ARP
    _id = list_address.get(address=address)[0]['id']
    list_address.set(id=_id, address=address, disabled='true')
    enable = list_address.get(address=address)[0]['disabled']
    return _id, enable