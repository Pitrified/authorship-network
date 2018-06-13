#!python2

from timeit import default_timer as timer
import os
from os.path import abspath
from os.path import dirname
from os.path import join
import re


def singleCollab():
  from EstraiIDAutoriDEIampi import estraiIDautori
  from EstraiPapAutAffDEI import estraiPapAutAffDEI
  import EstraiIDAutoriDEIampi as eaID
  import EstraiPapAutAffDEI as ePAAD
  from CreaEdgeCollab import creaEdgeCollab
  from EstraiAutoriCollab import estraiAutoriCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi

  celaborati = 'Versione3_Single\\'
  sub = 'Collab\\'
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  cfileRAW   = '..\FileRAW\\'
  pfAuthorRAW = cfileRAW + 'Authors1000.txt'
  # pfAuthorRAW = cfileRAW + 'AuthorsDA0A1000000.txt'
  # pfAuthorRAW = cfileRAW + 'Authors.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations1000.txt'
  # pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations.txt'

  pfPersone    = celaborati + 'PersoneDEI.txt'
  pfAutoriID   = celaborati + 'AutoriDEIMacro.txt'
  pfPapAutAff  = celaborati + 'PapAutAffDEIMacro.txt'
  pfEdgeCollab = celaborati + sub + 'EdgeCollabMacro.txt'
  pfAutCollab  = celaborati + sub + 'AutoriCollabMacro.txt'
  pfEdgeCollabUnificati = celaborati + sub + 'EdgeCollabUnificatiMacro.txt'
  pfAutCollabUnificati  = celaborati + sub + 'AutoriCollabUnificatiMacro.txt'
  pfEdgeGephi  = celaborati + sub + 'EdgeCollabUnificatiMacroGephi.tsv'
  pfAutGephi   = celaborati + sub + 'AutoriCollabUnificatiMacroGephi.tsv'

  print('inizio single')
  ##in pfPersone ho una lista di nomi del dipartimento
  ##estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
  start = timer()
  estraiIDautori(pfPersone, pfAuthorRAW, pfAutoriID)
  lap1 = timer()
  print 'completato estraiIDautori in {}'.format(lap1 - start)

  ##estraggo i paper scritti da questi IDautDEI
  pfAutoriID = celaborati + 'AutoriDEIMacroFull.txt'    #dati completi per test
  estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEI in {}'.format(lap2-lap1)

  ##estraggo gli EdgeCollab
  pfPapAutAff = celaborati + 'PapAutAffDEIMacroFull.txt'    #dati completi per test
  creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap3 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

  ##estraggo gli AutoriCollab
  estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
  lap4 = timer()
  print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)

  ##collasso i nodi
  collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
  lap5 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap5-lap4)

  ##preparo per gephi
  preparaPerGephi(pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)
  lap6 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap6-lap5)

  end = timer()
  print('completato single in {}'.format(end-start) )


def multiCollab():
  from EstraiIDAutoriDEIampiMulti import estraiIDautoriMulti
  from EstraiPapAutAffDEImulti import estraiPapAutAffDEImulti
  from CreaEdgeCollab import creaEdgeCollab
  from EstraiAutoriCollab import estraiAutoriCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi

  celaborati = 'Versione3_Multi\\'
  sub = 'Collab\\'
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  cfileRAW   = '..\FileRAW\\'
  pfAuthorRAW = cfileRAW + 'Authors1000.txt'
  # pfAuthorRAW = cfileRAW + 'AuthorsDA0A1000000.txt'
  # pfAuthorRAW = cfileRAW + 'Authors.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations1000.txt'
  # pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations.txt'

  tag = 'MC2'
  pfPersone    = celaborati + 'PersoneDEI.txt'
  pfAutoriID   = celaborati + 'AutoriDEI' + tag + '.txt'
  pfPapAutAff  = celaborati + 'PapAutAffDEI' + tag + '.txt'
  pfEdgeCollab = celaborati + sub + 'EdgeCollab' + tag + '.txt'
  pfAutCollab  = celaborati + sub + 'AutoriCollab' + tag + '.txt'
  pfEdgeCollabUnificati = celaborati + sub + 'EdgeCollabUnificati' + tag + '.txt'
  pfAutCollabUnificati  = celaborati + sub + 'AutoriCollabUnificati' + tag + '.txt'
  pfEdgeGephi  = celaborati + sub + 'EdgePadovaniUnificatiGephi' + tag + '.tsv'
  pfAutGephi   = celaborati + sub + 'AutoriPadovaniUnificatiGephi' + tag + '.tsv'

  print('inizio multiCollab')
  ##in pfPersone ho una lista di nomi del dipartimento
  ##estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
  start = timer()
  estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)
  lap1 = timer()
  print 'completato estraiIDautoriMulti in {}'.format(lap1 - start)

  ##estraggo i paper scritti da questi IDautDEI
  pfAutoriID = celaborati + 'AutoriDEIMacroFull.txt'    #dati completi per test
  estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEImulti in {}'.format(lap2-lap1)

  ##estraggo gli EdgeCollab
  pfPapAutAff = celaborati + 'PapAutAffDEImultiFull.txt'    #dati completi per test
  creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap3 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

  ##estraggo gli AutoriCollab
  estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
  lap4 = timer()
  print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)

  ##collasso i nodi
  collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
  lap5 = timer()
  print 'completato collassaNodiAmpi in {}'.format(lap5-lap4)

  ##preparo per gephi
  preparaPerGephi(pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)
  lap6 = timer()
  print 'completato preparaPerGephi in {}'.format(lap6-lap5)

  end = timer()
  print('completato multi in {}'.format(end-start) )


def modulo():
  import AnalisiMSR as amsr

  celaborati = 'Versione3_Single\\'
  # celaborati = 'Versione3_Multi\\'
  cfileRAW   = '..\FileRAW\\'
  pfAuthorRAW = cfileRAW + 'Authors1000.txt'
  # pfAuthorRAW = cfileRAW + 'AuthorsDA0A1000000.txt'
  # pfAuthorRAW = cfileRAW + 'Authors.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations1000.txt'
  # pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations.txt'

  pfPersone    = celaborati + 'PersoneDEI.txt'
  pfAutoriID   = celaborati + 'AutoriDEIMacroModulo.txt'
  pfPapAutAff  = celaborati + 'PapAutAffDEIMacroModulo.txt'
  pfEdgeCollab = celaborati + 'EdgeCollabMacroModulo.txt'
  pfAutCollab  = celaborati + 'AutoriCollabMacroModulo.txt'
  pfEdgeCollabUnificati = celaborati + 'EdgeCollabUnificatiMacroModulo.txt'
  pfAutCollabUnificati  = celaborati + 'AutoriCollabUnificatiMacroModulo.txt'
  pfEdgeGephi  = celaborati + 'EdgeCollabUnificatiMacroGephiModulo.tsv'
  pfAutGephi   = celaborati + 'AutoriCollabUnificatiMacroGephiModulo.tsv'

  print('inizio modulo')
  ##in pfPersone ho una lista di nomi del dipartimento
  ##estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
  start = timer()
  sIDautDEI = amsr.estraiIDautori(pfPersone, pfAuthorRAW, pfAutoriID)
  #print 'setlen:{} set:{}'.format(len(sIDautDEI), sIDautDEI)
  lap1 = timer()
  print 'completato estraiIDautori in {}'.format(lap1 - start)

  ##estraggo i paper scritti da questi IDautDEI
  pfAutoriID = celaborati + 'AutoriDEIMacroFull.txt'
  sIDautDEI = None    #ricalcola il set
  dPAA = amsr.estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff, sIDautDEI)
  #amsr.estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEI in {}'.format(lap2-lap1)

  ##estraggo gli EdgeCollab
  pfPapAutAff = celaborati + 'PapAutAffDEIMacroFull.txt'
  dPAA = None
  dEdgeCollab = amsr.creaEdgeCollab(pfPapAutAff, pfEdgeCollab, dPAA)
  # amsr.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap3 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

  ##estraggo gli AutoriCollab
  #pfEdgeCollab = celaborati + 'EdgeCollabMacroFull.txt'
  #amsr.estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab, dEdgeCollab)
  amsr.estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
  lap4 = timer()
  print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)

  ##collasso i nodi
  amsr.collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
  lap5 = timer()
  print 'completato collassaNodiAmpi in {}'.format(lap5-lap4)

  ##preparo per gephi
  amsr.preparaPerGephi(pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)
  lap6 = timer()
  print 'completato preparaPerGephi in {}'.format(lap6-lap5)

  end = timer()
  print('completato modulo in {}'.format(end-start) )


def singlePadova():
  from EstraiIDAutoriDEIampi import estraiIDautori
  from EstraiPapAutAffDEI import estraiPapAutAffDEI
  from EstraiPaperPadovaniCompleti import estraiPaperPadovaniCompleti
    #estrai paperpadovani per affiliazione se in PadovaPadua
      #(da PapAutAffDEI, devono comunque essere IDaut nella lista)
      #in eliminanonpadova.java
    #estrai autoripadovani
    #estrai paperpadovanicompleti
      #(da PapAutAffDEI prendo i paper scritti da IDaut con almeno un aff padovana)
  from CreaEdgeCollab import creaEdgeCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi

  celaborati = 'Versione3_Single\\'
  sub = 'Padovani\\'
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  pfAffPad = 'PadovaPadua.txt'
  cfileRAW   = '..\FileRAW\\'
  pfAuthorRAW = cfileRAW + 'Authors1000.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations1000.txt'

  pfPersone    = celaborati + 'PersoneDEI.txt'
  pfAutoriID   = celaborati + 'AutoriDEIMacroFull.txt'
  pfPapAutAff  = celaborati + 'PapAutAffDEIMacroFull.txt'
  pfPapPad = celaborati + sub + 'PaperPadovaniCompletiMacro.txt'
  pfAutPad = celaborati + sub + 'AutoriPadovaniMacro.txt'
  pfEdgePadovani = celaborati + sub + 'EdgePadovaniMacro.txt'
  pfEdgePadovaniUnificati = celaborati + sub + 'EdgePadovaniUnificatiMacro.txt'
  pfAutPadovaniUnificati  = celaborati + sub + 'AutoriPadovaniUnificatiMacro.txt'
  pfEdgeGephi  = celaborati + sub + 'EdgePadovaniUnificatiMacroGephi.tsv'
  pfAutGephi   = celaborati + sub + 'AutoriPadovaniUnificatiMacroGephi.tsv'

  #estraiIDautori(pfPersone, pfAuthorRAW, pfAutoriID)
  #estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  estraiPaperPadovaniCompleti(pfPapAutAff, pfAffPad, pfAutoriID, pfPapPad, pfAutPad)
  creaEdgeCollab(pfPapPad, pfEdgePadovani)
  collassaNodiAmpi(pfPersone, pfEdgePadovani, pfAutPad, pfEdgePadovaniUnificati, pfAutPadovaniUnificati)
  preparaPerGephi(pfEdgePadovaniUnificati, pfAutPadovaniUnificati, pfEdgeGephi, pfAutGephi)


def multiPadova():
  from EstraiIDAutoriDEIampiMulti import estraiIDautoriMulti
  from EstraiPapAutAffDEImulti import estraiPapAutAffDEImulti
  from EstraiPaperPadovaniCompleti import estraiPaperPadovaniCompleti
    #estrai paperpadovani per affiliazione se in PadovaPadua
      #(da PapAutAffDEI, devono comunque essere IDaut nella lista)
      #in eliminanonpadova.java
    #estrai autoripadovani
    #estrai paperpadovanicompleti
      #(da PapAutAffDEI prendo i paper scritti da IDaut con almeno un aff padovana)
  from CreaEdgeCollab import creaEdgeCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi

  celaborati = 'Versione3_Multi\\'
  sub = 'Padovani\\'
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  pfAffPad = 'PadovaPadua.txt'
  pfAffPad = 'Versione3_Multi\Amplia\AffiliationPadovaPadutaAlone.txt'
  cfileRAW   = '..\FileRAW\\'
  pfAuthorRAW = cfileRAW + 'Authors1000.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations1000.txt'

  tag = 'AffPP'
  pfPersone    = celaborati + 'PersoneDEI.txt'
  pfAutoriID   = celaborati + 'AutoriDEI' + tag + '.txt'
  pfPapAutAff  = celaborati + 'PapAutAffDEI' + tag + '.txt'
  pfPapPad = celaborati + sub + 'PaperPadovaniCompleti' + tag + '.txt'
  pfAutPad = celaborati + sub + 'AutoriPadovani' + tag + '.txt'
  pfEdgePadovani = celaborati + sub + 'EdgePadovani' + tag + '.txt'
  pfEdgePadovaniUnificati = celaborati + sub + 'EdgePadovaniUnificati' + tag + '.txt'
  pfAutPadovaniUnificati  = celaborati + sub + 'AutoriPadovaniUnificati' + tag + '.txt'
  pfEdgeGephi  = celaborati + sub + 'EdgePadovaniUnificatiGephi' + tag + '.tsv'
  pfAutGephi   = celaborati + sub + 'AutoriPadovaniUnificatiGephi' + tag + '.tsv'

  print('inizio multiPadova')
  start = timer()
  estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)
  lap1 = timer()
  print 'completato estraiIDautoriMulti in {}'.format(lap1 - start)

  pfAutoriID   = celaborati + 'AutoriDEIMacroFull.txt'                #tutti gli autori per test
  estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEImulti in {}'.format(lap2-lap1)

  pfPapAutAff  = celaborati + 'PapAutAffDEImultiFull.txt'             #tutti i paper per test
  estraiPaperPadovaniCompleti(pfPapAutAff, pfAffPad, pfAutoriID, pfPapPad, pfAutPad)
  lap3 = timer()
  print 'completato estraiPaperPadovaniCompleti in {}'.format(lap3-lap2)

  creaEdgeCollab(pfPapPad, pfEdgePadovani)
  lap4 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap4-lap3)

  collassaNodiAmpi(pfPersone, pfEdgePadovani, pfAutPad, pfEdgePadovaniUnificati, pfAutPadovaniUnificati)
  lap5 = timer()
  print 'completato collassaNodiAmpi in {}'.format(lap5-lap4)

  preparaPerGephi(pfEdgePadovaniUnificati, pfAutPadovaniUnificati, pfEdgeGephi, pfAutGephi)
  lap6 = timer()
  print 'completato preparaPerGephi in {}'.format(lap6-lap5)


def multiEstratti():
  from EstraiIDAutoriDEIampiMulti import estraiIDautoriMulti
  from EstraiPapAutAffDEImulti import estraiPapAutAffDEImulti
  from CreaEdgeCollab import creaEdgeCollab
  from EstraiAutoriCollab import estraiAutoriCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi

  celaborati = 'Versione3_Multi\\'
  sub = 'Amplia\\'
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  cfileRAW   = '..\FileRAW\\'
  pfAuthorRAW = cfileRAW + 'Authors1000.txt'
  # pfAuthorRAW = cfileRAW + 'AuthorsDA0A1000000.txt'
  # pfAuthorRAW = cfileRAW + 'Authors.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations1000.txt'
  # pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations.txt'

  tag = 'Estratti'
  # pfAutoriID   = celaborati + 'AutoriDEI' + tag + '.txt'
  pfPapAutAff  = celaborati + 'PapAutAffDEI' + tag + '.txt'
  pfEdgeCollab = celaborati + sub + 'EdgeCollab' + tag + '.txt'
  pfAutCollab  = celaborati + sub + 'AutoriCollab' + tag + '.txt'
  pfEdgeCollabUnificati = celaborati + sub + 'EdgeCollabUnificati' + tag + '.txt'
  pfAutCollabUnificati  = celaborati + sub + 'AutoriCollabUnificati' + tag + '.txt'
  pfEdgeGephi  = celaborati + sub + 'EdgePadovaniUnificatiGephi' + tag + '.tsv'
  pfAutGephi   = celaborati + sub + 'AutoriPadovaniUnificatiGephi' + tag + '.tsv'

  print('inizio multiEstratti')
  lap1 = timer()
  ##estraggo i paper scritti da questi IDaut
  pfAutoriID = celaborati + sub + 'AutEstrattiFulll.txt'    #dati completi per test
  estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEImulti in {}'.format(lap2-lap1)

  ##estraggo gli EdgeCollab
  # pfPapAutAff = celaborati + 'PapAutAffDEImultiFull.txt'    #dati completi per test
  creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap3 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

  ##estraggo gli AutoriCollab
  estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
  lap4 = timer()
  print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)

  ##collasso i nodi
  collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
  lap5 = timer()
  print 'completato collassaNodiAmpi in {}'.format(lap5-lap4)

  ##preparo per gephi
  preparaPerGephi(pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)
  lap6 = timer()
  print 'completato preparaPerGephi in {}'.format(lap6-lap5)

  end = timer()
  print('completato multi in {}'.format(end-start) )


def multiCollabSPGI():
  from EstraiIDAutoriDEIampiMulti import estraiIDautoriMulti
  from EstraiPapAutAffDEImulti import estraiPapAutAffDEImulti
  from CreaEdgeCollab import creaEdgeCollab
  from EstraiAutoriCollab import estraiAutoriCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi

  celaborati = 'Versione3_Multi\\'
  sub = 'Collab\\'
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  cfileRAW   = '..\FileRAW\\'
  # pfAuthorRAW = cfileRAW + 'Authors1000.txt'
  # pfAuthorRAW = cfileRAW + 'AuthorsDA0A1000000.txt'
  pfAuthorRAW = cfileRAW + 'Authors.txt'
  # pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations1000.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations.txt'

  tag = 'SPGI'
  pfPersone    = celaborati + 'PersoneNomi' + tag + '.txt'
  pfAutoriID   = celaborati + 'AutoriID' + tag + '.txt'
  pfPapAutAff  = celaborati + 'PapAutAff' + tag + '.txt'
  pfEdgeCollab = celaborati + sub + 'EdgeCollab' + tag + '.txt'
  pfAutCollab  = celaborati + sub + 'AutoriCollab' + tag + '.txt'
  pfEdgeCollabUnificati = celaborati + sub + 'EdgeCollabUnificati' + tag + '.txt'
  pfAutCollabUnificati  = celaborati + sub + 'AutoriCollabUnificati' + tag + '.txt'
  pfEdgeGephi  = celaborati + sub + 'EdgeUnificatiGephi' + tag + '.tsv'
  pfAutGephi   = celaborati + sub + 'AutoriUnificatiGephi' + tag + '.tsv'

  print('inizio multiCollabCTF')
  ##in pfPersone ho una lista di nomi del dipartimento
  ##estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
  start = timer()
  estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)
  lap1 = timer()
  print 'completato estraiIDautoriMulti in {}'.format(lap1 - start)

  ##estraggo i paper scritti da questi IDautDEI
  estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEImulti in {}'.format(lap2-lap1)

  ##estraggo gli EdgeCollab
  creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap3 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

  ##estraggo gli AutoriCollab
  estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
  lap4 = timer()
  print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)

  ##collasso i nodi
  collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
  lap5 = timer()
  print 'completato collassaNodiAmpi in {}'.format(lap5-lap4)

  ##preparo per gephi
  preparaPerGephi(pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)
  lap6 = timer()
  print 'completato preparaPerGephi in {}'.format(lap6-lap5)

  end = timer()
  print('completato multi in {}'.format(end-start) )


def multiPadovaSPGI():
  from EstraiIDAutoriDEIampiMulti import estraiIDautoriMulti
  from EstraiPapAutAffDEImulti import estraiPapAutAffDEImulti
  from EstraiPaperPadovaniCompleti import estraiPaperPadovaniCompleti
    #estrai paperpadovani per affiliazione se in PadovaPadua
      #(da PapAutAffDEI, devono comunque essere IDaut nella lista)
      #in eliminanonpadova.java
    #estrai autoripadovani
    #estrai paperpadovanicompleti
      #(da PapAutAffDEI prendo i paper scritti da IDaut con almeno un aff padovana)
  from CreaEdgeCollab import creaEdgeCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi

  celaborati = 'Versione3_Multi\\'
  sub = 'Padovani\\'
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  pfAffPad = 'PadovaPadua.txt'
  pfAffPad = 'Versione3_Multi\Amplia\AffiliationPadovaPadutaAlone.txt'
  cfileRAW   = '..\FileRAW\\'
  pfAuthorRAW = cfileRAW + 'Authors.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations.txt'

  tag = 'SPGIpad'
  pfPersone    = celaborati + 'PersoneNomi' + tag + '.txt'
  pfAutoriID   = celaborati + 'Autori' + tag + '.txt'
  pfPapAutAff  = celaborati + 'PapAutAff' + tag + '.txt'
  pfPapPad = celaborati + sub + 'PaperPadovaniCompleti' + tag + '.txt'
  pfAutPad = celaborati + sub + 'AutoriPadovani' + tag + '.txt'
  pfEdgePadovani = celaborati + sub + 'EdgePadovani' + tag + '.txt'
  pfEdgePadovaniUnificati = celaborati + sub + 'EdgePadovaniUnificati' + tag + '.txt'
  pfAutPadovaniUnificati  = celaborati + sub + 'AutoriPadovaniUnificati' + tag + '.txt'
  pfEdgeGephi  = celaborati + sub + 'EdgePadovaniUnificatiGephi' + tag + '.tsv'
  pfAutGephi   = celaborati + sub + 'AutoriPadovaniUnificatiGephi' + tag + '.tsv'

  print('inizio multiPadova')
  start = timer()
  estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)
  lap1 = timer()
  print 'completato estraiIDautoriMulti in {}'.format(lap1 - start)

  # pfAutoriID   = celaborati + 'AutoriDEIMacroFull.txt'                #tutti gli autori per test
  estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEImulti in {}'.format(lap2-lap1)

  # pfPapAutAff  = celaborati + 'PapAutAffDEImultiFull.txt'             #tutti i paper per test
  estraiPaperPadovaniCompleti(pfPapAutAff, pfAffPad, pfAutoriID, pfPapPad, pfAutPad)
  lap3 = timer()
  print 'completato estraiPaperPadovaniCompleti in {}'.format(lap3-lap2)

  creaEdgeCollab(pfPapPad, pfEdgePadovani)
  lap4 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap4-lap3)

  collassaNodiAmpi(pfPersone, pfEdgePadovani, pfAutPad, pfEdgePadovaniUnificati, pfAutPadovaniUnificati)
  lap5 = timer()
  print 'completato collassaNodiAmpi in {}'.format(lap5-lap4)

  preparaPerGephi(pfEdgePadovaniUnificati, pfAutPadovaniUnificati, pfEdgeGephi, pfAutGephi)
  lap6 = timer()
  print 'completato preparaPerGephi in {}'.format(lap6-lap5)


def multiProvaUpd():
  from EstraiIDAutoriDEIampiMulti import estraiIDautoriMulti
  from EstraiPapAutAffDEImulti import estraiPapAutAffDEImulti
  from CreaEdgeCollab import creaEdgeCollab
  from EstraiAutoriCollab import estraiAutoriCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi

  # celaborati = 'Versione3_Upd\\'
  celaborati = 'Versione3_Upd/'
  sub = ''
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  cfileRAW   = celaborati
  pfAuthorRAW = cfileRAW + 'Authors.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations.txt'

  tag = 'UPD'
  pfPersone    = celaborati + sub + 'PersoneNomi' + tag + '.txt'
  pfAutoriID   = celaborati + sub + 'AutoriID' + tag + '.txt'
  pfPapAutAff  = celaborati + sub + 'PapAutAff' + tag + '.txt'
  pfEdgeCollab = celaborati + sub + 'EdgeCollab' + tag + '.txt'
  pfAutCollab  = celaborati + sub + 'AutoriCollab' + tag + '.txt'
  pfEdgeCollabUnificati = celaborati + sub + 'EdgeCollabUnificati' + tag + '.txt'
  pfAutCollabUnificati  = celaborati + sub + 'AutoriCollabUnificati' + tag + '.txt'
  pfEdgeGephi  = celaborati + sub + 'EdgeUnificatiGephi' + tag + '.tsv'
  pfAutGephi   = celaborati + sub + 'AutoriUnificatiGephi' + tag + '.tsv'

  print('inizio multiCollab'+tag)
  ##in pfPersone ho una lista di nomi del dipartimento
  ##estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
  start = timer()
  estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)
  lap1 = timer()
  print 'completato estraiIDautoriMulti in {}'.format(lap1 - start)

  ##estraggo i paper scritti da questi IDautDEI
  estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEImulti in {}'.format(lap2-lap1)

  ##estraggo gli EdgeCollab
  creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap3 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

  ##estraggo gli AutoriCollab
  estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
  lap4 = timer()
  print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)

  ##collasso i nodi
  collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
  lap5 = timer()
  print 'completato collassaNodiAmpi in {}'.format(lap5-lap4)

  ##preparo per gephi
  preparaPerGephi(pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)
  lap6 = timer()
  print 'completato preparaPerGephi in {}'.format(lap6-lap5)

  end = timer()
  print('completato multi in {}'.format(end-start) )


def collassaNodiIteratoSolo():
  from EstraiIDAutoriDEIampiMulti import estraiIDautoriMulti
  from EstraiPapAutAffDEImulti import estraiPapAutAffDEImulti
  from CreaEdgeCollab import creaEdgeCollab
  from EstraiAutoriCollab import estraiAutoriCollab

  # from CollassaNodiAmpi import collassaNodiAmpi
  # from Verifiche_Test.PreparaPerGephi import preparaPerGephi

  aut =  dirname(__file__)
  tesi = dirname(aut)
  celaborati = 'Versione4_Short'
  sub = ''
  direlab = join(aut, celaborati)
  dirsub = join(aut, celaborati, sub)
  # for c in (aut, tesi, direlab, dirsub): print c
  cfileRAW = 'FileRAW'
  pfAuthorRAW = join(tesi, cfileRAW, 'Authors.txt')
  pfPapAutAffRAW = join(tesi, cfileRAW, 'PaperAuthorAffiliations.txt')

  tag = 'DEI'
  pfPersone = join(direlab, 'PersoneNomi' + tag + '.txt')
  pfAutoriID = join(direlab, 'AutoriID' + tag + '.txt')
  pfPapAutAff = join(direlab, 'PapAutAff' + tag + '.txt')

  pfEdgeCollab = join(dirsub, 'EdgeCollab' + tag + '.txt')
  pfAutCollab = join(dirsub, 'AutoriCollab' + tag + '.txt')

  print('inizio multiCollab'+tag)
  ##in pfPersone ho una lista di nomi del dipartimento
  ##estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
  start = timer()
  # estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)
  lap1 = timer()
  print 'completato estraiIDautoriMulti in {}'.format(lap1 - start)

  ##estraggo i paper scritti da questi IDautDEI
  # estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEImulti in {}'.format(lap2-lap1)

  ##estraggo gli EdgeCollab
  creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap3 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

  ##estraggo gli AutoriCollab
  estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
  lap4 = timer()
  print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)


def multiGiugno():
  from EstraiIDAutoriDEIampiMulti import estraiIDautoriMulti
  from EstraiPapAutAffDEImulti import estraiPapAutAffDEImulti
  from CreaEdgeCollab import creaEdgeCollab
  from EstraiAutoriCollab import estraiAutoriCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi

  # celaborati = 'Versione3_Upd\\'
  celaborati = 'Versione3_Giu'
  sub = ''
  if not os.path.exists(join(celaborati, sub)): os.makedirs(join(celaborati, sub))
  cfileRAW   = join('..', 'FileRAW') +'\\'
  print(cfileRAW)
  pfAuthorRAW = cfileRAW + 'Authors.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations.txt'

  tag = 'GIU'
  pfPersone    = join(celaborati, sub, 'PersoneNomi{}.txt'.format(tag))
  pfAutoriID   = join(celaborati, sub, 'AutoriID{}.txt'.format(tag))
  pfPapAutAff  = join(celaborati, sub, 'PapAutAff{}.txt'.format(tag))
  pfEdgeCollab = join(celaborati, sub, 'EdgeCollab{}.txt'.format(tag))
  pfAutCollab  = join(celaborati, sub, 'AutoriCollab{}.txt'.format(tag))
  pfEdgeCollabUnificati = join(celaborati, sub, 'EdgeCollabUnificati{}.txt'.format(tag))
  pfAutCollabUnificati  = join(celaborati, sub, 'AutoriCollabUnificati{}.txt'.format(tag))
  pfEdgeGephi  = join(celaborati, sub, 'EdgeUnificatiGephi{}.tsv'.format(tag))
  pfAutGephi   = join(celaborati, sub, 'AutoriUnificatiGephi{}.tsv'.format(tag))

  print('inizio multiCollab'+tag)
  start = timer()

  ##in pfPersone ho una lista di nomi del dipartimento
  ##estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
  estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)
  lap1 = timer()
  print 'completato estraiIDautoriMulti in {}'.format(lap1 - start)

  ##estraggo i paper scritti da questi IDautDEI
  estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEImulti in {}'.format(lap2-lap1)

  ##estraggo gli EdgeCollab
  creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap3 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

  ##estraggo gli AutoriCollab
  estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
  lap4 = timer()
  print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)

  ##collasso i nodi
  collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
  lap5 = timer()
  print 'completato collassaNodiAmpi in {}'.format(lap5-lap4)

  ##preparo per gephi
  preparaPerGephi(pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)
  lap6 = timer()
  print 'completato preparaPerGephi in {}'.format(lap6-lap5)

  end = timer()
  print('completato multi in {}'.format(end-start) )


def esplorazioneTotale():
  from EstraiIDAutoriDEIampiMulti import estraiIDautoriMulti
  from EstraiPapAutAffDEImulti import estraiPapAutAffDEImulti
  from EstraiAffPadovaneVeloce import estraiAffPadovaneVeloce
  from EstraiPaperPadovaniCompleti import estraiPaperPadovaniCompleti
  from CreaEdgeCollab import creaEdgeCollab
  from EstraiAutoriCollab import estraiAutoriCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  from CollassaNodiShortPathSort import collassaNodiShortPath
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi
  from Verifiche_Test.PreparaPerSNAP import preparaPerSNAP
  from AnalizzaSnap import analizzaGirvanNewman
  from MergeComSito import comunitaMergeAnalizza

  ctesi = abspath(join(__file__, '..', '..') )
  celaborati = join(ctesi, 'authorship-network', 'Versione4_Totale')
  sub = 'Quarta'

  if not os.path.exists(join(celaborati, sub)): os.makedirs(join(celaborati, sub))
  cfileRAW   = join(ctesi, 'FileRAW')
  pfAuthorRAW = join(cfileRAW, 'Authors.txt')
  pfPapAutAffRAW = join(cfileRAW, 'PaperAuthorAffiliations.txt')
  pfAffRAW = join(cfileRAW, 'Affiliations.txt')
  pfAuthorRAW = join(cfileRAW, 'Authors1000000.txt')
  pfPapAutAffRAW = join(cfileRAW, 'PaperAuthorAffiliations5000000.txt')

  tag = '_DEI'
  # pfPersone    = join(celaborati, sub, 'PersoneNomi{}.txt'.format(tag))
  pfPersone    = join(celaborati, 'PersoneNomi{}.txt'.format(tag))
  pfAbbreviate = join(celaborati, 'PersoneNomiComunitaAbbreviate{}.txt'.format(tag))
  pfAutoriID   = join(celaborati, sub, 'AutoriID{}.txt'.format(tag))
  # pfPapAutAff  = join(celaborati, sub, 'PapAutAff{}.txt'.format(tag))
  # pfEdgeCollab = join(celaborati, sub, 'EdgeCollab{}.txt'.format(tag))
  # pfAutCollab  = join(celaborati, sub, 'AutoriCollab{}.txt'.format(tag))
  # pfEdgeCollabUnificati = join(celaborati, sub, 'EdgeCollabUnificati{}.txt'.format(tag))
  # pfAutCollabUnificati  = join(celaborati, sub, 'AutoriCollabUnificati{}.txt'.format(tag))
  # pfEdgeGephi  = join(celaborati, sub, 'EdgeUnificatiGephi{}.tsv'.format(tag))
  # pfAutGephi   = join(celaborati, sub, 'AutoriUnificatiGephi{}.tsv'.format(tag))

  pftPapAutAff = join(celaborati, sub, 'PapAutAff{}{}.txt'.format('{}', tag))
  pftEdgeCollab = join(celaborati, sub, 'EdgeCollab{}{}.txt'.format('{}', tag))
  pftAutCollab  = join(celaborati, sub, 'AutoriCollab{}{}.txt'.format('{}', tag))
  pftEdgeCollabUnificati = join(celaborati, sub, 'EdgeCollabUnificati{}{}{}.txt'.format('{}', '{}', tag))
  pftAutCollabUnificati  = join(celaborati, sub, 'AutoriCollabUnificati{}{}{}.txt'.format('{}', '{}', tag))
  pftAutNumNome = join(celaborati, sub, 'AutoriCollabIdNumNome{}{}{}.txt'.format('{}', '{}', tag))
  pftPaj = join(celaborati, sub, 'AutoriEdgeCollab{}{}{}.paj'.format('{}', '{}', tag))
  pftGT = join(celaborati, sub, 'AutoriEdgeCollab{}{}{}_GT.tsv'.format('{}', '{}', tag))
  pftEdgeGephi  = join(celaborati, sub, 'EdgeUnificatiGephi{}{}{}.tsv'.format('{}', '{}', tag))
  pftAutGephi   = join(celaborati, sub, 'AutoriUnificatiGephi{}{}{}.tsv'.format('{}', '{}', tag))
  pftGrafoOut = join(celaborati, sub, 'Grafo{}{}{}{}.pdf'.format('{}', '{}', '{}', tag))
  pftClassi = join(celaborati, sub, 'Comunita{}{}{}{}.tsv'.format('{}', '{}', '{}', tag))
  pftMerge = join(celaborati, sub, 'AutoriMergeComunita{}{}{}{}.tsv'.format('{}', '{}', '{}', tag))
  pftFreq = join(celaborati, sub, 'ComunitaMergeFrequenza{}{}{}{}.tsv'.format('{}', '{}', '{}', tag))
  pfAffPad = join(celaborati, sub, 'AffiliationPadovaPadua.txt'.format())
  pfAutPad = join(celaborati, sub, 'AutoriPadovanichehannoscrittopaper.txt'.format())

  maxhops = 2
  strRegAff = 'pad(ov|u)a'
  regAff = re.compile(strRegAff, re.IGNORECASE)

  sceltePadova = ['_tutti', '_padovani']
  scelteUnione = ['_nomi', '_distanza']
  scelteComunita = ['_girvneu'] # , '_blockmodel'] # _blk lo aggiungo solo se GT funziona
  blockmodel = '_blockmodel'

  # print('Chiamo con \n\t{}'.format())

  print('Inizio l\'esplorazione totale {} {} {}'.format(celaborati, sub, tag))
  start = timer()

  # in pfPersone ho una lista di nomi del dipartimento
  # estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
  # print('\nChiamo estraiIDautoriMulti con\n\t{}\n\t{}\n\t{}'.format(pfPersone, pfAuthorRAW, pfAutoriID))
  estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)
  lap1 = timer()
  print 'completato estraiIDautoriMulti in {}'.format(lap1 - start)

  # AutoriID come se fossero estratti dall'intero file Authors.txt
  PFAUTORIIDPERTEST = join(celaborati, sub, 'AutoriID_FULLTEST.txt'.format())
  pfAutoriID = PFAUTORIIDPERTEST

  # estraggo i paper scritti da questi IDautDEI
  pfPAAtut = pftPapAutAff.format(sceltePadova[0])
  # print('\nChiamo estraiPapAutAffDEImulti con \n\t{}\n\t{}\n\t{}'.format( pfAutoriID, pfPapAutAffRAW, pfPAAtut))
  estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPAAtut)
  lap2 = timer()
  print 'completato estraiPapAutAffDEImulti in {}'.format(lap2-lap1)

  # estraggo le affiliation padovane
  # print('\nChiamo estraiAffPadovaneVeloce con \n\t{}\n\t{}\n\t{}'.format( pfAffRAW, pfAffPad, strRegAff))
  estraiAffPadovaneVeloce(pfAffRAW, pfAffPad, regAff)
  lap225 = timer()
  print('completato estraiAffPadovaneVeloce in {}'.format(lap225 - lap2) )

  # PapAutAff come se fossero estratti dal file completo
  PFTPAATUTPERTEST = join(celaborati, sub, 'PapAutAff{}{}.txt'.format('{}', '_FULLTEST'))
  pftPapAutAff = PFTPAATUTPERTEST

  # estraggo i paper con affiliation padovana
  pfPAAtut = pftPapAutAff.format(sceltePadova[0])
  pfPAApad = pftPapAutAff.format(sceltePadova[1])
  # print('\nChiamo estraiPaperPadovaniCompleti con \n\t{}\n\t{}\n\t{}\n\t{}\n\t{}'.format( pfPAAtut, pfAffPad, pfAutoriID, pfPAApad, pfAutPad ))
  estraiPaperPadovaniCompleti(pfPAAtut, pfAffPad, pfAutoriID, pfPAApad, pfAutPad)
  lap25 = timer()
  print('completato estraiPaperPadovaniCompleti in {}'.format(lap25 - lap2) )

  for sp in sceltePadova:
    print('\nInizio {}'.format(sp))
    pfPAA = pftPapAutAff.format(sp)
    pfEdgeCollab = pftEdgeCollab.format(sp)
    pfAutCollab = pftAutCollab.format(sp)

    # creo gli edge ed estraggo gli autori
    # print('\nChiamo creaEdgeCollab con \n\t{}\n\t{}'.format( pfPAA, pfEdgeCollab))
    creaEdgeCollab(pfPAA, pfEdgeCollab)
    # print('\nChiamo estraiAutoriCollab con \n\t{}\n\t{}\n\t{}'.format( pfAutoriID, pfEdgeCollab, pfAutCollab))
    estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)

    # collasso i nomi basandomi su nomi ed abbreviazioni
    pfEdgeCollabUnificati = pftEdgeCollabUnificati.format(sp, scelteUnione[0])
    pfAutCollabUnificati = pftAutCollabUnificati.format(sp, scelteUnione[0])
    # print('\nChiamo collassaNodiAmpi con \n\t{}\n\t{}\n\t{}\n\t{}\n\t{}'.format(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati))
    collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)

    # formatto i dati per SNAP e per GT
    pfPaj = pftPaj.format(sp, '')
    pfAutNumNome = pftAutNumNome.format(sp, '')
    pfGT = pftGT.format(sp, '')
    # print('\nChiamo preparaPerSNAP con \n\t{}\n\t{}\n\t{}\n\t{}\n\t{}'.format( pfEdgeCollab, pfAutCollab, pfPaj, pfAutNumNome, pfGT) )
    preparaPerSNAP(pfEdgeCollab, pfAutCollab, pfPaj, pfAutNumNome, pfGT)

    # collasso i nomi basandomi sulle distanze
    pfEdgeCollabUnificati = pftEdgeCollabUnificati.format(sp, scelteUnione[1])
    pfAutCollabUnificati = pftAutCollabUnificati.format(sp, scelteUnione[1])
    # print('\nChiamo collassaNodiShortPath con \n\t{}\n\t{}\n\t{}\n\t{}\n\tDistanza massima tra autori {}'.format( pfAutNumNome, pfPaj, pfEdgeCollabUnificati, pfAutCollabUnificati, maxhops) )
    collassaNodiShortPath(pfAutNumNome, pfPaj, pfEdgeCollabUnificati, pfAutCollabUnificati, maxhops)


    for su in scelteUnione:
      print('\nInizio {} {}'.format(sp, su))
      # preparo per Gephi
      pfEdgeCollabUnificati = pftEdgeCollabUnificati.format(sp, su)
      pfAutCollabUnificati = pftAutCollabUnificati.format(sp, su)
      pfEdgeGephi = pftEdgeGephi.format(sp, su)
      pfAutGephi = pftAutGephi.format(sp, su)
      # print('\nChiamo preparaPerGephi con \n\t{}\n\t{}\n\t{}\n\t{}'.format( pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi))
      preparaPerGephi( pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)

      # preparo per GT e SNAP
      pfPaj = pftPaj.format(sp, su)
      pfAutNumNome = pftAutNumNome.format(sp, su)
      pfGT = pftGT.format(sp, su)
      # print('\nChiamo preparaPerSNAP con \n\t{}\n\t{}\n\t{}\n\t{}\n\t{}'.format( pfEdgeCollab, pfAutCollab, pfPaj, pfAutNumNome, pfGT) )
      preparaPerSNAP(pfEdgeCollab, pfAutCollab, pfPaj, pfAutNumNome, pfGT)

      # con pIPajek genero comunita, ho il file pfPaj pronto da mangiare
      # pfPaj = ce l'ho gia'
      # pfAINN = # e' pfAutNumNome # ID e Numero e Nome
      pfClassi = pftClassi.format(sp, su, scelteComunita[0]) # file com di SNAP
      lapgns = timer()
      # print('\nChiamo analizzaGirvanNewman con \n\t{}\n\t{}\n\t{}'.format(pfPaj, pfAutNumNome, pfClassi) )
      analizzaGirvanNewman(pfPaj, pfAutNumNome, pfClassi)
      lapgne = timer()
      print('Completato analizzaGirvanNewman in {}'.format(lapgne - lapgns) )

      # disegno i grafi
      # TODO potrei colorarli con le varie comunita generate nei vari modi
      try:
        from DisegnaGrafoGT import disegnaGrafo
        # blockmodel = '_blockmodel'
        if blockmodel not in scelteComunita:
          scelteComunita.append(blockmodel)
        pfGrafoOut = pftGrafoOut.format(sp, su, blockmodel)
        pfClassi = pftClassi.format(sp, su, blockmodel)
        lapgts = timer()
        # print('\nChiamo disegnaGrafo con \n\t{}\n\t{}\n\t{}'.format(pfGT, pfGrafoOut, pfClassi) )
        disegnaGrafo(pfGT, pfGrafoOut, pfClassi)
        lapgte = timer()
        print('Completato disegnaGrafo in {}'.format(lapgte - lapgts) )
      except ImportError:
        print('Ti serve graph_tool, usa Linux')
      except:
        raise

      # analizzo le frequenze delle comunita generate da SNAP e da GT
      for sc in scelteComunita:
        print('Inizio {} {} {}'.format(sp, su, sc) )
  # pfAbbreviate = 'PersoneNomiComunitaAbbreviate{}.txt'.format(tag)
        pfClassi = pftClassi.format(sp, su, sc) # 'AutoriCollabClasse_padovani_distanza.tsv'
        pfMerge = pftMerge.format(sp, su, sc) # 'AutoriCollabClasseMergeComunita_padovani_distanza.tsv'
        pfFreq = pftFreq.format(sp, su, sc) # 'FrequenzaMergeComunita_padovani_distanza.tsv'

        comunitaMergeAnalizza(pfClassi, pfAbbreviate, pfMerge, pfFreq)


  end = timer()
  print('Completata l\'esplorazione in {} s'.format(end-start) )


if __name__ == '__main__':
  # singleCollab()
  # multiCollab()
  # modulo()
  # singlePadova()
  # multiPadova()
  # multiPadovaSPGI()
  # multiEstratti()
  # multiCollabCTF()
  # multiProvaUpd()
  # collassaNodiIteratoSolo()
  # multiGiugno()
  esplorazioneTotale()

