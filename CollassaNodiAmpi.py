#! python2

#carica da AutoriCollabOrdinatiNOMEpoiID.txt    IDaut Nome
#{nome1 : [id1, id2, id3]}
#{nome2 : [id4, id5, id6, id7]}
#traduci tutti gli edge "id2 id6" in "id1 id4"
#a rossi-> aldo rossi
#m rossi-> michele rossi

def printType(obj):
  print obj, " - ", type(obj)
  
#cerca l'ID nelle liste del dizionario e restituisce il primo ID della lista giusta
#deve sempre trovare l'ID nel dizionario
def trovaSostituto(id):
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

dpersone = {}                       #dizionario persone con abbreviazioni
fpersone = open("PersoneDEI.txt")
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
  
#fautori = open("AutoriCollabOrdinatiNOMEpoiIDridotto.txt", "r")
fautori = open("AutoriCollabAmpiOrdinatiNOMEpoiID.txt", "r")  #produce Bis
#fautori = open("AutoriPadovaniAmpiOrdinatiNOMEpoiID.txt", "r") #produce Bis
#fautori = open("AutoriDEIampi.txt", "r")          #produce Ter
dautori = {}

for line in fautori:
  pezzi = line.split("\t", 1)
  pezzi[1] = pezzi[1].rstrip()          #tolgo il \n
  nome = trovaNome(pezzi[1])        #trovo il nome completo
  if not dautori.has_key(nome):
    dautori.update({nome:[]})       #creo una lista vuota per la chiave nome, NOME
  print "Nome:",nome,"Pezzi[1]",pezzi[1]
  if nome == pezzi[1]:              #il nome era gia' completo
    dautori[nome].insert(0, pezzi[0])   #inserisco il nome all'inizo della lista
    print "Metto in cima lalala"
  else:                             #era un nome abbreviato
    dautori[nome].append(pezzi[0])  #aggiungo l'IDaut (relativo ad un abbreviazione) alla fine della lista  
fautori.close()

#print dautori

#fedge = open("EdgeDEIPesatiRidotto.txt", "r")
fedge = open("EdgeCollabPesatiAmpi.txt", "r")
#fedge = open("EdgePadovaniCompletiPesatiAmpi.txt", "r")
fedgenuovi = open("EdgeCollabPesatiAmpiUnificatiBis.txt", "w")
#fedgenuovi = open("EdgePadovaniCompletiPesatiAmpiUnificatiBis.txt", "w")
#fedgenuovi = open("EdgePadovaniCompletiPesatiAmpiUnificatiTer.txt", "w")
dpesato = {}

for line in fedge:
  pezzi = line.split("\t")
  id0 = trovaSostituto(pezzi[0])
  id1 = trovaSostituto(pezzi[1])
  
  if id0<id1: coppia = id0+"\t"+id1
  else: coppia = id1+"\t"+id0
  
  if not dpesato.has_key(coppia): dpesato.update({coppia:int(pezzi[2].rstrip())})
  else: dpesato[coppia]+=int(pezzi[2].rstrip())
    
#print dpesato

for entry in dpesato:
  fedgenuovi.write(entry+"\t"+str(dpesato[entry])+"\n")
  
fedge.close()
fedgenuovi.close()
