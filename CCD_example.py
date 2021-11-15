import ctypes
import numpy as np
import matplotlib.pyplot as plt
import time


dll = ctypes.WinDLL(r"C:\Program Files\Princeton Instruments\WinSpec\pvcam32.dll")


def my_print(string, func):
    print(string, bool(func), '; Error code: ', dll.pl_error_code(), '.')

def gr900_1800(xc, gratings):
    if gratings == 900:
        dx = 0.027142643764022978
        x_offset = 0.002714712485385462
        return np.linspace(xc - 1343 * dx / 2 - x_offset, xc + 1335 * dx / 2 - x_offset, 1340)  # if use central wevelenght
    elif gratings == 1800:
        x_offset = 0.03268222557835543
        dx = 0.010908887229220454
        return np.linspace(xc - 1343 * dx / 2 - x_offset, xc + 1335 * dx / 2 - x_offset, 1340)


cam_name = ctypes.c_buffer(32)
exp_time = ctypes.c_int(1000)
hCam = ctypes.c_int16()
size = ctypes.c_uint32()
status = ctypes.c_int16()
byte_cnt = ctypes.c_uint32()
numberframes = 5
x1 = 631.771
x2 = 668.115
xc = 650 # central wevelenght

# x = np.linspace(x1, x2, 1340) # if use start pixel and end pixel



data = gr900_1800(xc, 1800)

class Region(ctypes.Structure):
    _fields_ = [('s1', ctypes.c_uint16),
                ('s2', ctypes.c_uint16),
                ('sbin', ctypes.c_uint16),
                ('p1', ctypes.c_uint16),
                ('p2', ctypes.c_uint16),
                ('pbin', ctypes.c_uint16)]


s1 = 0
s2 = 1339
p1 = 0
p2 = 399
region = Region(s1, s2, 1, p1, p2, 400)


my_print('Camera initialization:', bool(dll.pl_pvcam_init()))
my_print('Getting camera name:', dll.pl_cam_get_name(0, ctypes.byref(cam_name)))
print('Camera name:', cam_name.value)
my_print('Opening camera:', dll.pl_cam_open(cam_name, ctypes.byref(hCam), 0))
my_print('Initializing exposure sequence:', dll.pl_exp_init_seq())
my_print('Setup exposure sequence:', dll.pl_exp_setup_seq(hCam, 1, 1, ctypes.byref(region), 0, exp_time, ctypes.byref(size)))
print('Buffer size', size.value)
array = np.zeros(size.value, dtype=np.uint16)
frame = array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))
for i in range(numberframes):
    my_print('Start exposure sequence: ', dll.pl_exp_start_seq(hCam, frame))
    while dll.pl_exp_check_status(hCam, ctypes.byref(status), ctypes.byref(byte_cnt)) and (status.value == 5 and status.value != 4):
        pass
    if status.value == 4:
        print('readout failed')
        break

    data = np.column_stack((data, frame[0:1340]))
    print('Frame = %i ' %i)

my_print('Finishing exposure sequence', dll.pl_exp_finish_seq(hCam, frame, 0))
my_print('Uninitializing exposure sequence', dll.pl_exp_uninit_seq())
my_print('Closing camera', dll.pl_cam_close(hCam))
my_print('Uninizializating pvcam32.dll', dll.pl_pvcam_uninit())

np.savetxt('data_test', data, fmt='%10.3f')
print('data saved')

#print(x[0], x[1339], x[0]-x[1], x[1]-x[2], len(x))
plt.plot(data[:, 0], data[:, 1:5])
plt.show()
#a = np.reshape(frame[0:(p2+1)*(s2+1)], (p2+1, s2+1))
#s = plt.pcolormesh(a)
#plt.colorbar(s)
#plt.show()
#np.savetxt('s.txt', np.transpose(a))


