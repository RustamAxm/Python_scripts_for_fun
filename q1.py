from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import numpy as np
import re
from matplotlib.pyplot import plot, show
Tk().withdraw()
names = askopenfilenames()
data_y = np.zeros((len(names), 2))
colormap = np.zeros((1341, len(names)+1))
k = 0
for name in names:
    match = re.findall('pol_[\-]*[0-9].[0-9]*', name)
    print(np.round(float(match[0][4:]), 1))
    data = np.loadtxt(name)
    # data_y[k, 0] = np.round(float(match[0][4:]), 1)
    # data_y[k, 1] = data[130, 1]
    colormap[1:, k+1] = data[:, 1]
    colormap[0, k+1] = np.round(float(match[0][4:]), 1)
    if k == 0:
        colormap[1:, 0] = data[:, 0]
    k += 1
plot(data_y[:, 0], data_y[:, 1], 'ro')
# np.savetxt(r'D:\Experiment and Data Processing\QD CdSe_ZnSe with Mn. 1886, 1-672\1886, CdSe_ZnMnSe QDs\2019-04-11, Faraday, circ exc, circ reg\reg528.93nm_pol(B)1.6K.txt', data_y)
np.savetxt(r'D:\Experiment and Data Processing\QD CdSe_ZnSe with Mn\1321, 1431, 1432\2019-04-15 lin exc, lin reg (glan+l4)\1431\Faraday_colormap_1.6K.txt', colormap)
show()

