# leakagePro-com
Python bindings for leakagePro. These bindings allow for logging device data as well as interacting with the device (setting valves etc...)

# Quick start

The following snippet sets valves, motors and gets current data.

```python
import LeakagePro

l = LeakagePro.LeakagePro()
l.setValve(0x1)
l.setMotor(0, 10)
data = l.getCurrentData()
```

# Installation

leakagePro-com requires python 3 and can be installed through pip
```
pip install leakagePro-com
```

# Examples

## Log data
leakagePro-com allows to log data in a csv file and into a pandas DataFrame located in RAM.

```python
import LeakagePro
import time

l = LeakagePro.LeakagePro(logFileName="myFile.csv", maxPandaSize=5000, csvSeparator=";", csvDecimal=",")
l.startLogging()
# data is now continuously written into myFile.csv using 'csvSeparator' as column separator
# and 'csvDecimal' as decimal separator. If you don't want the data to be written into a file
# you can set logFileName=None
time.sleep(10)
l.stopLogging()

# data can also be accessed through a pandas object. 
# To avoid memory overflow, the number of entries can be configured
# in the constructor through the parameter 'maxPandaSize'
dataSeries = l.getLoggingData()
```

## Connect to LeakagePro
By default, the LeakagePro class starts a discovery service and auto connects to the LeakagePro device.
There are a couple of options to further control this behaviour.

```python
import LeakagePro

# connect over TCP without autodiscover
l = LeakagePro.LeakagePro(autoDiscover=False, comType=LeakageComType.TCP, ipaddr="192.168.1.87, port=10000)
# connect over serial (USB) without autodiscover
l = LeakagePro.LeakagePro(autoDiscover=False, comType=LeakageComType.SERIAL, comport="COM6")
# Only autodiscover TCP interface
l = LeakagePro.LeakagePro(autoDiscover=True, autoDiscoverTypes=LeakageComType.TCP)
# Only autodiscover serial (USB) interface
l = LeakagePro.LeakagePro(autoDiscover=True, autoDiscoverTypes=LeakageComType.SERIAL)
```

## Trace communication
For debugging purposes, low level communication can be traced either to console or a custom callback.
```python
import LeakagePro

# All data sent to device and read from device is printed on console now
l = LeakagePro.LeakagePro(traceCom=True)
# All data sent to device and read from device can be accessed 
# through the traceCB callback now
def traceCB(data, direction):
  print(data, direction)
l = LeakagePro.LeakagePro(traceCom=True, traceCB=cb)
```

## Logging callbacks
When logging, a user callback can be defined which is called whenever new logging data is available
```python
import LeakagePro
import time

def logCB(curData, dataSeries, userData):
  print("new data")
  
l = LeakagePro.LeakagePro()
l.appendLogCB(logCB)
l.startLogging()
time.sleep(10)
l.stopLogging()
```

## Query version
The package version is available through the __version__ variable
```python
import LeakagePro
print(LeakagePro.__version__)
```

# Authors
Markus Proeller

See also the list of contributors who participated in this project.

# License
This project is licensed under the GPLv3 License - see the LICENSE file for details

# 3rd party libraries
We use the following 3rd party libraries:
 
- pandas (BSD 3-Clause License), see https://pandas.pydata.org/pandas-docs/stable/getting_started/overview.html
- zeroconf (LGPL), see https://github.com/jstasiak/python-zeroconf
- pyserial (custom), see https://pythonhosted.org/pyserial/appendix.html#license
