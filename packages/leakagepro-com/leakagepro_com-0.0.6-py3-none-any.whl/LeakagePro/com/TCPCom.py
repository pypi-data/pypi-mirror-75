# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:09:28 2020

@author: marku
"""
import socket
from .BaseCom import BaseCom

class TCPCom(BaseCom):
    def __init__(self, addr, conTimeout=1, ioTimeout=0.5, trace=False, traceCB=None):
        self.ipaddr = addr[0]
        self.port = addr[1]
        self.conTimeout = conTimeout
        self.ioTimeout = ioTimeout
        BaseCom.__init__(self, trace, traceCB)
        
    def _write(self, data):
        self.sock.send(data)
        
    def _read(self, nbytes):
        d = self.sock.recv(nbytes)
        return d
   
    def _connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.conTimeout)
        self.sock.connect((self.ipaddr, self.port))
        self.sock.settimeout(self.ioTimeout)
        
    def _disconnect(self):
        self.sock.close()