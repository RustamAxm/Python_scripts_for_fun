import serial
import numpy as np
import time

class Arduino():
    def __init__(self):
        self.A0 = []
        self.A1 = []
        self.cnt = 0
    def Open_Arduino(self):
        self.arduinoData = serial.Serial('com18', 9600, timeout=0.1)  # Creating our serial object named arduinoData
        time.sleep(2)
        print("Arduino is open")
    def run_Block(self):
        self.arduinoData.write(b's')
        #print("send s")
        while (self.arduinoData.inWaiting() == 0):  # Wait here until there is data
            pass  # do nothing
        self.arduinoString = self.arduinoData.readline()  # read the line of text from the serial port
        self.dataArray = self.arduinoString.split()  # Split it into an array called dataArray
        self.dataArray[0] = float(self.dataArray[0])
        self.dataArray[1] = float(self.dataArray[1])
        self.dataArray[2] = float(self.dataArray[2])
        self.dataArray[3] = float(self.dataArray[3])
        self.dataArray[4] = float(self.dataArray[4])
        # #time.sleep(0.1)
        #print(self.dataArray)
        return self.dataArray
    def Close_Arduino(self):
        self.arduinoData.close()

if __name__ == "__main__":
    x = Arduino()
    x.Open_Arduino()
    buf = x.run_Block()
    print(buf)
    for i in range(10):
        data = x.run_Block()
        print(data)
        buf = np.row_stack((buf, data))
    print(buf)
    x.Close_Arduino()
