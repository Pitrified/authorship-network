#! python2

def trovaSostituto(id, dAutori):
  """
  cerca l'ID nelle liste del dizionario e restituisce il primo ID della lista giusta
  deve sempre trovare l'ID nel dizionario
  """
  #if id in lIDconflitti: return id
  for entry in dAutori:
    #printType(dAutori[entry])
    if id in dAutori[entry]:
      #print dAutori[entry]
      return dAutori[entry][0]
  return "IDNOTFOUND!"

def trovaNome(abbreviato, dPersone):
  """
  cerca l'abbreviato nei set del dizionario e restituisce l'entry del set in cui lo trovi
  deve sempre trovare il nome
  dPersone sono solo nomi NON abbreviati
  m zorzi non sai a chi viene associato, a mattia o a michele
  """
  #if abbreviato in lconflitti: return abbreviato  #non restituisce la forma estesa
  for entry in dPersone:
    #printType(dPersone[entry])
    if abbreviato == entry:         # abbreviato era gia' il nome esteso
      return entry
    if abbreviato in dPersone[entry]:
      #print dPersone[entry]
      return entry
  return "NAMENOTFOUND!"

def collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati):
  """
  collassa i nodi
  #carica da AutoriCollabOrdinatiNOMEpoiID.txt    IDaut Nome
  #{nome1 : [id1, id2, id3]}
  #{nome2 : [id4, id5, id6, id7]}
  #traduci tutti gli edge "id2 id6" in "id1 id4"
  #a rossi-> aldo rossi
  #m rossi-> michele rossi
  """
  dPersone = {}                       # dizionario persone con abbreviazioni
  with open(pfPersone, 'rb') as fPersone:
    for line in fPersone:
      line = line.rstrip()
      dPersone.update({line:set()})   # a ciascun nome associo set di abbreviazioni
      pz = line.split()
      # print(pz, " ", len(pz))
      if len(pz)==2:
        dPersone[line].add(pz[0][0]+" "+pz[1])
      elif len(pz)==3:
        dPersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2])
        dPersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2])
        dPersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2])
      elif len(pz)==4:
        dPersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
        dPersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
        dPersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
        dPersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
        dPersone[line].add(pz[0]   +" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
        dPersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
        dPersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2]   +" "+pz[3])
      elif len(pz)==6:
        dPersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3][0]+" "+pz[4][0]+" "+pz[5])

  dAutori = {}    # {nome:[IDaut,IDaut,...,IDaut]}
  dIdAutori = {}  # {IDaut:nome}
  with open(pfAutCollab, 'rb') as fAutCollab:
    for line in fAutCollab:
      pezzi = line.rstrip().split('\t')     # pezzi[0] id; pezzi[1] nome senza \r\n

      nome =  trovaNome(pezzi[1], dPersone) # trovo il nome completo

      if not dAutori.has_key(nome):
        dAutori.update({nome:[]})           # creo una lista vuota per la chiave nome

      # print "Nome:",nome,"Pezzi[1]",pezzi[1]
      if nome == pezzi[1]:                  # il nome era gia' completo
        dAutori[nome].insert(0, pezzi[0])   # inserisco il nome all'inizio della lista
        # print "Metto in cima lalala"      # tengo per primi ID relativi a nomi completi
      else:                                 # era un nome abbreviato
        dAutori[nome].append(pezzi[0])      # aggiungo l'IDaut (relativo ad un abbreviazione) alla fine della lista

      dIdAutori.update({pezzi[0]:pezzi[1]})

  dEdgeCU = {}  #edge unificati
  dAutCU = {} #autori unificati
  with open(pfEdgeCollab, 'rb') as fEdgeCollab:
    for line in fEdgeCollab:
      pezzi = line.rstrip().split()
      id0 = trovaSostituto(pezzi[0], dAutori)
      id1 = trovaSostituto(pezzi[1], dAutori)

      if id0<id1: coppia = id0+"\t"+id1
      else: coppia = id1+"\t"+id0

      #if not dEdgeCU.has_key(coppia): dEdgeCU.update({coppia:int(pezzi[2].rstrip())})
      #else: dEdgeCU[coppia]+=int(pezzi[2].rstrip())
      if not dEdgeCU.has_key(coppia): dEdgeCU.update({coppia:int(pezzi[2])})
      else: dEdgeCU[coppia]+=int(pezzi[2])

      dAutCU.update({id0:dIdAutori[id0]})
      dAutCU.update({id1:dIdAutori[id1]})

  with open(pfEdgeCollabUnificati, 'wb') as fEdgeCollabUnificati:
    for entry in dEdgeCU:
      fEdgeCollabUnificati.write('{}\t{}\r\n'.format(entry, dEdgeCU[entry]))

  with open(pfAutCollabUnificati, 'wb') as fAutCollabUnificati:
    for entry in dAutCU:
      fAutCollabUnificati.write('{}\t{}\r\n'.format(entry, dAutCU[entry]))

if __name__ == '__main__':
  print 'This program is CollassaNodiAmpi, being run by itself'
  #PATH TO FILES
  celaborati = 'Versione3_Single\\'
  pfPersone = celaborati + 'PersoneDEI.txt'
  #pfEdgeCollab = celaborati + 'EdgeCollab.txt'
  pfEdgeCollab = celaborati + 'EdgeCollabMacroFull.txt'
  pfAutCollab = celaborati + 'AutoriCollab.txt'
  pfEdgeCollabUnificati = celaborati + 'EdgeCollabUnificati.txt'
  pfAutCollabUnificati = celaborati + 'AutoriCollabUnificati.txt'
  #pfAutLoop = celaborati + 'AutoriCollabLoop.txt'
  collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
  print 'finitoCNAsolo'
else:
  pass
  # print 'I am CollassaNodiAmpi, being imported from another module'

















# CARTELLA = "Versione2\\"
# #CARTELLA = "Versione1Ampi\\"

# def printType(obj):
  # print obj, " - ", type(obj)

# #cerca l'ID nelle liste del dizionario e restituisce il primo ID della lista giusta
# #deve sempre trovare l'ID nel dizionario
# def trovaSostituto(id):
  # if id in lIDconflitti: return id
  # for entry in dAutori:
    # #printType(dAutori[entry])
    # if id in dAutori[entry]:
      # #print dAutori[entry]
      # return dAutori[entry][0]
  # return "IDNOTFOUND!"

# #cerca l'abbreviato nei set del dizionario e restituisce l'entry del set in cui lo trovi
# #deve sempre trovare il nome
# def trovaNome(abbreviato):
  # if abbreviato in lconflitti: return abbreviato  #non restituisce la forma estesa
  # for entry in dPersone:
    # #printType(dPersone[entry])
    # if abbreviato == entry:         #abbreviato era gia' il nome esteso
      # return entry
    # if abbreviato in dPersone[entry]:
      # #print dPersone[entry]
      # return entry
  # return "NAMENOTFOUND!"

# dPersone = {}                       #dizionario persone con abbreviazioni
# fPersone = open(CARTELLA+"PersoneDEI.txt")
# for line in fPersone:
  # line = line.rstrip()
  # dPersone.update({line:set()})
  # pz = line.split()
  # #print(pz, " ", len(pz))
  # if len(pz)==2:
    # dPersone[line].add(pz[0][0]+" "+pz[1])
  # elif len(pz)==3:
    # dPersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2])
    # dPersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2])
    # dPersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2])
  # elif len(pz)==4:
    # dPersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
    # dPersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
    # dPersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
    # dPersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
    # dPersone[line].add(pz[0]   +" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
    # dPersone[line].add(pz[0]   +" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
    # dPersone[line].add(pz[0][0]+" "+pz[1]   +" "+pz[2]   +" "+pz[3])
  # elif len(pz)==6:
    # dPersone[line].add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3][0]+" "+pz[4][0]+" "+pz[5])

##selfloop
# lconflitti = ["m zorzi","g marin","m schiavon"]  #lista di nomi da mantenere abbreviati
# lIDconflitti = ["430A940B","0940501E","0FBC4502","3D94B201","42F1454E","41469B2F","3F95F553","4291A227","3485CD4D","3FDAF618","414C514D","3EA3BBB7","4149CAD1","3F93B63D","431A54FF","3EA3BBB7"] #lista di ID da non collassare
# print lconflitti
# print lIDconflitti

# #fautori = open(CARTELLA+"AutoriCollabOrdinatiNOMEpoiIDridotto.txt", "r")
# #fautori = open(CARTELLA+"AutoriCollabAmpiOrdinatiNOMEpoiID.txt", "r")  #produce Bis
# fautori = open(CARTELLA+"AutoriCollabAmpi.txt", "r")  #produce Bis
# #fautori = open(CARTELLA+"AutoriPadovaniAmpiOrdinatiNOMEpoiID.txt", "r") #produce Bis
# #fautori = open(CARTELLA+"AutoriPadovaniAmpi.txt", "r") #produce Bis
# #fautori = open(CARTELLA+"AutoriDEIampi.txt", "r")          #produce Ter
# dAutori = {}  #{nome:[IDaut,IDaut,...,IDaut]}
# dIdAutori = {}  #{IDaut:nome}

# for line in fautori:
  # pezzi = line.split("\t", 1)

  # pezzi[1] = pezzi[1].rstrip()      #tolgo il \n
  # nome = trovaNome(pezzi[1])        #trovo il nome completo
  # if not dAutori.has_key(nome):
    # dAutori.update({nome:[]})       #creo una lista vuota per la chiave nome, NOME

  # #print "Nome:",nome,"Pezzi[1]",pezzi[1]
  # if nome == pezzi[1]:              #il nome era gia' completo
    # dAutori[nome].insert(0, pezzi[0])   #inserisco il nome all'inizo della lista
    # #print "Metto in cima lalala"
  # else:                             #era un nome abbreviato
    # dAutori[nome].append(pezzi[0])  #aggiungo l'IDaut (relativo ad un abbreviazione) alla fine della lista

  # dIdAutori.update({pezzi[0]:pezzi[1]})
# fautori.close()

# #print dAutori
# #print dIdAutori



# #Bis e' per m zorzi e gli altri conflitti sulle abbreviazioni

# #fedge = open(CARTELLA+"EdgeDEIPesatiRidotto.txt", "r")
# fedge = open(CARTELLA+"EdgeCollabPesatiAmpi.txt", "r")
# #fedge = open(CARTELLA+"EdgePadovaniCompletiPesatiAmpi.txt", "r")

# #fedgenuovi = open(CARTELLA+"EdgeCollabPesatiAmpiUnificati.txt", "w")
# fedgenuovi = open(CARTELLA+"EdgeCollabPesatiAmpiUnificatiTer.txt", "w")
# #fedgenuovi = open(CARTELLA+"EdgePadovaniCompletiPesatiAmpiUnificatiTemp.txt", "w")
# #fedgenuovi = open(CARTELLA+"EdgePadovaniCompletiPesatiAmpiUnificatiBis.txt", "w")
# #fedgenuovi = open(CARTELLA+"EdgePadovaniCompletiPesatiAmpiUnificatiTer.txt", "w")

# #fautorinuovi = open(CARTELLA+"AutoriCollabAmpiUnificati.txt", "w")
# fautorinuovi = open(CARTELLA+"AutoriCollabAmpiUnificatiTer.txt", "w")
# #fautorinuovi = open(CARTELLA+"AutoriPadovaniAmpiUnificati.txt", "w")
# #fautorinuovi = open(CARTELLA+"AutoriPadovaniAmpiUnificatiBis.txt", "w")

##selfloop
# fautoriloop = open(CARTELLA+"AutoriCollabAULoopBis.txt", "w")
# fautoriloop.write("Counter\tid0\tid1\tpezzi[0]\tpezzi[1]\tPeso\tPCumula\tNome0\tNome1\tNPre0\tNPre1\n")
# dEdgeCU = {}  #edge unificati
# dAutCU = {} #autori unificati

# i = 0
# totpesi = 0
# for line in fedge:
  # pezzi = line.split("\t")

  # id0 = trovaSostituto(pezzi[0])
  # id1 = trovaSostituto(pezzi[1])
  # if id0<id1: coppia = id0+"\t"+id1
  # else: coppia = id1+"\t"+id0
  # if not dEdgeCU.has_key(coppia): dEdgeCU.update({coppia:int(pezzi[2].rstrip())})
  # else: dEdgeCU[coppia]+=int(pezzi[2].rstrip())

  # dAutCU.update({id0:dIdAutori[id0]})
  # dAutCU.update({id1:dIdAutori[id1]})

  ##selfloop
  # #controllo non siano nomi uguali
  # # nome0, nome1 = None, None
  # # for entry in dAutori:       #trova i nomi completi
    # # if id0 in dAutori[entry]:
      # # nome0 = entry
    # # if id1 in dAutori[entry]:
      # # nome1 = entry
  # nome0 = dIdAutori[id0]        #trova le abbreviazioni
  # nome1 = dIdAutori[id1]
  # nomepre0 = dIdAutori[pezzi[0]]
  # nomepre1 = dIdAutori[pezzi[1]]


  # if nome0 == nome1:
    # i+=1
    # peso = pezzi[2].rstrip()
    # totpesi += int(peso)
    # stringa = str(i)+"\t"+id0+"\t"+ id1+"\t"+ pezzi[0]+"\t"+ pezzi[1]+"\t"+str(peso)+"\t"+ str(totpesi)+"\t"+nome0+"\t"+ nome1+"\t"+nomepre0+"\t"+ nomepre1
    # print stringa
    # fautoriloop.write(stringa+"\n")

# #print dEdgeCU
# print "len ID:",str(len(dIdAutori)),"len unificati:",str(len(dAutCU))

# for entry in dEdgeCU:
  # fedgenuovi.write(entry+"\t"+str(dEdgeCU[entry])+"\n")

# for entry in dAutCU:
  # fautorinuovi.write(entry+"\t"+dAutCU[entry]+"\n")

# fedge.close()
# fedgenuovi.close()
# fautorinuovi.close()
# fautoriloop.close()

