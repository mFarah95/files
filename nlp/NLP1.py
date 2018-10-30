import random
import codecs
import re

random.seed(123)


f = codecs.open("nlp/pg3300.txt", "r", "utf-8")
text = f.read().encode('utf-8')

t = re.split(r"\n\s*\n", text)
#lines = f.read().split("\r\n\r\n")
print(len(t))
print(t[6])
