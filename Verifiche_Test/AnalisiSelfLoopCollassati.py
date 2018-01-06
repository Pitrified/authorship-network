#! python2

def ptype(obj):
  print obj, " - ", type(obj)
  
#cerca l'ID nelle liste del dizionario e restituisce il primo ID della lista giusta
#deve sempre trovare l'ID nel dizionario
def trovaSostituto(id):
  #print "cerco: " + id
  for entry in dautori:
    #printType(dautori[entry])
    if id in dautori[entry]:
      #print dautori[entry]
      return dautori[entry][0]
  return "IDNOTFOUND!"
  
#cerca l'abbreviato nei set del dizionario e restituisce l'entry del set in cui lo trovi
#deve sempre trovare il nome
def trovaNome(abbreviato):
  for entry in dpersone:
    #printType(dpersone[entry])
    if abbreviato == entry:         #abbreviato era gia' il nome esteso
      return entry
    if abbreviato in dpersone[entry]:
      #print dpersone[entry]
      return entry
  return "NAMENOTFOUND!"
  
import re
from timeit import default_timer as timer
 
start = timer()
CARTELLA = r'C:\Users\Test\Documents\Tesi\authorship-network\Versione2\\'    #cartella in cui lavora

##carico dizionario persone con abbreviazioni
dpersone = {} #{nome secondo cognome:set(n s cognome, ...)}
fpersone = open(CARTELLA+"PersoneDEI.txt")
for line in fpersone:
  line = line.rstrip()
  dpersone.update({line:set()})
  pz = line.split()
  #print(pz, " ", len(pz))
  if len(pz)==2:
    dpersone[line].add(pz[0][0]+" "+pz[1])
  elif len(pz)==3:
    dpersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2])
    dpersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2])
    dpersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2])
  elif len(pz)==4:
    dpersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
    dpersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
    dpersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
    dpersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
    dpersone[line].add(pz[0]   +" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
    dpersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
    dpersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2]   +" "+pz[3])
  elif len(pz)==6:
    dpersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3][0]+" "+pz[4][0]+" "+pz[5])
  

##Carico il dizionario dei paper
dpaa = {} #carico il dizionario {IDpaper: [ [IDa1,IDa2,IDa4,IDa3] , [line1, line2, line4, line3] ] }
#fpaa = open(CARTELLA+"PapAutAffDEIampi.txt")
#fpaa = open(CARTELLA+"PapAutAffDEIampiCollisioniCollab.txt")
fpaa = open(CARTELLA+"PapAutAffDEIampiCollisioniCollabCollassati.txt")
#fpaa = open(CARTELLA+"PaperPadovaniCompletiAmpi.txt")
for line in fpaa:
  pezzi = line.split("\t")
  if not dpaa.has_key(pezzi[0]): dpaa.update({pezzi[0]:[[],[]]})     #se non c'e' la chiave creo lista di due liste vuote
  dpaa[pezzi[0]][0].append(pezzi[1])        #nella prima lista gli IDautori
  dpaa[pezzi[0]][1].append(line)            #nella seconda lista tutte le linee
  #ptype(dpaa[pezzi[0]])
fpaa.close()
#$#print dpaa

##carico i dizionari degli autori
dautori = {}  #{nome:[IDaut,IDaut,...,IDaut]}
dIDautori = {}  #{IDaut:nome}
fautori = open(CARTELLA+"AutoriCollabAmpi.txt", "r")
#fautori = open(CARTELLA+"AutoriDEIampi.txt", "r")
for line in fautori:
  pezzi = line.split("\t", 1)
  pezzi[1] = pezzi[1].rstrip()      #tolgo il \n
  nome = trovaNome(pezzi[1])        #trovo il nome completo
  if not dautori.has_key(nome):
    dautori.update({nome:[]})       #creo una lista vuota per la chiave nome, NOME
  #print "Nome:",nome,"Pezzi[1]",pezzi[1]
  if nome == pezzi[1]:              #il nome era gia' completo
    dautori[nome].insert(0, pezzi[0])   #inserisco il nome all'inizo della lista
    #print "Metto in cima lalala"
  else:                             #era un nome abbreviato
    dautori[nome].append(pezzi[0])  #aggiungo l'IDaut (relativo ad un abbreviazione) alla fine della lista
  dIDautori.update({pezzi[0]:pezzi[1]})
fautori.close()
#print dautori
#print dIDautori

##dpersone   = {} #{nome secondo cognome:set(n s cognome, ...)}
##dautori    = {} #{nome completo:[IDaut,IDaut,...,IDaut]} (se presente nel file autori caricato)
##dIDautori  = {} #{IDaut:nome}   (nome anche abbreviato)
##dpaa       = {} #{IDpaper:[ [IDa1,IDa2,IDa4,IDa3] , [line1,line2,line4,line3] ]}
##dtp        = {} #{IDpaper:titolo}
##lpaperloop = [] #ID paper che hanno collisioni negli ID autori (SENZA contare le abbreviazioni o niente)

##controllo duplicati nei IDaut dei paper considerando gli ID collassati
lpaperloopcollassati = [] #ID paper che hanno collisioni negli ID autori (CONTANDO le abbreviazioni)
#sono proprio ID identici elencati come autori dello stesso paper
for entry in dpaa:
  lIDcollassati = []
  for id in dpaa[entry][0]:
    lIDcollassati.append(trovaSostituto(id))
  if len(lIDcollassati) <> len(set(lIDcollassati)):
    lpaperloopcollassati.append(entry)
lpaperloopcollassati.sort()
print str(len(lpaperloopcollassati))

##carico i titoli (da quelli filtrati se li ho gia')
dtp = {} #dizionario titoli paper {IDpaper:titolo}
#ftp = open(CARTELLA+"PapersDEITitoliAmpi.txt")
ftp = open(CARTELLA+"PapersDEITitoliAmpiCollisioniCollabCollassati.txt")
for line in ftp:
  pezzi = line.split("\t", 1)
  if pezzi[0] in lpaperloopcollassati:
    dtp.update({pezzi[0]:pezzi[1]})
ftp.close()

##filtro PapAutAffDEIampi secondo lpaperloopcollassati
# ftemp3 = open(CARTELLA+"PapAutAffDEIampiCollisioniCollabCollassati.txt", "w")
# ftemp4 = open(CARTELLA+"PapersDEITitoliAmpiCollisioniCollabCollassati.txt", "w")
# paacloop = ""
# tpcloop  = ""
# for entry in lpaperloopcollassati:
  # print entry, dtp[entry]
  # tpcloop += entry + "\t" + dtp[entry]
  # for line in dpaa[entry][1]:
   # paacloop += line
# ftemp3.write(paacloop)
# ftemp3.close()
# ftemp4.write(tpcloop)
# ftemp4.close()


##scrivo il file di descrizioni
i=0
fpaperloopcollassati = open(CARTELLA+"PaperAADALoopCollassatiBis.txt", "w")
dacollassati = {} #{IDcollassato:nome}  
for entry in lpaperloopcollassati:
  i+=1
  stringa = "##########\npaper {:3d} con ID aut duplicati nella lista [0]: ".format(i)+entry
  stringa += "\tlistaAutori: "+str(dpaa[entry][0])
  pezzidtp = dtp[entry].split("\t")
  stringa += "\nTitolo:"+pezzidtp[0]+"\tYear:"+pezzidtp[2]+"\tVenue Name:"+pezzidtp[5]+"\n"
  stringa += "listaLine:\n"
  for line in dpaa[entry][1]:
    stringa += line
  stringa += "Autori:\n"
  idcollassato = trovaSostituto(id)
  for id in dpaa[entry][0]:
    stringa += "ID:\t"+id+"\tNome:"+dIDautori[id]+"\tIDcollassato:"+idcollassato+"\tNomeColl:"+dIDautori[idcollassato]+"\n"
  fpaperloopcollassati.write(stringa)
  dacollassati.update({idcollassato:dIDautori[idcollassato]})
fpaperloopcollassati.close()


facollassati =  open(CARTELLA+"AutoriLoopCollassati.txt", "w")
for entry in dacollassati:
  facollassati.write(entry+"\t"+dacollassati[entry]+"\n")
facollassati.close()
end = timer()
print (end-start)

