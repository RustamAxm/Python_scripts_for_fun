# python class for working with an oscilloscope
#
#


import ctypes,time,traceback
from picostatus import*
import numpy as np

PS6000_BW_FULL = 0
PS6000_BW_20MHZ = 1
PS6000_BW_25MHZ = 2

RANGES = [.02,.05,.1,.2,.5,1.,2.,5.,10.,20.]
RANGE_MULT = [6.103515625e-07, #guess
    1.5378937007874018e-06,
 3.0757874015748035e-06,
 6.151574803149607e-06,
 1.5378937007874016e-05,
 3.075787401574803e-05,
 6.151574803149606e-05,
 0.00015378937007874016,
 0.0003075787401574803,
 0.0006151574803149606]

class Pico6000(ctypes.WinDLL):
    handle = 0
    bufflen = 1000000

    t1=0
    t2=0
    cnt_treshold = 10
    TIMEBASE_CONST = 125000000
    TIMEBASE_CONST0 = 1000000000
    minimalValue,maximalValue = -32512.,32512.
    def __init__(self,serialnumber = None,yrange = 9,timebase = 10,dx = 0,nSegments = 1,bufszPreferred = 1000000):
        self.serialnumber = serialnumber
        self.nSegments = nSegments
        self.maxSamples = 1000000 #just a default value, can be queried in setSegments
        self.channelsEnabled = set()
        self.sampCountWanted = bufszPreferred
        self.callback = print
        self.numChannels = 4
        self.buff = [None]*self.numChannels
        self.yrange = [yrange]*self.numChannels
        self.timeIndisposedMs = ctypes.c_long()
        self.pParameter = ctypes.c_void_p()
        if dx>8e-9:
            timebase = int(np.floor(dx*self.TIMEBASE_CONST+2))
        elif dx<=8e-9 and dx>0:
            timebase = int(np.floor(np.log2(dx*self.TIMEBASE_CONST0)))
            if timebase <0:
                timebase = 0
                print('timebase 0 (2ns) is available only in single-channel mode')

        if timebase in range(0,3):
            self.dx = 2.**timebase/self.TIMEBASE_CONST0
        else:
            self.dx = (float(timebase)-2)/self.TIMEBASE_CONST
        print("timebase =",timebase,"\tdx =",self.dx)
        self.timebase = ctypes.c_ulong(timebase)
        #Pico 2000 series device init
        super(Pico6000,self).__init__("ps6000.dll")
        if not self._handle:
            print("library was not loaded")
        #self.open()
        #CallBack = ctypes.CFUNCTYPE(
        DataReadyCallBackType = ctypes.WINFUNCTYPE(
                                      None,
                                      ctypes.c_short, #handle
                                      ctypes.c_ulong, #PICO_STATUS status,
                                      ctypes.c_ulong, #unsigned long noOfSamples,
                                      ctypes.c_short, # short overflow,
                                      ctypes.c_void_p #void * pParameter
                                        )
        self._dataReady = DataReadyCallBackType(self.DataReady)
        self.GetValuesAsync = self.ps6000GetValuesAsync
        self.GetValuesAsync.argtypes = [ctypes.c_short,
                                        ctypes.c_ulong,
                                        ctypes.POINTER(ctypes.c_ulong), #unsigned long * noOfSamples,
                                        ctypes.c_ulong,#unsigned long downSampleRatio,
                                        ctypes.c_short,#PS2000A_RATIO_MODE downSampleRatioMode, enum
                                        ctypes.c_ushort,#unsigned short segmentIndex,
                                        DataReadyCallBackType,
                                        ctypes.c_void_p #void * pParameter
                                        ]
        self.GetValuesAsync.restype = None

        BlockReadyCallBackType = ctypes.WINFUNCTYPE(
                                      None,
                                      ctypes.c_short, #handle
                                      ctypes.c_ulong, #PICO_STATUS status,
                                      ctypes.c_void_p #void * pParameter
                                        )
        self._blockReady = BlockReadyCallBackType(self.ps6000BlockReady)
        self.psRunBlock = self.ps6000RunBlock
        self.psRunBlock.argtypes = [  ctypes.c_short, #short handle,
                                    ctypes.c_long , #long noOfPreTriggerSamples,
                                    ctypes.c_long , #long noOfPostTriggerSamples,
                                    ctypes.c_ulong, #unsigned long timebase,
                                    ctypes.c_short, #short oversample,
                                    ctypes.POINTER(ctypes.c_long),#long * timeIndisposedMs,
                                    ctypes.c_short, #unsigned short segmentIndex,
                                    BlockReadyCallBackType,# self.callback, #ps2000aBlockReady lpReady,
                                    ctypes.c_void_p
                                    ]
        self.psRunBlock.restype = ctypes.c_ulong

        self.callbackparam = ctypes.c_void_p()
        self.onBlockReady = None
        self.onDataReady = None
    def open(self):
        self.handle  = ctypes.c_short()
        serial = ctypes.c_char_p(self.serialnumber)

        units_count = ctypes.c_short()
        serialLth = ctypes.c_short(100)
        #serials = ctypes.c_char_p()
        serials = ctypes.create_string_buffer(serialLth.value)
        self.call("ps6000EnumerateUnits",
                  ctypes.byref(units_count),
                  ctypes.byref(serials),
                  ctypes.byref(serialLth))
        print("found",units_count.value,"devices:",serials.value[:serialLth.value])


        res = self.ps6000OpenUnit(ctypes.byref(self.handle),self.serialnumber)
        if res == 3:
            print('No PicoScope 6000 Series device could be found')
            #sys.exit(res)
            return
        elif res == 0:
            print('PicoScope opened successfully. handle is %d' % self.handle.value)
        else:
            print('ps6000OpenUnit returned %s' % pico_error_string(res))
            #sys.exit(res)
            return
        self.setSegments(self.nSegments)
        #self.setChannel(0,self.yrange,offset = 0,enabled = True,coupling = 1)
        #self.setChannel(1,self.yrange,offset = 0,enabled = True,coupling = 1)
        #self.adjustBufferSize()

        CALLBACK = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.POINTER(ctypes.c_void_p))
        #self.callback = CALLBACK(self.readblock)
        #self.buff = (ctypes.c_short*self.bufflen)()

        #print ("buffer size set to",self.bufflen)
        #self.setdatabuffer()
        #self.x_vals = np.array([i*self.dx for i in xrange(0,self.bufflen)])
        # self.minimalValue,self.maximalValue =  self.getRange()
    def setup(self):
        pass
    # def getRange(self):
        # this is not avalable for 6000 series
        # mi = ctypes.c_short()
        # self.call("ps2000aGetAnalogueOffset",self.handle,ctypes.byref(mi))
        # ma = ctypes.c_short()
        # self.call("ps2000aMaximumValue",self.handle,ctypes.byref(ma))
        # return mi.value,ma.value
    def DataReady(self,handle,status,noOfSamples,overflow,pParameter):
        if status:
            print("ps6000GetValuesAsync returned:",pico_error_string(status))
        elif self.onDataReady:
            #self.onDataReady(handle,status,noOfSamples,overflow,pParameter)
            self.rxBytes = noOfSamples*self.numActiveChannels*2
            self.onDataReady()
        else:
            print("DataReady got:",handle,status,noOfSamples,overflow,pParameter)
    def ps6000BlockReady(self, handle, status, pParameter):
        if status:
            print("ps6000RunBlock asynchronously returned:",pico_error_string(status))
        elif self.onBlockReady:
            self.onBlockReady()
        else:
            print ("ps6000BlockReady got:",handle,status,pParameter)
    def setChannel(self,chan,yrange,offset = 0,enabled = True,coupling = 1):
        res = self.ps6000SetChannel(self.handle, #short handle,
            chan, # PS2000B_CHANNEL channel,
            enabled, # enabled,
            coupling, # PS2000A_COUPLING type,
            yrange+1, # PS2000A_RANGE range,
            offset, #float analogOffset
            PS6000_BW_FULL # bandwidth limiter
            )
        if res == 0:
            print('Channel %d set is OK' % chan)
            if enabled:
                self.channelsEnabled.add(chan)
                maxSampleChan = self.maxSamples/len(self.channelsEnabled)
                #self.adjustBufferSize()
            elif chan in self.channelsEnabled:
                self.channelsEnabled.remove(chan)
            self.yrange[chan] = yrange
        elif res == 15:
            print('The voltage range is not supported or is invalid. Channel # {} voltage range {}'.format(chan,yrange))
            return
        else:
            print('ps6000SetChannel returned %s' % pico_error_string(res))
        self.adjustBufferSize()
        self.setChanDatabuffer(chan)
        self.numActiveChannels = len(self.channelsEnabled)
    def increaseSensitivity(self,chan):
        yrange = self.yrange[chan]+1
        if yrange<len(RANGES):
            self.setChannel(chan,yrange)
    def decreaseSensitivity(self,chan):
        yrange = self.yrange[chan]-1
        if yrange>0:
            self.setChannel(chan,yrange)
    def enableChannel(self,chan,yrange = 10,offset = 0,coupling = 1):
        self.setChannel(chan,yrange,offset = offset,enabled = True,coupling = 1)
    def call(self,func_name,*args):
        func = self.__getattr__(func_name)
        # print(args,func,args[0])
        # self.test(*args)
        err = func(*args)
        if err:
            err_str = pico_error_string(err)
            if args:
                print("{}{} returned error {:X}".format(func,args,err))
            else:
                print("{}() returned error {:X}".format(func,err))
            print(err_str)
        return err
    def setETS(self,cycles,interleave):
        sampleTimePicoseconds = ctypes.c_long()
        res = self.ps6000SetEts(
            self.handle,    ##short handle,
            2,  #PS2000A_ETS_FAST ## PS2000A_ETS_MODE mode,
            cycles,    ##short etsCycles,
            interleave,    ##short etsInterleave,
            ctypes.byref(sampleTimePicoseconds) ##long * sampleTimePicoseconds
            )
        if res:
            if res ==13:
                print('ps6000SetEts error: A parameter is not valid.')
            elif res==44:
                print('ETS is set but no trigger has been set. A trigger setting is required for ETS.')
            else:
                print('ps6000SetEts returned %s' % pico_error_string(res))
            return 0
        if sampleTimePicoseconds.value:
            self.dx = sampleTimePicoseconds.value*1e-12
        self.x_vals = np.array([i*self.dx for i in range(0,self.bufflen)])
        return sampleTimePicoseconds.value
    def setSimpleTrigger(self,channel = 0,threshold = 0):
        res = self.ps6000SetSimpleTrigger(
            self.handle,##short handle,
            1,##short enable,
            channel,##PS2000A_CHANNEL source,
            0,##short threshold,
            3,##PS2000A_THRESHOLD_DIRECTION direction,
            0,##unsigned long delay,
            100##short autoTrigger_ms
            )
        if res:
            print('ps6000SetSimpleTrigger returned %s' % pico_error_string(res))
            ##sys.exit()
#     def setTrigger(self): # not implemented yet
#         chan_prop = self.call("tTriggerChannelProperties",0,1000,0,1000,0,1)
#         trig_chan_array_type = tTriggerChannelProperties*1
#         trig_chan_array = trig_chan_array_type(tTriggerChannelProperties(0,1000,0,1000,0,1))
# ##        typedef struct tTriggerChannelProperties
##{
##short thresholdUpper;
##unsigned short thresholdUpperHysteresis;
##short thresholdLower;
##unsigned short thresholdLowerHysteresis;
##PS2000A_CHANNEL channel;
##PS2000A_THRESHOLD_MODE thresholdMode;
##} PS2000A_TRIGGER_CHANNEL_PROPERTIES
        # res = self.ps2000aSetTriggerChannelProperties (
        #     self.handle,##short handle,
        #     ctypes.byref(trig_chan_array), ##PS2000A_TRIGGER_CHANNEL_PROPERTIES * channelProperties,
        #     1, ##short nChannelProperties,
        #     0,##short auxOutputEnable,
        #     100 ##long autoTriggerMilliseconds
        #     )
        # if res:
        #     if res ==73:
        #         print('An invalid parameter was passed to\
        #     ps2000aSetTriggerChannelProperties.')
        #     else:
        #         print('ps2000aSetTriggerChannelProperties returned %s' % pico_error_string(res))
    def close(self):
        self.ps6000CloseUnit(self.handle)
    def runblock(self):
        if self.handle:
            err = self.psRunBlock(
                self.handle, #short handle,
                self.bufflen/2 , #long noOfPreTriggerSamples,
                self.bufflen/2, #long noOfPostTriggerSamples,
                self.timebase, #unsigned long timebase,
                0, #short oversample,
                ctypes.byref(self.timeIndisposedMs),
                0, #unsigned short segmentIndex,
                ctypes.c_void_p(0),# self.callback, #ps2000aBlockReady lpReady,
                self.callbackparam #void * pParameter
                )
            if err:
                print('ps6000RunBlock returned %s' % pico_error_string(err))
            return err
    def runBlockA(self,segmentIndex = 0):
        if self.handle:
            try:
                arg = ctypes.c_int(42)
                err = self.psRunBlock(
                    self.handle, #short handle,
                    int(self.sampCountWanted/2) , #long noOfPreTriggerSamples,
                    int(self.sampCountWanted/2), #long noOfPostTriggerSamples,
                    self.timebase, #unsigned long timebase,
                    0, #short oversample,
                    ctypes.byref(self.timeIndisposedMs),
                    segmentIndex, #unsigned short segmentIndex,
                    self._blockReady,# self.callback, #ps2000aBlockReady lpReady,
                    self.callbackparam #void * pParameter
                    )
                if err:
                    print('ps6000RunBlock returned %s' % pico_error_string(err))
                return err
            except:
                traceback.print_exc()
    # def setCallBack(self,callback):
    #     if callable(callback):
    #         self.callback = callback
    # def runstreaming(self):
    #     self.streaming = True
    #     self.sampleInterval = ctypes.c_long(1000)
    #     #self.overviewBufferSize = ctypes.c_ulong(1000)
    #     if self.handle:
    #         err = self.ps2000aRunStreaming(
    #             self.handle, #short handle,
    #             ctypes.byref(self.sampleInterval),#unsigned long * sampleInterval,
    #             3,#PS2000A_US PS2000A_TIME_UNITS sampleIntervalTimeUnits
    #             1024,#unsigned long maxPreTriggerSamples,
    #             1024,#unsigned long maxPostTriggerSamples,
    #             0,#short autoStop,
    #             1,#unsigned long downSampleRatio,
    #             0,# PS2000A_RATIO_MODE_NONE PS2000A_RATIO_MODE downSampleRatioMode,
    #             self.bufflen #unsigned long overviewBufferSize
    #             )
    #         if err:
    #             print('ps2000aRunStreaming returned',pico_error_string(err))
    #         return err
    def stop(self):
        res =  self.ps6000Stop(self.handle)
        if res:
            print('ps6000Stop returned %s' % pico_error_string(res))
    def setdatabuffer(self):
        for chan in self.channelsEnabled:
            self.setChanDatabuffer(chan)
        print(self.buff)
    def setChanDatabuffer(self,chan):
        self.buff[chan] = np.zeros((self.bufflen),dtype = np.short)
        err = self.ps6000SetDataBuffer (
            self.handle, ##short handle,
            chan,##int channel,
            #ctypes.cast(self.buff, ctypes.POINTER(ctypes.c_short)),##short * buffer,
            self.buff[chan].ctypes.data_as(ctypes.POINTER(ctypes.c_short)),  ##short * buffer,
            self.bufflen,##long bufferLth,
            0 ##PS2000A_RATIO_MODE mode
            )
        if err:
            print('ps6000SetDataBuffer returned %s' % pico_error_string(err))
        else:
            print("chan {} buffer is {} samples, dx = {}, rec.length = {}".format(
                chan, self.bufflen,self.dx,self.bufflen*self.dx))
    def getDataByPolling(self,timeout = 0.1):
        while not self.isReady():
            time.sleep(0.1)
        self.t2 = time.clock()
        #local_time = time.time()
        self.t_aqck = self.t2-self.t1
        self.t1 = self.t2
        return self.getValuesS()
    def getValuesS(self):
        noOfSamples = ctypes.c_long(self.bufflen)
        overflow = ctypes.c_short()
        err = self.ps6000GetValues(
            self.handle,##short handle,
            0,##unsigned long startIndex,
            ctypes.byref(noOfSamples),##unsigned long * noOfSamples,
            0,##unsigned long downSampleRatio,
            0,##PS2000A_RATIO_MODE downSampleRatioMode,
            0,##unsigned short segmentIndex,
            ctypes.byref(overflow)##short * overflow
            )
        if err:
            print('ps6000GetValues returned %s' % pico_error_string(err))
        if overflow.value:
            print("overflow",overflow.value)
        #print('noOfSamples %d' % noOfSamples.value)
        return noOfSamples.value
    def getValuesA(self,segmentIndex = 0):

            noOfSamples = ctypes.c_ulong(self.bufflen)
            overflow = ctypes.c_short()
            err = self.ps6000GetValuesAsync(
                self.handle,##short handle,
                0,##unsigned long startIndex,
                ctypes.byref(noOfSamples),##unsigned long * noOfSamples,
                0,##unsigned long downSampleRatio,
                0,##PS2000A_RATIO_MODE downSampleRatioMode,
                segmentIndex,##unsigned short segmentIndex,
                self._dataReady,
                self.callbackparam
                )
            if err:
                print('ps6000GetValues returned %s' % pico_error_string(err))
            return err
    # def getMaxBufferSize(self):
    #     pass
    def setSegments(self,nSegments = 1):
        """
        nSegment = from 1 to 32
        """
        self.nSegments = nSegments
        nMaxSample = ctypes.c_long()
        self.call("ps6000MemorySegments",self.handle, nSegments,ctypes.byref(nMaxSample))
        self.maxSamples = nMaxSample.value
        #self.adjustBufferSize()
        print("# of memory segments",self.nSegments,"maximal # of samples",self.maxSamples)
        return self.maxSamples
    def adjustBufferSize(self):
        if self.channelsEnabled:
            maxSampChan = self.maxSamples/len(self.channelsEnabled)
            sz = self.bufflen
            if self.bufflen > maxSampChan:
                self.bufflen = maxSampChan
                print("buffer was reduced from",sz,"to", self.bufflen)
                #self.setdatabuffer()
            elif self.bufflen<self.sampCountWanted and self.bufflen < maxSampChan:
                self.bufflen = min(self.sampCountWanted,self.maxSamples)
                print("buffer was increased from",sz,"to", self.bufflen)
                #self.setdatabuffer()
            self.x_vals = np.arange(0,self.bufflen*self.dx,self.dx)

        # print("maxSample is",self.maxSamples,"buffer size is",self.bufflen)
    def measure_frequency(self):
        # if self.runblock():
        #     return
        while not self.isReady():
            time.sleep(0.1)
        self.t2 = time.clock()
        local_time = time.time()
        aqt = self.t2-self.t1
        self.t1 = self.t2
        self.getValues()
        #freq,freqerr = freq_from_crossings(self.buff,self.dx)
        #freq,freqerr = freq_from_fft(self.buff,self.dx)
        freq,freqerr = freq_from_peaks(self.buff,self.dx)
        #print('%.2f (%.2f) MHz  aquisition time %f'% (freq*1e-6,freqerr*1e-6,aqt))
        return local_time,freq,freqerr,aqt
    def count(self):
##        if self.runblock():
##            return
        while not self.isReady():
            time.sleep(0.1)
        self.t2 = time.clock()
        local_time = time.time()
        aqt = self.t2-self.t1
        self.t1 = self.t2
        self.getValues()
        #freq,freqerr = freq_from_crossings(self.buff,self.dx)
        count = 0
        for v in self.buff:
            if v>self.cnt_treshold:
                count+=1
        #freq,freqerr = freq_from_peaks(self.buff,self.dx)
        #print('%.2f (%.2f) MHz  aquisition time %f'% (freq*1e-6,freqerr*1e-6,aqt))
        return local_time,count,aqt
    def getChanValuesF(self,chan):
        #print(self.buff[chan].ptp(),"->",self.buff[chan].ptp()*RANGE_MULT[self.yrange[chan]])
        return self.buff[chan]*RANGE_MULT[self.yrange[chan]]


    def getValues(self):
        if not self.streaming:
            res = self.ps6000SetDataBuffer (
                self.handle, ##short handle,
                0,##int channel,
                #ctypes.cast(self.buff, ctypes.POINTER(ctypes.c_short)),##short * buffer,
                self.buff.ctypes.data_as(ctypes.POINTER(ctypes.c_short)),  ##short * buffer,
                self.sampCountWanted,##long bufferLth,
                0,##unsigned short segmentIndex,
                0 ##PS2000A_RATIO_MODE mode
                )
            if res:
                print('ps6000SetDataBuffer returned %s' % pico_error_string(res))

        noOfSamples = ctypes.c_long(self.bufflen)
        overflow = ctypes.c_short()
        res = self.ps6000GetValues(
            self.handle,##short handle,
            0,##unsigned long startIndex,
            ctypes.byref(noOfSamples),##unsigned long * noOfSamples,
            0,##unsigned long downSampleRatio,
            0,##PS2000A_RATIO_MODE downSampleRatioMode,
            0,##unsigned short segmentIndex,
            ctypes.byref(overflow)##short * overflow
            )
        if res:
            print('ps6000GetValues returned %s' % pico_error_string(res))
        if overflow.value:
            print("overflow",overflow.value)
        print('noOfSamples %d' % noOfSamples.value)
        return noOfSamples.value
    def isReady(self):
        ready = ctypes.c_short()
        self.ps6000IsReady (
            self.handle,# short handle,
            ctypes.byref(ready) #short * ready
            )
        return bool(ready)
