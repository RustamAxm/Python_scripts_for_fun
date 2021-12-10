from zSR400.SR400 import SR400
import time

dev = SR400('COM2')
dev.Polarisation_setup()
# dev.Counter_A_chanell()
dev.Counter_Reset_and_Start()

# print(dev.Data_A_chanell())
print(dev.Data_Polarisation())