import visa#подключаем библиотеку visa
import time
rm = visa.ResourceManager()
rg1 = rm.list_resources()#запрос кортежа подключенных портов
print(rg1)
Multik = rm.open_resource("USB0::0x2A8D::0x1401::MY60000506::INSTR")

print(Multik.query("*IDN?"))

# rm = visa.ResourceManager()
# name = rm.list_resources()
# print(name)
#
# with rm.open_resource("USB0::0x2A8D::0x1401::MY60000506::INSTR") as Multik:
#     print(Multik.query('*IDN?'))
#     print(Multik)
sum=0
i = 0
for k in range(100):
    sum += float(Multik.query("READ?"))
    i += 1
    # print(sum, i)
    if i==100:
        print("напряжение 10 отчетов = ", sum/i)
        i = 0
        sum = 0
Multik.close()

