#!python2

from timeit import default_timer as timer
import os
from os.path import abspath
from os.path import dirname
from os.path import join
import re

def esplorazioneTotale():
  from EstraiIDAutoriDEIampiMulti import estraiIDautoriMulti
  from EstraiPapAutAffDEImulti import estraiPapAutAffDEImulti
  from EstraiAffPadovaneVeloce import estraiAffPadovaneVeloce
  from EstraiPaperPadovaniCompleti import estraiPaperPadovaniCompleti
  from CreaEdgeCollab import creaEdgeCollab
  from EstraiAutoriCollab import estraiAutoriCollab
  from CollassaNodiAmpi import collassaNodiAmpi
  from CollassaNodiShortPathSort import collassaNodiShortPath
  from CollassaNodiEdge import collassaNodiEdge
  from Verifiche_Test.PreparaPerGephi import preparaPerGephi
  from Verifiche_Test.PreparaPerSNAP import preparaPerSNAP, preparaGC
  from AnalizzaSnap import analizzaGirvanNewman, analizzaClausetNewmanMoore
  from MergeComSito import comunitaMergeAnalizza
  from GraficaFrequenze import graficaFrequenzePerSito, graficaFrequenzePerGenerate
  from sklearn.metrics import homogeneity_completeness_v_measure
  from validazione import getComClu, aggregaValidazione

  ctesi = abspath(join(__file__, '..', '..') )
  celaborati = join(ctesi, 'authorship-network', 'Versione5')
  sub = 'Quinta'

  if not os.path.exists(join(celaborati, sub)): os.makedirs(join(celaborati, sub))
  cfileRAW   = join(ctesi, 'FileRAW')
  pfAuthorRAW = join(cfileRAW, 'Authors.txt')
  pfPapAutAffRAW = join(cfileRAW, 'PaperAuthorAffiliations.txt')
  pfAffRAW = join(cfileRAW, 'Affiliations.txt')
  # TEST
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
  subautedge = 'AutoriEdge'
  if not os.path.exists(join(celaborati, sub, subautedge) ): os.makedirs(join(celaborati, sub, subautedge))
  pftEdgeCollab = join(celaborati, sub, subautedge, 'EdgeCollab{}{}.txt'.format('{}', tag))
  pftAutCollab  = join(celaborati, sub, subautedge, 'AutoriCollab{}{}.txt'.format('{}', tag))
  pftEdgeCollabUnificati = join(celaborati, sub, subautedge, 'EdgeCollabUnificati{}{}{}.txt'.format('{}', '{}', tag))
  pftAutCollabUnificati  = join(celaborati, sub, subautedge, 'AutoriCollabUnificati{}{}{}.txt'.format('{}', '{}', tag))
  pftAutNumNome = join(celaborati, sub, subautedge, 'AutoriCollabIdNumNome{}{}{}.txt'.format('{}', '{}', tag))
  pftAutNumNomeGC = join(celaborati, sub, subautedge, 'AutoriCollabIdNumNome{}{}_GC{}.txt'.format('{}', '{}', tag))
  pftPaj = join(celaborati, sub, subautedge, 'AutoriEdgeCollab{}{}{}.paj'.format('{}', '{}', tag))
  pftPajGC = join(celaborati, sub, subautedge, 'AutoriEdgeCollab{}{}_GC{}.paj'.format('{}', '{}', tag))
  pftGT = join(celaborati, sub, subautedge, 'AutoriEdgeCollab{}{}{}_GT.tsv'.format('{}', '{}', tag))
  pftGTGC = join(celaborati, sub, subautedge, 'AutoriEdgeCollab{}{}_GC{}_GT.tsv'.format('{}', '{}', tag))
  pftEdgeGephi  = join(celaborati, sub, subautedge, 'EdgeUnificatiGephi{}{}{}.tsv'.format('{}', '{}', tag))
  pftAutGephi   = join(celaborati, sub, subautedge, 'AutoriUnificatiGephi{}{}{}.tsv'.format('{}', '{}', tag))
  pftGrafoOut = join(celaborati, sub, 'Grafo{}{}{}{}.pdf'.format('{}', '{}', '{}', tag))
  subcom = 'Comunita'
  if not os.path.exists(join(celaborati, sub, subcom) ): os.makedirs(join(celaborati, sub, subcom))
  pftClassi = join(celaborati, sub, subcom, 'Comunita{}{}{}{}.tsv'.format('{}', '{}', '{}', tag))
  pftMerge = join(celaborati, sub, subautedge, 'AutoriMergeComunita{}{}{}{}.tsv'.format('{}', '{}', '{}', tag))
  pftFreq = join(celaborati, sub, subcom, 'ComunitaMergeFrequenza{}{}{}{}.tsv'.format('{}', '{}', '{}', tag))
  subgrafici = 'Grafici'
  if not os.path.exists(join(celaborati, sub, subgrafici) ): os.makedirs(join(celaborati, sub, subgrafici))
  pftGrafico = join(celaborati, sub, subgrafici, 'Grafico{}{}{}{}{}.pdf'.format('{}', '{}', '{}', '{}', tag))
  pfAffPad = join(celaborati, sub, 'AffiliationPadovaPadua.txt'.format())
  pfAutPad = join(celaborati, sub, subautedge, 'AutoriPadovanichehannoscrittopaper.txt'.format())
  pftValidation = join(celaborati, sub, 'Validation{}.{}'.format(tag, '{}'))

  maxhops = 2
  strRegAff = 'pad(ov|u)a'
  regAff = re.compile(strRegAff, re.IGNORECASE)

  sceltePadova = ['_tutti', '_padovani']
  scelteUnione = ['_nomi', '_distanza', '_edge']
  scelteComunita = ['_girvnew', '_GC_girvnew', '_clanemo', '_GC_clanemo'] # , '_blockmodel'] # _blk lo aggiungo solo se GT funziona
  blockmodel = '_blockmodel'
  blockmodelGC = '_GC_blockmodel'
  scelteGrafico = ['_sito', '_generate']
  validation = {}

  # print('Chiamo con \n\t{}'.format())

  print('Inizio l\'esplorazione totale {} {}'.format(join(celaborati, sub), tag))
  start = timer()

  # in pfPersone ho una lista di nomi del dipartimento
  # estraggo gli IDautDEI corrispondenti (anche alle abbreviazioni)
  # print('\nChiamo estraiIDautoriMulti con\n\t{}\n\t{}\n\t{}'.format(pfPersone, pfAuthorRAW, pfAutoriID))
  estraiIDautoriMulti(pfPersone, pfAuthorRAW, pfAutoriID)
  lap1 = timer()
  print 'completato estraiIDautoriMulti in {}'.format(lap1 - start)

  # AutoriID come se fossero estratti dall'intero file Authors.txt TEST
  PFAUTORIIDPERTEST = join(celaborati, 'AutoriID_FULLTEST.txt'.format())
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

  # PapAutAff come se fossero estratti dal file completo TEST
  PFTPAATUTPERTEST = join(celaborati, 'PapAutAff{}{}.txt'.format('{}', '_FULLTEST'))
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

    # collasso i nomi basandomi sugli edge
    pfEdgeCollabUnificati = pftEdgeCollabUnificati.format(sp, scelteUnione[2])
    pfAutCollabUnificati = pftAutCollabUnificati.format(sp, scelteUnione[2])
    # print('\nChiamo collassaNodiEdge con \n\t{}\n\t{}\n\t{}\n\t{}\n\t'.format(  pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati) )
    collassaNodiEdge(pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)

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
      # print('\nChiamo preparaPerSNAP con \n\t{}\n\t{}\n\t{}\n\t{}\n\t{}'.format( pfEdgeCollabUnificati, pfAutCollabUnificati, pfPaj, pfAutNumNome, pfGT) )
      preparaPerSNAP(pfEdgeCollabUnificati, pfAutCollabUnificati, pfPaj, pfAutNumNome, pfGT)

      # estraggo la componente centrale
      pfPajGC = pftPajGC.format(sp, su)
      pfAutNumNomeGC = pftAutNumNomeGC.format(sp, su)
      pfGTGC = pftGTGC.format(sp, su)
      preparaGC(pfPaj, pfAutNumNome, pfPajGC, pfAutNumNomeGC, pfGTGC)

      # con pIPajek genero comunita, ho il file pfPaj pronto da mangiare
      # pfPaj = ce l'ho gia'
      # pfAINN = # e' pfAutNumNome # ID e Numero e Nome
      pfClassi = pftClassi.format(sp, su, scelteComunita[0]) # file com di SNAP
      pfClassiGC = pftClassi.format(sp, su, scelteComunita[1])
      lapgns = timer()
      # print('\nChiamo analizzaGirvanNewman con \n\t{}\n\t{}\n\t{}'.format(pfPaj, pfAutNumNome, pfClassi) )
      analizzaGirvanNewman(pfPaj, pfAutNumNome, pfClassi)
      analizzaGirvanNewman(pfPajGC, pfAutNumNomeGC, pfClassiGC)
      lapgne = timer()
      print('Completato analizzaGirvanNewman in {}'.format(lapgne - lapgns) )

      pfClassi = pftClassi.format(sp, su, scelteComunita[2]) # file com di SNAP
      pfClassiGC = pftClassi.format(sp, su, scelteComunita[3]) # file com di SNAP
      lapgns = timer()
      # print('\nChiamo analizzaClausetNewmanMoore con \n\t{}\n\t{}\n\t{}'.format(pfPaj, pfAutNumNome, pfClassi) )
      analizzaClausetNewmanMoore(pfPaj, pfAutNumNome, pfClassi)
      analizzaClausetNewmanMoore(pfPajGC, pfAutNumNomeGC, pfClassiGC)
      lapgne = timer()
      print('Completato analizzaClausetNewmanMoore in {}'.format(lapgne - lapgns) )

      # disegno i grafi
      # TODO potrei colorarli con le varie comunita generate nei vari modi
      try:
        from DisegnaGrafoGT import disegnaGrafo
        # blockmodel = '_blockmodel'
        if blockmodel not in scelteComunita:
          scelteComunita.append(blockmodel)
          scelteComunita.append(blockmodelGC)
        pfGrafoOut = pftGrafoOut.format(sp, su, '{}{}'.format(blockmodel, '{}'))
        pfClassi = pftClassi.format(sp, su, blockmodel)
        pfGrafoOutGC = pftGrafoOut.format(sp, su, '{}{}'.format(blockmodelGC, '{}'))
        pfClassiGC = pftClassi.format(sp, su, blockmodelGC)
        lapgts = timer()
        # print('\nChiamo disegnaGrafo con \n\t{}\n\t{}\n\t{}'.format(pfGT, pfGrafoOut, pfClassi) )
        disegnaGrafo(pfGT, pfGrafoOut, pfClassi)
        disegnaGrafo(pfGTGC, pfGrafoOutGC, pfClassiGC, isgc=True)
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

        # pfMerge ha esattamente i vettori di classi e cluster
        com, clu, comnn, clunn = getComClu(pfMerge)
        # chiave = 'v{}{}{}'.format(sp, su, sc)
        # validation[chiave] = homogeneity_completeness_v_measure(com, clu)
        # print('{} {}'.format(chiave , validation[chiave]) )
        chiave = 'v{}{}{}_noNone'.format(sp, su, sc)
        validation[chiave] = homogeneity_completeness_v_measure(comnn, clunn)
        print('{} {}'.format(chiave , validation[chiave]) )

        pfGrafico = pftGrafico.format(sp, su, sc, scelteGrafico[0])
        # print('\nChiamo graficaFrequenzePerSito con \n\t{}\n\t{}'.format(pfFreq, pfGrafico) )
        graficaFrequenzePerSito(pfFreq, pfGrafico)
        pfGrafico = pftGrafico.format(sp, su, sc, scelteGrafico[1])
        graficaFrequenzePerGenerate(pfFreq, pfGrafico)

  aggregaValidazione(pftValidation, validation)

  end = timer()
  print('Completata l\'esplorazione in {} s'.format(end-start) )

if __name__ == '__main__':
  esplorazioneTotale()
