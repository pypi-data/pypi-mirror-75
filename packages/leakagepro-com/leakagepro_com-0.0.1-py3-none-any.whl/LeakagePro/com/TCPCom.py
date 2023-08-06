# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:09:28 2020

@author: marku
"""
import socket

class TCPCom:
    def __init__(self, ipaddr, port=10000, conTimeout=1, ioTimeout=0.5):
        self.ipaddr = ipaddr
        self.port = port
        self.conTimeout = conTimeout
        self.ioTimeout = ioTimeout        
        self.connect()
        
    def write(self, data):
        self.sock.send(data)
        
    def read(self, nbytes):
        return self.sock.recv(nbytes)
    
    def readLine(self, maxBytes=None, delimiter=[b"\n"]):
        data = b""
        delimFound = False
        while not delimFound:
            d = self.sock.recv(1)
            data += d
            for delim in delimiter:
                if data.find(delim) != -1:
                    delimFound = True
                    break
            
            if maxBytes != None:
                if len(data) >= maxBytes:
                    break
                
        return data
    
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.conTimeout)
        self.sock.connect((self.ipaddr, self.port))
        self.sock.settimeout(self.ioTimeout)
        
    def disconnect(self):
        self.sock.close()