# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:09:28 2020

@author: marku
"""

class BaseCom:
    def __init__(self, trace=False, traceCB=None):
        self._trace = trace
        self._traceCB = traceCB
        self.connect()

    def _write(self, data):
        raise NotImplementedError("Must be implemented in concrete class")
        
    def _read(self, nbytes):
        raise NotImplementedError("Must be implemented in concrete class")
        
    def _connect(self):
        raise NotImplementedError("Must be implemented in concrete class")
        
    def _disconnect(self):
        raise NotImplementedError("Must be implemented in concrete class")
        
    def connect(self):
        self._connect()
        
    def disconnect(self):
        self._disconnect()
        
    def setTrace(self, trace, cb):
        self._trace = trace
        self._traceCB = cb
                
    def write(self, data):
        self._write(data)
        if self._trace:
            if self._traceCB == None:
                print(">", data)
            else:
                self._traceCB(data, "WRITE")
        
    def read(self, nbytes):
        d = self._read(nbytes)
        if self._trace and len(d) > 0:
            if self._traceCB == None:
                print(d.decode(), end='')
            else:
                self._traceCB(d, "READ")
        return d
    
    def readLine(self, maxBytes=None, delimiter=[b"\n"]):
        data = b""
        delimFound = False
        while not delimFound:
            d = self.read(1)
            data += d
            for delim in delimiter:
                if data.find(delim) != -1:
                    delimFound = True
                    break
            
            if maxBytes != None:
                if len(data) >= maxBytes:
                    break
            
        return data