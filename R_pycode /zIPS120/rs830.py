from SerialClass import SerialClass
import numpy as np
import time
""" """

class rs830(SerialClass):
    """
        This class allows to use the IPS120 equipment. Contains the methods which allows to control one.
        Usage:
            rs= rs830('COM8')
        """
    def __init__(self, com):
        super().__init__(com)

    def __check_snap(self, param):
        """
            internal function used by method SNAP
            ensures that the SNAP-params are correct
        """
        if param not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11):
            raise Exception(
                    "SNAP: Parameters can only be 1(?X), 2(?Y), 3(?R), 4(??), 5(?Aux In 1), 6(?Aux In 2), 7(?Aux In 3), 8(?Aux In 4), 9(?Reference Frequency), 10(?CH1 display) or 11(?CH2 display)")

    def SNAP(self, Param1, Param2, Param3=None, Param4=None, Param5=None, Param6=None):
        """The SNAP? command records the values of either 2, 3, 4, 5 or 6 param-
        eters at a single instant. For example, SNAP? is a way to query values of
        X and Y (or R and ?) which are taken at the same time. This is important
        when the time constant is very short. Using the OUTP? or OUTR? com-
        mands will result in time delays, which may be greater than the time con-
        stant, between reading X and Y (or R and ?).
        The SNAP? command requires at least two parameters and at most six
        parameters. The parameters i, j, k, l, m, n select the parameters below.

        i,j,k,l,m,n     parameter
        1               X
        2               Y
        3               R
        4               ?
        5               Aux In 1
        6               Aux In 2
        7               Aux In 3
        8               Aux In 4
        9               Reference Frequency
        10              CH1 display
        11              CH2 display
        The requested values are returned in a single string with the values sep-
        arated by commas and in the order in which they were requested. For
        example, the SNAP?1,2,9,5 will return the values of X, Y, Freq and
        Aux In 1. These values will be returned in a single string such as
        "0.951359,0.0253297,1000.00,1.234".
        The first value is X, the second is Y, the third is f, and the fourth is
        Aux In 1.
        The values of X and Y are recorded at a single instant. The values of R
        and ? are also recorded at a single instant. Thus reading X,Y OR R,?
        yields a coherent snapshot of the output signal. If X,Y,R and ? are all
        read, then the values of X,Y are recorded approximately 10?s apart from
        R,?. Thus, the values of X and Y may not yield the exact values of R and
        ? from a single SNAP? query.
        The values of the Aux Inputs may have an uncertainty of up to 32?s. The
        frequency is computed only every other period or 40 ms, whichever is
        longer.

        The SNAP? command is a query only command. The SNAP? command
        is used to record various parameters simultaneously, not to transfer data
        quickly[1].
        """
        self.__check_snap(Param1)
        self.__check_snap(Param2)
        cmdstr = 'SNAP?' + ' ' + str(Param1) + ',' + str(Param2);
        if Param3 != None:
            self.__check_snap(Param3);
            cmdstr += ',' + str(Param3);
        if Param4 != None:
            self.__check_snap(Param4);
            cmdstr += ',' + str(Param4);
        if Param5 != None:
            self.__check_snap(Param5);
            cmdstr += ',' + str(Param5);
        if Param6 != None:
            self.__check_snap(Param6);
            cmdstr += ',' + str(Param6);
        return self.query(cmdstr)


if __name__ == "__main__":
    rs1 = rs830('COM8')
    rs2 = rs830('COM15')
   # data = []
    data = rs1.SNAP(1,  2, 3, 4, 9).rstrip().split(',')
    data1 = rs2.SNAP(1, 2, 3, 4, 9).rstrip().split(',')
    print(data)
    print(data1)


