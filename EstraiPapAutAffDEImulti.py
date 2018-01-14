#! python2

import os
import multiprocessing as mp
from timeit import default_timer as timer
import traceback
import re

def processaPAADm(pfPapAutAffRAW, chunkStart, chunkSize, sIDautDEI):
  try:
    #carica solo le linee da processare
    with open(pfPapAutAffRAW, 'rb') as fPapAutAffRAW:
      fPapAutAffRAW.seek(chunkStart)
      lines = fPapAutAffRAW.read(chunkSize).splitlines()
      #print 'PPA: chunkStart: {} chunkSize: {} pfPapAutAffRAW: {} lines opened: {}'.format(chunkStart, chunkSize, pfPapAutAffRAW, lines)
    chuRes = ''
    for line in lines:
      pezzi = line.split('\t')
      if len(pezzi)>=2:
        if pezzi[1] in sIDautDEI:
        # if pezzi[1] in sIDautDEI or re.search('pad(ov|u)a', line, re.I): # che tanto non serve a niente perche trovo paper scritti a padova da autori che non sono nel dei
        # if re.search('pad(ov|u)a', line, re.I):  # 352s  # da questa lista di paper posso estrarre affiliation padovane che forse non erano in PadovaPadua
          # chuRes += '{}\n'.format(line)
          chuRes += '{}\r\n'.format(line.rstrip())
      else:
        'errore alla linea {}'.format(line)
    return chuRes
    
  except:
    traceback.print_exc()
    raise
    

def chunkMyFile(fpath, roughSize):
  fileEnd = os.path.getsize(fpath)
  with open(fpath, 'rb') as f:
    chunkEnd = f.tell()
    while True:
      chunkStart = chunkEnd
      f.seek(roughSize, 1)  #1 rispetto alla pos corrente - os.SEEK_CUR
      f.readline()          #il chunk finisce alla fine della riga
      chunkEnd = f.tell()
      #print 'CMF: chunkStart: {} chunkSize: {} pfPapAutAffRAW: {}'.format(chunkStart, chunkEnd-chunkStart, fpath)
      yield chunkStart, chunkEnd-chunkStart #lo uso come generatore
      if chunkEnd > fileEnd:  #EOF superata
        break
      

def estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPapAutAff, sIDautDEI=None):
  """
  in pfAutoriID ci sono record IDaut-nomeAut, carico gli ID nel set
  in pfPapAutAffRAW ci sono record IDpap-IDaut-IDaff, se IDaut e' nel set allora
  in pfPapAutAff salvo i record
  in sIDautDEI ho il set precaricato degli IDaut
  """
  # print 'pfPapAutAff:{}\tpfPapAutAffRAW:{}\tpfAutoriID:{}'.format(pfPapAutAff, pfPapAutAffRAW, pfAutoriID)
  # proceso scrittore con coda dei risultati scitti subito ???
  if sIDautDEI is None:
    sIDautDEI = set()
    # print 'devo caricare il set perche non l\'avevo'
    with open(pfAutoriID, 'rb') as fAutoriID:
      for line in fAutoriID:
        sIDautDEI.add(line.split('\t')[0])
  # else:
    # print 'arrivato {}'.format(sIDautDEI)

  roughSize = 1024*1024
  pool = mp.Pool(mp.cpu_count())
  lresult = []

  for chunkStart, chunkSize in chunkMyFile(pfPapAutAffRAW, roughSize):
    lresult.append(pool.apply_async(processaPAADm,(pfPapAutAffRAW, chunkStart, chunkSize, sIDautDEI) ) )
    
  with open(pfPapAutAff, 'wb') as fPapAutAff:
    for r in lresult:
      fPapAutAff.write(r.get())
      
  pool.close()

if __name__ == '__main__':
  print 'This program is EstraiPapAutAffDEImulti, being run by itself' 
  #PATH TO FILES
  celaborati = 'Versione3_Multi\\'
  pfAutoriID = celaborati + 'AutoriDEI.txt'
  pfAutoriID = celaborati + 'AutoriDEIMacroFull.txt'
  #pfPapAutAffRAW = '..\FileRAW\PaperAuthorAffiliations5000000.txt'
  #pfPapAutAffRAW = '..\FileRAW\PaperAuthorAffiliations.txt'
  pfPapAutAffRAW = '..\FileRAW\PaperAuthorAffiliations1000.txt'
  #pfPapAutAffRAW = '..\FileRAW\PaperAuthorAffiliations500.txt'
  pfPapAutAff = celaborati + 'PapAutAffDEImultiFull.txt'
  pfPapAutAff = celaborati + 'PapAutAffDEImultiIDePaduanonono.txt'
  start = timer()
  estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  end = timer()
  print 'Completato estraiPapAutAffDEImulti in {}'.format(end-start)
else:
  pass
  #tutti i processi figli eseguono questo codice
  #print 'I am EstraiPapAutAffDEImulti, being imported from another module'
  