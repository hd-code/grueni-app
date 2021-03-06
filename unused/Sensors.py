import sys
import time
import datetime
import json
import Adafruit_ADS1x15
import Adafruit_DHT
import smbus
from datetime import datetime, timezone, timedelta

# defines some variables and consts
adc                      = Adafruit_ADS1x15.ADS1115()
bus                      = smbus.SMBus(1)
jsonData                 = {}
jsonData['Tomato']       = []

DEVICE                   = 0x23 # Default device I2C address
ONE_TIME_HIGH_RES_MODE_1 = 0x20 # Start measurement at 1lx resolution. Time typically 120ms

SENSOR                   = 22   # DHT 22
PIN                      = 4    # GPIO 4

def convertLight():
    data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE_1)
    result = (data[1] + (256 * data[0])) / 1.2
    return result

def convertMoisture():
    data = adc.read_adc(0, 2)
    result = ((data - 18600) / 100) / 1.48
    return result

def convertTemperature():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    return temperature

def convertHumidity():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    return humidity

def writeJson():
#    d = datetime.datetime.now()
    jsonData['Tomato'].append({
#	    'time'        : d.timestamp(),
	    'light'       : convertLight(),
	    'temperature' : convertTemperature(),
	    'humidity'    : convertHumidity(),
	    'drought'     : convertMoisture(),
	    'size'        : 8.0
    })

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(jsonData, f, indent=4)

def displayOutput():
    print('-------------------------------------------------------------')
    print('Light Level   : ' + format(convertLight(), '.1f')       + ' lx')
    print('Temperature   : ' + format(convertTemperature(), '.1f') + ' *')
    print('Humidity      : ' + format(convertHumidity(), '.1f')    + ' %')
    print('Drought Level : ' + format(convertMoisture(), '.1f')    + ' %') 

def main():

  while True:
   # now = datetime.now()
  #  writeJson()
    displayOutput()
    time.sleep(3)
   #print(format(convertMoisture(), '.1f'))
   # timedelta = datetime.now() - now

   # print(timedelta)
   # writeJson()
   # time.sleep(1)


# run Script
if __name__=="__main__":
   main()
