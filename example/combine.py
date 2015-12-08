#Feel free to use this script as you want.
#But I'm curious of what you intend to do. I just want to know how useful this script is.

from __future__ import print_function
import re

deflist=open('D:/Python/def list.txt',encoding='utf-8-sig')

#synlist=open('D:/Python/synonyms list.txt')

ipalist=open('D:/Python/ipa list.txt',encoding='utf-8-sig')

out=open('D:/Python/combine.txt','w+',encoding='utf-8-sig')


with open(r"D:/Python/anhviet109K.dict",encoding="utf-8-sig") as f:
    vdic=f.readlines()
    
def startwith(line,word): #startswith() is readability, but slow for simple actions
    return line[:len(word)] == word
    


def vietnamese(word):
    block=[]
    i=0    
    for line in vdic:
        if startwith(line,'@'+word): 
            line=line[1:].strip('\n')+'<br>'
            line=line.replace(line.split()[0],'<b>'+line.split()[0]+'</b>')
            block.append(line)
            
            j=1
            while '@' not in vdic[i+j]:
                line_after_word=vdic[i+j].strip('\n')
                if startwith(line_after_word,'*'): line_after_word='<small><i>'+line_after_word[1:].strip()+'</i></small>'        
                elif startwith(line_after_word,'='): line_after_word='<ul><ul><li>'+line_after_word[1:].strip().replace('+ ','<br>')+'</li></ul></ul>'
                elif startwith(line_after_word,'!'): line_after_word='<ul>IDIOM<li>'+line_after_word[1:]+'</li></ul>'
                elif startwith(line_after_word,'!') and 'IDIOM' in vdic[i-2]: line_after_word='<ul><li>'+line_after_word[1:]+'</li></ul>'
                
                elif startwith(line_after_word,'-'):
                    if startwith(vdic[i+j-1],'!'): 
                        line_after_word='<ul><ul>'+line_after_word[1:].strip()+'</ul></ul>'
                    elif startwith(vdic[i+j-1],'*') or startwith(vdic[i+j-1],'@') or startwith(vdic[i+j-1],'-') or startwith(vdic[i+j-1],'/') or startwith(vdic[i+j-1],'='):
                        line_after_word='<ul><li>'+line_after_word[1:].strip()+'</li></ul>'                        
                
                    else: line_after_word='MISS A LINE'
                print(i,j,line_after_word)
                
                block.append(line_after_word)
                j+=1
        
            print(word.upper(),''.join(block).strip('\n'))
        i+=1
    return ''.join(block).strip('\n')

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)
    
def replace_all(line):
    dic={"; noun ":" <br><i><small>noun </small></i><br>",
         "; verb ":" <br><i><small>verb </small></i><br>",
         "; adj. ":" <br><i><small>adj. </small></i><br>"}
    for i,j in dic.items(): line = line.replace(i,j)
        
    dic={" noun ":" <i><small>noun</small></i><br> ",
         " verb ":" <i><small>verb</small></i><br> ",
         " adj. ":" <i><small>adj.</small></i><br> "}
    for i,j in dic.items(): line = line.replace(i,j)    


    return ''.join(line).strip('\n')

for line in deflist:
    defline=replace_all(line)
    word=defline.split()[0]
    defi=defline.split(" ",2)[2].strip() 
    link='http://dictionary.reference.com/browse/'+word
    image='<img src="'+word+'.jpg"/>'
    image_link='http://www.google.com/images?q='+word
    
    ipaline=ipalist.readline() 
    ipa='/'+re.findall(r'(?<=\/).*?(?=\/)',ipaline)[0]+'/'
    sound='['+re.findall(r'(?<=\[).*?(?=\])',ipaline.split()[1])[0]+']'
    
    barron=open("Barrons word list.tsv",encoding="utf-8-sig") 
    for lineb in barron:
        if startwith(lineb,word):
            describe=' '.join(lineb.split()[1:]).strip('\n');break
        else: describe=''
            
#    syn=" ".join(synlist.readline().split()[2:])
    
    vietword=vietnamese(word)
#    print(word.upper(),defi,describe)
#    print(word.upper(),defi,sep='\t',file=out)
    print(word,ipa,defi,describe,link,image_link,image,sound,vietword,file=out,sep='\t')



out.close()
print('\nDONE')
