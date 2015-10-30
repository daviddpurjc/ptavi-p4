#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dic = {}

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion\r\n\r\n")
        print (self.client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print("El cliente nos manda " + line.decode('utf-8'))
            #hacemos las muvis
            deco = line.decode('utf-8')
            if  deco.startswith('REGISTER'):
                self.dic[self.client_address[0]] = deco[deco.find(':')+1:deco.find('SIP')-1]
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
        print(self.dic)

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
