from ctypes import *
import sys
import os
import numpy as np
import re
import pyqtgraph as pg
import time

if sys.version_info >= (3, 0):
    import urllib.parse

cur_dir = os.path.abspath(os.path.dirname(__file__))
ximc_dir = os.path.join(cur_dir, "ximc")
ximc_package_dir = os.path.join(ximc_dir, "crossplatform", "wrappers", "python")
sys.path.append(ximc_package_dir)  # add ximc.py wrapper to python path

if sys.platform in ("win32", "win64"):
    libdir = os.path.join(ximc_dir, sys.platform)
    os.environ["Path"] = libdir + ";" + os.environ["Path"]  # add dll
try:
    from pyximc import *
except ImportError as err:
    print(
        "Can't import pyximc module. The most probable reason is that you changed the relative location of the testpython.py and pyximc.py files. See developers' documentation for details.")
    exit()
except OSError as err:
    print(
        "Can't load libximc library. Please add all shared libraries to the appropriate places. It is decribed in detail in developers' documentation. On Linux make sure you installed libximc-dev package.\nmake sure that the architecture of the system and the interpreter is the same")
    exit()



class RotationStage():
    def __init__(self):

        self.lib = WinDLL(r'C:\D\PyTest\ximc\win32\libximc.dll')
        self.lib.set_bindy_key(os.path.join(ximc_dir, "win32", "keyfile.sqlite").encode("utf-8"))
        probe_flags = EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_NETWORK
        enum_hints = b"addr=192.168.0.1,172.16.2.3"
        devenum = self.lib.enumerate_devices(probe_flags, enum_hints)
        dev_count = self.lib.get_device_count(devenum)
        print("Device count: " + repr(dev_count))
        if dev_count == 1:
            open_name = self.lib.get_device_name(devenum, 0)
            self.device_id = self.lib.open_device(open_name)
            print("Rotation 0")
        elif dev_count == 2:
            open_name = self.lib.get_device_name(devenum, 0)# по тупому 2 вращателя
            self.device_id = self.lib.open_device(open_name)
            open_name1 = self.lib.get_device_name(devenum, 1)
            self.device_id_1 = self.lib.open_device(open_name1)
            print("Rotation 0 and 1")
        else:
            print("!!!!")

    def move_Rotation_0(self, distance):
        print("\nGoing to {0} steps".format(distance))
        self.lib.command_move(self.device_id, distance, 0)
        errcnt = 0
        while True:
            position = self.get_position_0()
            if position == distance:
                return True
            errcnt += 1
            if np.abs(position - distance) < 2:
                errcnt += 100
            if errcnt > 10000:
                print('Step motor did not reach the {} position, returned at {} instead.'.format(distance, position))
                return True

    def move_Rotation_1(self, distance):
        print("\nGoing to {0} steps".format(distance))
        self.lib.command_move(self.device_id_1, distance, 0)
        errcnt = 0
        while True:
            position = self.get_position_1()
            if position == distance:
                return True
            errcnt += 1
            if np.abs(position - distance) < 2:
                errcnt += 100
            if errcnt > 10000:
                print('Step motor did not reach the {} position, returned at {} instead.'.format(distance, position))
                return True


    def move_Rotation_Togever(self, distance_0, distance_1):
        print("\n1 Going to {0} steps".format(distance_0))
        print("2 Going to {0} steps".format(distance_1))
        self.lib.command_move(self.device_id, distance_0, 0)
        self.lib.command_move(self.device_id_1, distance_1, 0)
        errcnt = 0
        while True:
            position0 = self.get_position_0()
            position1 = self.get_position_1()
            if (position0 == distance_0) and (position1 == distance_1):
                return True
            errcnt += 1
            if (np.abs(position0 - distance_0) < 2) or (np.abs(position1 - distance_1) < 2):
                errcnt += 100
            if errcnt > 10000:
                print('Step motor did not reach the {} position, returned at {} instead.'.format(distance, position0))
                return True


    def get_position_0(self):
        x_pos = get_position_t()
        self.lib.get_position(self.device_id, byref(x_pos))
        return x_pos.Position

    def get_position_1(self):
        x_pos = get_position_t()
        self.lib.get_position(self.device_id_1, byref(x_pos))
        return x_pos.Position

    def Sigma_1(self):
        self.move_Rotation_0(0)

    def Sigma_2(self):
        self.move_Rotation_0(7200)


if __name__ == '__main__':
    rs = RotationStage()
    print('Rotational stage initialized')

    number_of_steps = 1

    for step in range(number_of_steps):
        Time = time.time()
        rs.Sigma_2()  # s1 - 64300 ____ for 45deg lin pol 36075
        # rs.move_Rotation_1(7200)
        print('Measuring s1 polarization')
        # rs.move_Rotation_Togever(0, 7200)
        # rs.Sigma_2()  # s2 - 57100____ for 45deg lin pol 44295
        # rs.move_Rotation_1(0)
        # rs.move_Rotation_Togever(7200, 0)
        print('Measuring s2 polarization')
        print((time.time() - Time), "sec")




