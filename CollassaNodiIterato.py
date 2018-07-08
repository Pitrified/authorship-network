#!python2

from CollassaNodiShortPathSort import collassaNodiShortPath as cnsp
from Verifiche_Test.PreparaPerSNAP import preparaPerSNAP as pps
from Verifiche_Test.PreparaPerGephi import preparaPerGephi as ppg
# from os import getcwd
from os import makedirs
from os.path import dirname
from os.path import join
from os.path import exists
from os.path import abspath
from shutil import copyfile
# preparaPerSNAP(pfEdge, pfAut, pfPaj, pfAutNum)
# collassaNodiShortPath(pfAutINN, pfDatiPaj, pfEdgeUnif, pfAutUnif, maxhops)
from MergeComSito import comunitaMergeAnalizza
from sklearn.metrics import homogeneity_completeness_v_measure
from validazione import getComClu, aggregaValidazione
from AnalizzaSnap import analizzaGirvanNewman, analizzaClausetNewmanMoore
from DisegnaGrafoGT import disegnaGrafo

def collassaNodiIterato(pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati, maxhops, numit):
  diriter = join(abspath(dirname(pfEdgeCollab)), 'Iter')
  print(diriter)
  if not exists(diriter): makedirs(diriter)

  pftAutNumNome = join(diriter, 'AutNumNume_{}_{}.txt').format(maxhops, '{}')
  pftPaj = join(diriter, 'AutoriEdge_{}_{}.paj').format(maxhops, '{}')
  pftGT = join(diriter, 'AutoriEdge_{}_{}_GT.tsv').format(maxhops, '{}')
  pftEdgeCollabUnificati = join(diriter, 'EdgeCollabUnificati_{}_{}.txt').format(maxhops, '{}')
  pftAutCollabUnificati = join(diriter, 'AutoriCollabUnificati_{}_{}.txt').format(maxhops, '{}')

  pfPaj = pftPaj.format(0)
  pfAutNumNome = pftAutNumNome.format(0)
  pfGT = pftGT.format(0)
  pps(pfEdgeCollab, pfAutCollab, pfPaj, pfAutNumNome, pfGT)

  pfECU = pftEdgeCollabUnificati.format(0)
  pfACU = pftAutCollabUnificati.format(0)
  copyfile(pfEdgeCollab, pfECU)
  copyfile(pfAutCollab, pfACU)

  for i in range(1, numit+1):
    pfECU = pftEdgeCollabUnificati.format(i)
    pfACU = pftAutCollabUnificati.format(i)
    cnsp(pfAutNumNome, pfPaj, pfECU, pfACU, maxhops)

    pfPaj = pftPaj.format(i)
    pfAutNumNome = pftAutNumNome.format(i)
    pfGT = pftGT.format(i)
    pps(pfECU, pfACU, pfPaj, pfAutNumNome, pfGT)

  copyfile(pfECU, pfEdgeCollabUnificati)
  copyfile(pfACU, pfAutCollabUnificati)

def findBest():
  aut =  abspath(dirname(__file__) )
  celaborati = 'Versione5'
  sub = 'Seconda'
  tp = 'tutti'
  pfEdgeCollab = join(aut, celaborati, sub, 'EdgeCollab_{}_DEI.txt').format(tp)
  pfAutCollab = join(aut, celaborati, sub, 'AutoriCollab_{}_DEI.txt').format(tp)

  pftEdgeCollabUnificati = join(aut, celaborati, sub, 'EdgeCollabUnificati_{}_{{}}_{{}}_DEI.txt').format(tp)
  pftAutCollabUnificati = join(aut, celaborati, sub, 'AutoriCollabUnificati_{}_{{}}_{{}}_DEI.txt').format(tp)

  pftAutNumNome = join(aut, celaborati, sub, 'AutNumNume_{}_{{}}_{{}}_DEI.txt').format(tp)
  pftPaj = join(aut, celaborati, sub, 'AutoriEdge_{}_{{}}_{{}}_DEI.paj').format(tp)
  pftGT = join(aut, celaborati, sub, 'AutoriEdge_{}_{{}}_{{}}_DEI_GT.tsv').format(tp)

  pftClassi = join(aut, celaborati, sub, 'Classi_{}_{{}}_{{}}_{{}}_DEI_GT.tsv').format(tp)
  sc = ['girnew', 'clanemo', 'block']

  pftGrafoout = join(aut, celaborati, sub, 'Grafo_{}_{{}}_{{}}_{{}}_DEI_GT.pdf').format(tp)

  pftMerge = join(aut, celaborati, sub, 'Merge_{}_{{}}_{{}}_{{}}_DEI_GT.txt').format(tp)
  pftFreq = join(aut, celaborati, sub, 'Freq_{}_{{}}_{{}}_{{}}_DEI_GT.txt').format(tp)
  pfAbbreviate = join(celaborati, 'PersoneNomiComunitaAbbreviate_DEI.txt')

  validation = {}

  for mh in [2,3,4,5,10]: # range(2, 5):
    for ni in [0,1,2,3,4,5,10]: # range(0, 6):
      pfEdCoUn = pftEdgeCollabUnificati.format(mh, ni)
      pfAuCoUn = pftAutCollabUnificati.format(mh, ni)
      # print 'mh: {} ni: {} '.format(mh, ni),
      # collassaNodiIterato(pfEdgeCollab, pfAutCollab, pfEdCoUn, pfAuCoUn, mh, ni)

      pfANN = pftAutNumNome.format(mh, ni)
      pfPaj = pftPaj.format(mh, ni)
      pfGT = pftGT.format(mh, ni)
      pps(pfEdCoUn, pfAuCoUn, pfPaj, pfANN, pfGT)

      pfClassi = pftClassi.format(mh, ni, sc[0])
      # analizzaGirvanNewman(pfPaj, pfANN, pfClassi)

      pfClassi = pftClassi.format(mh, ni, sc[1])
      # analizzaClausetNewmanMoore(pfPaj, pfANN, pfClassi)

      pfClassi = pftClassi.format(mh, ni, sc[2])
      pfGrafoout = pftGrafoout.format(mh, ni, sc[2])
      # disegnaGrafo(pfGT, pfGrafoout, pfClassi)

      vmeasure = []
      for s in sc:
        pfMerge = pftMerge.format(mh, ni, s)
        pfFreq = pftFreq.format(mh, ni, s)
        comunitaMergeAnalizza(pfClassi, pfAbbreviate, pfMerge, pfFreq)
        com, clu, comnn, clunn = getComClu(pfMerge)
        # print(len(comnn), len(clunn) )
        # validation[chiave] = homogeneity_completeness_v_measure(comnn, clunn)
        vmeasure.append(homogeneity_completeness_v_measure(comnn, clunn)[2] )
        # vmeasure.append(homogeneity_completeness_v_measure(comnn, clunn))

      chiave = '{:02}_{:02}'.format(mh, ni)
      # print(vmeasure)
      validation[chiave] = sum(vmeasure) / float(len(vmeasure))

  for c in sorted(validation):
    print('{}\t{}'.format(c, validation[c]) )

if __name__ == '__main__':
  print 'CollassaNodiIterato da solo'
  # aut =  abspath(dirname(__file__) )
  # print(aut)
  # celaborati = 'Versione5'
  # sub = 'Seconda'

  # tp = 'tutti'
  # pfEdgeCollab = join(aut, celaborati, sub, 'EdgeCollab_{}_DEI.txt').format(tp)
  # pfAutCollab = join(aut, celaborati, sub, 'AutoriCollab_{}_DEI.txt').format(tp)
  # pfAutNumNome = join(aut, celaborati, sub, 'AutNumNume_{}_DEI.txt').format(tp)
  # pfPaj = join(aut, celaborati, sub, 'AutoriEdge_{}_DEI.paj').format(tp)
  # pfGT = join(aut, celaborati, sub, 'AutoriEdge_{}_DEI_GT.tsv').format(tp)
  # print(pfPaj)

  # pfEdgeCollabUnificati = join(aut, celaborati, sub, 'EdgeCollabUnificati_{}_DEI.txt').format(tp)
  # pfAutCollabUnificati = join(aut, celaborati, sub, 'AutoriCollabUnificati_{}_DEI.txt').format(tp)

  # maxhops = 3
  # numit = 4
  # collassaNodiIterato(pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati, maxhops, numit)

  findBest()
