#! python2

#carica da AutoriCollabOrdinatiNOMEpoiID.txt
#nome1 - id1, id2, id3
#nome2 - id4, id5, id6, id7
#traduci tutti gli edge "id2 id6" in "id1 id4"

def printType(obj):
  print obj, " di tipo ", type(obj)

fautori = open("AutoriCollabOrdinatiNOMEpoiID.txt", "r")

dautori = {}

for line in fautori:
  pezzi = line.split("\t", 1)
  
  if not dautori.has_key(pezzi[1]):
    dautori.update({pezzi[1]:set()})    #creo un set vuoto per la chiave pezzi[1]
  
  dautori[pezzi[1]].add(pezzi[0])       #aggiungo l'ID al set
  
  
  # if dautori.has_key(pezzi[1]):
    # dautori[pezzi[1]].add(pezzi[0])
  # else:
    # #dautori.update({pezzi[1]:set(pezzi[0])})
    # dautori.update({pezzi[1]:set()})
    # dautori[pezzi[1]].add(pezzi[0])    
    # printType(pezzi[0])

print dautori
