#Code by Sahak Sahakyan
#Library for ds18b20 temperature sensor
#Contact`
#Email: sahak.sahakyan2017@gmail.com

import sys
import glob
import os

class DsbS():

    def __init__(self, initial=False):
        if initial:
            os.system('modprobe w1-gpio')
            os.system('modprobe w1-therm')

    def getSensorIds(slef):
        return [i.split("/")[5] for i in glob.glob("/sys/bus/w1/devices/28-0*/w1_slave")]

    def getTemps(self, Ttype="C"):
        temps = list()

        if len([i.split("/")[5] for i in glob.glob("/sys/bus/w1/devices/28-0*/w1_slave")]) < 1: print("NO DEVICES FOUND"); return "Null"

        for sensor in glob.glob("/sys/bus/w1/devices/28-0*/w1_slave"):
            id = sensor.split("/")[5]
            try:
                f = open(sensor, "r")
                data = f.read()
                f.close()
                if "YES" in data:
                    (discard, sep, reading) = data.partition(' t=')
                    if Ttype.lower() == "c":
                        t = float(reading) / 1000.0
                        temps.append(t)
                    elif Ttype.lower() == "f":
                        t = (float(reading) / 1000.0 * 9 / 5) + 32
                        temps.append(t)
                    elif Ttype.lower() == "k":
                        t = (float(reading) / 1000.0) + 273.15
                        temps.append(t)
                    else:
                        t = float(reading) / 1000.0
                        temps.append(t)
                        print("WARNING: UNKOWN TEMPERATURE TYPE")
                    
                else:
                    print("EROR WHILE READING TEMPERATURE")
            except:
                print("EROR WHILE READING TEMPERATURE1")
        
        return temps

    def getIdTemp(self, Ttype="c"):
        temps = dict()

        if len([i.split("/")[5] for i in glob.glob("/sys/bus/w1/devices/28-0*/w1_slave")]) < 1: print("NO DEVICES FOUND"); return "Null"

        for sensor in glob.glob("/sys/bus/w1/devices/28-0*/w1_slave"):
            id = sensor.split("/")[5]
            try:
                f = open(sensor, "r")
                data = f.read()
                f.close()
                if "YES" in data:
                    (discard, sep, reading) = data.partition(' t=')
                    if Ttype.lower() == "c":
                        t = float(reading) / 1000.0
                        temps[sensor] = t
                    elif Ttype.lower() == "f":
                        t = (float(reading) / 1000.0 * 9 / 5) + 32
                        temps[sensor] = t
                    elif Ttype.lower() == "k":
                        t = (float(reading) / 1000.0) + 273.15
                        temps[sensor] = t
                    else:
                        t = float(reading) / 1000.0
                        temps[sensor] = t
                        print("WARNING: UNKOWN TEMPERATURE TYPE")
                    
                else:
                    print("EROR WHILE READING TEMPERATURE")
            except:
                print("EROR WHILE READING TEMPERATURE")
        
        return temps