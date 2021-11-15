# -*- coding: utf-8
#
# Colin O'Flynn, Copyright (C) 2013. All Rights Reserved. <coflynn@newae.com>
import time
import numpy as np
from picoscope import ps6000


import matplotlib.pyplot as plt
'''For Scipy'''
import scipy
import scipy.fftpack
from scipy.signal import blackman #FFT window

Buff_size = int(2**16)
SamplFreq = 100E6 #1250 for FFT
Sample_count = 1000 #колво спектров до 500


def Plotter(x,y,Summ):
    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.plot(x, y)
    plt.grid(b=None, which='major', axis='both')

    plt.subplot(2, 1, 2)
    plt.plot(x, Summ)
    plt.grid(b=None, which='major', axis='both')

    plt.show()

def fft(signal, freq):
    # w = blackman(len(signal)) #window for digital filter
    FFT = abs(scipy.fftpack.fft(signal))
    # FFTdb = 20*scipy.log10(FFT)
    freqs = scipy.fftpack.fftfreq(len(signal), 1/freq)
    # FFTdb = FFTdb[2:len(freqs)/2]
    # freqs = freqs[2:len(freqs)/2]
    return (freqs, FFT)


def average(arr, n):
    end = n * int(len(arr) / n)
    return np.mean(arr[:end].reshape(-1, n), 1)

def examplePS6000():
    print("Attempting to open...")
    ps = ps6000.PS6000()
    # Example of simple capture
    res = ps.setSamplingFrequency(SamplFreq, Buff_size)
    sampleRate = res[0]  # noqa
    print("Sampling @ %f MHz, %d samples" % (res[0]/1E6, res[1]))
    ps.setChannel("A", "AC", 100E-3)
    # ps.setChannel("B", "AC", 50E-3)
    Sum = np.array(0)
    Time = time.clock()

    for i in range(0, Sample_count):


        ps.runBlock()
        while(ps.isReady() is False):
            time.sleep(0.01)
        if i % 100 == 0:
             print("Sampling Done %i" %i)
        data = ps.getDataV("A", Buff_size) #- ps.getDataV("B", Buff_size)
        A = np.column_stack(fft(data, sampleRate))
        Sum = Sum + A[:,1]

    # np.savetxt('test2.txt',blockdata ,  fmt='%10.4f')
    ps.close()
    print("Accumulation time = ", (time.clock() - Time)/60, 'min')
    np.savetxt('17102019_testGU_average_DC50.txt',
               np.column_stack((average(A[:, 0], 8), average(Sum, 8))), fmt='%10.4f')
    print("Data saved")



if __name__ == "__main__":
 examplePS6000()
