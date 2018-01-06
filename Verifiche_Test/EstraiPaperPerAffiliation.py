#! python2

#con "pad(ov|u)a" -> sipad:77177 nopad:24118491 noaff:264069014 @@ 269s
#se c'e' padovua nel record PapAutAff (nel nome aff) copia il paper

import re
from timeit import default_timer as timer
start1 = timer()

  
dir = r'C:\Users\Test\Documents\Tesi\FileRAW'    #cartella in cui lavora
dir = r'C:\Users\Test\Documents\Linguaggi\Prove\proveFileMulti'    #cartella in cui lavora
nome = "PaperAuthorAffiliations5000000.txt"
nome = "PaperAuthorAffiliationConLineaCheNonIdentifica.txt"
nome = "PaperAuthorAffiliations.txt"
fullname = dir+"\\"+nome
finput = open(fullname, "r")

nome = "PaperAAPadovaBis.txt"
nome = "C:\Users\Test\Documents\Linguaggi\Prove\proveFileMulti\PaperAAPadovaFullBinary.txt"
fullname = nome
foutput = open(fullname, "w")

noaff,nopad,sipad,i = 0,0,0,0
soutput = ""
try:
  for line in finput:
    i+=1
    if i%1000000 == 0: print i
    pezzi = line.split("\t")
    if pezzi[2] == "":  #IDaff
      noaff += 1
    else:               #pezzi 34 sono nomi
      nomeaff = ""
      if len(pezzi)>=4:
        nomeaff += pezzi[3]
      if len(pezzi)>=5:
        nomeaff += pezzi[4]
      match = re.search("pad(ov|u)a", nomeaff, re.I)
      if match:
        #print line.rstrip()
        soutput += line
        sipad += 1
      else:
        nopad += 1
except:
  print "Bloccato alla riga {} che contiene {}".format(i, line)
  #Bloccato alla riga 288264682 che contiene 078534A9	391CF352	016D6331	Faculty of Engineering, University of Tehran, Tehran, Iran#TAB#TAB#
  #aveva AFF ma non pezzi[4]

  
print "sipad:{} nopad:{} noaff:{}".format(sipad, nopad, noaff)
#con "pad(ov|u)a" -> sipad:77177 nopad:24118491 noaff:264069014
foutput.write(soutput)


finput.close()
foutput.close()

end1 = timer()
print 'tempo: {}'.format(end1-start1)