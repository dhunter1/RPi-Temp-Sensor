import os
import time
import smtplib

class Sensor:
    def __init__(self, name, address):  #Use command cd /sys/bus/w1/devices then ls to find address
        self.name = name
        self.address = '/sys/bus/w1/devices/' + address + '/w1_slave'
        self.temp = 100.0
        sensors.append(self)

    def update_temp_sensor(self):
        try:
            rawTempFile = open(self.address, 'r')
            lines = rawTempFile.readlines()
            rawTempFile.close()
            for line in lines:
                tEqualsIndex = line.find('t=')
                if tEqualsIndex != -1:
                    tempString = line[tEqualsIndex + 2:]
                    tempRaw = float(tempString) / 1000.0
                    self.temp = round((tempRaw * 9.0 / 5.0 + 32.0), 1)
        except IOError:
            self.temp = -99.99

    def get_temp_reading(self):
        if self.temp == -99.99:
            message = self.name + ': Sensor not found'
        else:    
            message = self.name + ': ' + str(self.temp) + '*F'
        return message

def send_temp_reading():
    server = smtplib.SMTP('smtp.gmail.com', 587)                        #Connect to Gmail Server
    server.starttls()
    server.login('temperaturenotifications@gmail.com', '<password>')
    message = '\nTemperature Alert: \n'
    for sensor in sensors:
        sensor.update_temp_sensor()
        message = message + '\n' + sensor.get_temp_reading()
    server.sendmail('Temperature', '5551234567@txt.att.net', message)   #Enter your SMTP address
    server.quit()

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sensors = []
message = '\nTemperature Alert: \n'             #Line breaks necessary to format text message correctly

NE_sensor = Sensor('NE', '28-0516b3b851ff');    #Instantiate sensors here
SE_sensor = Sensor('SE', '28-0416c04694ff');
NW_sensor = Sensor('NW', '28-0516b38115ff');
SW_sensor = Sensor('SW', '28-0316b41d7dff'); 

while True:                                     #Begin infinite loop for constant temperature monitoring
    for sensor in sensors:
        sensor.update_temp_sensor()
        print sensor.get_temp_reading()
        if sensor.temp > 76:                    #Set temperature threshold here
            send_temp_reading()
            break
        if time.localtime()[2] == 1 and time.localtime()[3] == 9:           #Monthly test on the 1st of every month at 9am
            send_temp_reading()
            break
    time.sleep(3600)
