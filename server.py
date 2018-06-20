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
client_names = ['C', 'B', 'A']

server.bind((ip_address, port))
server.listen(number_clients)

connections = []

def reply_msg(client_msg, connection, address):
    global resources
    
    sleep(2)
    
    if client_msg['msg_type'] == 0:
        flag = 0

        for resource in resources:
            if resource == '':
                flag += 1

        if flag == 0 and resources[0] != resources[1]:
            for resource in resources:
                if resource == client_msg['client_name']:
                    resource = ''

            json_msg = {
                'msg_type': 1,
                'msg_subtype': 2
            }
            print 'Recurso ' + str(client_msg['resource_index']) + ' NO otorgado a ' + client_msg['client_name']
            print resources
            connection.send(json.dumps(json_msg))

        elif flag == 0 and resources[0] == resources[1]:
            json_msg = {
                'msg_type': 1,
                'msg_subtype': 2
            }
            print 'Recurso ' + str(client_msg['resource_index']) + ' NO otorgado a ' + client_msg['client_name']
            print resources
            connection.send(json.dumps(json_msg))

        elif resources[client_msg['resource_index']] == '':
            resources[client_msg['resource_index']] = str(client_msg['client_name'])
            json_msg = {
                'msg_type': 1,
                'msg_subtype': 1,
                'resource_index': client_msg['resource_index']
            }
            print 'Recurso ' + str(client_msg['resource_index']) + ' otorgado a ' + client_msg['client_name']
            print resources
            connection.send(json.dumps(json_msg))

        else:
            json_msg = {
                'msg_type': 1,
                'msg_subtype': 0,
            }
            print 'Recurso ' + str(client_msg['resource_index']) + ' NO otorgado a ' + client_msg['client_name']
            print resources
            connection.send(json.dumps(json_msg))
    
    elif client_msg['msg_type'] == 1:
        resources[client_msg['resource_index']] = str(client_msg['client_name'])
        json_msg = {
            'msg_type': 2,
            'resource_index': client_msg['resource_index']
        }
        print 'Recurso ' + str(client_msg['resource_index']) + ' otorgado a ' + client_msg['client_name']
        print 'Todos los recursos ocupados por ' + client_msg['client_name']
        print resources
        connection.send(json.dumps(json_msg))

    elif client_msg['msg_type'] == 2:
        resources = ['', '', '']
        json_msg = {
            'msg_type': 3,
        }
        print 'Recursos devueltos por ' + client_msg['client_name']
        print resources
        connection.send(json.dumps(json_msg))


def connection_thread(connection, address, index):
    client_name = client_names[index]
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
