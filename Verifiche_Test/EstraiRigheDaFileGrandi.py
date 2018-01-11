#! python2

import re
 
dir = r'C:\Users\Test\Documents\Tesi\FileRAW'    #cartella in cui lavora
dir = 'C:\Users\Pietro\Documents\University\Tesi\FileRAW\\'
nome = 'Affiliations'
# nome = 'Authors'
fullname = dir+'\\'+nome+'.txt'
# fullname = 'PaperAuthorAffiliations288.txt'
finput = open(fullname, 'rb')


firstline = 0
lastline  = 1000
buflength = 0

if firstline <> 0:
  nome = nome+'DA'+str(firstline)+'A'+str(lastline)+'.txt'
else:
  nome = nome+str(lastline)+'.txt'
  
#nome = 'OUTTPUTT.txt'
fullname = nome
fullname = dir+'\\'+nome#+'.txt'
foutput = open(fullname, 'wb')


i = 0
soutput = ''
for line in finput:
  i+=1
  if i%1000000 == 0: print i
  if i>firstline and i<=lastline:
    soutput += line
    buflength +=1
  if buflength == 10000:
    foutput.write(soutput)
    buflength = 0
    soutput = ''
    print 'scrivo 10k'
  if i>lastline:
    print 'BREAK'
    break
  # print line.rstrip()
  # foutput.write(line)
  # pezzi = line.split('\t')
  # print 'len: {} pezzi: {}'.format(len(pezzi), pezzi)
    
foutput.write(soutput)
print 'DONE'
finput.close()
foutput.close()
