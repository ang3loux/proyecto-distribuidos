# Python 2.7
import socket
import select
import sys
import os
import random
from time import sleep
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print "Uso correcto: script, direccion IP y puerto"
    exit()

ipAddress = str(sys.argv[1])
port = int(sys.argv[2])

server.connect((ipAddress, port))

# def sleepThread():
#     sleepTime = random.randint(1, 10)
#     print sleepTime
#     sleep(sleepTime)

os.system('clear')
while True:
    jsonTest = {
        'first_name': 'Guido',
        'second_name': 'Rossum',
        'titles': ['BDFL', 'Developer'],
    }

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]

    read_sockets, write_socket, error_socket = select.select(
        sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            test = json.loads(message)
            print test['first_name']
        else:
            message = sys.stdin.readline()
            server.send(json.dumps(jsonTest))
            sys.stdout.write("JSON enviado\n")
            # sys.stdout.write(message)
            sys.stdout.flush()

server.close()
