#! python2

import os
from os.path import abspath
from os.path import dirname
from os.path import join
import multiprocessing as mp
from timeit import default_timer as timer
import traceback
# from Updater import Upd

#da soloid.txt ho una lista di id autore
#in Authors.txt ci sono ID-autori, cerco gli id

def chunkMyFile(fpath, roughSize):
  """
  generatore che divide un file in pezzi di circa roughSize byte
  """
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


def processaAutPerID(pfAuthorRAW, chunkStart, chunkSize, sIDautori):
  try:
    # carica solo le linee da processare
    with open(pfAuthorRAW, 'rb') as fAuthorRAW:
      fAuthorRAW.seek(chunkStart)
      lines = fAuthorRAW.read(chunkSize).splitlines()
    chuRes = ''
    for line in lines:
      pezzi = line.split('\t')
      if pezzi[0] in sIDautori:
        chuRes += '{}\r\n'.format(line)
    return chuRes
  except:
    traceback.print_exc()
    raise

def estraiAutoriPerID(pfSoloIDautore, pfAuthorRAW, pfAutoriID):
  """
  in pfSoloIDautore (PersoneDEI.txt) ho una lista di nomi
  in pfAuthorRAW (Authors.txt) ci sono record IDaut-nomeAut, cerco i nomi nel set
  salvo il record in pfAutoriID (AutoriDEIampi.txt)
  """
  # print 'pfSoloIDautore:{}\tpfAuthorRAW:{}\tpfAutoriID:{}'.format(pfSoloIDautore, pfAuthorRAW, pfAutoriID)
  # popolo il set
  sIDautori = set()
  with open(pfSoloIDautore, 'rb') as fSoloID:
    for line in fSoloID:
      pezzi = line.rstrip().split('\t')
      autID = pezzi[0]
      sIDautori.add(autID)
  # print(sIDautori)
  # print 'abbreviazioni {}'.format(len(sIDautori))

  roughSize = 1024*1024 *10
  pool = mp.Pool(mp.cpu_count())
  lresult = []

  sizeAraw = os.path.getsize(pfAuthorRAW)
  print 'sizeAuthorRAW: {} chunks: {} roughSize: {}'.format(sizeAraw, sizeAraw/roughSize, roughSize)

  for chunkStart, chunkSize in chunkMyFile(pfAuthorRAW, roughSize):
    lresult.append(pool.apply_async(processaAutPerID,(pfAuthorRAW, chunkStart, chunkSize, sIDautori) ) )

  with open(pfAutoriID, 'wb') as fAutoriID:
    for r in lresult:
      fAutoriID.write(r.get())
      # up.update('next')

  pool.close()

if __name__ == '__main__':
  print 'This program is EstraiIDAutoriDEIampiMulti, being run by itself'

  #PATH TO FILES
  celaborati = '.\Versione3_Upd\\'
  # celaborati = './Versione3_Upd/'
  pfSoloIDautore = celaborati + 'PersoneDEI.txt'
  pfAutoriID = celaborati + 'AutoriDEIupd.txt'
  # pfAuthorRAW = '..\FileRAW\Authors10.txt'
  # pfAuthorRAW = '..\FileRAW\Authors1000.txt'
  pfAuthorRAW = '..\FileRAW\Authors.txt'
  # pfAuthorRAW = '../FileRAW/Authors.txt'

  ctesi = abspath(join(__file__, '..', '..') )
  celaborati = join(ctesi, 'authorship-network', 'Versione5')
  sub = 'ApostolicoSingolo'
  tag = '_DEI'
  if not os.path.exists(join(celaborati, sub)): os.makedirs(join(celaborati, sub))
  cfileRAW   = join(ctesi, 'FileRAW')
  pfAuthorRAW = join(cfileRAW, 'Authors.txt')
  pfSoloIDautore = join(celaborati, 'PersoneNomi_apostolico{}.txt'.format(tag))
  pfAutoriID = join(celaborati, sub, 'AutoriID{}.txt'.format(tag))
  print('\nChiamo estraiIDautoriMulti con\n\t{}\n\t{}\n\t{}'.format(pfSoloIDautore, pfAuthorRAW, pfAutoriID))

  start = timer()
  estraiIDautoriMulti(pfSoloIDautore, pfAuthorRAW, pfAutoriID)
  end = timer()
  print 'Completato estraiIDautoriMulti in {}'.format(end-start)
else:
  pass
  # print 'I am EstraiIDAutoriDEIampiMulti, being imported from another module'
  #_init_import() #se serve fare cose al momento dell'importazione
  #print 'finitoEIADAimport'
