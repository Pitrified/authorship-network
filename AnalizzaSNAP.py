#!python2

from __future__ import print_function
import snap
from os.path import join

def analizzaGirvanNewman(pfPaj, pfAINN, pfMod):
  # prende un grafo in formato Pajek
  # restituisce le comunita come ID Nome Comunita
  g = snap.LoadPajek(snap.PUNGraph, pfPaj)

  comunita = snap.TCnComV()
  modularity = snap.CommunityGirvanNewman(g, comunita)
  dMod = {} # {numero : classe}
  classe = 0
  for com in comunita:
    # print('comunita {} = '.format(classe), end='' )
    for nodo in com:
      # print('{} '.format(nodo), end='')
      dMod.update({nodo:classe})
    classe += 1
    # print('')
  print('Numero di comunita analizzaGirvanNewman: {}'.format(classe) )

  dNum = {}
  with open(pfAINN, 'rb') as fAINN:
    for line in fAINN:
      autID, autNum, autNome = line.rstrip().split('\t')
      autNum = int(autNum)
      dNum.update( { autNum : [autID, autNome] } )
  # print(dNum)
  with open(pfMod, 'wb') as fMod:
    for autNum in dNum:
      fMod.write('{}\t{}\t{}\r\n'.format(dNum[autNum][0], dNum[autNum][1], dMod[autNum] ) )

  return classe # numero di comunita trovate

def analizzaClausetNewmanMoore(pfPaj, pfAINN, pfMod):
  # prende un grafo in formato Pajek
  # restituisce le comunita come ID Nome Comunita
  g = snap.LoadPajek(snap.PUNGraph, pfPaj)

  comunita = snap.TCnComV()
  modularity = snap.CommunityCNM(g, comunita)
  dMod = {} # {numero : classe}
  classe = 0
  for com in comunita:
    # print('comunita {} = '.format(classe), end='' )
    for nodo in com:
      # print('{} '.format(nodo), end='')
      dMod.update({nodo:classe})
    classe += 1
    # print('')
  print('Numero di comunita analizzaClausetNewmanMoore: {}'.format(classe) )

  dNum = {}
  with open(pfAINN, 'rb') as fAINN:
    for line in fAINN:
      autID, autNum, autNome = line.rstrip().split('\t')
      autNum = int(autNum)
      dNum.update( { autNum : [autID, autNome] } )
  # print(dNum)
  with open(pfMod, 'wb') as fMod:
    for autNum in dNum:
      fMod.write('{}\t{}\t{}\r\n'.format(dNum[autNum][0], dNum[autNum][1], dMod[autNum] ) )

  return classe # numero di comunita trovate

if __name__ == '__main__':
  # pfPaj = 'DatiSNAP1.paj'
  # pfPaj = join('Versione4_Totale', 'Nona', 'AutoriEdgeCollab_tutti_nomi_DEI.paj')
  pfPaj = join('Versione4_Totale', 'Nona', 'provapaj.paj')
  pfAINN = join('Versione4_Totale', 'Nona', 'AutoriCollabIdNumNome_tutti_DEI.txt')  # ID e Numero e Nome
  # pfAut = 'AutoriCollabUnificatiMacro.txt'
  pfMod = join('Versione4_Totale', 'Nona', 'AutoriCollabClasse_CNM.tsv')
  analizzaClausetNewmanMoore(pfPaj, pfAINN, pfMod)
