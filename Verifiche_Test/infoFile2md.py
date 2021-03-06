#! python2

import re
  
 
dir = r'C:\Users\Test\Documents\Tesi\authorship-network\Versione2'    #cartella in cui lavora
nome = "LegendaFile.info"
fullname = dir+"\\"+nome
finput = open(fullname, "r")
strInput = finput.readline()        #tolgo la prima riga di titolo
strInput = finput.read()

nome = "LegendaFile.md"
fullname = dir+"\\"+nome
foutput = open(fullname, "w")
foutput.write("# FILE\n")
foutput.write("Nome|#entry|Generato da|Struttura|Commento\n")
foutput.write("|-|-|-|-|-|\n")
foutput.write(re.sub("(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\n", r'|<p style="width:130px;"><sub>\1</sub></p> | <sub>\2</sub> | <p style="width:130px;"><sub>\3</sub></p> | <p style="width:80px;"><sub>\4</sub></p> | <sub>\5</sub>|\n', strInput))

finput.close()
foutput.close()

# #strelab = re.sub("", "", strInput)    #tolgo il titolo
# for line in finput:
  # #linelab = re.sub("(<.*?>)\t(<.*?>)\t(<.*?>)\t(<.*?>)\t(<.*?>)\n", "\1aa\2bb\3cc\4dd\5", line)
  # linelab = re.sub("(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\n", r'|<p style="width:130px;">\1</p> | \2 | <p style="width:130px;">\3</p> | <p style="width:80px;">\4</p> | \5|\n', line)
  # foutput.write(linelab)
  # #serched = re.search("(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\n", line)
  # #print line,"==>",linelab
  # #if serched: print serched.groups()
  # #else: print 'nomatch'


### FORMATO ### 
#|Nome|num entry|generato da|struttura|commento
#PersoneDEIOLD.txt	353	manualmente	nomi	nomi di afferenti DEI dal sito di dipartimento


#|Titolo|CollassaNodiAmpi.py|
#|-|-|
#|Input|EdgeCollabPesatiAmpi.txt (1)<br/>EdgePadovaniCompletiPesatiAmpi.txt (2)|
#|Database|PersoneDEI.txt<br/>AutoriCollabAmpiOrdinatiNOMEpoiID.txt (1)<br/>AutoriPadovaniAmpiOrdinatiNOMEpoiID.txt (2)|
#|Output|EdgeCollabPesatiAmpiUnificatiBis.txt (1)<br/>EdgePadovaniCompletiPesatiAmpiUnificatiBis.txt (2)|
#|Descrizione|collassa i nodi risalendo anche da abbreviazione a nome completo|
#|Commento|ci sono IDaut associati ad omonimi che non sono persone DEI; ci sono IDaut multipli relativi alla stessa persona (nome) DEI<br/>considerando le iniziali il numero di omonimi in sale vistosamente (8379 contro 2135) (il falso positivo prima era solo mario rossi, ora sono tutti gli m rossi, dove m corrisponde a mario ma anche michele, mirko, massimiliana, marina...) (da PersoneDEI ad AutoriDEI x6; da PersoneDEIampie a AutoriDEIampi x11)|


#<br/>		a capo
#<li>item1</li><li>item2</li>		lista
#<p>nota</p>	paragrafo -> aggiunge padding

#|Titolo|CollassaNodiAmpi.py|
#|-|-|
#|Input|asdasd|
#|Output|<li>EdgeDEIPesatiUnificati.txt</li><li>EdgePadovaniCompletiPesatiUnificati.txt</li>|
#|Output|EdgeDEIPesatiUnificati.txt<br/>EdgeDEIPesatiUnificati.txt (1)<br/>EdgePadovaniCompletiPesatiUnificati.txt(2)|
#|Output|EdgeDEIPesatiUnificati.txt<br/>1) EdgeDEIPesatiUnificati.txt<br/>2) EdgePadovaniCompletiPesatiUnificati.txt|
