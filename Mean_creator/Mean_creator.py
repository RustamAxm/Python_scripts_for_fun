import numpy as np
import matplotlib.pyplot as plt
a=[]
N=10
def running_mean(x, N):
    for i in range(int(len(x)/N)-1):
     a.append(np.sum(x[N*i:N*(i+1)]))
    return a



data=np.loadtxt('For_prep.dat', float)[0:]
print(data)


result2 = running_mean(data, N)

print(result2 )
time=[]
for i in range(int(len(data)/N)-1):
  time.append(len(data)*0.290/len(result2)*i)
print(len(result2))
print(len(time))
np.savetxt('result.txt',np.column_stack((time[:len(result2)],result2)),  fmt='%10.4f')

# np.savetxt('result.txt',result2,  fmt='%10.4f')


plt.plot(time[:len(result2)],result2, 'o')
plt.show()