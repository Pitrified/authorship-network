#! python2

def preparaPerGephi(pfEdge, pfAut, pfEdgeGephi, pfAutGephi):
  with open(pfEdge, 'rb') as fEdge:
    strInput = fEdge.read()
    
  with open(pfEdgeGephi, 'wb') as fEdgeGephi:
    fEdgeGephi.write("Source\tTarget\tWeight\tType\r\n")
    fEdgeGephi.write(strInput.replace("\r\n","\tUndirected\r\n" ) )
    
  with open(pfAut, 'rb') as fAut:
    strInput = fAut.read()
    
  with open(pfAutGephi, 'wb') as fAutGephi:
    fAutGephi.write("id\tLabel\r\n")
    fAutGephi.write(strInput)
 
def estraiIDautori(pfPersone, pfAuthorRAW, pfAutoriID):
  """
  in pfPersone (PersoneDEI.txt) ho una lista di nomi
  in pfAuthorRAW (Authors.txt) ci sono record IDaut-nomeAut, cerco i nomi nel set
  salvo il record in pfAutoriID (AutoriDEIampi.txt)
  """
  print 'pfPersone:{}\tpfAuthorRAW:{}\tpfAutoriID:{}'.format(pfPersone, pfAuthorRAW, pfAutoriID)
  #popolo il set
  sPersone = set()
  with open(pfPersone, 'rb') as fPersone:
    for line in fPersone:
      line = line.rstrip()
      sPersone.add(line)
      pz = line.split()
      #print(pz, " ", len(pz))
      if len(pz)==2:
        sPersone.add(pz[0][0]+" "+pz[1])
      elif len(pz)==3:
        sPersone.add(pz[0][0]+" "+pz[1][0]+" "+pz[2])
        sPersone.add(pz[0]   +" "+pz[1][0]+" "+pz[2])
        sPersone.add(pz[0][0]+" "+pz[1]   +" "+pz[2])
      elif len(pz)==4:
        sPersone.add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
        sPersone.add(pz[0]   +" "+pz[1][0]+" "+pz[2][0]+" "+pz[3])
        sPersone.add(pz[0][0]+" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
        sPersone.add(pz[0][0]+" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
        sPersone.add(pz[0]   +" "+pz[1]   +" "+pz[2][0]+" "+pz[3])
        sPersone.add(pz[0]   +" "+pz[1][0]+" "+pz[2]   +" "+pz[3])
        sPersone.add(pz[0][0]+" "+pz[1]   +" "+pz[2]   +" "+pz[3])
      elif len(pz)==6:
        sPersone.add(pz[0][0]+" "+pz[1][0]+" "+pz[2][0]+" "+pz[3][0]+" "+pz[4][0]+" "+pz[5])
  print 'abbreviazioni {}'.format(len(sPersone))
  
  #cerco i nomi nel set
  #popolo il set degli IDautDEI
  sIDautDEI = set()
  with open(pfAuthorRAW, 'rb') as fAutoriRAW, open(pfAutoriID, 'wb') as fAutoriID:
    for line in fAutoriRAW:
      pezzi = line.rstrip().split('\t')         #record IDaut-nomeAut
      #print 'pezzi[1]: <{}>'.format(pezzi[1])
      if pezzi[1] in sPersone:                  #pezzi[1] : nomeAut
        #print pezzi[1]
        fAutoriID.write(line)
        sIDautDEI.add(pezzi[0])                 #pezzi[0] : IDaut
  return sIDautDEI

def estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff, sIDautDEI=None):
  """
  in pfAutoriID ci sono record IDaut-nomeAut, carico gli ID nel set
  in pfPapAutAffRAW ci sono record IDpap-IDaut-IDaff, se IDaut e' nel set allora
  in pfPapAutAff salvo i record
  in sIDautDEI ho il set precaricato degli IDaut
  """
  if sIDautDEI is None:
    sIDautDEI = set()
    #print 'devo caricare il set perche non l\'avevo'
    with open(pfAutoriID, 'rb') as fAutoriID:
      for line in fAutoriID:
        sIDautDEI.add(line.split('\t')[0])
  #else:
    #print 'arrivato {}'.format(sIDautDEI)
    
  dPAA = {}
  with open(pfPapAutAffRAW, 'rb') as fPapAutAffRAW, open(pfPapAutAff, 'wb') as fPapAutAff:
    for line in fPapAutAffRAW:
      pezzi = line.split("\t")
      if pezzi[1] in sIDautDEI:
        #fPapAutAff.write(line.rstrip()+'\n')  #newline perche in binary mode
        fPapAutAff.write(line)  #newline perche in binary mode
        #print line,
        if not dPAA.has_key(pezzi[0]):
          dPAA.update({pezzi[0]:[]})      #se non c'e' la chiave creo lista vuota
        dPAA[pezzi[0]].append(pezzi[1])   #carico IDaut nella lista
  return dPAA
 
def creaEdgeCollab(pfPapAutAff, pfEdgeCollab, dPAA=None):
  """
  in pfPapAutAff ho IDpap-IDaut
  in dPAA carico {IDpap:[IDa1, IDa2, IDa4, IDa3]}
  in pfEdgeCollab creo edge IDa1-2, IDa1-4, IDa1-3, IDa2-4, IDa2-3, IDa3-4 con pesi
  """
  if dPAA is None:
    dPAA = {}
    with open(pfPapAutAff, 'rb') as fPapAutAff:
      for line in fPapAutAff:
        #print line,
        pezzi = line.rstrip().split("\t")
        if not dPAA.has_key(pezzi[0]):    #pezzi[0] : IDpap
          dPAA.update({pezzi[0]:[]})      #se non c'e' la chiave creo lista vuota
        dPAA[pezzi[0]].append(pezzi[1])   #carico pezzi[1] = IDaut nella lista
  #else:
    #print 'arrivato {}'.format(dPAA)

  dEdgeCollab = {}
  for entry in dPAA:
    ledge = dPAA[entry]
    #print len(ledge)
    i=0
    #ptype(ledge)
    while i<len(ledge)-1:
      j=i+1
      while j<len(ledge):
        if ledge[i]<ledge[j]: coppia = ledge[i]+"\t"+ledge[j]
        else: coppia = ledge[j]+"\t"+ledge[i]
        #print coppia
        if not dEdgeCollab.has_key(coppia): dEdgeCollab.update({coppia:1})
        else: dEdgeCollab[coppia]+=1      
        j+=1
      i+=1
  #print dEdgeCollab
    
  with open(pfEdgeCollab, 'wb') as fEdgeCollab: 
    for entry in dEdgeCollab:
      fEdgeCollab.write('{}\t{}\r\n'.format(entry, dEdgeCollab[entry]))
      #fEdgeCollab.write(entry+"\t"+str(dEdgeCollab[entry])+"\n")
  return dEdgeCollab
 
def estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab, dEdgeCollab=None):
  """
  in pfAutoriID ho gli IDaut-nomeAut DEI
  in pfEdgeCollab ho gli EdgeCollab come coppie di IDaut1-IDaut2
  in pfAutCollab se IDaut1 o IDaut2 sono in IDautDEI li copio
  """
  if dEdgeCollab is None:
    dEdgeCollab = {}
    with open(pfEdgeCollab, 'rb') as fEdgeCollab: 
      for line in fEdgeCollab:
        pezzi = line.split('\t')
        dEdgeCollab.update({pezzi[0]+'\t'+pezzi[1]:0})
  #else:
    #print 'arrivato {}'.format(dEdgeCollab)
    
  sEdgeCollab = set()
  for entry in dEdgeCollab:
    pezzi = entry.split()
    sEdgeCollab.add(pezzi[0])
    sEdgeCollab.add(pezzi[1])
    
  with open(pfAutoriID, 'rb') as fAutoriID, open(pfAutCollab, 'wb') as fAutCollab:
    for line in fAutoriID:
      pezzi = line.split('\t')
      if pezzi[0] in sEdgeCollab:
        fAutCollab.write(line)

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
  eve sempre trovare il nome
  """
  #if abbreviato in lconflitti: return abbreviato  #non restituisce la forma estesa 
  for entry in dPersone:
    #printType(dPersone[entry])
    if abbreviato == entry:         #abbreviato era gia' il nome esteso
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
  dPersone = {}                       #dizionario persone con abbreviazioni
  with open(pfPersone, 'rb') as fPersone:
    for line in fPersone:
      line = line.rstrip()
      dPersone.update({line:set()})
      pz = line.split()
      #print(pz, " ", len(pz))
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
      
  dAutori = {}  #{nome:[IDaut,IDaut,...,IDaut]}
  dIdAutori = {}  #{IDaut:nome}
  with open(pfAutCollab, 'rb') as fAutCollab:
    for line in fAutCollab:
      pezzi = line.rstrip().split('\t')    #pezzi[0] id; pezzi[1] nome senza \n
      
      nome =  trovaNome(pezzi[1], dPersone)       #trovo il nome completo
      
      if not dAutori.has_key(nome):
        dAutori.update({nome:[]})       #creo una lista vuota per la chiave nome
      
      #print "Nome:",nome,"Pezzi[1]",pezzi[1]
      if nome == pezzi[1]:              #il nome era gia' completo
        dAutori[nome].insert(0, pezzi[0])   #inserisco il nome all'inizio della lista
        #print "Metto in cima lalala"
      else:                             #era un nome abbreviato
        dAutori[nome].append(pezzi[0])  #aggiungo l'IDaut (relativo ad un abbreviazione) alla fine della lista

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
  print 'This program is AnalisiMSR, being run by itself' 
  
  print 'Still does nothing'
else:
  print 'I am AnalisiMSR, being imported from another module'
  