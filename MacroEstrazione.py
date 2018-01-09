#!python2

from timeit import default_timer as timer



def singleCollab():
  import EstraiIDAutoriDEIampi as eaID
  import EstraiPapAutAffDEI as ePAAD
  import CreaEdgeCollab as cec
  import EstraiAutoriCollab as eac
  import CollassaNodiAmpi as cna
  from Verifiche_Test import PreparaPerGephi as ppg

  celaborati = 'Versione3_Single\\'
  # cfileRAW   = 'C:\Users\Test\Documents\Tesi\FileRAW\\'
  cfileRAW   = 'C:\Users\Pietro\Documents\University\Tesi\FileRAW\\'
  pfAuthorRAW = cfileRAW + 'Authors1000.txt'
  # pfAuthorRAW = cfileRAW + 'AuthorsDA0A1000000.txt'
  # pfAuthorRAW = cfileRAW + 'Authors.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations1000.txt'
  # pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations.txt'

  pfPersone    = celaborati + 'PersoneDEI.txt'
  pfAutoriID   = celaborati + 'AutoriDEIMacro.txt'
  pfPapAutAff  = celaborati + 'PapAutAffDEIMacro.txt'
  pfEdgeCollab = celaborati + 'EdgeCollabMacro.txt'
  pfAutCollab  = celaborati + 'AutoriCollabMacro.txt'
  pfEdgeCollabUnificati = celaborati + 'EdgeCollabUnificatiMacro.txt'
  pfAutCollabUnificati  = celaborati + 'AutoriCollabUnificatiMacro.txt'
  pfEdgeGephi  = celaborati + 'EdgeCollabUnificatiMacroGephi.tsv'
  pfAutGephi   = celaborati + 'AutoriCollabUnificatiMacroGephi.tsv'
    
  print('inizio single')
  ##in pfPersone ho una lista di nomi del dipartimento
  ##estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
  start = timer()
  sIDautDEI = eaID.estraiIDautori(pfPersone, pfAuthorRAW, pfAutoriID)
  #print 'setlen:{} set:{}'.format(len(sIDautDEI), sIDautDEI)
  lap1 = timer()
  print 'completato estraiIDautori in {}'.format(lap1 - start)

  ##estraggo i paper scritti da questi IDautDEI
  dPAA = ePAAD.estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff, sIDautDEI)
  #ePAAD.estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEI in {}'.format(lap2-lap1)

  ##estraggo gli EdgeCollab
  dEdgeCollab = cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab, dPAA)
  # cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap3 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

  ##estraggo gli AutoriCollab
  pfAutoriID = celaborati + 'AutoriDEIMacroFull.txt'    #dati completi per test
  pfEdgeCollab = celaborati + 'EdgeCollabMacroFull.txt'
  #eac.estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab, dEdgeCollab)
  eac.estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
  lap4 = timer()
  print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)

  ##collasso i nodi
  cna.collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
  # cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap5 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap5-lap4)

  ##preparo per gephi
  ppg.preparaPerGephi(pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)
  # cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap6 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap6-lap5)

  end = timer()
  print('completato single in {}'.format(end-start) )
  
  
def multiCollab():
  import EstraiIDAutoriDEIampiMulti as eaIDm
  import EstraiPapAutAffDEImulti as ePAADm
  import CreaEdgeCollab as cec
  import EstraiAutoriCollab as eac
  import CollassaNodiAmpi as cna
  from Verifiche_Test import PreparaPerGephi as ppg
  
  
  celaborati = 'Versione3_Multi\\'
  # cfileRAW   = 'C:\Users\Test\Documents\Tesi\FileRAW\\'
  cfileRAW   = 'C:\Users\Pietro\Documents\University\Tesi\FileRAW\\'
  pfAuthorRAW = cfileRAW + 'Authors1000.txt'
  # pfAuthorRAW = cfileRAW + 'AuthorsDA0A1000000.txt'
  # pfAuthorRAW = cfileRAW + 'Authors.txt'
  pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations1000.txt'
  # pfPapAutAffRAW = cfileRAW + 'PaperAuthorAffiliations.txt'

  pfPersone    = celaborati + 'PersoneDEI.txt'
  pfAutoriID   = celaborati + 'AutoriDEIMacro.txt'
  pfPapAutAff  = celaborati + 'PapAutAffDEIMacro.txt'
  pfEdgeCollab = celaborati + 'EdgeCollabMacro.txt'
  pfAutCollab  = celaborati + 'AutoriCollabMacro.txt'
  pfEdgeCollabUnificati = celaborati + 'EdgeCollabUnificatiMacro.txt'
  pfAutCollabUnificati  = celaborati + 'AutoriCollabUnificatiMacro.txt'
  pfEdgeGephi  = celaborati + 'EdgeCollabUnificatiMacroGephi.tsv'
  pfAutGephi   = celaborati + 'AutoriCollabUnificatiMacroGephi.tsv'
  
  
  print('inizio multi')
  ##in pfPersone ho una lista di nomi del dipartimento
  ##estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
  start = timer()
  sIDautDEI = eaIDm.estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)
  #print 'setlen:{} set:{}'.format(len(sIDautDEI), sIDautDEI)
  lap1 = timer()
  print 'completato estraiIDautori in {}'.format(lap1 - start)

  ##estraggo i paper scritti da questi IDautDEI
  pfAutoriID = celaborati + 'AutoriDEIMacroFull.txt'    #dati completi per test
  sIDautDEI = None    #ricalcola il set
  dPAA = ePAADm.estraiPapAutAffDEImulti(pfAutoriID, pfPapAutAffRAW, pfPapAutAff, sIDautDEI)
  #ePAADm.estraiPapAutAffDEI(pfAutoriID, pfPapAutAffRAW, pfPapAutAff)
  lap2 = timer()
  print 'completato estraiPapAutAffDEI in {}'.format(lap2-lap1)

  ##estraggo gli EdgeCollab
  pfPapAutAff = celaborati + 'PapAutAffDEImultiFull.txt'
  dPAA = None
  dEdgeCollab = cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab, dPAA)
  # cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap3 = timer()
  print 'completato creaEdgeCollab in {}'.format(lap3-lap2)

  ##estraggo gli AutoriCollab
  #pfEdgeCollab = celaborati + 'EdgeCollabMacroFull.txt'
  #eac.estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab, dEdgeCollab)
  eac.estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
  lap4 = timer()
  print 'completato estraiAutoriCollab in {}'.format(lap4-lap3)

  ##collasso i nodi
  cna.collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
  lap5 = timer()
  print 'completato collassaNodiAmpi in {}'.format(lap5-lap4)

  ##preparo per gephi
  ppg.preparaPerGephi(pfEdgeCollabUnificati, pfAutCollabUnificati, pfEdgeGephi, pfAutGephi)
  # cec.creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  lap6 = timer()
  print 'completato preparaPerGephi in {}'.format(lap6-lap5)

  end = timer()
  print('completato multi in {}'.format(end-start) )
  
  
def modulo():
  import AnalisiMSR as amsr

  celaborati = 'Versione3_Single\\'
  # celaborati = 'Versione3_Multi\\'
  # cfileRAW   = 'C:\Users\Test\Documents\Tesi\FileRAW\\'
  cfileRAW   = 'C:\Users\Pietro\Documents\University\Tesi\FileRAW\\'
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
  #import CreaEdgeCollab as cec
  from CreaEdgeCollab import creaEdgeCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  #from Verifiche_Test import PreparaPerGephi as ppg
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi
  
  
  celaborati = 'Versione3_Single\\'
  sub = 'Padovani\\'
  pfAffPad = 'PadovaPadua.txt'
  
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
  
  
  

if __name__ == '__main__':
  #singleCollab()
  #multiCollab()
  #modulo()
  singlePadova()
else:
  pass








