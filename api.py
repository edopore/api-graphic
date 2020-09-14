import routeros_api
import pandas as pd


def connect(host, username, password):
    connection = routeros_api.RouterOsApiPool(host,
                                              username=username,
                                              password=password,
                                              port=8740,
                                              plaintext_login=True)
    api = connection.get_api()
    print('Conexión Establecida')
    return api, connection


def disconnect(connection):
    print("Desconexión Exitosa")
    return connection.disconnect()


def obteneripinfo(app,ip):
    lista = app.get_resource('/ip/arp')
    user = lista.get(address=ip)
    return user, lista


def desactivarfile(file, app):
    file = pd.read_excel(file)
    ip = file['DIRECCION IP']
    print(len(ip))
    for dire in ip:
        print(dire)
        _id, enable = desactivar(app, dire)
        return _id, enable


def activarfile(file, app):
    file = pd.read_excel(file)
    ip = file['DIRECCION IP']
    print(len(ip))
    for dire in ip:
        print(dire)
        _id, enable = activar(app, dire)
    return _id, enable


def activar(app, address):
    ip, lista = obteneripinfo(app, address)
    if ip:
        _id = ip[0]['id']
        lista.set(id=_id, address=address, disabled='false')
        enable = lista.get(address=address)[0]['disabled']
    else:
        _id = ''
        enable = ''
    return _id, enable


def desactivar(app, address):
    ip, lista = obteneripinfo(app, address)
    if ip:
        _id = ip[0]['id']
        lista.set(id=_id, address=address, disabled='true')
        enable = lista.get(address=address)[0]['disabled']
    else:
        _id = ''
        enable = ''
    return _id, enable
