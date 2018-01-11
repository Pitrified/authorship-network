#!python2

def estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab, dEdgeCollab=None):
  """
  in pfAutoriID ho gli IDaut-nomeAut DEI
  in pfEdgeCollab ho gli EdgeCollab come coppie di IDaut1-IDaut2
  in pfAutCollab se IDaut1 o IDaut2 sono in IDautDEI li copio
  """
  if dEdgeCollab is None:
    dEdgeCollab = {}
    with open(pfEdgeCollab, 'rb') as fEdgeCollab: 
      for line in fEdgeCollab:
        pezzi = line.split('\t')
        dEdgeCollab.update({pezzi[0]+'\t'+pezzi[1]:0})
  #else:
    #print 'arrivato {}'.format(dEdgeCollab)
    
  sEdgeCollab = set()
  for entry in dEdgeCollab:
    pezzi = entry.split()
    sEdgeCollab.add(pezzi[0])
    sEdgeCollab.add(pezzi[1])
    
  with open(pfAutoriID, 'rb') as fAutoriID, open(pfAutCollab, 'wb') as fAutCollab:
    for line in fAutoriID:
      pezzi = line.split('\t')
      if pezzi[0] in sEdgeCollab:
        fAutCollab.write(line)

  
if __name__ == '__main__':
  print 'This program is EstraiAutoriCollab, being run by itself' 
  #PATH TO FILES
  celaborati = 'Versione3_Single\\'
  pfAutoriID = celaborati + 'AutoriDEI.txt'
  pfAutoriID = celaborati + 'AutoriDEIMacroFull.txt'
  pfEdgeCollab = celaborati + 'EdgeCollab.txt'
  pfEdgeCollab = celaborati + 'EdgeCollabMacroFull.txt'
  pfAutCollab = celaborati + 'AutoriCollab.txt'
  estraiAutoriCollab(pfAutoriID, pfEdgeCollab, pfAutCollab)
  print 'finitoEACsolo'
else:
  pass
  # print 'I am EstraiAutoriCollab, being imported from another module'


