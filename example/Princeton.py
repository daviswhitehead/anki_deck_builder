# -*- coding: utf-8 -*-
from __future__ import print_function

f=open('Princeton_source.csv',encoding="utf8")
g=open('wordlist.txt','w+',encoding='utf8')

for line in f:
    word=line.split()[0]
    print(word,file=g)
    print(word)
    
    
g.close()
print('Done')