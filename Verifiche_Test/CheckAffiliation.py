#! python2

import re

##affiliation conosciute
dir = r'C:\Users\Test\Documents\Tesi\authorship-network'
nome = 'PadovaPadua.txt'
fullname = dir+'\\'+nome
fpadua = open(fullname)
spadua = set()
for line in fpadua:
  pezzi = line.split('\t')
  spadua.add(pezzi[0])
#print spadua
print 'len spadua ' + str(len(spadua))
fpadua.close()
 
##affiliation nuove
dir = r'C:\Users\Test\Documents\Tesi\authorship-network\Verifiche_Test' 
nome = 'PaperAAPadova.txt'
fullname = dir+'\\'+nome
faffiliation = open(fullname, 'r')

nome = 'PaperAffNonNota.txt'
fullname = dir+'\\'+nome
fnonnoti = open(fullname, 'w')
snonnote = set()
saffiliation = set()
for line in faffiliation:
  pezzi = line.split('\t')
  if pezzi[2] not in spadua:
    fnonnoti.write(line)
    snonnote.add(pezzi[2])
  saffiliation.add(pezzi[2])
#print saffiliation
print 'len saffiliation ' + str(len(saffiliation))
print 'len snonnote ' + str(len(snonnote))

fnonnoti.close()
faffiliation.close()

# len spadua 8285
# len saffiliation 3661
# len snonnote 481

##file gigante
dir = r'C:\Users\Test\Documents\Tesi\FileRAW' 
#dir = r'C:\Users\Test\Documents\Tesi\authorship-network\Verifiche_Test' 
nome = 'Affiliations.txt'
#nome = 'AffiliationsDA0A1000.txt'
fullname = dir+'\\'+nome
ftutte = open(fullname, 'r')

dir = r'C:\Users\Test\Documents\Tesi\authorship-network\Verifiche_Test' 
nome = 'AffiliationNonNote.txt'
fullname = dir+'\\'+nome
fnuove = open(fullname, 'w')

##cerco i nomi nel file
for line in ftutte:
  pezzi = line.split('\t')
  if pezzi[0] in snonnote:
    fnuove.write(line)
    print line.rstrip()
  
ftutte.close()
fnuove.close()