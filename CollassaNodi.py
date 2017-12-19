#! python2

#carica da AutoriCollabOrdinatiNOMEpoiID.txt
#nome1 - id1, id2, id3
#nome2 - id4, id5, id6, id7
#traduci tutti gli edge "id2 id6" in "id1 id4"

def printType(obj):
  print obj, " - ", type(obj)
  
#cerca l'ID nei set del dizionario e restituisce il primo ID del set giusto
#deve sempre trovare l'ID nel dizionario
def trovaSostituto(id):
  for entry in dautori:
    #printType(dautori[entry])
    if id in dautori[entry]:
      #print dautori[entry]
      return dautori[entry][0]
  return "NOTFOUND!"

#fautori = open("AutoriCollabOrdinatiNOMEpoiIDridotto.txt", "r")
fautori = open("AutoriPadovaniOrdinatiNOMEpoiID.txt", "r")
#with open('AutoriCollabOrdinatiNOMEpoiID.txt', 'r') as fautori

dautori = {}

for line in fautori:
  pezzi = line.split("\t", 1)
  pezzi[1] = pezzi[1].rstrip()          #tolgo il \n
  if not dautori.has_key(pezzi[1]):
    dautori.update({pezzi[1]:[]})       #creo una lista vuota per la chiave pezzi[1]
  
  dautori[pezzi[1]].append(pezzi[0])    #aggiungo l'ID alla lista  
fautori.close()

print dautori

#fedge = open("EdgeDEIPesatiRidotto.txt", "r")
fedge = open("EdgePadovaniCompletiPesati.txt", "r")
fedgenuovi = open("EdgePadovaniCompletiPesatiUnificati.txt", "w")
dpesato = {}

for line in fedge:
  pezzi = line.split("\t")
  #riga = trovaSostituto(pezzi[0])+"\t"+trovaSostituto(pezzi[1])+"\t"+pezzi[2]
  #fedgenuovi.write(riga)
  
  id0 = trovaSostituto(pezzi[0])
  id1 = trovaSostituto(pezzi[1])
  
  if id0<id1:
    coppia = id0+"\t"+id1
  else:
    coppia = id1+"\t"+id0
  
  if not dpesato.has_key(coppia):
    dpesato.update({coppia:int(pezzi[2].rstrip())})
  else:
    dpesato[coppia]+=int(pezzi[2].rstrip())
    
print dpesato

for entry in dpesato:
  fedgenuovi.write(entry+"\t"+str(dpesato[entry])+"\n")
  
fedge.close()
fedgenuovi.close()