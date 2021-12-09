from urllib.request import urlopen
import re
import collections
s = str(urlopen('https://stepik.org/media/attachments/lesson/209719/2.html').read().decode('utf-8'))

reg = '<code>(.*?)</code>'
l = sorted(re.findall(reg, s))
d = collections.Counter(l)
print(d)
