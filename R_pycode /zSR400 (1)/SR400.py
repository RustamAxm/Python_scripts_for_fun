from SerialClass import SerialClass
import numpy as np
import time
""" """

class SR400(SerialClass):
    """
        Usage:
            rs= sr400('COM11')
        """
    def __init__(self, com):
        super().__init__(com)

    def Counter_Reset_and_Start(self, T=1):
        self.query("CR;CS")
        time.sleep(T)

    def Counter_A_chanell(self, T=1,  D_level=-12e-3):
        """
        Тут просто считаем, что идет на канал А
        """
        print("Setting Counter A Setup....")
        self.query("CM 0")  # Setup mode A, B, T
        self.query("NP1")  # установили 1 период
        self.query("CP2,{}".format(T*1e7))  #установили время накопления 1 сек при внутреннем клоке 10МГц

        self.query("CI 0,1; GM 0,0; DS 0,1; DL 0, {} ".format(D_level))  # канал А input 1, GateMode = CW
        time.sleep(2)
        return print("Counter A Set")

    def Polarisation_setup(self, T=1, D_level = -12e-3):
        """
        Нужно помнить что это настройки для кварца 42кГц, если будет другой кварц,
        то нужно поменять параметры Gate для каждого канала
        """
        print("Setting Polarisation Setup....")
        self.query("CM 0")  # Setup mode A, B, T
        self.query("NP1")  # установили 1 период
        self.query("CP2,{}".format(T*1e7))  # установили время накопления 1 сек при внутреннем клоке 10МГц

        "for chanell A setup"
        self.query("CI 0,1; GD 0,0E-6; GM 0,1; GW 0,4E-6; DS 0,1; DL 0, {} ".format(D_level))  # канал А input 1, GateDelay for A = 0e-6 sec, GateMode = Fixed;
        # GateWidth A = 4E-6 sec

        "for chanell B setup"
        self.query("CI 1,1; GD 1,12E-6; GM 1,1; GW 1,4E-6; DS 1,1; DL 1, {}".format(D_level))  # канал B input 1, GateDelay for B = 12e-6 sec, GateMode = Fixed;
        # GateWidth B = 4E-6 sec

        time.sleep(2)
        return print("Polarisation Setup Set")


    def Data_Polarisation(self):
        A = int(self.query('QA'))
        B = int(self.query('QB'))
        if ((A or B) <= 0):
            print("ERROR: division by zero")
            return A, B
        else:
            POL = (A - B) / (A + B)
        return A, B, POL

    def Data_A_chanell(self):
        A = int(self.query('QA'))
        return A

    def TRPL_setup(self):
        print("Ой пока не написал")


if __name__ == '__main__':
    dev = SR400('COM11')
    T = 0.5 #Время измерения
    D_level = -12e-3 # уровень дискриминации в вольтах
    # dev.Counter_A_chanell(T, D_level)
    dev.Polarisation_setup(T, D_level) #Время измерения в сек, и уровень диксретизации в вольтах
    while True:
        dev.Counter_Reset_and_Start(T) #Врмемя паузы равное времени подсчета

        # print(dev.Data_A_chanell())
        print(dev.Data_Polarisation())