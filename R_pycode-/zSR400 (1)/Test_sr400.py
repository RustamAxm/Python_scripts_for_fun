from zSR400.SR400 import SR400
import numpy as np
from zSpectrometer.Spectrometer import Spectrometer
from zIPS120.IPS120_ver2 import MagneticField
import time


Wavelenght = np.linspace(540, 640, 51)

Sr = SR400('COM11')
D_level = -12e-3 # дикриминатор SR400
T = 1 #вркмя измерения
Sr.Polarisation_setup(T, D_level)
accumulations = 5
dev = Spectrometer()
dev.goto_nm_with_set_nm_per_min_SUBTRUCTIVE(Wavelenght[0], 1000)
time.sleep(2)

mf = MagneticField()
print('Magnetic field initialized')
field = np.zeros(1)

Time = time.time()

for b in range(len(field)):
    mf.goto(field[b])
    for i in range(len(Wavelenght)):
        dev.goto_nm_with_set_nm_per_min_SUBTRUCTIVE(Wavelenght[i], 1000)
        # time.sleep(0.75)
        c1 = 0
        c2 = 0
        for k in range(accumulations):
            print('Accumulation: {}/{}'.format(k + 1, accumulations))
            Sr.Counter_Reset_and_Start(T)
            answer = Sr.Data_Polarisation()
            c1 += float(answer[0])
            c2 += float(answer[1])
        pol = (c2 - c1) / (c2 + c1) * 100
        '''for F(Wavelenght)'''
        data = np.array([Wavelenght[i], float(c1), float(c2), float(pol)])
        print(data)
        if i == 0:
            Res = data
        else:
            Res = np.row_stack(((Res, data)))


    np.savetxt('ZnSe Mn0012_{}Tesla_1.5K_4mW_PEM_slit 500_detsigma+.txt'.format(field[b]), Res, fmt='%10.8f',
                   header='Wavelenght(nm)   C1   C2   POL(%)', comments='')


print((time.time()-Time)/60, "min")
print("Experiment done")