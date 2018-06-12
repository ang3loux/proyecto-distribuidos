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

# def sleepThread():
#     sleepTime = random.randint(1, 5)
#     print sleepTime
#     sleep(sleepTime)

os.system('clear')


def fn2():
    flag = 0

    for resource in resources:
        if resource == '':
            flag += 1

    if flag >= 2:
        print 'Recursos faltantes:', flag
        while True:
            index = random.randint(0, 2)
            if resources[index] == '':
                json_msg = {
                    'typemsg': 0,
                    'msg': index,
                    'msg2':name,
                }
                print 'Recurso pedido:', index
                server.send(json.dumps(json_msg))
                break

    elif flag == 1:
        # PEDIR EL QUE FALTA
        print flag

    else:
        # SE DUERME
        print flag


def desitions(msg):
    if msg['typemsg'] == 0:
        name = msg['msg']
        print 'Mi etiqueta es:', name

    elif msg['typemsg'] == 1:
        if msg['msg'] == 0:
			print 'Recurso ocupado'
            # band = 0
            # for i in msg['msg2']:
            #     if i != '':
            #         band +=1
            # if band == 3:
            #     json_votacion = {
			# 		'msgtype' : '3',
			# 		'msg'  : "Hacer votacion", 
			# 	}
			# 	server.send(json.dumps(json_votacion))
			# else:
			# 	band = 0
			# 	while band == 0:
			# 		option = random.randint(0, 2)
			# 		for opt in msg['msg2']:
			# 			if opt == option:
			# 				band =1
			# 				json_solicitar = {
			# 					'msgtype': '0',
			# 					'msg'  : opt,
			# 				}
			# 				server.send(json.dumps(json_solicitar))
        else:
            print 'Recurso agregado'
            global name
            resources[msg['msg2']] = name

    fn2()


while True:
    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]

    read_sockets, write_socket, error_socket = select.select(
        sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            json_msg = socks.recv(2048)
            desitions(json.loads(json_msg))

        # else:
        #     message = sys.stdin.readline()
        #     server.send(json.dumps(jsonTest))
        #     sys.stdout.write("JSON enviado\n")
        #     # sys.stdout.write(message)
        #     sys.stdout.flush()
            
    #fn2()

server.close()
