import numpy as np
import os
A = []
Shape = []
lamb_ex = []
Intensity1 = []
Intensity2 = []
error = []

for file in os.listdir(path="."):
    if file.endswith(".txt"):
        A.append(file)
print(len(A))
for i in range(0, len(A), 2):
    # print('{}'.format(A[i]))
    data1 = np.loadtxt('{}'.format(A[i]))
    data2 = np.loadtxt('{}'.format(A[i+1]))
    # print(np.shape(data1))
    # print(A[i].rsplit( ".", 1 )[ 0 ])
    POL = (data1[:, 3] - data2[:, 3]) / (data1[:, 3] + data2[:, 3] - np.min(data2[:, 3]) - np. min(data1[:, 3]))
    Data3 = np.column_stack((data1[:, 0], data1[:, 0] - float("".join(l for l in A[i].rsplit( ".", 1 )[ 0 ] if l in ".0123456789")), data1[:, 3]- np.min(data1[:, 3]), data2[:, 3] - np.min(data2[:, 3]), POL))
    print(np.shape(Data3))
    np.savetxt('POL_{}'.format(A[i]), Data3, header='wavelenght(nm) Delta(nm) I+ I- POL', comments='')
    for j in range(len(POL)):
        if Data3[j, 1] >= 1:
            Shape.append(POL[j])
            Intensity1.append(Data3[j, 3])
            Intensity2.append(Data3[j, 2])
            error.append(1/np.sqrt(Data3[j, 3] + Data3[j, 2]))
            break
    lamb_ex.append(float("".join(l for l in A[i].rsplit(".", 1)[0] if l in ".0123456789")))
print(lamb_ex, np.shape(Shape))
np.savetxt('POL_lambda', np.column_stack((lamb_ex, Shape, Intensity1, Intensity2, error)), header='EX_wavelenght(nm)  POL Intensity1 Intensity2 error', comments='')