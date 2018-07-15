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
  from CollassaNodiAmpi import collassaNodiPerNome
  from CollassaNodiIterato import collassaNodiIterato
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
  # celaborati = join(ctesi, 'authorship-network', 'Versione6_amplia')
  celaborati = join(ctesi, 'authorship-network', 'Versione7')
  # sub = 'Amplia5'
  sub = 'Seconda'
  TEST = False
  TEST = True

  if not os.path.exists(join(celaborati, sub)): os.makedirs(join(celaborati, sub))
  cfileRAW   = join(ctesi, 'FileRAW')
  pfAuthorRAW = join(cfileRAW, 'Authors.txt')
  pfPapAutAffRAW = join(cfileRAW, 'PaperAuthorAffiliations.txt')
  pfAffRAW = join(cfileRAW, 'Affiliations.txt')
  # TEST
  if TEST:
    pfAuthorRAW = join(cfileRAW, 'Authors1000000.txt')
    pfPapAutAffRAW = join(cfileRAW, 'PaperAuthorAffiliations5000000.txt')
    PFAUTORIIDPERTEST = join(celaborati, 'AutoriID_FULLTEST.txt'.format())
    # PFAUTORIIDPERTEST = join(celaborati, 'AutoriID_filtrati_DEI.txt'.format())
    PFTPAATUTPERTEST = join(celaborati, 'PapAutAff{}{}.txt'.format('{}', '_FULLTEST'))
    # PFTPAATUTPERTEST = join(celaborati, 'PaperAuthorAff{}{}.txt'.format('{}', '_filtrati'))

  tag = '_DEI'
  # pfPersone    = join(celaborati, sub, 'PersoneNomi{}.txt'.format(tag))
  pfPersone    = join(celaborati, 'PersoneNomi{}.txt'.format(tag))
  pfAbbreviate = join(celaborati, 'PersoneNomiComunitaAbbreviate{}.txt'.format(tag))
  # pfPersone    = join(celaborati, 'PersoneNomi_apostolico{}.txt'.format(tag))
  # pfAbbreviate = join(celaborati, 'PersoneNomiComunitaAbbreviate_apostolico{}.txt'.format(tag))
  pfAutoriID   = join(celaborati, sub, 'AutoriID{}.txt'.format(tag))

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
  pftPajGC = join(celaborati, sub, subautedge, 'AutoriEdgeCollab{}{}_Gc{}.paj'.format('{}', '{}', tag))
  pftGT = join(celaborati, sub, subautedge, 'AutoriEdgeCollab{}{}{}_GT.tsv'.format('{}', '{}', tag))
  pftGTGC = join(celaborati, sub, subautedge, 'AutoriEdgeCollab{}{}_Gc{}_GT.tsv'.format('{}', '{}', tag))
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
  pftValidation = join(celaborati, sub, 'Validation{}{}.{}'.format('{}', tag, '{}'))

  maxhops = 2
  numit = 3
  strRegAff = 'pad(ov|u)a'
  regAff = re.compile(strRegAff, re.IGNORECASE)

  sceltePadova = {
      'Tutti' : '_tutti',
      'Pad' : '_padovani',
    }
  scelteUnione = {
      'Nomi' : '_nomi',
      'Dist' : '_distanza',
      'Edge' : '_edge',
    }
  scelteComunita = {
      'GirNew' : '_girvnew',         # Gi
      'GirNewGC' : '_GC_girvnew',    # Gg
      'GirNewGC' : '_Zgirvnew',    # Gg
      'ClaNeMo' : '_clanemo',        # Cl
      'ClaNeMoGC' : '_GC_clanemo',   # Gc
      'ClaNeMoGC' : '_Zclanemo',   # Gc
    } # , '_blockmodel'] # _blk lo aggiungo solo se GT funziona
  # sceltePadova = [
    # '_tutti',
    # '_padovani',
    # ]
  # scelteUnione = [
    # '_nomi',
    # '_distanza',
    # '_edge',
    # ]
  # scelteComunita = [
    # '_girvnew',
    # # '_GC_girvnew',
    # '_clanemo',
    # # '_GC_clanemo',
    # ] # , '_blockmodel'] # _blk lo aggiungo solo se GT funziona
  blockmodeltag = None
  blockmodeltag = 'Block'
  blockmodel = '_blockmodel'
  blockmodeltagGC = None
  blockmodeltagGC = 'BlockGC'
  # blockmodelGC = '_GC_blockmodel'
  blockmodelGC = '_Zblockmodel'
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
  if TEST:
    pfAutoriID = PFAUTORIIDPERTEST

  # estraggo i paper scritti da questi IDautDEI
  pfPAAtut = pftPapAutAff.format(sceltePadova['Tutti'])
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
  if TEST:
    pftPapAutAff = PFTPAATUTPERTEST

  # estraggo i paper con affiliation padovana
  pfPAAtut = pftPapAutAff.format(sceltePadova['Tutti'])
  pfPAApad = pftPapAutAff.format(sceltePadova['Pad'])
  # print('\nChiamo estraiPaperPadovaniCompleti con \n\t{}\n\t{}\n\t{}\n\t{}\n\t{}'.format( pfPAAtut, pfAffPad, pfAutoriID, pfPAApad, pfAutPad ))
  estraiPaperPadovaniCompleti(pfPAAtut, pfAffPad, pfAutoriID, pfPAApad, pfAutPad)
  lap25 = timer()
  print('completato estraiPaperPadovaniCompleti in {}'.format(lap25 - lap2) )

  for sp in sorted(sceltePadova, reverse=True):
    sp = sceltePadova[sp]
    print('\nInizio {}'.format(sp))
    pfPAA = pftPapAutAff.format(sp)
    pfEdgeCollab = pftEdgeCollab.format(sp)
    pfAutCollab = pftAutCollab.format(sp)

    # creo gli edge ed estraggo gli autori
    # print('\nChiamo creaEdgeCollab con \n\t{}\n\t{}'.format( pfPAA, pfEdgeCollab))
    creaEdgeCollab(pfPAA, pfEdgeCollab)
    # print('\nChiamo estraiAutoriCollab con \n\t{}\n\t{}\n\t{}'.format( pfAutoriID, pfEdgeCollab, pfAutCollab))
    estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)

    nosu = '_nonuniti'
    pfPaj = pftPaj.format(sp, nosu)
    pfAutNumNome = pftAutNumNome.format(sp, nosu)
    pfGT = pftGT.format(sp, nosu)
    preparaPerSNAP(pfEdgeCollab, pfAutCollab, pfPaj, pfAutNumNome, pfGT)
    pfEdgeGep = pftEdgeGephi.format(sp, nosu)
    pfAutGep = pftAutGephi.format(sp, nosu)
    preparaPerGephi(pfEdgeCollab, pfAutCollab, pfEdgeGep, pfAutGep)
    # disegno i grafi non collassati
    try:
      from DisegnaGrafoGT import disegnaGrafo
      pfGrafoOut = pftGrafoOut.format(sp, nosu, '{}{}'.format(blockmodel, '{}'))
      pfClassi = pftClassi.format(sp, nosu, blockmodel)
      disegnaGrafo(pfGT, pfGrafoOut, pfClassi)
    except ImportError:
      print('Ti serve graph_tool, usa Linux')
    except:
      raise

    # collasso i nomi basandomi su nomi ed abbreviazioni
    if 'Nomi' in scelteUnione:
      pfEdgeCollabUnificati = pftEdgeCollabUnificati.format(sp, scelteUnione['Nomi'])
      pfAutCollabUnificati = pftAutCollabUnificati.format(sp, scelteUnione['Nomi'])
      # print('\nChiamo collassaNodiAmpi con \n\t{}\n\t{}\n\t{}\n\t{}\n\t{}'.format(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati))
      # collassaNodiAmpi(pfPersone, pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
      collassaNodiPerNome(pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)

    # formatto i dati per SNAP e per GT
    pfPaj = pftPaj.format(sp, '')
    pfAutNumNome = pftAutNumNome.format(sp, '')
    pfGT = pftGT.format(sp, '')
    # print('\nChiamo preparaPerSNAP con \n\t{}\n\t{}\n\t{}\n\t{}\n\t{}'.format( pfEdgeCollab, pfAutCollab, pfPaj, pfAutNumNome, pfGT) )
    preparaPerSNAP(pfEdgeCollab, pfAutCollab, pfPaj, pfAutNumNome, pfGT)

    # collasso i nomi basandomi sulle distanze
    if 'Dist' in scelteUnione:
      pfEdgeCollabUnificati = pftEdgeCollabUnificati.format(sp, scelteUnione['Dist'])
      pfAutCollabUnificati = pftAutCollabUnificati.format(sp, scelteUnione['Dist'])
      # print('\nChiamo collassaNodiShortPath con \n\t{}\n\t{}\n\t{}\n\t{}\n\tDistanza massima tra autori {}'.format( pfAutNumNome, pfPaj, pfEdgeCollabUnificati, pfAutCollabUnificati, maxhops) )
      # collassaNodiShortPath(pfAutNumNome, pfPaj, pfEdgeCollabUnificati, pfAutCollabUnificati, maxhops)
      collassaNodiIterato(pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati, maxhops, numit)

    # collasso i nomi basandomi sugli edge
    if 'Edge' in scelteUnione:
      pfEdgeCollabUnificati = pftEdgeCollabUnificati.format(sp, scelteUnione['Edge'])
      pfAutCollabUnificati = pftAutCollabUnificati.format(sp, scelteUnione['Edge'])
      # print('\nChiamo collassaNodiEdge con \n\t{}\n\t{}\n\t{}\n\t{}\n\t'.format( pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati) )
      collassaNodiEdge(pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)

    for su in scelteUnione:
      su = scelteUnione[su]
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
      lapgns = timer()
      if 'GirNew' in scelteComunita:
        pfClassi = pftClassi.format(sp, su, scelteComunita['GirNew']) # file com di SNAP
        # print('\nChiamo analizzaGirvanNewman con \n\t{}\n\t{}\n\t{}'.format(pfPaj, pfAutNumNome, pfClassi) )
        analizzaGirvanNewman(pfPaj, pfAutNumNome, pfClassi)
      if 'GirNewGC' in scelteComunita:
        pfClassiGC = pftClassi.format(sp, su, scelteComunita['GirNewGC'])
        analizzaGirvanNewman(pfPajGC, pfAutNumNomeGC, pfClassiGC)
      lapgne = timer()
      print('Completato analizzaGirvanNewman in {}'.format(lapgne - lapgns) )

      lapgns = timer()
      if 'ClaNeMo' in scelteComunita:
        pfClassi = pftClassi.format(sp, su, scelteComunita['ClaNeMo']) # file com di SNAP
        # print('\nChiamo analizzaClausetNewmanMoore con \n\t{}\n\t{}\n\t{}'.format(pfPaj, pfAutNumNome, pfClassi) )
        analizzaClausetNewmanMoore(pfPaj, pfAutNumNome, pfClassi)
      if 'ClaNeMoGC' in scelteComunita:
        pfClassiGC = pftClassi.format(sp, su, scelteComunita['ClaNeMoGC']) # file com di SNAP
        analizzaClausetNewmanMoore(pfPajGC, pfAutNumNomeGC, pfClassiGC)
      lapgne = timer()
      print('Completato analizzaClausetNewmanMoore in {}'.format(lapgne - lapgns) )

      # disegno i grafi
      # TODO potrei colorarli con le varie comunita generate nei vari modi
      try:
        lapgts = timer()
        from DisegnaGrafoGT import disegnaGrafo
        # blockmodel = '_blockmodel'
        if blockmodeltag:
          scelteComunita[blockmodeltag] = blockmodel
          pfGrafoOut = pftGrafoOut.format(sp, su, '{}{}'.format(blockmodel, '{}'))
          pfClassi = pftClassi.format(sp, su, blockmodel)
          # print('\nChiamo disegnaGrafo con \n\t{}\n\t{}\n\t{}'.format(pfGT, pfGrafoOut, pfClassi) )
          disegnaGrafo(pfGT, pfGrafoOut, pfClassi)
        if blockmodeltagGC:
          scelteComunita[blockmodeltagGC] = blockmodelGC
          pfGrafoOutGC = pftGrafoOut.format(sp, su, '{}{}'.format(blockmodelGC, '{}'))
          pfClassiGC = pftClassi.format(sp, su, blockmodelGC)
          disegnaGrafo(pfGTGC, pfGrafoOutGC, pfClassiGC, isgc=True)
        lapgte = timer()
        print('Completato disegnaGrafo in {}'.format(lapgte - lapgts) )
      except ImportError:
        print('Ti serve graph_tool, usa Linux')
      except:
        raise

      # analizzo le frequenze delle comunita generate da SNAP e da GT
      for sc in scelteComunita:
        sc = scelteComunita[sc]
        print('Inizio {} {} {}'.format(sp, su, sc) )
        pfClassi = pftClassi.format(sp, su, sc) # 'AutoriCollabClasse_padovani_distanza.tsv'
        pfMerge = pftMerge.format(sp, su, sc) # 'AutoriCollabClasseMergeComunita_padovani_distanza.tsv'
        pfFreq = pftFreq.format(sp, su, sc) # 'FrequenzaMergeComunita_padovani_distanza.tsv'

        comunitaMergeAnalizza(pfClassi, pfAbbreviate, pfMerge, pfFreq)

        # pfMerge ha esattamente i vettori di classi e cluster
        com, clu, comnn, clunn = getComClu(pfMerge)
        # chiave = 'v{}{}{}'.format(sp, su, sc)
        # validation[chiave] = homogeneity_completeness_v_measure(com, clu)
        # print('{} {}'.format(chiave , validation[chiave]) )
        # chiave = 'v{}{}{}_noNone'.format(sp, su, sc)
        ssp = sp[1:3].capitalize()
        ssu = su[1:3].capitalize()
        ssc = sc[1:3].capitalize()
        chiave = '{}{}{}'.format(ssp, ssu, ssc)
        # chiave = '{}{}{}'.format(ssc, ssp, ssu)
        # chiave = '{}{}{}'.format(ssu, ssp, ssc)
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
