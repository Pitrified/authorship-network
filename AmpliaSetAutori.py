#!python2

from timeit import default_timer as timer
import os
from os.path import abspath
from os.path import dirname
from os.path import join
import re
from EstraiIDAutoriDEIampiMulti import estraiIDautoriMulti
from EstraiPapAutAffDEImulti import estraiPapAutAffDEImulti
from EstraiPaperPerPaper import estraiPapAutAffPerPaper
from EstraiAutoriPerID import estraiAutoriPerID
from EstraiAffPadovaneVeloce import estraiAffPadovaneVeloce
from EstraiPaperPadovaniCompleti import estraiPaperPadovaniCompleti

def ampliaSetAutori(pfPersone, pfAuthorRAW, pftAutoriID, pfPapAutAffRAW, pftPAA, pfAffRAW, regAff, pfAffPad):
  # dai nomi estraggo gli IDaut del primo set
  pfAutoriID = pftAutoriID.format('_base')
  estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)

  # dagli IDaut estraggo pap-aut-aff
  pfPAA = pftPAA.format('_base')
  estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPAA)

  # amplio i paper
  pfPAAampliato = pftPAA.format('_ampliato')
  estraiPapAutAffPerPaper(pfPAA, pfPapAutAffRAW, pfPAAampliato)

  # carico papID-maxaut
  dIDpap = {} # { IDpap : max autore }
  with open(pfPAAampliato, 'rb') as fPAAampliato:
    for line in fPAAampliato:
      pezzi = line.rstrip().split('\t')
      papID = pezzi[0]
      progAut = int(pezzi[5])
      if papID in dIDpap:
        if progAut > dIDpap[papID]:
          dIDpap[papID] = progAut
      else:
        dIDpap[papID] = progAut
  # for papID in sorted(dIDpap, key=lambda x: dIDpap[x]) : print('{} {}'.format(papID, dIDpap[papID] ) )

  # riduco i paper scritti da troppi autori
  maxaut = 20
  pfPAAfiltrati = pftPAA.format('_filtrati')
  with open(pfPAAampliato, 'rb') as fPAAampliato, open(pfPAAfiltrati, 'wb') as fPAAfiltrati:
    for line in fPAAampliato:
      pezzi = line.rstrip().split('\t')
      papID = pezzi[0]
      if dIDpap[papID] < maxaut:
        fPAAfiltrati.write(line)

  # estraggo gli autori # se voglio li filtro
  sAutAmpliati = set()
  with open(pfPAAfiltrati, 'rb') as fPAAfiltrati:
    for line in fPAAfiltrati:
      pezzi = line.rstrip().split('\t')
      IDaut = pezzi[1]
      sAutAmpliati.add(IDaut)

  # scrivo gli id su un file
  pfSoloIDautore = pftAutoriID.format('_ID_filtrati')
  with open(pfSoloIDautore, 'wb') as fSoloIDautore:
    for autID in sAutAmpliati:
      fSoloIDautore.write('{}\r\n'.format(autID) )

  # cerco e scrivo TUTTI i nomi, anche i coautori mai visti
  pfAutoriIDampliati = pftAutoriID.format('_filtrati')
  estraiAutoriPerID(pfSoloIDautore, pfAuthorRAW, pfAutoriIDampliati)


  # filtro solo i paper padovani: troppo restrittivo perdo Bombi
  estraiAffPadovaneVeloce(pfAffRAW, pfAffPad, regAff)
  pfPAApad = pftPAA.format('_padovani')
  pfAutTutti = pfAutoriID
  pfAutPad = pftAutoriID.format('_padovani')
  estraiPaperPadovaniCompleti(pfPAAfiltrati, pfAffPad, pfAutTutti, pfPAApad, pfAutPad)

  # estraggo gli autori # se voglio li filtro
  sAutAmpliati = set()
  with open(pfPAApad, 'rb') as fPAApad:
    for line in fPAApad:
      pezzi = line.rstrip().split('\t')
      IDaut = pezzi[1]
      sAutAmpliati.add(IDaut)

  # scrivo gli id su un file
  pfSoloIDautore = pftAutoriID.format('_ID_pad')
  with open(pfSoloIDautore, 'wb') as fSoloIDautore:
    for autID in sAutAmpliati:
      fSoloIDautore.write('{}\r\n'.format(autID) )

  # cerco e scrivo TUTTI i nomi, anche i coautori mai visti
  pfAutoriIDampliati = pftAutoriID.format('_pad')
  estraiAutoriPerID(pfSoloIDautore, pfAuthorRAW, pfAutoriIDampliati)





def main():
  ctesi = abspath(join(__file__, '..', '..') )

  cfileRAW   = join(ctesi, 'FileRAW')
  pfAuthorRAW = join(cfileRAW, 'Authors.txt')
  pfPapAutAffRAW = join(cfileRAW, 'PaperAuthorAffiliations.txt')
  pfAffRAW = join(cfileRAW, 'Affiliations.txt')

  celaborati = join(ctesi, 'authorship-network', 'Versione5')
  sub = 'AmpliaSetBis'
  if not os.path.exists(join(celaborati, sub)): os.makedirs(join(celaborati, sub))

  tag = '_DEI'
  pfPersone = join(celaborati, 'PersoneNomi_apostolico{}.txt'.format(tag))
  pftAutoriID = join(celaborati, sub, 'AutoriID{{}}{}.txt'.format(tag))
  pftPAA = join(celaborati, sub, 'PaperAuthorAff{}.txt')
  pfAffPad = join(celaborati, sub, 'AffiliationPadovane.txt')
  print('\nChiamo estraiIDautoriMulti con\n\t{}\n\t{}\n\t{}'.format(pfPersone, pfAuthorRAW, pftAutoriID))
  print('\nChiamo estraiPapAutAffDEImulti con\n\t{}\n\t{}\n\t{}'.format(pftAutoriID, pfPapAutAffRAW, pftPAA))

  strRegAff = 'pad(ov|u)a'
  regAff = re.compile(strRegAff, re.IGNORECASE)

  start = timer()
  ampliaSetAutori(pfPersone, pfAuthorRAW, pftAutoriID, pfPapAutAffRAW, pftPAA, pfAffRAW, regAff, pfAffPad)
  end = timer()
  print 'Completato estraiIDautoriMulti in {}'.format(end-start)

if __name__ == '__main__':
  print 'This program is EstraiIDAutoriDEIampiMulti, being run by itself'
  main()
