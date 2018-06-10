#! python2

from os.path import join, abspath
from timeit import default_timer as timer
import multiprocessing as mp
import os
import re
import traceback


def processaAm(pfAffRAW, chunkStart, chunkSize, regaff):
  try:
    #carica solo le linee da processare
    with open(pfAffRAW, 'rb') as fPapAffPad:
      fPapAffPad.seek(chunkStart)
      lines = fPapAffPad.read(chunkSize).splitlines()
    chuRes = ''
    regex = 0
    for line in lines:
      pezzi = line.split('\t')
      # if re.search('pad(ov|u)a', line):
      if regaff.search(line):
        chuRes += '{}\r\n'.format(line.rstrip())
        regex += 1
    return chuRes, regex
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

def estraiAffPadovaneVeloce(pfAffRAW, pfAffPad, regaff):
  roughSize = 1024*1024
  pool = mp.Pool(mp.cpu_count())
  lresult = []

  sizeAraw = os.path.getsize(pfAffRAW)
  print 'sizeAffRAW: {} chunks: {} roughSize: {}'.format(sizeAraw, sizeAraw/roughSize, roughSize)

  for chunkStart, chunkSize in chunkMyFile(pfAffRAW, roughSize):
    lresult.append(pool.apply_async(processaAm,(pfAffRAW, chunkStart, chunkSize, regaff) ) )

  totregex = 0
  with open(pfAffPad, 'wb') as fAffPad:
    for r in lresult:
      fAffPad.write(r.get()[0])
      totregex += r.get()[1]
  # print('totregex: {}'.format(totregex) )
  pool.close()

if __name__ == '__main__':
  print('This program is EstraiAffPadovaneVeloce, being run by itself')

  ctesi = abspath(join(__file__, '..', '..') )
  celaborati = join(ctesi, 'authorship-network', 'Versione4_Totale')
  sub = 'Prima'
  tag = 'Prova'

  if not os.path.exists(join(celaborati, sub)): os.makedirs(join(celaborati, sub))
  cfileRAW = join(ctesi, 'FileRAW')
  pfAffRAW = join(cfileRAW, 'Affiliations.txt')
  pfAffPad = join(celaborati, sub, 'AffiliationPadovaPadua{}.txt'.format(tag))

  regaff = re.compile('pad(ov|u)a', re.IGNORECASE)
  start = timer()
  estraiAffPadovaneVeloce(pfAffRAW, pfAffPad, regaff)
  end = timer()
  print 'Completato estraiAffPadovaneVeloce in {}'.format(end-start)






