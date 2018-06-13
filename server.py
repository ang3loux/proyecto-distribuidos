# Python 2.7
import socket
import select
import sys
import os
from thread import *
from time import sleep
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print "Uso correcto: script, direccion IP y puerto"
    exit()

ip_address = str(sys.argv[1])
port = int(sys.argv[2])
number_clients = 3
resources = ['', '', '']
client_names = {
    'by_name': {
        'A': 2,
        'B': 1,
        'C': 0,
    },
    'by_index': ['C', 'B', 'A']
}

server.bind((ip_address, port))
server.listen(number_clients)

connections = []


def reply_msg(client_msg, connection, address):
    global resources

    if client_msg['msg_type'] == 0:
        if resources[client_msg['resource_index']] == '':
            resources[client_msg['resource_index']] = client_msg['client_name']
            json_msg = {
                'msg_type': 1,
                'msg_subtype': 1,
                'resource_index': client_msg['resource_index']
            }
            print 'Recurso ' + str(client_msg['resource_index']) + ' otorgado a ' + client_msg['client_name']
            connection.send(json.dumps(json_msg))

        else:
            json_msg = {
                'msg_type': 1,
                'msg_subtype': 0,
            }
            print 'Recurso ' + str(client_msg['resource_index']) + ' NO otorgado a ' + client_msg['client_name']
            connection.send(json.dumps(json_msg))
    
    elif client_msg['msg_type'] == 1:
        queued_client = resources[client_msg['resource_index']]
        resources[client_msg['resource_index']] = client_msg['client_name']
        json_msg = {
            'msg_type': 2,
            'queued_client': queued_client,
            'queued_resource': client_msg['resource_index']
        }
        print 'Recurso ' + str(client_msg['resource_index']) + ' otorgado a ' + client_msg['client_name']

        if queued_client:
            print 'Cliente ' + queued_client + ' puesto en espera'
        connection.send(json.dumps(json_msg))

    elif client_msg['msg_type'] == 2:
        resources = ['', '', '']
        json_msg = {
            'msg_type': 3,
        }
        print 'Recursos devueltos'
        broadcast_message(json.dumps(json_msg))
        # DEVOLVER RECURSO AL CLIENTE QUE SE LE QUITO


def connection_thread(connection, address, index):
    client_name = client_names['by_index'][index]
    json_msg = {
        'msg_type': 0,
        'client_name': client_name,
    }

    print 'Asignado a ' + address[0] + ' el nombre ' + client_name
    connection.send(json.dumps(json_msg))

    while True:
        print '--------------------------------------------------'

        try:
            json_msg = connection.recv(2048)
            if json_msg:
                reply_msg(json.loads(json_msg), connection, address)

            else:
                remove_connection(connection)

        except:
            continue


def broadcast_message(msg):
    for connection in connections:
        try:
            connection.send(msg)
        except:
            remove_connection(connection)


def remove_connection(connection):
    if connection in connections:
        connection.close()
        connections.remove(connection)
        print "Cliente desconectado. Conexion cerrada."


os.system('clear')

print "Iniciando servidor"
print "IP: " + ip_address
print "Puerto: " + str(port)
print "Nro de clientes: " + str(number_clients)
print "\nEsperando a clientes..."

while number_clients > 0:
    number_clients -= 1
    connection, address = server.accept()
    connections.append(connection)
    print "<" + address[0] + "> conectado"
    start_new_thread(connection_thread, (connection, address, number_clients))

dato = raw_input("\nPresione enter para terminar.\n")
print "\nCerrando conexiones..."
for connection in connections:
    connection.close()
print "\nCerrando servidor."
server.close()
