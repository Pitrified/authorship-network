#!python2

from __future__ import print_function
import snap


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
  # print('Numero di comunita: {}'.format(classe+1) )

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

  return classe+1 # numero di comunita trovate

if __name__ == '__main__':
  # pfPaj = 'DatiSNAP1.paj'
  pfPaj = 'AutoriEdgeCollab_padovani_distanza_DEI.paj'
  pfAINN = 'AutoriCollabIdNumNome_padovani_distanza_DEI.txt'  # ID e Numero e Nome
  # pfAut = 'AutoriCollabUnificatiMacro.txt'
  pfMod = 'AutoriCollabClasse_padovani_distanza.tsv'
  analizzaGirvanNewman(pfPaj, pfAINN, pfMod)
