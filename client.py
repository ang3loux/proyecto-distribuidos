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
resources = ['', '', '']
name = ''

server.connect((ipAddress, port))

def sleep_thread():
    sleep_time = random.randint(1, 5)
    print 'Me voy a dormir por ' + str(sleep_time) + ' seg(s)'
    sleep(sleep_time)


def send_msg(args):
    global name
    global resources
    flag = 0
    missing_resource = -1

    for idx, resource in enumerate(resources):
        if resource == '':
            flag += 1
            missing_resource = idx

    if flag >= 2:
        print 'Recursos faltantes: ' + str(flag)
        while True:
            index = random.randint(0, 2)
            if resources[index] == '':
                json_msg = {
                    'msg_type': 0,
                    'resource_index': index,
                    'client_name': name,
                }
                print 'Recurso pedido: ' + str(index)
                break

    elif flag == 1:
        json_msg = {
            'msg_type': 1,
            'resource_index': missing_resource,
            'client_name': name
        }
        print 'Unico recurso faltante'
        print 'Recurso pedido: ' + str(missing_resource)

    else:
        sleep_thread()
        json_msg = {
            'msg_type': 2,
            'queued_client': args['queued_client'],
            'queued_resource': args['queued_resource'],
            'client_name': name
        }
        print 'Liberando todos los recursos tomados'

    server.send(json.dumps(json_msg))


def receive_msg(server_msg):
    global name
    global resources
    args = {}

    if server_msg['msg_type'] == 0:
        name = server_msg['client_name']
        print 'Mi etiqueta es: ' + name

    elif server_msg['msg_type'] == 1:
        if server_msg['msg_subtype'] == 0:
			print 'Recurso ocupado'

        else:
            print 'Recurso agregado'
            resources[server_msg['resource_index']] = name
    
    elif server_msg['msg_type'] == 2:
        print 'Recurso agregado'
        resources[server_msg['queued_resource']] = name
        args['queued_client'] = server_msg['queued_client']
        args['queued_resource'] = server_msg['queued_resource']

    elif server_msg['msg_type'] == 3:
        resources = ['', '', '']
        print 'Recursos liberados'

    print '--------------------------------------------------'
    
    sleep_thread() 
    send_msg(args)


os.system('clear')

while True:
    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]

    read_sockets, write_socket, error_socket = select.select(
        sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            json_msg = socks.recv(2048)
            receive_msg(json.loads(json_msg))

        # else:
        #     message = sys.stdin.readline()
        #     server.send(json.dumps(jsonTest))
        #     sys.stdout.write("JSON enviado\n")
        #     # sys.stdout.write(message)
        #     sys.stdout.flush()

server.close()
