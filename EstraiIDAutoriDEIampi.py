#! python2

#da PersoneDEI.txt ho una lista di nomi
#in Authors.txt ci sono ID-autori, cerco gli autori
#salvo il AutoriDEIampi

def estraiIDautori(pfPersone, pfAuthorRAW, pfAutoriID):
  """
  in pfPersone (PersoneDEI.txt) ho una lista di nomi
  in pfAuthorRAW (Authors.txt) ci sono record IDaut-nomeAut, cerco i nomi nel set
  salvo il record in pfAutoriID (AutoriDEIampi.txt)
  """
  #print 'pfPersone:{}\tpfAuthorRAW:{}\tpfAutoriID:{}'.format(pfPersone, pfAuthorRAW, pfAutoriID)
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
  #print 'abbreviazioni {}'.format(len(sPersone))
  
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



if __name__ == '__main__':
  print 'This program is EstraiIDAutoriDEIampi, being run by itself'
  #PATH TO FILES
  celaborati = 'Versione3_Single\\'
  pfPersone = celaborati + 'PersoneDEI.txt'
  pfAutoriID = celaborati + 'AutoriDEI.txt'
  pfAuthorRAW = 'C:\Users\Test\Documents\Tesi\FileRAW\Authors10.txt'
  estraiIDautori(pfPersone, pfAuthorRAW, pfAutoriID)
  #faccio cose che servono quando sono da solo
  print 'finitoEIADAsolo'
else:
  print 'I am EstraiIDAutoriDEIampi, being imported from another module'
  #_init_import() #se serve fare cose al momento dell'importazione
  #print 'finitoEIADAimport'
