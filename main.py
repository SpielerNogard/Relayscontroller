import mariadb
from datetime import datetime
import time
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
USB_PORT = "/dev/ttyACM0"  # Arduino Uno WiFi Rev2
# Imports
import serial

import config

try:
   usb = serial.Serial(USB_PORT, 9600, timeout=2)
except:
   print("ERROR - Could not open USB serial port.  Please check your port name and permissions.")
   print("Exiting program.")
   exit()


class Device_Watcher(object):
    def __init__(self):
        self.Server = config.server
        self.Username = config.username
        self.Password = config.password
        self.Databasename = config.databasename

        self.devices = config.mydevices
        self.afktime = config.afktime

        self.lastData = []

        self.run()

    def run(self):
        while True:
            SQL = "SELECT * FROM `v_trs_status`"
            self.check_status(SQL)
            self.process_information()
            time.sleep(600)

    def restart_device(self,name):
        Position = self.devices.index(name)
        print("restarting: ",name)
        if Position == 0:
            Befehl = "eins"
        elif Position == 1:
            Befehl = "zwei"
        elif Position == 2:
            Befehl = "drei"
        elif Position == 3:
            Befehl = "vier"
        elif Position == 4:
            Befehl = "funf"
        elif Position == 5:
            Befehl = "sechs"
        elif Position == 6:
            Befehl = "sieben"
        elif Position == 7:
            Befehl = "acht"
        elif Position == 8:
            Befehl = "neun"
        elif Position == 9:
            Befehl = "zehn"
        elif Position == 10:
            Befehl = "elf"
        elif Position == 11:
            Befehl = "zwolf"
        elif Position == 12:
            Befehl = "dreizehn"
        elif Position == 13:
            Befehl = "vierzehn"
        elif Position == 14:
            Befehl = "funfzehn"
        elif Position == 15:
            Befehl = "sechzehn"
        
        Befehl_on=bytes(Befehl+"_on", 'utf-8')
        Befehl_off=bytes(Befehl+"_off", 'utf-8')
        usb.write(Befehl_off)  # send command to Arduino
        time.sleep(30)
        usb.write(Befehl_on)
    def process_information(self):
        for a in self.lastData:
            #print(a)
            instance_id = a[0]
            device_id= a[1]
            name = a[2]
            routePos= a[3]
            routeMax= a[4]
            area_id= a[5]
            rmname= a[6]
            mode = a[7]
            rebootCounter= a[8]
            init = a[9]
            currentSleepTime= a[10]
            rebootingOption= a[11]
            restartCounter= a[12]
            globalrebootcount= a[13]
            globalrestartcount= a[14]
            lastPogoRestart= a[15]
            lastProtoDateTime= a[16]
            LastPogoReboot= a[17]
            currentPos= a[18]
            lastPos = a[19]
            currentPos_raw= a[20]
            lastPos_raw= a[21]

            #if name in self.devices:
            now = datetime.now()
            dt_object = datetime.fromtimestamp(lastProtoDateTime)
            minutes_diff = (now - dt_object).total_seconds() / 60.0
            print(name," : ","last Update=", dt_object," current time=", now," difference=", minutes_diff,"mins")
            if minutes_diff > 60:
                self.restart_device(name)

        

    def check_status(self,SQL):
        try:
            conn = mariadb.connect(
        user=self.Username,
        password=self.Password,
        host=self.Server,
        port=3306,
        database=self.Databasename

        )
            print("Information: Connected to Database: "+str(self.Databasename)+" with User: "+str(self.Username))
        except mariadb.Error as e:
            print(f"Error: Cant connecting to MariaDB Platform: {e}")
            sys.exit(1)
        cur = conn.cursor()
        print("Information: SQL command is executed: "+str(SQL))
        cur.execute(SQL) 
        Ergebnis1 = cur
        Ergebnis = []
        for a in Ergebnis1:
            Ergebnis.append(a)
        conn.close()
        print("Information: Connection to Database closed")
        self.lastData = Ergebnis


if __name__ == "__main__":
    BOB = Device_Watcher()

