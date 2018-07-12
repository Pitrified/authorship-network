#! python2

import os
from os.path import abspath
from os.path import dirname
from os.path import join
import multiprocessing as mp
from timeit import default_timer as timer
import traceback
# from Updater import Upd

#da PersoneDEI.txt ho una lista di nomi
#in Authors.txt ci sono ID-autori, cerco gli autori
#salvo il AutoriDEIampi

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


def processaEIADAm(pfAuthorRAW, chunkStart, chunkSize, sPersone):
  try:
    # carica solo le linee da processare
    with open(pfAuthorRAW, 'rb') as fAuthorRAW:
      fAuthorRAW.seek(chunkStart)
      lines = fAuthorRAW.read(chunkSize).splitlines()
    chuRes = ''
    for line in lines:
      pezzi = line.split('\t')
      if pezzi[1] in sPersone:
        # chuRes += '{}\n'.format(line)
        # chuRes += '{}\r\n'.format(line.rstrip())
        chuRes += '{}\r\n'.format(line)
    return chuRes
  except:
    traceback.print_exc()
    raise


def creaSetAbbreviazioni(pfPersone):
  sPersone = set()
  with open(pfPersone, 'rb') as fPersone:
    for line in fPersone:
      line = line.rstrip()
      sPersone.add(line)
      pz = line.split()
      # print(pz, " ", len(pz))
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
  return sPersone


def estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID):
  """
  in pfPersone (PersoneDEI.txt) ho una lista di nomi
  in pfAuthorRAW (Authors.txt) ci sono record IDaut-nomeAut, cerco i nomi nel set
  salvo il record in pfAutoriID (AutoriDEIampi.txt)
  """
  # print 'pfPersone:{}\tpfAuthorRAW:{}\tpfAutoriID:{}'.format(pfPersone, pfAuthorRAW, pfAutoriID)
  # popolo il set
  sPersone = creaSetAbbreviazioni(pfPersone)
  # print(sPersone)
  # print 'abbreviazioni {}'.format(len(sPersone))

  # cerco i nomi nel set
  # popolo il set degli IDautDEI
  # sIDautDEI = set()
  # with open(pfAuthorRAW, 'rb') as fAutoriRAW, open(pfAutoriID, 'wb') as fAutoriID:
    # for line in fAutoriRAW:
      # pezzi = line.rstrip().split('\t')         #record IDaut-nomeAut
      # # print 'pezzi[1]: <{}>'.format(pezzi[1])
      # if pezzi[1] in sPersone:                  #pezzi[1] : nomeAut
        # # print pezzi[1]
        # fAutoriID.write(line)
        # sIDautDEI.add(pezzi[0])                 #pezzi[0] : IDaut


  roughSize = 1024*1024 *10
  pool = mp.Pool(mp.cpu_count())
  lresult = []

  sizeAraw = os.path.getsize(pfAuthorRAW)
  print 'sizeAuthorRAW: {} chunks: {} roughSize: {}'.format(sizeAraw, sizeAraw/roughSize, roughSize)
  # up  = Upd(sizeAraw/roughSize)
  # up.update('redraw')

  for chunkStart, chunkSize in chunkMyFile(pfAuthorRAW, roughSize):
    lresult.append(pool.apply_async(processaEIADAm,(pfAuthorRAW, chunkStart, chunkSize, sPersone) ) )

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
  pfPersone = celaborati + 'PersoneDEI.txt'
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
  pfPersone = join(celaborati, 'PersoneNomi_apostolico{}.txt'.format(tag))
  pfAutoriID = join(celaborati, sub, 'AutoriID{}.txt'.format(tag))
  print('\nChiamo estraiIDautoriMulti con\n\t{}\n\t{}\n\t{}'.format(pfPersone, pfAuthorRAW, pfAutoriID))

  start = timer()
  estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)
  end = timer()
  print 'Completato estraiIDautoriMulti in {}'.format(end-start)
else:
  pass
  # print 'I am EstraiIDAutoriDEIampiMulti, being imported from another module'
  #_init_import() #se serve fare cose al momento dell'importazione
  #print 'finitoEIADAimport'
