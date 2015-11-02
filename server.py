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
    direccion = ''
    campoexpire = ''
    listas = []
    

    def handle(self):
        """ Metodo principal del servidor. """
        # Comprueba que no tenemos usuarios registrados, y llama al metodo json2registered.
        if self.listas == []:
            self.json2registered()
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print (self.client_address)
        line = self.rfile.read()
        print("El cliente nos manda " + line.decode('utf-8'))
        deco = line.decode('utf-8')
        self.campoexpire = deco[deco.find('s:')+3:]
        if deco.startswith('REGISTER'):
            self.direccion = deco[deco.find(':')+1:deco.find('SIP')-1]
            self.dic[self.direccion] = self.client_address[0]
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        if self.campoexpire == '0\r\n':
            del self.dic[self.direccion]
        print(self.dic)
        self.register2json()

    def register2json(self):
        """ Gestionamos los usuarios registrados"""
        expira = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(self.campoexpire)+time.time()))
        dicc2 = {'address' : self.client_address[0], 'expires': expira}
        # Recorremos la lista de listas de usuarios para que si ya existía el usuario, borremos su informacion
        # que será actualizada con su nuevo valor de expiración.
        for lista in self.listas:
            if lista[0] == self.direccion:
                self.listas.remove(lista)
        self.listas.append([self.direccion,dicc2])
        # Comprobamos la expiracion de los usuarios registrados, y si alguno ha caducado lo borramos.
        for lista in self.listas:
            if lista[1]['expires'] <= time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time())):
                self.listas.remove(lista)
        json.dump(self.listas, open("registered.json",'w'), sort_keys=True, indent=4, separators=(',', ': '))

    def json2registered(self):
        """ Comprueba si existe un fichero json para usarlo como lista de usuarios registrados """
        try:
            self.listas = json.load(open("registered.json",'r'))
            print (self.listas)
        except:
            pass

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
    
    
