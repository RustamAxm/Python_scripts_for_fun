import numpy as np
import glob, os
import matplotlib.pyplot as plt
a=[]
b=[]
def running_mean(x, y, N):
    for i in range(int(len(x)/N)-1):
     a.append(np.sum(x[N*i:N*(i+1)]))
     b.append(np.sum(y[N * i:N * (i + 1)]))
     time2 = [i * 0.29*N for i in range(len(a))]
    return  a, b

data = np.zeros(4087)
print(data)
for file in glob.glob("*.mp"):
    print(file)
    data = data + np.loadtxt(file, float, skiprows=37)

print(np.shape(data), max(data))
time1 = [i*0.29 for i in range(len(data))]

print(data[2103])
np.savetxt('data.txt',data,  fmt='%10.4f')

# pol = (data[:1958]-data[2104:])/(data[:1958]+data[2104:])
Array = np.column_stack((running_mean(data[:1959], data[2103:], 10)))


np.savetxt('Array.txt',Array,  fmt='%10.4f')
plt.plot(time1,data, 'o')
plt.show()