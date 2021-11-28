from urllib.request import urlopen
s = str(urlopen('https://stepik.org/media/attachments/lesson/209717/1.html').read().decode('utf-8'))
print(s.count('C++'))
print(s.count('Python'))
