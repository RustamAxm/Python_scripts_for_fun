import numpy as np
import glob, os
import matplotlib.pyplot as plt

for file in glob.glob("*.mp"):
    print(file)
    data = np.loadtxt(file, float)