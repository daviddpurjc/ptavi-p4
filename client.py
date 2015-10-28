#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

try:
    sys.argv[5] =! None
except ValueError:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")

# Dirección IP del servidor.
SERVER = sys.argv[1]
PORT = sys.argv[2]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

# Contenido que vamos a enviar
if sys.argv[3] == 'register':
    REGISTER = sys.argv[3]
    DIRECCION = sys.argv[4]
    expires = sys.argv[5]
    LINE = 'REGISTER sip:'+DIRECCION+' SIP/2.0\r\n\r\n'+ 'Expires: '+expires+'\r\n\r\n'
    print("Enviando: " + LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
##else:
  #  LINE = sys.argv[3:]
   # print("Enviando: " + LINE)
    #my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    #data = my_socket.recv(1024)


print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
