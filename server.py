#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dic = {}

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion\r\n\r\n")
        print (self.client_address)
        line = self.rfile.read()
        print("El cliente nos manda " + line.decode('utf-8'))
            #hacemos las muvis
        deco = line.decode('utf-8')
        if deco.startswith('REGISTER'):
            direccion = deco[deco.find(':')+1:deco.find('SIP')-1]
            self.dic[direccion] = self.client_address[0]
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        if deco[deco.find('s:')+3:] == '0\r\n':
            del self.dic[direccion]
        print(self.dic)
        
    def register2json(self):
        print('caca')
        line = self.rfile.read()
        print('caca2')
        deco = line.decode('utf-8')
        direccion = deco[deco.find(':')+1:deco.find('SIP')-1] 
        campoexpire = deco[deco.find('s:')+3:]
        caducidad = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(campoexpire)+time.time()))
        dicc2 = {'address' : self.client_address[0], 'expires': caducidad}
        lista = [direccion,dicc2]
        json.dump(lista, open("registered.json",'w'), sort_keys=True, indent=4, separators=(',', ': '))
            # Si no hay más líneas salimos del bucle infinito


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
    #serv.register2json()
    
    
