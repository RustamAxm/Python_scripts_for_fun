from SerialClass import SerialClass
from UT804 import UT804

Hall = UT804()
Data = SerialClass('COM8')
Magnet = SerialClass('COM9')

start_field = 0
end_field = 1
step_field = 0.05
current_field = start_field
while current_field < end_field:
    current_field += step_field
    data = [
        '{:0.4f}'.format(current_field),
        Hall.read()[0],
        Data.query('OUTP?1').replace('\n', ''),
        Data.query('OUTP?2').replace('\n', ''),
        Data.query('OUTP?3').replace('\n', ''),
        Data.query('OUTP?4').replace('\n', '')
    ]
    with open('s.txt', 'a+') as file:
        file.write('\t'.join(data) + '\n')






