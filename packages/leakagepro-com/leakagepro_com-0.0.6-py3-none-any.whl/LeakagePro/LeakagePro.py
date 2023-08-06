# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:09:28 2020

@author: marku
"""
from .com import SerialCom, TCPCom
from threading import Thread
import time
import pandas as pd
from multiprocessing import Lock
import os
from .LeakageProTypes import LeakageComType, LeakageComDiscovery
from .Discovery import LeakageProDiscovery
import pkg_resources

__version__ = pkg_resources.get_distribution("leakagePro-com").version

class AutoDiscover:
    def __init__(self, types=LeakageComType.ALL, verbose=False, timeout=5):
        self._timeout = timeout
        self._types = types
        self._verbose= verbose
    
    def _onDeviceDiscovered(self, conType, data, appearType):
        if self._types != LeakageComType.ALL:
            if conType != self._types:
                return
        
        if appearType == LeakageComDiscovery.APPEAR:
            dev = {}
            dev["data"] = data
            dev["type"] = conType
            self._deviceDiscovered.append(dev)
        else:
            self._deviceDiscovered = list(filter(lambda a: 
                                                 a["data"]["address"] != data["address"],
                                                 self._deviceDiscovered))
                
    def discover(self):
        self._deviceDiscovered = []
        
        disco = LeakageProDiscovery(verbose=self._verbose)
        disco.setCB(self._onDeviceDiscovered)
        disco.start()
        start = time.time()
        while len(self._deviceDiscovered) == 0:
            time.sleep(1)
            if time.time() - start > self._timeout:
                raise RuntimeError("Timeout in device discovery")
        disco.stop()
        comType = self._deviceDiscovered[0]["type"]
        if comType == LeakageComType.TCP:
            ipaddr = self._deviceDiscovered[0]["data"]["address"]
            port = self._deviceDiscovered[0]["data"]["port"]
            addr = (ipaddr, port)
        else:
            addr = (self._deviceDiscovered[0]["data"]["address"], )
        
        return comType, addr
                    

class LeakagePro:
    CHUNK = 1024
    
    def __init__(self, logFileName=None, comType=LeakageComType.TCP, ipaddr=None, 
                 port=10000, conTimeout=3, ioTimeout=0.5, logChunkSize=30,
                 maxPandaSize=5000, csvSeparator="\t", csvDecimal=",",
                 delLogFile=False, autoDiscover=True, autoDiscoverTypes=LeakageComType.ALL,
                 discoverTimeout=5, comport="COM6", verbose=False, traceCom=False,
                 traceCB=None):

        self._verbose = verbose

        if logFileName != None:
            if delLogFile == False and os.path.exists(logFileName):
                raise RuntimeError("log file %s exists, but parameter delLogFile=False"%
                                   os.path.abspath(logFileName))
            elif delLogFile == True and os.path.exists(logFileName):
                os.remove(logFileName)
                

        if autoDiscover:
            disco = AutoDiscover(autoDiscoverTypes, self._verbose, discoverTimeout)
            comType, addr = disco.discover()
        
        if comType == LeakageComType.SERIAL:
            if not autoDiscover:
                addr = (comport)
            self.com = SerialCom.SerialCom(addr, conTimeout, ioTimeout, trace=traceCom, traceCB=traceCB)
        elif comType == LeakageComType.TCP:
            if not autoDiscover:
                addr = (ipaddr, port)
            self.com = TCPCom.TCPCom(addr, conTimeout, ioTimeout, trace=traceCom, traceCB=traceCB)
        else:
            raise RuntimeError("Unknown com type %s"%str(comType))
            
        self._mutex = Lock()
        self._csvSeparator = csvSeparator
        self._csvDecimal = csvDecimal
        self.logFileName = logFileName
        self._logCBs = []
        
        self._maxPandaSize = maxPandaSize
        if logChunkSize > maxPandaSize:
            logChunkSize = maxPandaSize
        self._logChunkSize = logChunkSize
        
        self._threadRunning = False
        self.enaOutput(False)
        
    def setTrace(self, trace, cb=None):
        self.com.setTrace(trace, cb)
                
    def appendLogCB(self, cb, userData=None):
        d = {"func":cb, "data": userData}
        self._logCBs.append(d)
                    
    def workerThread(self):
        self._threadRunning = True
        self.enaOutput(True)
        
        errCnt = 0
        firstWrite = True
        logCnt = 0
        
        while not self._stopThread:
            try:
                self.curData = self.getOutput()
                errCnt = 0
            except:
                errCnt += 1
            
            if errCnt > 3:
                print("errCnt > 3, reset connection")
                errCnt = 0
                self.resetConnection()
                print("... connection reset successful, continue")
                continue
            
            if self.curData == None:
                self.resetConnection()
            elif type(self.curDataPD) == type(None):
                self.curDataPD = pd.DataFrame(columns=list(self.curData.keys()))
            
            if self.curData != None:
                self.curDataPD = self.curDataPD.append(self.curData, ignore_index=True)
                logCnt += 1
                
                if len(self.curDataPD) > self._maxPandaSize:
                    self.curDataPD = self.curDataPD.iloc[-self._maxPandaSize:]
                
                try:
                    for cb in self._logCBs:
                        cb["func"](self.curData, self.curDataPD, cb["data"])
                except:
                    print("error in callback")
                
                if logCnt >= self._logChunkSize and self.logFileName != None:
                    self.curDataPD.iloc[-logCnt:].to_csv(self.logFileName, header=firstWrite, 
                                       mode="a", index=False, decimal=self._csvDecimal,
                                       sep=self._csvSeparator)
                    firstWrite = False
                    logCnt = 0

        # log remaining content
        if logCnt != 0 and self.logFileName != None:
            self.curDataPD.iloc[-logCnt:].to_csv(self.logFileName, header=firstWrite,
                               mode="a", index=False, decimal=self._csvDecimal,
                               sep=self._csvSeparator)
        self.enaOutput(False)
        self._threadRunning = False
            
    def stopLogging(self, timeout = 5):
        if self.isLogging():
            self._stopThread = True
            now = time.time()
            while self.isLogging():
                if time.time() - now > timeout:
                    raise RuntimeError("Logging timed out")
                time.sleep(0.1)
                
    def startLogging(self, timeout = 5):
        if not self.isLogging():
            self._stopThread = False
            self.curData = None
            self.curDataPD = None
            self._worker = Thread(target=self.workerThread)
            self._worker.start()
            
    def isLogging(self):
        return self._threadRunning
        
    def enaOutput(self, ena):
        with self._mutex:
            if ena:
                self.com.write(b"O\r\n")
            else:
                self.com.write(b"o\r\n")
                time.sleep(0.5)
                nbytes = self.CHUNK
                while nbytes == self.CHUNK:
                    data = self.com.read(self.CHUNK)
                    if type(data) != type(None):
                        nbytes = len(data)
                    else:
                        nbytes = 0
                
    def _execAndCheck(self, cmd, logKey, valExpected, timeout, errDetails, radix=10):
        with self._mutex:
            self.com.write(cmd.encode())
            if not self.isLogging():
                rv = self.com.readLine()
            
        if self.isLogging():
            self._waitLogValue(logKey, valExpected, timeout, "Timeout %s"%errDetails)
        else:
            rv = rv.decode().strip()
            valRead = int(rv.split(" ")[1], radix)
            if valExpected != valRead:
                raise RuntimeError("Error %s"%errDetails)
        
    def _waitLogValue(self, key, value, timeout, errMsg):
        start = time.time()
        while True:
            curData = self.getCurrentData()
            valRead = curData[key]
            if valRead == value:
                break;
            if time.time() - start > timeout:
                raise RuntimeError(errMsg)
            time.sleep(0.1)
        
    def setValve(self, val, timeout=5):
        if val < 0 or val > 0xF:
            raise ValueError("val must be in range [0..15], but is %d"%val)
        
        cmd = "v%x\r\n"%val
        self._execAndCheck(cmd, "V", val, timeout, "setting valves", radix=2)
                
    def setMotor(self, motor, percent, timeout=5):
        if percent < 0 or percent > 100:
            raise ValueError("eprcent must be in range [0..100], but is %d"%percent)
        
        if motor == 0:
            m = "m"
            k = "m0"
        elif motor == 1:
            m = "n"
            k = "m1"
        else:
            raise ValueError("argument motor must be 0 or 1, but is %s"%str(motor))
            
        cmd = m+"%d\r\n"%percent
        self._execAndCheck(cmd, k, percent, timeout, "setting motor", radix=10)
                
    def getCurrentData(self, timeout=5):
        if self.isLogging():
            start = time.time()
            while True:
                data = self.curData
                if type(data) != type(None):
                    break
                if time.time() - start > timeout:
                    raise RuntimeError("Timeout getting log data")
                time.sleep(0.1)
        else:
            data = self.getOutput(doQuery=True)
        return data
    
    def getLoggingData(self):
        return self.curDataPD
        
    def getOutput(self, doQuery=False):
        rv = None
        with self._mutex:
            if doQuery:
                self.com.write(b"o\r\n")
            data = self.com.readLine().decode().strip()
        if len(data) != 0:
            values = data.split("\t")[0::2]
            keys = ["time"] + data.split("\t")[1::2]
            rv = {}
            for k, v in zip(keys, values):
                if k == "rp" or k == "ap" or k == "rt" or k == "at":
                    rv[k] = float(v)
                elif k == "V":
                    rv[k] = int(v, 2)
                else:
                    rv[k] = int(v)
        return rv
    
    def resetConnection(self):
        with self._mutex:
            self.com.disconnect()
            time.sleep(1)
            self.com.connect()
        self.enaOutput(True)
        