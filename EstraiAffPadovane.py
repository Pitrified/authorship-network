#! python2

import os
import multiprocessing as mp
from timeit import default_timer as timer
import traceback
import re


def processaAm(pfAffRAW, chunkStart, chunkSize, sIDAffPad, regaff):
  try:
    #carica solo le linee da processare
    with open(pfAffRAW, 'rb') as fPapAffPad:
      fPapAffPad.seek(chunkStart)
      lines = fPapAffPad.read(chunkSize).splitlines()
    chuRes = ''
    id = 0
    regex = 0
    for line in lines:
      pezzi = line.split('\t')
      if pezzi[0] in sIDAffPad:
        chuRes += '{}\r\n'.format(line.rstrip())
        id+=1
      else:
        # if re.search('pad(ov|u)a', line, re.I):  # 127s
        if regaff.search(line):
          chuRes += '{}\r\n'.format(line.rstrip())
          regex += 1
    return chuRes, id, regex

  except:
    traceback.print_exc()
    raise


def processaPAAm(pfPapAutAffRAW, chunkStart, chunkSize, regaff):
  try:
    #carica solo le linee da processare
    with open(pfPapAutAffRAW, 'rb') as fPapAutAffRAW:
      fPapAutAffRAW.seek(chunkStart)
      lines = fPapAutAffRAW.read(chunkSize).splitlines()
      #print 'PPA: chunkStart: {} chunkSize: {} pfPapAutAffRAW: {} lines opened: {}'.format(chunkStart, chunkSize, pfPapAutAffRAW, lines)
    chuRes = ''
    for line in lines:
      # if re.search('pad(ov|u)a', line, re.I):  # 127s
      if regaff.search(line):
        chuRes += '{}\r\n'.format(line.rstrip())
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


def estraiAffPadovane(pfPapAutAffRAW, pfPapAffPad, regaff):
  """
  in pfPapAutAffRAW ci sono record IDpap-IDaut-IDaff-nomeAff, se nomeAff contiene padovua allora
  in pfPapAffPad salvo i record
  scorro AffiliationsRAW ed estraggo quelle viste in pfPapAffPad E quelle con padovua dentro
  """
  # proceso scrittore con coda dei risultati scitti subito ???

  roughSize = 1024*1024
  pool = mp.Pool(mp.cpu_count())
  lresult = []

  for chunkStart, chunkSize in chunkMyFile(pfPapAutAffRAW, roughSize):
    lresult.append(pool.apply_async(processaPAAm,(pfPapAutAffRAW, chunkStart, chunkSize, regaff) ) )

  # paper con padovua nel nome aff
  with open(pfPapAffPad, 'wb') as fPapAffPad:
    for r in lresult:
      fPapAffPad.write(r.get())

  # paper con padovua nel nome aff
  sIDAffPad = set()
  i=0
  # pfPapAffPad = celaborati + sub + 'PaperAffPad' + 'FULL' + '.txt'  # per test
  with open(pfPapAffPad, 'rb') as fPapAffPad:
    for line in fPapAffPad:
      i+=1
      pezzi = line.split('\t')
      #print('line: {} pezzi: {} len(pezzi): {} '.format(line.rstrip(), pezzi, len(pezzi)) )
      if len(pezzi)>2:
        sIDAffPad.add(pezzi[2])
  print('AffPad univoche PaperAffPad: {}, numero di PaperAffPad: {}'.format(len(sIDAffPad), i) )

  lresult = []
  # scorro Affiliations.txt e prendo quelle con pad(ov|u)a E quelle in fPapAffPad
  for chunkStart, chunkSize in chunkMyFile(pfAffRAW, roughSize):
    lresult.append(pool.apply_async(processaAm,(pfAffRAW, chunkStart, chunkSize, sIDAffPad, regaff)))

  totid, totregex = 0,0
  with open(pfAffPad, 'wb') as fAffPad:
    for r in lresult:
      fAffPad.write(r.get()[0])
      totid += r.get()[1]
      totregex += r.get()[2]
  print('totid: {} totregex: {}'.format(totid, totregex) )
  pool.close()

if __name__ == '__main__':
  print 'This program is estraiAffPadovane, being run by itself'
  #PATH TO FILES
  celaborati = 'Versione3_Multi\\'
  sub = 'Amplia\\'
  celaborati = 'Versione4_Totale\\'
  sub = 'AnalisAff\\'
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  tag = 'Alone'
  # pfAutoriID = celaborati + sub + 'AutoriDEI' + tag + '.txt'
  pfPapAutAffRAW = '..\FileRAW\PaperAuthorAffiliations.txt'
  # pfPapAutAffRAW = '..\FileRAW\PaperAuthorAffiliations1000.txt'
  pfAffRAW = '..\FileRAW\Affiliations.txt'
  pfPapAffPad = celaborati + sub + 'PaperAffPad' + tag + '.txt'
  pfAffPad = celaborati + sub + 'AffiliationPadovaPadua' + tag + '.txt'
  regaff = re.compile('pad(ov|u)a', re.IGNORECASE)
  start = timer()
  estraiAffPadovane(pfPapAutAffRAW, pfPapAffPad, regaff)
  end = timer()
  print 'Completato estraiAffPadovane in {}'.format(end-start)
else:
  pass
  #tutti i processi figli eseguono questo codice
  #print 'I am EstraiPapAutAffDEImulti, being imported from another module'

