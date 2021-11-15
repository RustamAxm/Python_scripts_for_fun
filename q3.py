import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import re

Tk().withdraw()
names = askopenfilenames()
k = 0
data_x = np.linspace(730.15, 765.72, 1340)
for name in names:
    loaded = np.loadtxt(name)
    loaded[:, 0] = data_x
    np.savetxt(name, loaded)

