import time
import picoscope_2000_class,picoscope_6000_class
import numpy as np
MAX_WAIT_TIME = 4
PICOSCOPE_SERIES = 6

wait = True
cnt_bytes = 0

def show_results():
    global wait,cnt_bytes

    dataA = ps.getChanValuesF(0)
    dataB = ps.getChanValuesF(1)
    cnt_bytes+=ps.rxBytes
    print("got chan A {} samples, max {:.3g}, ptp {:.3g}".format(len(dataA),dataA.max(),dataA.ptp()))
    print("got chan B {} samples, max {:.3g}, ptp {:.3g}".format(len(dataB), dataB.max(), dataB.ptp()))
    wait = False

if PICOSCOPE_SERIES==2:
    ps = picoscope_2000_class.Pico2000(dx = 4e-9, bufszPreferred=1000000)
elif PICOSCOPE_SERIES == 6:
    ps = picoscope_6000_class.Pico6000(dx=4e-9, bufszPreferred=1000000)
ps.onBlockReady = ps.getValuesA
ps.onDataReady = show_results


ps.open()
ps.enableChannel(0,yrange  = 2)
ps.enableChannel(1,yrange  = 2)
# ps.enableChannel(2,yrange  = 6)
# ps.enableChannel(3,yrange  = 6)



t0 = time.time()
t = 0

ps.runBlockA()

while t<MAX_WAIT_TIME:
    while t<MAX_WAIT_TIME and wait:
        time.sleep(0.1)
        t = time.time()-t0
    ps.runBlockA()
    wait = True
    t = time.time() - t0
t = time.time()-t0
print("test finished, average data rate is {} MB/s".format(cnt_bytes/t/2**20))
ps.close()