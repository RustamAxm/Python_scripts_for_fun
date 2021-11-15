import time
import sys
import struct
import numpy as np
from collections import Counter
import io

class PH_PTU_to_data:
    def __init__(self):
        # Tag Types
        self.tyEmpty8 = struct.unpack(">i", bytes.fromhex("FFFF0008"))[0]
        self.tyBool8 = struct.unpack(">i", bytes.fromhex("00000008"))[0]
        self.tyInt8 = struct.unpack(">i", bytes.fromhex("10000008"))[0]
        self.tyBitSet64 = struct.unpack(">i", bytes.fromhex("11000008"))[0]
        self.tyColor8 = struct.unpack(">i", bytes.fromhex("12000008"))[0]
        self.tyFloat8 = struct.unpack(">i", bytes.fromhex("20000008"))[0]
        self.tyTDateTime = struct.unpack(">i", bytes.fromhex("21000008"))[0]
        self.tyFloat8Array = struct.unpack(">i", bytes.fromhex("2001FFFF"))[0]
        self.tyAnsiString = struct.unpack(">i", bytes.fromhex("4001FFFF"))[0]
        self.tyWideString = struct.unpack(">i", bytes.fromhex("4002FFFF"))[0]
        self.tyBinaryBlob = struct.unpack(">i", bytes.fromhex("FFFFFFFF"))[0]
        # Record types
        self.rtPicoHarpT3 = struct.unpack(">i", bytes.fromhex('00010303'))[0]
        self.rtPicoHarpT2 = struct.unpack(">i", bytes.fromhex('00010203'))[0]

    def Process(self, inputFile, Resolution = 4):
        # global variables
        global inputfile
        global outputfile
        global recNum
        global oflcorrection
        global truensync
        global dlen
        global isT2
        global globRes
        global numRecords

        CH1 = []
        CH2 = []
        inputfile = inputFile
        # The following is needed for support of wide strings
        outputfile = io.open("Test_PTU.txt", "w+", encoding="utf-16le")

        # Check if inputfile is a valid PTU file
        # Python strings don't have terminating NULL characters, so they're stripped
        magic = inputfile.read(8).decode("utf-8").strip('\0')
        if magic != "PQTTTR":
            print("ERROR: Magic invalid, this is not a PTU file.")
            inputfile.close()
            outputfile.close()
            exit(0)

        version = inputfile.read(8).decode("utf-8").strip('\0')
        outputfile.write("Tag version: %s\n" % version)

        # Write the header data to outputfile and also save it in memory.
        # There's no do ... while in Python, so an if statement inside the while loop
        # breaks out of it
        tagDataList = []  # Contains tuples of (tagName, tagValue)
        while True:
            tagIdent = inputfile.read(32).decode("utf-8").strip('\0')
            tagIdx = struct.unpack("<i", inputfile.read(4))[0]
            tagTyp = struct.unpack("<i", inputfile.read(4))[0]
            if tagIdx > -1:
                evalName = tagIdent + '(' + str(tagIdx) + ')'
            else:
                evalName = tagIdent
            outputfile.write("\n%-40s" % evalName)
            if tagTyp == self.tyEmpty8:
                inputfile.read(8)
                outputfile.write("<empty Tag>")
                tagDataList.append((evalName, "<empty Tag>"))
            elif tagTyp == self.tyBool8:
                tagInt = struct.unpack("<q", inputfile.read(8))[0]
                if tagInt == 0:
                    outputfile.write("False")
                    tagDataList.append((evalName, "False"))
                else:
                    outputfile.write("True")
                    tagDataList.append((evalName, "True"))
            elif tagTyp == self.tyInt8:
                tagInt = struct.unpack("<q", inputfile.read(8))[0]
                outputfile.write("%d" % tagInt)
                tagDataList.append((evalName, tagInt))
            elif tagTyp == self.tyBitSet64:
                tagInt = struct.unpack("<q", inputfile.read(8))[0]
                outputfile.write("{0:#0{1}x}".format(tagInt, 18))
                tagDataList.append((evalName, tagInt))
            elif tagTyp == self.tyColor8:
                tagInt = struct.unpack("<q", inputfile.read(8))[0]
                outputfile.write("{0:#0{1}x}".format(tagInt, 18))
                tagDataList.append((evalName, tagInt))
            elif tagTyp == self.tyFloat8:
                tagFloat = struct.unpack("<d", inputfile.read(8))[0]
                outputfile.write("%-3E" % tagFloat)
                tagDataList.append((evalName, tagFloat))
            elif tagTyp == self.tyFloat8Array:
                tagInt = struct.unpack("<q", inputfile.read(8))[0]
                outputfile.write("<Float array with %d entries>" % tagInt / 8)
                tagDataList.append((evalName, tagInt))
            elif tagTyp == self.tyTDateTime:
                tagFloat = struct.unpack("<d", inputfile.read(8))[0]
                tagTime = int((tagFloat - 25569) * 86400)
                tagTime = time.gmtime(tagTime)
                outputfile.write(time.strftime("%a %b %d %H:%M:%S %Y", tagTime))
                tagDataList.append((evalName, tagTime))
            elif tagTyp == self.tyAnsiString:
                tagInt = struct.unpack("<q", inputfile.read(8))[0]
                tagString = inputfile.read(tagInt).decode("utf-8").strip("\0")
                outputfile.write("%s" % tagString)
                tagDataList.append((evalName, tagString))
            elif tagTyp == self.tyWideString:
                tagInt = struct.unpack("<q", inputfile.read(8))[0]
                tagString = inputfile.read(tagInt).decode("utf-16le", errors="ignore").strip("\0")
                outputfile.write(tagString)
                tagDataList.append((evalName, tagString))
            elif tagTyp == self.tyBinaryBlob:
                tagInt = struct.unpack("<q", inputfile.read(8))[0]
                outputfile.write("<Binary blob with %d bytes>" % tagInt)
                tagDataList.append((evalName, tagInt))
            else:
                print("ERROR: Unknown tag type")
                exit(0)
            if tagIdent == "Header_End":
                break

        # Reformat the saved data for easier access
        tagNames = [tagDataList[i][0] for i in range(0, len(tagDataList))]
        tagValues = [tagDataList[i][1] for i in range(0, len(tagDataList))]

        # get important variables from headers
        numRecords = tagValues[tagNames.index("TTResult_NumberOfRecords")]
        globRes = tagValues[tagNames.index("MeasDesc_GlobalResolution")]
        print("Writing %d records, this may take a while..." % numRecords)

        def gotOverflow(count):
            global outputfile, recNum
            outputfile.write("%u OFL * %2x\n" % (recNum, count))

        def gotMarker(timeTag, markers, bool):
            global outputfile, recNum
            outputfile.write("%u MAR %2x %u\n" % (recNum, markers, timeTag))
            return not bool

        def gotPhoton(timeTag, channel, dtime):
            global outputfile, isT2, recNum
            if isT2:
                outputfile.write("%u CHN %1x %u %8.0lf\n" % (recNum, channel, timeTag, \
                                                             (timeTag * globRes * 1e12)))
            else:
                outputfile.write("%u CHN %1x %u %8.0lf %10u\n" % (recNum, channel, \
                                                                  timeTag, (timeTag * globRes * 1e9), dtime))

        def readPT3():
            global inputfile, outputfile, recNum, oflcorrection, dlen, numRecords
            T3WRAPAROUND = 65536
            bool = True
            for recNum in range(0, numRecords):
                # The data is stored in 32 bits that need to be divided into smaller
                # groups of bits, with each group of bits representing a different
                # variable. In this case, channel, dtime and nsync. This can easily be
                # achieved by converting the 32 bits to a string, dividing the groups
                # with simple array slicing, and then converting back into the integers.
                try:
                    recordData = "{0:0{1}b}".format(struct.unpack("<I", inputfile.read(4))[0], 32)
                except:
                    print("The file ended earlier than expected, at record %d/%d." \
                          % (recNum, numRecords))
                    exit(0)

                channel = int(recordData[0:4], base=2)
                dtime = int(recordData[4:16], base=2)
                nsync = int(recordData[16:32], base=2)

                if channel == 0xF:  # Special record
                    if dtime == 0:  # Not a marker, so overflow
                        gotOverflow(1)
                        oflcorrection += T3WRAPAROUND
                    else:
                        truensync = oflcorrection + nsync
                        bool = gotMarker(truensync, dtime, bool)
                else:
                    if channel == 0 or channel > 4:  # Should not occur
                        print("Illegal Channel: #%1d %1u" % (dlen, channel))
                        outputfile.write("\nIllegal channel ")
                    truensync = oflcorrection + nsync
                    gotPhoton(truensync, channel, dtime)
                    if bool:
                        CH1.append(dtime)
                        # print(bool, len(CH1))
                    else:
                        CH2.append(dtime)
                        # print(bool, len(CH2))
                    dlen += 1
                if recNum % 100000 == 0:
                    sys.stdout.write("\rProgress: %.1f%%" % (float(recNum) * 100 / float(numRecords)))
                    sys.stdout.flush()

        def readPT2():
            global inputfile, outputfile, recNum, oflcorrection, numRecords
            T2WRAPAROUND = 210698240
            for recNum in range(0, numRecords):
                try:
                    recordData = "{0:0{1}b}".format(struct.unpack("<I", inputfile.read(4))[0], 32)
                except:
                    print("The file ended earlier than expected, at record %d/%d." \
                          % (recNum, numRecords))
                    exit(0)

                channel = int(recordData[0:4], base=2)
                time = int(recordData[4:32], base=2)
                if channel == 0xF:  # Special record
                    # lower 4 bits of time are marker bits
                    markers = int(recordData[28:32], base=2)
                    if markers == 0:  # Not a marker, so overflow
                        gotOverflow(1)
                        oflcorrection += T2WRAPAROUND
                    else:
                        # Actually, the lower 4 bits for the time aren't valid because
                        # they belong to the marker. But the error caused by them is
                        # so small that we can just ignore it.
                        truetime = oflcorrection + time
                        gotMarker(truetime, markers)
                else:
                    if channel > 4:  # Should not occur
                        print("Illegal Channel: #%1d %1u" % (recNum, channel))
                        outputfile.write("\nIllegal channel ")
                    truetime = oflcorrection + time
                    gotPhoton(truetime, channel, time)
                if recNum % 100000 == 0:
                    sys.stdout.write("\rProgress: %.1f%%" % (float(recNum) * 100 / float(numRecords)))
                    sys.stdout.flush()

        oflcorrection = 0
        dlen = 0
        outputfile.write("\n-----------------------\n")
        recordType = tagValues[tagNames.index("TTResultFormat_TTTRRecType")]
        if recordType == self.rtPicoHarpT2:
            isT2 = True
            print("PicoHarp T2 data")
            outputfile.write("PicoHarp T2 data\n")
            outputfile.write("\nrecord# chan   nsync truetime/ps\n")
            readPT2()
        elif recordType == self.rtPicoHarpT3:
            isT2 = False
            print("PicoHarp T3 data")
            outputfile.write("PicoHarp T3 data\n")
            outputfile.write("\nrecord# chan   nsync truetime/ns dtime\n")
            readPT3()
            lists1 = sorted(Counter(CH1).items())
            lists2 = sorted(Counter(CH2).items())
            # print(lists, np.shape(lists))
            x1, y1 = zip(*lists1)
            x2, y2 = zip(*lists2)
            data = np.zeros((4096, 3))
            for i in range(4096):
                data[i][0] = i * Resolution
            for j in range(len(x1)):
                data[x1[j], 1] = y1[j]
            for k in range(len(x2)):
                data[x2[k], 2] = y2[k]
        else:
            print("ERROR: Unknown record type")
            exit(0)

        inputfile.close()
        outputfile.close()
        return data

if __name__ == "__main__":


    import matplotlib.pyplot as plt
    # sigma_plus = Counter(CH1)
    # sigma_minus = Counter(CH2)
    # print(sigma_plus)
    # def Table_maker(sigma_plus, sigma_minus):
    #
    #     lists1 = sorted(sigma_plus.items())
    #     lists2 = sorted(sigma_minus.items())
    #     # print(lists, np.shape(lists))
    #     x1, y1 = zip(*lists1)
    #     x2, y2 = zip(*lists2)
    #     plt.figure(1)
    #     plt.plot(x1, y1)
    #     data = np.zeros((4096, 3))
    #     Resolution = 256
    #     print(data)
    #     print(len(x1))
    #     print(len(x2))
    #     for i in range(4096):
    #         data[i][0] = i*Resolution
    #     for j in range(len(x1)):
    #         data[x1[j], 1] = y1[j]
    #     for k in range(len(x2)):
    #         data[x2[k], 2] = y2[k]
    #         # print(dape(data))
    #     return data
    PH = PH_PTU_to_data()
    inputFile=open("default_ptu_test.ptu", "rb")
    data_for_plot=PH.Process(inputFile, Resolution = 256)
    np.savetxt('Test_save data.txt', data_for_plot)
    plt.figure(2)
    plt.plot(data_for_plot[:, 0], data_for_plot[:, 1], data_for_plot[:, 0], data_for_plot[:, 2])
    # # plt.figure(2)
    # # plt.plot(sigma_plus)
    plt.show()