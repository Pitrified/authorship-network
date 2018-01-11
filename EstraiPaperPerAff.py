#! python2

import os
import multiprocessing as mp
from timeit import default_timer as timer
import traceback
import re


def estraiAutPerID(pfAutRAW, chunkStart, chunkSize, sAutDaEstr):
  try:
    #carica solo le linee da processare
    with open(pfAutRAW, 'rb') as fAutRAW:
      fAutRAW.seek(chunkStart)
      lines = fAutRAW.read(chunkSize).splitlines()
      #print 'PPA: chunkStart: {} chunkSize: {} pfPapAutAffRAW: {} lines opened: {}'.format(chunkStart, chunkSize, pfPapAutAffRAW, lines)
    chuRes = ''
    for line in lines:
      pezzi = line.split('\t')
      if pezzi[0] in sAutDaEstr:
        # chuRes += '{}\r\n'.format(line.rstrip())
        chuRes += '{}\r\n'.format(line)
    return chuRes
    
  except:
    traceback.print_exc()
    raise


def estraiPapPerAut(pfPapAutAffRAW, chunkStart, chunkSize, sAutDaEstr):
  try:
    #carica solo le linee da processare
    with open(pfPapAutAffRAW, 'rb') as fPapAutAffRAW:
      fPapAutAffRAW.seek(chunkStart)
      lines = fPapAutAffRAW.read(chunkSize).splitlines()
      #print 'PPA: chunkStart: {} chunkSize: {} pfPapAutAffRAW: {} lines opened: {}'.format(chunkStart, chunkSize, pfPapAutAffRAW, lines)
    chuRes = ''
    for line in lines:
      pezzi = line.split('\t')
      if pezzi[1] in sAutDaEstr:
        # chuRes += '{}\r\n'.format(line.rstrip())
        chuRes += '{}\r\n'.format(line)
    return chuRes
    
  except:
    traceback.print_exc()
    raise
  

def estraiPapPerAff(pfPapAutAffRAW, chunkStart, chunkSize, sAffDaEstr):
  try:
    #carica solo le linee da processare
    with open(pfPapAutAffRAW, 'rb') as fPapAutAffRAW:
      fPapAutAffRAW.seek(chunkStart)
      lines = fPapAutAffRAW.read(chunkSize).splitlines()
      #print 'PPA: chunkStart: {} chunkSize: {} pfPapAutAffRAW: {} lines opened: {}'.format(chunkStart, chunkSize, pfPapAutAffRAW, lines)
    chuRes = ''
    # print(lines)
    for line in lines:
      pezzi = line.split('\t')
      if len(pezzi) > 2:
        if pezzi[2] in sAffDaEstr:
          # chuRes += '{}\r\n'.format(line.rstrip())
          chuRes += '{}\r\n'.format(line)
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
      

def estraiAffPadovane(pfPapAutAffRAW, pfAffDaEstr, pfPapAutAffEstr, pfAutRAW, pfAutEstr, pfPersEstr):
  """
  in pfPapAutAffRAW ci sono record IDpap-IDaut-IDaff, se IDaff in sAffDaEstr
  in pfPapAutAffEstr salvo i record PaestraiPapPerAffPad
  in pfAutEstr salvo gli IDaut con nome (li ho in pfAutRAW)
  """
  # proceso scrittore con coda dei risultati scitti subito ???

  roughSize = 1024*1024
  pool = mp.Pool(mp.cpu_count())
  lres = []
  
  # load IDaff
  sAffDaEstr = set()
  # print('pfAffDaEstr: {}'.format(pfAffDaEstr) )
  with open(pfAffDaEstr, 'rb') as fAffDaEstr:
    for line in fAffDaEstr:
      sAffDaEstr.add(line.split('\t')[0])   # pezzi[0] sempre presente
  # print('len(sAffDaEstr): {}'.format(len(sAffDaEstr)) )

  for chunkStart, chunkSize in chunkMyFile(pfPapAutAffRAW, roughSize):
    lres.append(pool.apply_async(estraiPapPerAff,(pfPapAutAffRAW, chunkStart, chunkSize, sAffDaEstr) ) )
    
  # paper con IDaff in sAffDaEstr
  with open(pfPapAutAffEstr, 'wb') as fPapAutAffEstr:
    for r in lres:
      fPapAutAffEstr.write(r.get())
      
  # load IDaut
  pfPapAutAffEstr = celaborati + sub + 'PaperAutAffEstratti' + 'Fulll' + '.txt' # per test
  sIDAutDaEstr = set()
  print('pfPapAutAffEstr: {}'.format(pfPapAutAffEstr) )
  with open(pfPapAutAffEstr, 'rb') as fPapAutAffEstr:
    for line in fPapAutAffEstr:
      sIDAutDaEstr.add(line.split('\t')[1])   # pezzi[1] sempre presente
  print('len(sIDAutDaEstr): {}'.format(len(sIDAutDaEstr)) )
    
  for chunkStart, chunkSize in chunkMyFile(pfAutRAW, roughSize):
    lres.append(pool.apply_async(estraiAutPerID,(pfAutRAW, chunkStart, chunkSize, sIDAutDaEstr)))
  
  # autori con IDaut in sAutDaEstr
  with open(pfAutEstr, 'wb') as fAutEstr:
    for r in lres:
      fAutEstr.write(r.get())
      
  # load nomiaut
  sNomiAut = set()
  # pfAutEstr  = celaborati + sub + 'AutEstratti' + 'Fulll' + '.txt'
  with open(pfAutEstr, 'rb') as fAutEstr:
    for line in fAutEstr:
      sNomiAut.add(line.split('\t')[1])     # gia con \r\n
    
  # scrivo i nomiEstratti
  with open(pfPersEstr, 'wb') as fPersEstr:
    for line in sNomiAut:
      fPersEstr.write(line)
    
  # # paper con padovua nel nome aff
  # sIDAffPad = set()
  # i=0
  # pfPapAffPad = celaborati + sub + 'PaestraiPapPerAffPad' + 'FULL' + '.txt'  # per test
  # with open(pfPapAffPad, 'rb') as fPapAffPad:
    # for line in fPapAffPad:
      # i+=1
      # pezzi = line.split('\t')
      # #print('line: {} pezzi: {} len(pezzi): {} '.format(line.rstrip(), pezzi, len(pezzi)) )
      # if len(pezzi)>2:
        # sIDAffPad.add(pezzi[2])
  # print('AffPad univoche PaestraiPapPerAffPad: {}, numero di PaestraiPapPerAffPad: {}'.format(len(sIDAffPad), i) )
  
  # lres = []
  # # scorro Affiliations.txt e prendo quelle con padovua E quelle in fPapAffPad
  # for chunkStart, chunkSize in chunkMyFile(pfAffRAW, roughSize):
    # lres.append(pool.apply_async(processaAm,(pfAffRAW, chunkStart, chunkSize, sIDAffPad)))
  
  # totid, totregex = 0,0
  # with open(pfAffPad, 'wb') as fAffPad:
    # for r in lres:
      # fAffPad.write(r.get()[0])
      # totid += r.get()[1]
      # totregex += r.get()[2]
  # print('totid: {} totregex: {}'.format(totid, totregex) )
  pool.close()

if __name__ == '__main__':
  print 'This program is estraiPaperPerAff, being run by itself' 
  # PATH TO FILES
  craw = 'C:\Users\Pietro\Documents\University\Tesi\FileRAW\\'
  pfPapAutAffRAW = craw + 'PaperAuthorAffiliations1000.txt'
  # pfPapAutAffRAW = craw + 'PaperAuthorAffiliations.txt'
  pfAffRAW = craw + 'Affiliations.txt'
  pfAutRAW = craw + 'Authors1000.txt'
  # pfAutRAW = craw + 'Authors.txt'
  
  celaborati = 'Versione3_Multi\\'
  sub = 'Amplia\\'
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  tag = 'Fullll'
  # pfAutoriID = celaborati + sub + 'AutoriDEI' + tag + '.txt'
  # pfPapAffPad = celaborati + sub + 'PaestraiPapPerAffPad' + tag + '.txt'
  # pfAffPad    = celaborati + sub + 'AffiliationPadovaPaduta' + tag + '.txt'
  pfAffDaEstr = celaborati + sub + 'AffiliationPadovaPadutaFiltroDEIeliminati.txt'
  pfPapAutAffEstr = celaborati + sub + 'PaperAutAffEstratti' + tag + '.txt'
  pfAutEstr  = celaborati + sub + 'AutEstratti' + tag + '.txt'
  pfPersEstr = celaborati + sub + 'PersEstratte' + tag + '.txt'
  
  start = timer()
  estraiAffPadovane(pfPapAutAffRAW, pfAffDaEstr, pfPapAutAffEstr, pfAutRAW, pfAutEstr, pfPersEstr)
  end = timer()
  print 'Completato estraiPaperPerAff in {}'.format(end-start)
else:
  pass
  # tutti i processi figli eseguono questo codice
  # print 'I am EstraiPapAutAffDEImulti, being imported from another module'
  