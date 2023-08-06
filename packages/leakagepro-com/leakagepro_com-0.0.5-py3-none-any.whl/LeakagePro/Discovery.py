# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 23:36:18 2020

@author: marku
"""
from zeroconf import ServiceBrowser, Zeroconf
from threading import Thread
import time
from LeakagePro import LeakageComType
import socket
import serial.tools.list_ports

class MyListener:
    def __init__(self, cb, verbose):
        self._cb = cb
        self._verbose = verbose
        
    def setCB(self, cb):
        self._cb = cb

    def remove_service(self, zeroconf, type, name):
        if self._verbose:
            print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        
        data = {}
        data["address"] = socket.inet_ntoa(info.addresses[0])
        data["port"] =  info.port
        if self._cb != None:
            try:
                self._cb(LeakageComType.TCP, data)
            except:
                print("exception in zeroconf callback")

        if self._verbose:
            print("Service %s added, service info: %s" % (name, info))

class LeakageProDiscovery:
    def __init__(self, vid=4292, pid=60000, verbose=False):
        self._threadRunning = False
        self._stopThread = False
        self._onDiscover = None
        self._serialDev = None
        self._pid = pid
        self._vid = vid
        self._verbose = verbose
        self.listener = None
        
    def setCB(self, cb):
        self._onDiscover = cb
        if type(self.listener) != type(None):
            self.listener.setCB(cb)
        
    def workerThread(self):
        self._threadRunning = True
        self._stopThread = False
        
        zeroconf = Zeroconf()
        self.listener = MyListener(self._onDiscover, self._verbose)
        browser = ServiceBrowser(zeroconf, "_lkp._tcp.local.", self.listener)
        
        while not self._stopThread:
            prts = serial.tools.list_ports.comports()
            found = False
            for p in prts:
                if p.pid == self._pid and p.vid == self._vid:
                    found = True
                    if type(self._serialDev) == type(None):
                        self._serialDev = p
                        if self._onDiscover != None:
                            data = {}
                            data["address"] = p[0]
                            try:
                                self._onDiscover(LeakageComType.SERIAL, data)
                            except:
                                print ("error in discover callback")
                        break
                        
            if not found:
                self._serialDev = None
                    
            time.sleep(1)
            
        zeroconf.close()
        self._threadRunning = False
    
    def stop(self, timeout = 5):
        if self.isRunning():
            self._stopThread = True
            now = time.time()
            while self.isRunning():
                if time.time() - now > timeout:
                    raise RuntimeError("Stopping timed out")
                time.sleep(0.1)
                
    def start(self, timeout = 5):
        if not self.isRunning():
            self._stopThread = False
            self._worker = Thread(target=self.workerThread)
            self._worker.start()
            
    def isRunning(self):
        return self._threadRunning

if __name__ == "__main__":
    def onNewDevice(tech, data):
        print("device found:", tech, data)
    d = LeakageProDiscovery()
    d.setCB(onNewDevice)
    d.start()