from PicoHarp_demo32.PicoHarp import PicoHarp
import numpy as np

x = PicoHarp()
x.InitPH(0) # set binning 0...7 resolution = 4ps*2^(binning) if 0 res= 4ps, if 7 res= 512ps
for j in range(5):
    Data = x.Mesurement(1000) #Set mesurement time in milliseconds
    np.savetxt('Counts_{}.txt'.format(j), Data, fmt='%10.3f')
x.closeDevices() # MustHave!!!!!