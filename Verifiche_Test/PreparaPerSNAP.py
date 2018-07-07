#! python2

# import re
from os import getcwd
from os.path import dirname
from os.path import join
import snap

def preparaPerSNAP(pfEdge, pfAut, pfPaj, pfAutNum, pfGT):
  # with open(pfPaj, 'wb') as fPaj, with open(pfEdge, 'rb') as fEdge,
  with open(pfPaj, 'wb') as fPaj, open(pfGT, 'wb') as fGT:
    # carico dizionario dIDaut {IDaut: [IDnumerico, nomeAut]}
    # carico dizionario dNaut  {IDnumerico: nomeAut}
    with open(pfAut, 'rb') as fAut, open(pfAutNum, 'wb') as fAutNum:
      dIDaut = {}
      dNaut  = {}
      i = 1
      for lIDautNome in fAut:
        pezzi = lIDautNome.rstrip().split('\t')
        if not pezzi[0] in dIDaut:
          dIDaut.update({pezzi[0]:[i, pezzi[1]]})
          dNaut.update({i: [pezzi[1] , pezzi[0] ] } )
          fAutNum.write(pezzi[0]+'\t'+`i`+'\t'+pezzi[1]+'\r\n')
          i += 1
        else:
          print('Ho gia visto {}'.format(pezzi[0]))
      # print dIDaut

    fPaj.write('*Vertices '+str(len(dIDaut))+'\r\n')
    fGT.write('*Vertices {}\r\n'.format(str(len(dIDaut))))
    for i in range(1, len(dNaut)+1):
      fPaj.write(str(i)+' "'+dNaut[i][0]+'"\r\n')
      fGT.write('{}\t{}\t{}\r\n'.format(str(i-1), dNaut[i][0], dNaut[i][1]) )

    fPaj.write('*Edges\r\n')
    fGT.write('*Edges\r\n')
    with open(pfEdge, 'rb') as fEdge:
      for lEdge in fEdge:
        pezzi = lEdge.rstrip().split('\t')
        id0 = pezzi[0]
        id1 = pezzi[1]
        peso= pezzi[2]
        idNum0 = dIDaut[id0][0]
        idNum1 = dIDaut[id1][0]
        # fPaj.write(dIDaut[pezzi[0]][0]+'\t'   )
        # fPaj.write(dIDaut[id0][0]+'\t'+dIDaut[id1][0]+'\t'+str(peso)+'\r\n')
        if id0 != id1:
          fPaj.write(`idNum0`+' '+`idNum1`+' '+peso+'\r\n')
          fGT.write('{}\t{}\t{}\r\n'.format(idNum0-1, idNum1-1, peso) )

def preparaGC(pfPaj, pfAutNum, pfPajGC, pfAutNumGC, pfGTGC):
  with open(pfPaj, 'rb') as fPaj, open(pfAutNum, 'rb') as fAutNum:
    dNum = {}
    for line in fAutNum:
      ID, num, nome = line.rstrip().split('\t')
      num = int(num)
      dNum[num] = [ID, nome]
    dVecchiNuovi = {}
    dNuoviVecchi = {}
    with open(pfPajGC, 'wb') as fPajGC, open(pfAutNumGC, 'wb') as fAutNumGC, open(pfGTGC, 'wb') as fGTGC:
      g = snap.LoadPajek(snap.PUNGraph, pfPaj)
      gc = snap.GetMxWcc(g)
      # for n in gc.Nodes(): print(n.GetId())
      # print(gc.GetNodes())
      # print([x.GetId() for x in gc.Nodes() ] )
      # print([(x.GetSrcNId(), x.GetDstNId() ) for x in gc.Edges() ] )

      nuovo = 1
      for vecchio in gc.Nodes():
        dVecchiNuovi[vecchio.GetId()] = nuovo
        dNuoviVecchi[nuovo] = vecchio.GetId()
        nuovo += 1
      fPajGC.write('*Vertices {}\r\n'.format( len(dNuoviVecchi) ) )
      fGTGC.write('*Vertices {}\r\n'.format( len(dNuoviVecchi) ) )
      for i in range(1, len(dNuoviVecchi)+1):
        idnome = dNum[dNuoviVecchi[i]]
        fPajGC.write('{} "{}"\r\n'.format(i, idnome[1]) )
        fGTGC.write('{}\t{}\t{}\r\n'.format(i-1, idnome[1], idnome[0] ) )
        fAutNumGC.write('{}\t{}\t{}\r\n'.format(idnome[0], i, idnome[1] ) )

      fPajGC.write('*Edges\r\n')
      fGTGC.write('*Edges\r\n')
      line = fPaj.readline()
      while line != '*Edges\r\n': line = fPaj.readline()
      for line in fPaj:
        vsrc, vdst, peso = line.rstrip().split()
        vsrc = int(vsrc)
        vdst = int(vdst)
        if vsrc in dVecchiNuovi and vdst in dVecchiNuovi:
          nsrc = dVecchiNuovi[vsrc]
          ndst = dVecchiNuovi[vdst]
          fPajGC.write('{} {} {}\r\n'.format(nsrc, ndst, peso) )
          fGTGC.write('{}\t{}\t{}\r\n'.format(nsrc-1, ndst-1, peso) )





if __name__ == '__main__':
  print 'This program is preparaPerSNAP, being run by itself'
  #PATH TO FILES
  pardir = dirname(dirname(__file__)) # dir(file)=aut/ver; dd(f)=aut
  celaborati = 'Versione3_Multi'
  nEdge = 'EdgeCollabMacro'
  nEdge = 'EdgeCollabUnifShortPath2'
  # nEdge = 'EdgeCollabUnifGT'
  pfEdge = join(pardir, celaborati, nEdge+'.txt')
  nAut = 'AutoriCollabMacro'
  nAut = 'AutoriCollabUnifShortPath2'
  # nAut = 'AutoriCollabUnifGT'
  pfAut = join(pardir, celaborati, nAut+'.txt')
  nAutNum = 'AutoriCollab'
  nAutNum = 'AutoriCollabSP2'
  nAutNum = 'AutoriCollabGT'
  pfAutNum = join(pardir, celaborati, nAutNum+'IdNumNomi.txt')
  nPaj = 'Collab'
  nPaj = 'CollabSP2'
  nPaj = 'CollabGT'
  pfPaj = join(pardir, celaborati, 'AutoriEdge'+nPaj+'SNAP.paj')
  # for pf in [pfEdge, pfAut, pfAutNum, pfPaj]: print pf
  nGT = 'CollabGT'
  pfGT = join(pardir, celaborati, 'AutoriEdge{}GT.tsv'.format(nGT))
  # preparaPerSNAP(pfEdge, pfAut, pfPaj, pfAutNum, pfGT)


  celaborati = 'Versione4_Totale'
  pfPaj = join(pardir, celaborati, 'Nona', 'AutoriEdgeCollab_tutti_distanza_DEI.paj')
  pfAutNum = join(pardir, celaborati, 'Nona', 'AutoriCollabIdNumNome_tutti_distanza_DEI.txt')
  pfPajGC = join(pardir, celaborati, 'Nona', 'AutoriEdgeCollab_tutti_distanza_DEI_GIANTCOMP.txt')
  pfAutNumGC = join(pardir, celaborati, 'Nona', 'AutoriCollabIdNumNome_tutti_distanza_DEI_GIANTCOMP.txt')
  pfGTGC = join(pardir, celaborati, 'Nona', 'AutoriEdgeCollab_tutti_distanza_DEI_GT_GIANTCOMP.txt')

  preparaGC(pfPaj, pfAutNum, pfPajGC, pfAutNumGC, pfGTGC)



  print 'finitoPPSsolo'
