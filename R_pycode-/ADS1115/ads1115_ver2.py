from zIPS120.IPS120_ver2 import MagneticField
import serial
import time
import numpy as np
import re

mf = MagneticField()
# arduino = serial.Serial('com18', 9600, timeout=0.1)  # Creating our serial object named arduinoData
time.sleep(2)
field = np.array((0.05, -0.05))
while True:
    # while (arduino.inWaiting() == 0):  # Wait here until there is data
    #     pass
    # answer = arduino.readline().split()
    # trigger = float(answer[0])/5000
    # print(np.round(trigger, 3))
    # mf.query('J'+str(np.round(trigger, 3)))


    # print(field)
    # if trigger >= 0.001:
    #     # time.sleep(2)
    #     # mf.query('J'+str(np.round(field[i], 2)))
    #     # print("go to")
    #     mf.goto(field[0])
    #     print("HIGHT")
    #     print(np.round(trigger, 3))
    # elif trigger <= -0.001:
    #     mf.goto(field[1])
    #     print("LOW")
    for i in range(len(field)):
        mf.goto(field[i])


