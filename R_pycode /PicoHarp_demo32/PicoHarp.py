import time
import ctypes as ct
from ctypes import byref

class PicoHarp:
    def __init__(self):
        self.LIB_VERSION = "3.0"
        self.HISTCHAN = 65536
        self.MAXDEVNUM = 8
        self.MODE_HIST = 0
        self.FLAG_OVERFLOW = 0x0040

        # Measurement parameters, these are hardcoded since this is just a demo
        self.binning = 0  # you can change this
        self.offset = 0
        self.tacq = 1000  # Measurement time in millisec, you can change this
        self.syncDivider = 1  # you can change this
        self.CFDZeroCross0 = 10  # you can change this (in mV)
        self.CFDLevel0 = 100  # you can change this (in mV)
        self.CFDZeroCross1 = 10  # you can change this (in mV)
        self.CFDLevel1 = 50  # you can change this (in mV)
        self.cmd = 0

        # Variables to store information read from DLLs
        self.counts = (ct.c_uint * self.HISTCHAN)()
        self.dev = []
        self.libVersion = ct.create_string_buffer(b"", 8)
        self.hwSerial = ct.create_string_buffer(b"", 8)
        self.hwPartno = ct.create_string_buffer(b"", 8)
        self.hwVersion = ct.create_string_buffer(b"", 8)
        self.hwModel = ct.create_string_buffer(b"", 16)
        self.errorString = ct.create_string_buffer(b"", 40)
        self.resolution = ct.c_double()
        self.countRate0 = ct.c_int()
        self.countRate1 = ct.c_int()
        self.flags = ct.c_int()

        self.phlib = ct.WinDLL("phlib.dll")

        self.phlib.PH_GetLibraryVersion(self.libVersion)
        print("Library version is %s" % self.libVersion.value.decode("utf-8"))
        if self.libVersion.value.decode("utf-8") != self.LIB_VERSION:
            print("Warning: The application was built for version %s" % self.LIB_VERSION)

    def InitPH(self, binning=0):
        print("\nSearching for PicoHarp devices...")
        print("Devidx     Status")
        for i in range(0, self.MAXDEVNUM):
            retcode = self.phlib.PH_OpenDevice(ct.c_int(i), self.hwSerial)
            if retcode == 0:
                print("  %1d        S/N %s" % (i, self.hwSerial.value.decode("utf-8")))
                self.dev.append(i)
            else:
                if retcode == -1:  # ERROR_DEVICE_OPEN_FAIL
                    print("  %1d        no device" % i)
                else:
                    self.phlib.PH_GetErrorString(self.errorString, ct.c_int(retcode))
                    print("  %1d        %s" % (i, self.errorString.value.decode("utf8")))

        if len(self.dev) < 1:
            print("No device available.")
            self.closeDevices()
        print("Using device #%1d" % self.dev[0])
        print("\nInitializing the device...")
        self.tryfunc(self.phlib.PH_Initialize(ct.c_int(self.dev[0]), ct.c_int(self.MODE_HIST)), "Initialize")

        # Only for information
        self.tryfunc(self.phlib.PH_GetHardwareInfo(self.dev[0], self.hwModel, self.hwPartno, self.hwVersion), \
                "GetHardwareInfo")
        print("Found Model %s Part no %s Version %s" % (self.hwModel.value.decode("utf-8"), \
                                                        self.hwPartno.value.decode("utf-8"),
                                                        self.hwVersion.value.decode("utf-8")))

        print("\nCalibrating...")
        self.tryfunc(self.phlib.PH_Calibrate(ct.c_int(self.dev[0])), "Calibrate")

        self.tryfunc(self.phlib.PH_SetSyncDiv(ct.c_int(self.dev[0]), ct.c_int(self.syncDivider)), "SetSyncDiv")

        self.tryfunc(
            self.phlib.PH_SetInputCFD(ct.c_int(self.dev[0]), ct.c_int(0), ct.c_int(self.CFDLevel0), \
                                 ct.c_int(self.CFDZeroCross0)), \
            "SetInputCFD"
        )

        self.tryfunc(
            self.phlib.PH_SetInputCFD(ct.c_int(self.dev[0]), ct.c_int(1), ct.c_int(self.CFDLevel1), \
                                 ct.c_int(self.CFDZeroCross1)), \
            "SetInputCFD"
        )

        self.tryfunc(self.phlib.PH_SetBinning(ct.c_int(self.dev[0]), ct.c_int(binning)), "SetBinning")
        self.tryfunc(self.phlib.PH_SetOffset(ct.c_int(self.dev[0]), ct.c_int(self.offset)), "SetOffset")
        self.tryfunc(self.phlib.PH_GetResolution(ct.c_int(self.dev[0]), byref(self.resolution)), "GetResolution")

        # Note: after Init or SetSyncDiv you must allow 100 ms for valid count rate readings
        time.sleep(0.2)

        self.tryfunc(self.phlib.PH_GetCountRate(ct.c_int(self.dev[0]), ct.c_int(0), byref(self.countRate0)), \
                "GetCountRate")
        self.tryfunc(self.phlib.PH_GetCountRate(ct.c_int(self.dev[0]), ct.c_int(1), byref(self.countRate1)), \
                "GetCountRate")

        print("Resolution=%lf Countrate0=%d/s Countrate1=%d/s" % (self.resolution.value, \
                                                                  self.countRate0.value, self.countRate1.value))

        self.tryfunc(self.phlib.PH_SetStopOverflow(ct.c_int(self.dev[0]), ct.c_int(1), ct.c_int(65535)), \
                "SetStopOverflow")

    def Mesurement(self, tacq=1000):
        # Always use block 0 if not routing
        self.tryfunc(self.phlib.PH_ClearHistMem(ct.c_int(self.dev[0]), ct.c_int(0)), "ClearHistMeM")
        self.tryfunc(self.phlib.PH_GetCountRate(ct.c_int(self.dev[0]), ct.c_int(0), byref(self.countRate0)), \
                "GetCountRate")
        self.tryfunc(self.phlib.PH_GetCountRate(ct.c_int(self.dev[0]), ct.c_int(1), byref(self.countRate1)), \
                "GetCountRate")

        print("Countrate0=%d/s Countrate1=%d/s" % (self.countRate0.value, self.countRate1.value))

        self.tryfunc(self.phlib.PH_StartMeas(ct.c_int(self.dev[0]), ct.c_int(tacq)), "StartMeas")

        print("\nMeasuring for %d milliseconds..." % tacq)

        waitloop = 0
        ctcstatus = ct.c_int(0)
        while ctcstatus.value == 0:
            self.tryfunc(self.phlib.PH_CTCStatus(ct.c_int(self.dev[0]), byref(ctcstatus)), "CTCStatus")
            waitloop += 1

        self.tryfunc(self.phlib.PH_StopMeas(ct.c_int(self.dev[0])), "StopMeas")
        self.tryfunc(self.phlib.PH_GetHistogram(ct.c_int(self.dev[0]), byref(self.counts), ct.c_int(0)), \
                "GetHistogram")
        self.tryfunc(self.phlib.PH_GetFlags(ct.c_int(self.dev[0]), byref(self.flags)), "GetFlags")

        integralCount = 0
        for i in range(0, self.HISTCHAN):
            integralCount += self.counts[i]

        print("\nWaitloop=%1d  TotalCount=%1.0lf" % (waitloop, integralCount))

        if self.flags.value & self.FLAG_OVERFLOW > 0:
            print("  Overflow.")

        return self.counts


    def closeDevices(self):
        for i in range(0, self.MAXDEVNUM):
            self.phlib.PH_CloseDevice(ct.c_int(i))
        exit(0)

    def tryfunc(self, retcode, funcName):
        if retcode < 0:
            self.phlib.PH_GetErrorString(self.errorString, ct.c_int(retcode))
            print("PH_%s error %d (%s). Aborted." % (funcName, retcode, \
                                                     self.errorString.value.decode("utf-8")))
            self.closeDevices()

if __name__ == "__main__":
    import numpy as np
    x = PicoHarp()
    x.InitPH(0) # set binning 0...7 resolution = 4ps*2^(binning) if 0 res= 4ps, if 7 res= 512ps
    for j in range(3):
        Data = x.Mesurement(2000) #Set mesurement time in milliseconds
        np.savetxt('Counts_{}.txt'.format(j), Data, fmt='%10.3f')
    x.closeDevices() # MustHave!!!!!
