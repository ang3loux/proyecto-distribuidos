# Python 2.7
import socket
import select
import sys
import os
from thread import *
from time import sleep

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 5:
    print "Uso correcto: script, direccion IP, puerto, numero de clientes e iteraciones"
    exit()

ipAddress = str(sys.argv[1])
port = int(sys.argv[2])
numberClients = int(sys.argv[3])
iterations = int(sys.argv[4])

server.bind((ipAddress, port))
server.listen(numberClients)

connections = []


def connectionThread(connection, address):
    connection.send("Conectado al servidor, esperando a los demas clientes...")

    while True:
        try:
            message = connection.recv(2048)
            if message:
                print "<" + address[0] + "> " + message

            else:
                removeConnection(connection)

        except:
            continue


def broadcastMessage(message):
    for connection in connections:
        try:
            connection.send(message)
        except:
            removeConnection(connection)


def removeConnection(connection):
    if connection in connections:
        connection.close()
        connections.remove(connection)
        print "Cliente desconectado. Conexion cerrada."


def codeMessage(message):
    print "Code message"


def decodeMessagge(message):
    print "Decode message"


os.system('clear')
print "Iniciando servidor"
print "IP: " + ipAddress
print "Puerto: " + str(port)
print "Nro de clientes: " + str(numberClients)
print "Iteraciones: " + str(iterations)
print "\nEsperando a clientes..."

while numberClients > 0:
    numberClients -= 1
    connection, address = server.accept()
    connections.append(connection)
    print "<" + address[0] + "> conectado"
    start_new_thread(connectionThread, (connection, address))

sleep(1)
print "\nClientes conectados, inicio de proceso..."
broadcastMessage("Clientes conectados, inicio de proceso...")
for connection in connections:
    try:
        connection.send("message")
    except:
        removeConnection(connection)

dato = raw_input("\nPresione enter para terminar.")
print "\nCerrando conexiones..."
for connection in connections:
    connection.close()
print "\nCerrando servidor."
server.close()
