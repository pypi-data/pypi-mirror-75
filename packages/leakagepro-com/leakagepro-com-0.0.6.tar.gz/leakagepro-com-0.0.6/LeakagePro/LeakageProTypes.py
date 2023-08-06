# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 23:36:18 2020

@author: marku
"""
from enum import Enum

class LeakageComType(Enum):
    SERIAL = 1,
    TCP = 2
    ALL = 3
    
class LeakageComDiscovery(Enum):
    APPEAR = 1,
    DISAPPEAR = 2