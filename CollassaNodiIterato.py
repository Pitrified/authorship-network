#!python2

from CollassaNodiShortPathSort import collassaNodiShortPath as cnsp
from Verifiche_Test.PreparaPerSNAP import preparaPerSNAP as pps
from Verifiche_Test.PreparaPerGephi import preparaPerGephi as ppg
# from os import getcwd
from os import makedirs
from os.path import dirname
from os.path import join
from os.path import exists
# preparaPerSNAP(pfEdge, pfAut, pfPaj, pfAutNum)
# collassaNodiShortPath(pfAutINN, pfDatiPaj, pfEdgeUnif, pfAutUnif, maxhops)

def collassaNodiIterato(dirs, files, numit, maxhops):
  direlab = dirs[0]
  dirsub = dirs[1]
  diriter = dirs[2]
  if not exists(diriter): makedirs(diriter)
  # files sono path completi ai dati iniziali di edge e autori
  pfEdgeCollab = files[0]
  pfAutCollab = files[1]

  # preparo i dati iniziali per SNAP
  sPaj = 'AutoriEdgeCollab_{}.paj'
  sAutINN = 'AutoriCollabIdNumNomi_{}.txt'
  pfPaj = join(diriter, sPaj.format(0))
  pfAutINN = join(diriter, sAutINN.format(0))
  pps(pfEdgeCollab, pfAutCollab, pfPaj, pfAutINN)
  sEdgeCU = 'EdgeCUShortPath_{}_{}.txt'.format(maxhops, '{}')
  # print sEdgeC
  # print sEdgeC.format(2)
  sAutCU = 'AutoriCUShortPath_{}_{}.txt'.format(maxhops, '{}')

  for i in range(1, numit+1):
    pfEdgeCU = join(diriter, sEdgeCU.format(i))
    pfAutCU = join(diriter, sAutCU.format(i))
    # mangia INN e PAJ i-1 crea Edge Autori i
    cnsp(pfAutINN, pfPaj, pfEdgeCU, pfAutCU, maxhops)

    pfPaj = join(diriter, sPaj.format(i))
    pfAutINN = join(diriter, sAutINN.format(i))
    # mangia Edge Autori i crea INN e PAJ i
    pps(pfEdgeCU, pfAutCU, pfPaj, pfAutINN)

  nEdgeGephi = 'EdgeCUShortPath_{}_{}.tsv'.format(maxhops, numit)
  pfEdgeGephi = join(direlab, nEdgeGephi)
  nAutGephi = 'AutoriCUShortPath_{}_{}.tsv'.format(maxhops, numit)
  pfAutGephi = join(direlab, nAutGephi)
  ppg(pfEdgeCU, pfAutCU, pfEdgeGephi, pfAutGephi)



if __name__ == '__main__':
  print 'CollassaNodiIterato da solo'
  aut =  dirname(__file__)
  celaborati = 'Versione4_Short'
  sub = ''
  iterati = 'Iter'
  direlab = join(aut, celaborati)
  dirsub = join(aut, celaborati, sub)
  diriter = join(aut, celaborati, sub, iterati)
  dirs = (direlab, dirsub, diriter)

  tag = 'DEI'
  nEdgeCollab = 'EdgeCollab{}.txt'.format(tag)
  pfEdgeCollab = join(dirsub, nEdgeCollab)
  nAutCollab = 'AutoriCollab{}.txt'.format(tag)
  pfAutCollab = join(dirsub, nAutCollab)
  files = (pfEdgeCollab, pfAutCollab)

  maxhops = 3
  numit = 2
  collassaNodiIterato(dirs, files, numit, maxhops)
  # print diriter
