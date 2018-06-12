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

ipAddress = str(sys.argv[1])
port = int(sys.argv[2])
number_clients = 3
resource = ['', '', '']

server.bind((ipAddress, port))
server.listen(number_clients)

connections = []


def desitions(msg, connection, address):
    if msg['typemsg'] == 0:
        if resource[msg['msg']] == '':
            resource[msg['msg']] = msg['msg2']
            json_msg = {
                'typemsg': 1,
                'msg': 1,
                'msg2': msg['msg']
            }
            print 'Recurso otorgado'
            connection.send(json.dumps(json_msg))
        else:
            json_msg = {
                'typemsg': 1,
                'msg': 0,
            }
            print 'Recurso no otorgado'
            connection.send(json.dumps(json_msg))


def connection_thread(connection, address, index):
    if index == 2:
        name_client = 'A'
    elif index == 1:
        name_client = 'B'
    else:
        name_client = 'C'

    json_start = {
        'typemsg': 0,
        'msg': name_client,
    }

    print 'Asignado a', address[0], 'el nombre', name_client
    connection.send(json.dumps(json_start))

    while True:
        try:
            json_msg = connection.recv(2048)
            if json_msg:
                # print "<" + address[0] + "> " + json_msg
                # connection.send("HOLA")
                desitions(json.loads(json_msg), connection, address)

            else:
                remove_connection(connection)

        except:
            continue


def broadcast_message(message):
    for connection in connections:
        try:
            connection.send(message)
        except:
            remove_connection(connection)


def remove_connection(connection):
    if connection in connections:
        connection.close()
        connections.remove(connection)
        print "Cliente desconectado. Conexion cerrada."


os.system('clear')
print "Iniciando servidor"
print "IP: " + ipAddress
print "Puerto: " + str(port)
print "Nro de clientes: " + str(number_clients)
print "\nEsperando a clientes..."

while number_clients > 0:
    number_clients -= 1
    connection, address = server.accept()
    connections.append(connection)
    print "<" + address[0] + "> conectado"
    start_new_thread(connection_thread, (connection, address, number_clients))

# sleep(1)
# print "\nClientes conectados, inicio de proceso..."
# broadcast_message("Clientes conectados, inicio de proceso...\n")

dato = raw_input("\nPresione enter para terminar.\n")
print "\nCerrando conexiones..."
for connection in connections:
    connection.close()
print "\nCerrando servidor."
server.close()
