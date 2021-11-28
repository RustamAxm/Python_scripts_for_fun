str1 = str(input())
key1 = str(input())
str2 = str(input())
key2 = str(input())

dic = dict()
output_1 = str()
output_2 = str()

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

for i in range(len(str1)):
    dic[str1[i]] = key1[i]

for x in str2:
    output_1 += dic.get(x)

for v in key2:
    output_2 += get_key(dic, v)

print(output_1)
print(output_2)


