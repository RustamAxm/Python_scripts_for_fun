from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import pyqtgraph as pg
import numpy as np
from picoscope import ps6000
import time
import scipy
import scipy.fftpack
import traceback

class WorkerThread(QThread):
    data_signal = pyqtSignal(object)
    def __init__(self, ps):
        super().__init__()
        self.ps = ps


    def run(self):

        def fft(signal, freq):
            # w = blackman(len(signal)) #window for digital filter
            FFT = abs(scipy.fftpack.fft(signal))
            # FFTdb = 20*scipy.log10(FFT)
            freqs = scipy.fftpack.fftfreq(len(signal), 1 / freq)
            # FFTdb = FFTdb[2:len(freqs)/2]
            # freqs = freqs[2:len(freqs)/2]
            return (freqs, FFT)

        def window(size):
            return np.ones(size)/float(size)

        def average(arr, n):
            end = n * int(len(arr)/n)
            return np.mean(arr[:end].reshape(-1,n),1)

        # Example of simple capture
        Buff_size = int(2 ** 16)
        SamplFreq = 1250E6  # 1250 for FFT
        Sample_count = 300000# колво спектров до 500
        res = self.ps.setSamplingFrequency(SamplFreq, Buff_size)
        sampleRate = res[0]  # noqa
        print("Sampling @ %f MHz, %d samples" % (res[0] / 1E6, res[1]))
        self.ps.setChannel("A", "AC", 50E-3)
        self.ps.setChannel("B", "AC", 50E-3)
        Sum = np.array(0)
        Time = time.clock()

        for i in range(0, Sample_count):

            self.ps.runBlock()
            while (self.ps.isReady() is False):
                time.sleep(0.01)

            data = self.ps.getDataV("A", Buff_size) - self.ps.getDataV("B", Buff_size)


            A = np.column_stack(fft(data, sampleRate))
            Sum = Sum + A[:, 1]
            if i% 10 == 0:
                self.data_signal.emit({'x': A[:, 0], 'y': Sum})
                print("Sampling Done %i" % i)
        #np.savetxt('test2.txt',blockdata ,  fmt='%10.4f')
        self.ps.close()
        print(abs(Time-time.clock())/60, "min")
        np.savetxt('31102018_CdMnTe_T=10K_0.2000Tesla_785nm.txt', np.column_stack((A[:, 0], Sum)), fmt='%10.4f')
       # np.savetxt('30102018_test_aver_.txt', np.column_stack((A[:, 0], np.convolve(Sum, window(100),'same'))), fmt='%10.4f')
        np.savetxt('31102018_CdMnTe_T=10K_0.2000Tesla_785nm_average.txt', np.column_stack((average(A[:, 0],64), average(Sum, 64))), fmt='%10.4f')
        print("Data saved")



class MyWidget(pg.GraphicsWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        ps = ps6000.PS6000()
        self.worker_thread = WorkerThread(ps)
        self.worker_thread.start()

        # self.timer = QtCore.QTimer(self)
        # self.timer.setInterval(100)  # in milliseconds
        # self.timer.start()
        # self.timer.timeout.connect(self.onNewData)

        self.plotItem = self.addPlot(title="Lidar points")
        self.plotDataItem = self.plotItem.plot([])

        self.worker_thread.data_signal.connect(self.plotDataItem.setData)



    def setData(self, x, y):
        self.plotDataItem.setData(x, y)


    def onNewData(self):
        numPoints = 1000
        x = np.random.normal(size=numPoints)
        y = np.random.normal(size=numPoints)
        self.setData(x, y)



def main():
    app = QtWidgets.QApplication([])

    pg.setConfigOptions(antialias=False) # True seems to work as well

    win = MyWidget()
    win.show()
    win.resize(800,600)
    win.raise_()
    app.exec_()


if __name__ == "__main__":
    main()