#! python2

#carica da AutoriCollabOrdinatiNOMEpoiID.txt
#nome1 - id1, id2, id3
#nome2 - id4, id5, id6, id7
#traduci tutti gli edge "id2 id6" in "id1 id4"

def printType(obj):
  print obj, " - ", type(obj)
  
#cerca l'ID nei set del dizionario e restituisce il primo ID del set giusto
def trovaSostituto(id):
  for entry in dautori:
    #printType(dautori[entry])
    if id in dautori[entry]:
      print dautori[entry]

fautori = open("AutoriCollabOrdinatiNOMEpoiIDridotto.txt", "r")
#with open('AutoriCollabOrdinatiNOMEpoiID.txt', 'r') as fautori

dautori = {}

for line in fautori:
  pezzi = line.split("\t", 1)
  pezzi[1] = pezzi[1].rstrip()          #tolgo il \n
  if not dautori.has_key(pezzi[1]):
    dautori.update({pezzi[1]:set()})    #creo un set vuoto per la chiave pezzi[1]
  
  dautori[pezzi[1]].add(pezzi[0])       #aggiungo l'ID al set  
fautori.close()

print dautori

fedge = open("EdgeDEIPesatiRidotto.txt", "r")
fedgenuovi = open("EdgeDEIPesatiUnificati.txt", "w")

for line in fedge:
  pezzi = line.split("\t", 1)
  trovaSostituto(pezzi[0])
  
  