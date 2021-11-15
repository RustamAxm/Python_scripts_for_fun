import usb.core
import usb.util
import time
import sys


device = usb.core.find(idVendor=0x1A86, idProduct=0xE008)
#device.set_configuration()
ep = usb.util.find_descriptor(device[0][0, 0], custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)==usb.util.ENDPOINT_IN)
outpint = []
outpchr = []
outphex = []
if 1:
    while 1:
        answer = device.read(ep.bEndpointAddress, ep.wMaxPacketSize)
        print(answer)
elif 1:
    while 1:
        #answer = device.read(ep.bEndpointAddress, ep.wMaxPacketSize)
        answer = ep.read(ep.wMaxPacketSize)
        if answer[0] == 241:
            outpint.append(str(answer[1]))
            outpchr.append(chr(answer[1]))
            outphex.append(hex(answer[1]))
            if answer[1] == 138:
                print(len(outpchr))
                print(outpint[5:11])
                print(outpchr[5:11])
                print(outphex[5:11])
                print('\n***\n')
                outpint = []
                outpchr = []
                outphex = []


#  ['176', '176', '176', '176', '182', '49', '181', '176', '49', '13', '138']                   00.007 nF
#  ['°', '°', '°', '°', '¶', '1', 'µ', '°', '1', '\r', '\x8a']
#  ['0xb0', '0xb0', '0xb0', '0xb0', '0xb6', '0x31', '0xb5', '0xb0', '0x31', '0xd', '0x8a']
#
#  ['186', '186', '176', '188', '186', '182', '52', '176', '49', '13', '138']                   .0L MOhm
#  ['º', 'º', '°', '¼', 'º', '¶', '4', '°', '1', '\r', '\x8a']
#  ['0xba', '0xba', '0xb0', '0xbc', '0xba', '0xb6', '0x34', '0xb0', '0x31', '0xd', '0x8a']
#
#  ['176', '176', '185', '52', '185', '176', '179', '176', '176', '13', '138']                   009.49 mV
#  ['°', '°', '¹', '4', '¹', '°', '³', '°', '°', '\r', '\x8a']
#  ['0xb0', '0xb0', '0xb9', '0x34', '0xb9', '0xb0', '0xb3', '0xb0', '0xb0', '0xd', '0x8a']
#
#  ['176', '176', '50', '55', '49', '49', '50', '179', '49', '13', '138']                        0.0271 V
#  ['°', '°', '2', '7', '1', '1', '2', '³', '1', '\r', '\x8a']
#  ['0xb0', '0xb0', '0x32', '0x37', '0x31', '0x31', '0x32', '0xb3', '0x31', '0xd', '0x8a']
#
#  ['176', '176', '176', '176', '176', '49', '49', '176', '49', '13', '138']                     0.0000 V
#  ['°', '°', '°', '°', '°', '1', '1', '°', '1', '\r', '\x8a']
#  ['0xb0', '0xb0', '0xb0', '0xb0', '0xb0', '0x31', '0x31', '0xb0', '0x31', '0xd', '0x8a']
#
#
#
#
#
#
#
#
#
