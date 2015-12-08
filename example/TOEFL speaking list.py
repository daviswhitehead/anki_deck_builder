from __future__ import print_function
import os

os.remove('D:/speaking_list1.txt')
f=open('D:/speaking_list.txt')
g=open('D:/speaking_list1.txt','w+')

for line in f:
    y=list(line)
    print(line)
    for i in range(0,len(y)):
        if y[i].isdigit() and y[i+1]=='.':
            y[i]='\n'
            y[i+1]=''
            y[i+2]='\n'
            y[i-1]=''
        elif y[i]=='=' or y[i]=='
':y[i]=''
        #print(y[i],file=g)

    
    gline=''.join(y)
    print(gline,file=g)

g.close()
print('DONE')
