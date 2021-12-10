from SerialClass import SerialClass
import time
import re

class Spectrometer:
    program_offset = [0.00, 0.0, 0.0]

    def __init__(self):
        with open('C:\D\PyTest\R_pycode\zSpectrometer\cfg.txt', 'r') as file:
            self.stage1_offset, self.stage2_offset, self.stage3_offset = \
                [float(x.split(sep='=')[1]) for x in file.readlines()]
        self.stage1_offset += self.program_offset[0]
        self.stage2_offset += self.program_offset[1]
        self.stage3_offset += self.program_offset[2]
        self.stage1 = SerialClass('COM5')
        self.stage2 = SerialClass('COM6')
        self.stage3 = SerialClass('COM7')

    def get_serial_model(self):
        self.serial_no_1 = self.stage1.query('SERIAL')
        self.model_no_1 = self.stage1.query('MODEL')
        return self.serial_no_1, self.model_no_1

    def get_nm(self):
        self.curr_nm1 = self.stage1.query('?NM')
        self.curr_nm2 = self.stage2.query('?NM')
        self.curr_nm3 = self.stage3.query('?NM')
        return self.curr_nm1, self.curr_nm2, self.curr_nm3

    def get_nm_per_min(self):
        self.curr_nm_min1 = self.stage1.query('?NM/MIN')
        self.curr_nm_min2 = self.stage2.query('?NM/MIN')
        return self.curr_nm_min1, self.curr_nm_min2

    def goto_nm_max_speed_STAGE_1(self, position):
        goto_stage1 = position + self.stage1_offset
        self.stage1.query('%0.3f GOTO' % goto_stage1)

    def goto_nm_max_speed_STAGE_2(self, position):
        goto_stage2 = position + self.stage2_offset
        self.stage2.query('%0.3f GOTO' % goto_stage2)

    def goto_nm_with_set_nm_per_min_STAGE_1(self, nm, nm_per_min=100):
        goto_stage1 = nm + self.stage1_offset #+ 0.32 - 0.0112*(nm - 585.25)
        self.stage1.query('%0.2f NM/MIN' % nm_per_min)
        # print('Set nm/min = %0.1f' % nm_per_min)
        self.stage1.query('%0.2f >NM' % goto_stage1)

        char1 = 0
        while char1 != 1:
            string1 = self.stage1.query('MONO-?DONE')

            char1 = float("".join(i for i in string1 if i in "0123456789"))

            print(self.get_nm())
            time.sleep(0.2)
        self.stage1.query('MONO-STOP')
        print("Scan done?: " + 'yes' if (char1 == 1) else 'No')
        return self.get_nm()

    def goto_nm_with_set_nm_per_min_STAGE_2(self, nm, nm_per_min=100):
        goto_stage2 = nm + self.stage2_offset #+ 0.32 - 0.0112*(nm - 585.25)
        self.stage2.query('%0.2f NM/MIN' % nm_per_min)
        # print('Set nm/min = %0.1f' % nm_per_min)
        self.stage2.query('%0.2f >NM' % goto_stage2)

        char2 = 0
        while char2 != 1:
            string2 = self.stage2.query('MONO-?DONE')

            char2 = float("".join(i for i in string2 if i in "0123456789"))

            print(self.get_nm())
            time.sleep(0.2)
        self.stage2.query('MONO-STOP')
        print("Scan done?: " + 'yes' if (char2 == 1) else 'No')
        return self.get_nm()

    def goto_nm_with_set_nm_per_min_SUBTRUCTIVE(self, nm, nm_per_min=100):
        goto_stage1 = nm + self.stage1_offset
        goto_stage2 = -nm - self.stage2_offset
        self.stage1.query('%0.2f NM/MIN' % nm_per_min)
        self.stage2.query('%0.2f NM/MIN' % nm_per_min)
        # print('Set nm/min = %0.1f' % nm_per_min)
        self.stage1.query('%0.2f >NM' % goto_stage1)
        self.stage2.query('%0.2f >NM' % goto_stage2)

        char1 = 0
        char2 = 0
        while (char1 != 1 or char2 != 1):
            string1 = self.stage1.query('MONO-?DONE')
            string2 = self.stage2.query('MONO-?DONE')

            char1 = float("".join(i for i in string1 if i in "0123456789"))
            char2 = float("".join(i for i in string2 if i in "0123456789"))

            print(self.get_nm())
            time.sleep(0.2)
        self.stage1.query('MONO-STOP')
        self.stage2.query('MONO-STOP')
        time.sleep(2)
        print("Scan done?: " + 'yes' if (char1 == 1 and char2 == 1) else 'No')
        return self.get_nm()

    def goto_nm_with_set_nm_per_min_ADDITIVE(self, nm, nm_per_min=100):
        goto_stage1 = nm + self.stage1_offset
        goto_stage2 = nm + self.stage2_offset
        self.stage1.query('%0.2f NM/MIN' % nm_per_min)
        self.stage2.query('%0.2f NM/MIN' % nm_per_min)
        # print('Set nm/min = %0.1f' % nm_per_min)
        self.stage1.query('%0.2f >NM' % goto_stage1)
        self.stage2.query('%0.2f >NM' % goto_stage2)

        char1 = 0
        char2 = 0
        while (char1 != 1 or char2 != 1):
            string1 = self.stage1.query('MONO-?DONE')
            string2 = self.stage2.query('MONO-?DONE')

            char1 = float("".join(i for i in string1 if i in "0123456789"))
            char2 = float("".join(i for i in string2 if i in "0123456789"))

            print(self.get_nm())
            time.sleep(0.2)
        self.stage1.query('MONO-STOP')
        self.stage2.query('MONO-STOP')
        # time.sleep(2)
        print("Scan done?: " + 'yes' if (char1 == 1 and char2 == 1) else 'No')
        return self.get_nm()

    def SET_ENT_SLIT(self, microns):
        print(self.stage1.query('side-ent-slit %i microns' % microns))
        time.sleep(10)
        return self.stage1.query('side-ent-slit ?microns')

    def SET_EXIT_SLIT(self, microns):
        print(self.stage1.query('front-exit-slit %i microns' % microns))
        time.sleep(10)
        return self.stage1.query('front-exit-slit ?microns')


    def stop(self):
        self.stage1.query('MONO-STOP')


if __name__ == '__main__':

    import numpy as np
    dev = Spectrometer()
    Time = time.time()
    print(dev.get_serial_model())
    print(dev.get_nm())
    print(dev.get_nm_per_min())
    # string = dev.stage1.query('MONO-STOP')

    for i in range(1):
        print(dev.goto_nm_with_set_nm_per_min_SUBTRUCTIVE(690, 1000))
    # dev.goto_nm_max_speed_STAGE_2(-831)*


    # field = np.hstack((np.linspace(-6, -3, 6, endpoint=False), np.linspace(-3, 3, 30,endpoint=False),np.linspace(3, 6, 7)))
    # print(field, np.shape(field))

        # print(dev.stage2.query('MONO-?DONE'))

    print((time.time() - Time) / 60, "min")
    # print(dev.SET_ENT_SLIT(50))
    # print(dev.SET_EXIT_SLIT(50))







# for i in range(len(Wavelenght)):
    #
    #     dev.goto(Wavelenght[i])
    #     time.sleep(0.1)
    #     string = dev.stage1.query('?NM')
    #     print(float(re.sub(r'[^0-9.]+', r'', string)) - dev.stage1_offset)
    #     time.sleep(1)

    # print(dev.stage2.query('?NM'))
    # print(dev.stage3.query('?NM'))
    #print(dev.stage2.query('side-ent-slit 500 microns'))
    #print(dev.stage3.query('exit-mirror side'))
    #print(dev.stage2.query('side-ent-slit ?microns'))