import zmq
import sys
import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from Arduino import Arduino
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np




class WorkerThread(QThread):
    data_signal = pyqtSignal(object)
    def __init__(self, Ar, publisher, context):
        super().__init__()
        self.Ar = Ar
        self.publisher = publisher
        self.context = context


    def run(self):

        while True:
                dataArray = self.Ar.run_Block()
                self.data_signal.emit(dataArray)
                #print(type(dataArray))
                self.publisher.send_multipart([b"A0", b"%f" % dataArray[1], b"%f" % dataArray[2],
                                               b"%f" % dataArray[3], b"%f" % dataArray[4]])
                time.sleep(0.1)


def main():
    A0 = []
    A1 = []
    A2 = []
    A3 = []
    A4 = []
    def update(dataArray):
        #print(dataArray)
        A0.append(dataArray[0])
        A1.append(dataArray[1])
        A2.append(dataArray[2])
        A3.append(dataArray[3])
        A4.append(dataArray[4])
       # print(A0)
        p1.setData(x=A0, y=A1)
        p2.setData(x=A0, y=A2)
        p3.setData(x=A0, y=A3)


    app = QtGui.QApplication([])
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('pyqtgraph example: PlotWidget')
    mw.resize(800, 600)
    cw = QtGui.QWidget()
    mw.setCentralWidget(cw)
    l = QtGui.QVBoxLayout()
    cw.setLayout(l)

    pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
    l.addWidget(pw)
    pw2 = pg.PlotWidget(name='Plot2')
    l.addWidget(pw2)
    pw3 = pg.PlotWidget()
    l.addWidget(pw3)

    mw.show()

    p1 = pw.plot()
    p1.setPen((200, 200, 100))
    rect = QtGui.QGraphicsRectItem(QtCore.QRectF())
    rect.setPen(QtGui.QPen(QtGui.QColor(100, 200, 100)))
    pw.addItem(rect)
    pw.setYRange(0, 4000)

    p2 = pw2.plot()
    p2.setPen((200, 200, 100))
    rect = QtGui.QGraphicsRectItem(QtCore.QRectF())
    rect.setPen(QtGui.QPen(QtGui.QColor(100, 200, 100)))
    pw2.addItem(rect)
    pw2.setYRange(0, 4000)

    p3 = pw3.plot()
    p3.setPen((200, 200, 100))
    rect = QtGui.QGraphicsRectItem(QtCore.QRectF())
    rect.setPen(QtGui.QPen(QtGui.QColor(100, 200, 100)))
    pw3.addItem(rect)
    pw3.setYRange(0, 4000)
    '''Connect to Arduino'''
    Ar = Arduino()
    Ar.Open_Arduino()
    '''ZMQ part'''
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://127.0.0.1:5563")
    print("Publisher is open")

    worker_thread = WorkerThread(Ar, publisher, context)
    worker_thread.start()
    worker_thread.data_signal.connect(update)
   # worker_thread.data_signal.connect(p2.setData)
   # worker_thread.data_signal.connect(p3.setData)

    app.exec_()
    Ar.Close_Arduino()
    print('Arduino is closed')
    publisher.close()
    context.term()
    print('Publisher is closed')

if __name__ == "__main__":
    main()