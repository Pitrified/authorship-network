#! python2

 
# #tempo: 172.679247183 righeparsizzate: 288264682
# #tempo: 187.196060742 righeparsizzate: 325498062

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

if __name__ == '__main__':
  print 'This program is EstraiPapAutAffDEI, being run by itself' 
  #PATH TO FILES
  celaborati = 'Versione3_Single\\'
  pfAutoriID = celaborati + 'AutoriDEI.txt'
  pfPapAutAffRAW = '..\FileRAW\PaperAuthorAffiliations500.txt'
  pfPapAutAff = celaborati + 'PapAutAffDEI.txt'
  estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
else:
  print 'I am EstraiPapAutAffDEI, being imported from another module'
  

