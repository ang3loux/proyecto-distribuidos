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

if len(sys.argv) != 5:
    print "Uso correcto: script, direccion IP y puerto"
    exit()

ipAddress = str(sys.argv[1])
port = int(sys.argv[2])
numberClients = 3

server.bind((ipAddress, port))
server.listen(numberClients)

connections = []

def connection_thread(connection, address):
    connection.send("Conectado al servidor, esperando a los demas clientes...")

    while True:
        try:
            message = connection.recv(2048)
            if message:
                # print "<" + address[0] + "> " + message
                # connection.send("HOLA")
                print message
                connection.send(message)

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


def code_message(message):
    print "Code message"


def decode_messagge(message):
    print "Decode message"

# def start_process():


os.system('clear')
print "Iniciando servidor"
print "IP: " + ipAddress
print "Puerto: " + str(port)
print "Nro de clientes: " + str(numberClients)
print "\nEsperando a clientes..."

while numberClients > 0:
    numberClients -= 1
    connection, address = server.accept()
    connections.append(connection)
    print "<" + address[0] + "> conectado"
    start_new_thread(connection_thread, (connection, address))

sleep(1)
print "\nClientes conectados, inicio de proceso..."
broadcast_message("Clientes conectados, inicio de proceso...\n")

dato = raw_input("\nPresione enter para terminar.\n")
print "\nCerrando conexiones..."
for connection in connections:
    connection.close()
print "\nCerrando servidor."
server.close()
