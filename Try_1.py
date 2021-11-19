# f = open("input.txt", "r")
# for line in f:
#     a, b = line.split()
# f_out = open("output.txt", "w")
# f_out.write(str(int(a) + int(b)))

# j = input().strip()
# s = input().strip()
#
# result = 0
#
# for i in s:
#     print(i)
#     if i in j:
#         result += 1
#
# print(result)

import numpy as np

N = int(input())
k = int(input())
a=[]
summ=[]
for i in range(N):
    a.append(float(input()))

for i in range(len(a)-k+1):
    summ.append(sum(a[i:i+k]))
max = summ[0]
max_index = 0
for i in range(len(summ)):
    if summ[i]>max:
        max_index=i

resh = sum(a[:max_index]) + sum(a[max_index+k:])
print(resh)