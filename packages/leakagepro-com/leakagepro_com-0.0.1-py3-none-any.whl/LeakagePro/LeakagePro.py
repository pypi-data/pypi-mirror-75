# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:09:28 2020

@author: marku
"""
from enum import Enum
from .com import SerialCom, TCPCom
from threading import Thread
import time
import pandas as pd

class LeakageComType(Enum):
    SERIAL = 1,
    TCP = 2

class LeakagePro:
    CHUNK = 1024
    
    def __init__(self, logFileName, comType=LeakageComType.TCP, ipaddr=None, 
                 port=10000, conTimeout=3, ioTimeout=0.5,
                 logChunkSize=1000, maxPandaSize=5000):
        
        if comType == LeakageComType.SERIAL:
            self.com = SerialCom.SerialCom(conTimeout, ioTimeout)
        elif comType == LeakageComType.TCP:
            self.com = TCPCom.TCPCom(ipaddr, port, conTimeout, ioTimeout)
        else:
            raise RuntimeError("Unknown com type %s"%str(comType))
            
        self.logFileName = logFileName
        self._logCBs = []
        
        self._maxPandaSize = maxPandaSize
        if logChunkSize > maxPandaSize:
            logChunkSize = maxPandaSize
        self._logChunkSize = logChunkSize
        
        self._threadRunning = False
        self.start()
        
    def appendLogCB(self, cb, userData=None):
        d = {"func":cb, "data": userData}
        self._logCBs.append(d)
                    
    def workerThread(self):
        self._threadRunning = True
        self.enaOutput()
        
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
                
                if logCnt >= self._logChunkSize or self._forceLog == True:
                    
                    self.curDataPD.iloc[-logCnt:].to_csv(self.logFileName, header=firstWrite, mode="a", index=False)
                    firstWrite = False
                    self._forceLog = False
                    self._logConf = True
                    logCnt = 0

#        log remaining content
        if logCnt != 0:
            self.curDataPD.iloc[-logCnt:].to_csv(self.logFileName, header=firstWrite, mode="a", index=False)
        self.enaOutput()        
        self._threadRunning = False
        
    def doLog(self, timeout = 5):
        self._logConf = False
        self._forceLog = True
        now = time.time()
        while not self._logConf:
            if time.time() - now > timeout:
                raise RuntimeError("Logging timed out")
            time.sleep(0.1)
            
    def stop(self, timeout = 5):
        if self.isRunning():
            self._stopThread = True
            now = time.time()
            while self.isRunning():
                if time.time() - now > timeout:
                    raise RuntimeError("Logging timed out")
                time.sleep(0.1)
                
    def start(self, timeout = 5):
        if not self.isRunning():
            self._stopThread = False
            self.curData = None
            self.curDataPD = None
            self._forceLog = False
            self._worker = Thread(target=self.workerThread)
            self._worker.start()
            
    def isRunning(self):
        return self._threadRunning
        
    def enaOutput(self):
        self.com.write(b"O\r\n")
        
    def getOutput(self):
        rv = None
        data = self.com.readLine().decode().strip()
        if len(data) != 0:
            values = data.split("\t")[0::2]
            keys = ["time"] + data.split("\t")[1::2]
            rv = {}
            for k, v in zip(keys, values):
                if k == "rp" or k == "ap" or k == "rt" or k == "at":
                    rv[k] = float(v)
                else:
                    rv[k] = int(v)
        return rv
    
    def resetConnection(self):
        self.com.disconnect()
        time.sleep(1)
        self.com.connect()
        self.enaOutput()