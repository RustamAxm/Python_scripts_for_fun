import numpy as np

Sum = 0

b = [[1, -1],
     [3, 1],
     [2, 2],
     [4, 1],
     [5, 1],
     [6, 2],
     [7, -1],
     [-1, -1],
     [-3, 1],
     [-2, 2],
     [-4, 1],
     [-5, 1],
     [-6, 2],
     [-7, -1]
]
#print(b)
b.sort(key=lambda x:x[0])
N = np.shape(b)[0]
print(b, N)
X = np.sum(b, axis=0)/N
#print(X[0])

for i in range(N):
    b[i][0] = b[i][0] - X[0]
    #print(b[i][0])

for i in range(int(N/2)):
    if (b[i][0] == - b[-1-i][0]) and (b[i][1] == b[-1-i][1]):
        Sum = Sum + 1
print(Sum, int(N/2))
if Sum == int(N/2):
    print("Symmetry on ", X[0])
else:
    print("Symmetry = None")

