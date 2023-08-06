# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 23:36:18 2020

@author: marku
"""
from zeroconf import ServiceBrowser, Zeroconf
from threading import Thread
import time
from .LeakageProTypes import LeakageComType, LeakageComDiscovery
import socket
import serial.tools.list_ports

class MyZeroconfListener:
    def __init__(self, cb, verbose):
        self._cb = cb
        self._verbose = verbose
        
    def setCB(self, cb):
        self._cb = cb
        
    def getAddrInfo(self, zeroconf, typ, name):
        info = zeroconf.get_service_info(typ, name)
        
        data = {}
        data["address"] = socket.inet_ntoa(info.addresses[0])
        data["port"] =  info.port
        return data
    
    def execCB(self, data, discoType):
        if self._cb != None:
            try:
                self._cb(LeakageComType.TCP, data, discoType)
            except:
                print("exception in zeroconf callback")

    def remove_service(self, zeroconf, typ, name):
        data = self.getAddrInfo(zeroconf, typ, name)
        self.execCB(data, LeakageComDiscovery.DISAPPEAR)

    def add_service(self, zeroconf, typ, name):
        data = self.getAddrInfo(zeroconf, typ, name)
        self.execCB(data, LeakageComDiscovery.APPEAR)

        if self._verbose:
            info = zeroconf.get_service_info(typ, name)
            print("Service %s added, service info: %s" % (name, info))

class MySerialListener:
    def __init__(self, cb, verbose, vid, pid):
        self._cb = cb
        self._verbose = verbose
        self._pid = pid
        self._vid = vid
        self._serialDev = None
    
    def setCB(self, cb):
        self._cb = cb
        
    def execCB(self, data, typ):
        if self._cb != None:
            try:
                self._cb(LeakageComType.SERIAL, data, typ)
            except:
                print ("error in discover callback")
    
    def discover(self):
        prts = serial.tools.list_ports.comports()
        found = False
        for p in prts:
            if p.pid == self._pid and p.vid == self._vid:
                found = True
                if type(self._serialDev) == type(None):
                    if self._verbose:
                        print("Serial device added %s"%str(p))
                    self._serialDev = p
                    data = {}
                    data["address"] = p[0]
                    self.execCB(data, LeakageComDiscovery.APPEAR)
                    break
                    
        if not found:
            if type(self._serialDev) != type(None):
                data = {}
                data["address"] = self._serialDev[0]
                if self._verbose:
                    print("Serial device removed %s"%str(self._serialDev))
                self.execCB(data, LeakageComDiscovery.DISAPPEAR)
            self._serialDev = None

class LeakageProDiscovery:
    def __init__(self, vid=4292, pid=60000, verbose=False):
        self._threadRunning = False
        self._stopThread = False
        self._onDiscover = None
        self._verbose = verbose
        self.listener = None
        self.serialListener = MySerialListener(self._onDiscover, self._verbose, vid, pid)
        
    def setCB(self, cb):
        self._onDiscover = cb
        if type(self.listener) != type(None):
            self.listener.setCB(cb)
        self.serialListener.setCB(cb)
        
    def workerThread(self):
        self._threadRunning = True
        self._stopThread = False
        
        zeroconf = Zeroconf()
        self.listener = MyZeroconfListener(self._onDiscover, self._verbose)
        browser = ServiceBrowser(zeroconf, "_lkp._tcp.local.", self.listener)
        
        while not self._stopThread:
            self.serialListener.discover()
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