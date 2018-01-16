#! python2

import re

def preparaPerSNAP(pfEdge, pfAut, pfPaj, pfAutNum):
  # with open(pfPaj, 'wb') as fPaj, with open(pfEdge, 'rb') as fEdge, 
  with open(pfPaj, 'wb') as fPaj:
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
          dNaut.update({i:pezzi[1]})
          fAutNum.write(pezzi[0]+'\t'+`i`+'\r\n')
          i += 1
      print dIDaut
    
    fPaj.write('*Vertices '+str(len(dIDaut))+'\r\n')
    for i in range(1, len(dNaut)+1):
      fPaj.write(str(i)+' "'+dNaut[i]+'"\r\n')
  
    fPaj.write('*Edges\r\n')
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
        fPaj.write(`idNum0`+' '+`idNum1`+' '+peso+'\r\n')
  
  # with open(pfEdge, 'rb') as fEdge:
    # strInput = fEdge.read()
    
  # with open(pfEdgeGephi, 'wb') as fEdgeGephi:
    # fEdgeGephi.write("Source\tTarget\tWeight\tType\teLabel\r\n")
    # fEdgeGephi.write(strInput.replace("\r\n","\tUndirected\t0\r\n" ) )
    
  # with open(pfAut, 'rb') as fAut:
    # strInput = fAut.read()
    
  # with open(pfAutGephi, 'wb') as fAutGephi:
    # fAutGephi.write("id\tLabel\r\n")
    # fAutGephi.write(strInput)
  
if __name__ == '__main__':
  print 'This program is preparaPerSNAP, being run by itself' 
  #PATH TO FILES
  celaborati = '..\\Versione3_Multi\\'
  pfEdge = celaborati + 'EdgeCollabUnificatiMacro.txt'
  pfAut = celaborati + 'AutoriCollabUnificatiMacro.txt'
  pfAutNum = celaborati + 'AutoriIDeNumeri.txt'
  pfPaj = celaborati + 'DatiSNAP1.paj'
  preparaPerSNAP(pfEdge, pfAut, pfPaj, pfAutNum)
  print 'finitoPPSsolo'
else:
  pass
  # print 'I am preparaPerSNAP, being imported from another module'