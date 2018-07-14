#!python2

from os import makedirs
from os.path import dirname
from os.path import join
from os.path import exists
from os.path import abspath

def abbrevia(nome):
  # restituisce il nome abbreviato
  tocchi = nome.split()
  if len(tocchi) == 1:
    return nome
  else:
    abb = ''
    for t in tocchi[:-1]:
      abb += t[0] + ' '
    abb += tocchi[-1]
    # print('nome {} abbreviato {} '.format(nome, abb))
    return abb

def getLeader(setID, dId):
  # in setID ho gli ID che collasseranno
  # li faccio diventare una lista, che ordino in base alla lunghezza nome
  # prendo l'ultimo elemento che e' il piu' lungo -> non abbreviato se c'e'
  return sorted( list( setID ) , key=lambda x: dId[x])[-1]

def unificaAutori(dAutColl, gliID):
  lospiegone = '''
    n1 n5  [[id1_3, id1_2], [id5_1, id5_1]]
    dAC -> id1_2 = set(id1_3)
           id1_3 = set(id1_2)
    n1 n2  [[id1_1, id1_2], [id2_1, id2_1]]
    dAC -> id1_1 = set(id1_2)
           id1_2 = set(id1_1)
    n1 n3  [[id1_1, id1_4], [id3_1, id3_1]]
    dAC -> id1_1 = set(id1_2, id1_4)
           id1_4 = set(id1_1) MA ANCHE id1_2 va scoperto, e va pure aggiornato
    tuttigliid = set(id1_1, id1_2, id1_4) creata scorrendo tutti i set degli id gia presenti
           id1_1, id1_2, id1_4 = set(id1_1, id1_2, id1_4)
    manca anche id1_3 !!!
           itero su una lista in cui aggiungo i nodi
    '''
  tuttiID = list(gliID)
  # print('tutti {}'.format(tuttiID) )
  lenprima = len(tuttiID)
  for ID in tuttiID:
    for newID in dAutColl[ID]:
      if newID not in tuttiID:
        # tuttiID.extend(dAutColl[ID] )
        tuttiID.extend([newID])
  setID = set(tuttiID)
  for ID in tuttiID:
    dAutColl[ID] = setID # forse ricreo il set ogni volta
  # print('tutti dopo {}'.format(tuttiID) )
  # if lenprima > 5: print('tutti prima lungo {} dopo {}'.format(lenprima, len(tuttiID) ) )

def collassaNodiEdge(pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati):
  # carico autori
  dId = {}    # {id:nome}
  with open(pfAutCollab, 'rb') as fAutCollab:
    for line in fAutCollab:
      autID, autNome = line.rstrip().split('\t')
      dId[autID] = autNome
    # print('len(dId): {}'.format( len(dId) ) )

  dEdgeNomi = {} # {'n cog\ta rossi' : [ [id, di, cog], [id, di, rossi] ] }
  with open(pfEdgeCollab, 'rb') as fEdgeCollab:
    for line in fEdgeCollab:
      src, dst, peso = line.rstrip().split('\t')
      peso = int(peso)
      nomesrc = dId[src]
      nomedst = dId[dst]
      # print('{} {}\t{} {}'.format(nomesrc, abbrevia(nomesrc), nomedst, abbrevia(nomedst) ) )
      nas = abbrevia(nomesrc)
      nad = abbrevia(nomedst)
      if nas < nad:
        edgenomi = '{}\t{}'.format(nas, nad)
      elif nas > nad:
        edgenomi = '{}\t{}'.format(nad, nas)
        tmp = src # se inverto le abbreviazioni inverto anche gli ID
        src = dst
        dst = tmp
      else: # erano uguali
        # print('Uguali {} {} {} {}'.format(src, dst, dId[src], dId[dst]) )
        edgenomi = '{}\t{}'.format(nad, nas)

      if edgenomi in dEdgeNomi:
        dEdgeNomi[edgenomi][0].append(src)
        dEdgeNomi[edgenomi][1].append(dst)
        dEdgeNomi[edgenomi][2].append(peso)
      else:
        dEdgeNomi[edgenomi] = [ [src], [dst] , [peso] ]

  # totedges = 0
  # for en in sorted(dEdgeNomi):
    # print('edgenomi: {}\t{}'.format(en, dEdgeNomi[en] ) )
    # totedges += len(dEdgeNomi[en][0])
  # print('edge totali {}'.format(totedges) )

  # scorro il dEdgeNomi e aggrego gli autori
  dAutColl = {i : set([i]) for i in dId} # { id0 : set(id1, id3), id1 : set(id0, id3), ... }
  # print('autori totali {} edge totali {}'.format(len(dAutColl), len(dEdgeNomi) ) )
  j = 0
  totedges = len(dEdgeNomi)
  for en in dEdgeNomi:
    j += 1
    edgerange = dEdgeNomi[en][0]
    # if len(edgerange) > 5: print('edge {} di {} con range {}'.format(j, totedges, edgerange) )
    if len(dEdgeNomi[en][0]) > 1: # ho almeno due edge tra i due autori
      unificaAutori(dAutColl, dEdgeNomi[en][0])
      unificaAutori(dAutColl, dEdgeNomi[en][1])

  # for ID in sorted(dAutColl, key = lambda x: dId[next(iter(dAutColl[x]) ) ] ):
    # print('{} {} {}'.format(ID, dAutColl[ID], [dId[x] for x in dAutColl[ID] ] ) )

  # per ogni ID trovo il leader -> id del nome piu' lungo
  dLeader = {}
  for ID in dAutColl:
    dLeader[ID] = getLeader(dAutColl[ID], dId)
  # for ID in sorted(dLeader, key=lambda x: dId[dLeader[x]]):
    # print('ID {} leader {} nome {} nomeleader {}'.format(ID, dLeader[ID], dId[ID], dId[dLeader[ID]] ) )
  # for ID in sorted(dAutColl, key = lambda x: dId[next(iter(dAutColl[x]) ) ] ):
    # print('ID {} {} {} leader {} {}'.format(ID, dAutColl[ID], [dId[x] for x in dAutColl[ID] ] , dLeader[ID], dId[dLeader[ID]]) )

  # passo il dEdgeNomi e aggrego gli edge
  dEdgeColl = {} # sl dl peso
  j = 0
  totedges = len(dEdgeNomi)
  for en in dEdgeNomi:
    edgerange = len(dEdgeNomi[en][0])
    j += 1
    # print('edge {} di {} con range {}'.format(j, totedges, edgerange) )
    for i in range(len(dEdgeNomi[en][0]) ):
      src = dEdgeNomi[en][0][i]
      dst = dEdgeNomi[en][1][i]
      peso = dEdgeNomi[en][2][i]
      # print('vecchi {} {} {}'.format(src, dst, peso) )
      srclead = dLeader[src]
      dstlead = dLeader[dst]
      if srclead > dstlead:
        tmp = srclead
        srclead = dstlead
        dstlead = tmp
      # print('vecchi {} {} nuovi {} {} {} {} {} {} {}'.format(src, dst, srclead, dstlead, peso, dId[src], dId[dst], dId[srclead], dId[dstlead]) )
      newEdge = '{}\t{}'.format(srclead, dstlead)
      if newEdge in dEdgeColl:
        dEdgeColl[newEdge] += peso
      else:
        dEdgeColl[newEdge] = peso

  with open(pfEdgeCollabUnificati, 'wb') as fECU:
    for edge in dEdgeColl:
      fECU.write('{}\t{}\r\n'.format(edge, dEdgeColl[edge]) )

  with open(pfAutCollabUnificati, 'wb') as fACU:
    for ID in set([dLeader[x] for x in dLeader] ):
      fACU.write('{}\t{}\r\n'.format(ID, dId[ID] ) )

if __name__ == '__main__':
  print 'CollassaNodiEdge da solo'
  aut = abspath(dirname(__file__) )
  # print(curdir)
  celaborati = 'Versione5'
  sub = 'Quarta'
  if not exists(join(celaborati, sub)): makedirs(join(celaborati, sub))
  tp = 'tutti'
  tp = 'padovani'
  pfEdgeCollab = join(aut, celaborati, 'EdgeCollab_{}_DEI.txt').format(tp)
  pfAutCollab = join(aut, celaborati, 'AutoriCollab_{}_DEI.txt').format(tp)
  pfEdgeCollabUnificati = join(aut, celaborati, sub, 'EdgeCU_Edge_{}_DEI.txt').format(tp)
  pfAutCollabUnificati = join(aut, celaborati, sub, 'AutoriCU_Edge_{}_DEI.txt').format(tp)
  collassaNodiEdge(pfEdgeCollab, pfAutCollab, pfEdgeCollabUnificati, pfAutCollabUnificati)
