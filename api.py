import routeros_api
import getpass
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
    file = pd.read_excel(file)
    ip = ip2str(file['DIRECCION IP'])
    print(len(ip))
    list_address = app.get_resource('/ip/arp')  # Obtiene Datos de la tabla ARP
    for dire in ip:
        _id = list_address.get(address=dire)[0]['id']
        print('ip address: ', list_address.get(address=dire)[0]['address'], 'id: ', _id)
        list_address.set(id=_id, address=dire, disabled='true')
    return


def activarfile(file, app):
    file = pd.read_excel(file)
    ip = ip2str(file['DIRECCION IP'])
    print(len(ip))
    list_address = app.get_resource('/ip/arp')  # Obtiene Datos de la tabla ARP
    for dire in ip:
        _id = list_address.get(address=dire)[0]['id']
        print('ip address:', dire, ' id:', _id)
        list_address.set(id=_id, address=dire, disabled='false')
    return


def activar(app):
    list_address = app.get_resource('/ip/arp')  # Obtiene Datos de la tabla ARP
    while True:
        address = input("Dirección IP Usuario: ")
        if address:
            _id = list_address.get(address=address)[0]['id']
            print(list_address.get(address=address))
            # list_address.set(id=_id, address=address, disabled='true')
        else:
            break
    return


def desactivar(app):
    list_address = app.get_resource('/ip/arp')  # Obtiene Datos de la tabla ARP
    while True:
        address = input("Dirección IP Usuario: ")
        if address:
            _id = list_address.get(address=address)[0]['id']
            print(list_address.get(address=address))
            # list_address.set(id=_id, address=address, disabled='true')
        else:
            break
    return


def ip2str(x_val):
    ipstr = []
    for i in x_val:
        aux = str(i)
        ipstr.append(aux)
    return ipstr
