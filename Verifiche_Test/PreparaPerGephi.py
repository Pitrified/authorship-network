#! python2

# import re
from os.path import join

def preparaPerGephi(pfEdge, pfAut, pfEdgeGephi, pfAutGephi):
  with open(pfEdge, 'rb') as fEdge:
    strInput = fEdge.read()

  with open(pfEdgeGephi, 'wb') as fEdgeGephi:
    fEdgeGephi.write("Source\tTarget\tWeight\tType\teLabel\r\n")
    fEdgeGephi.write(strInput.replace("\r\n","\tUndirected\t0\r\n" ) )

  with open(pfAut, 'rb') as fAut:
    strInput = fAut.read()

  with open(pfAutGephi, 'wb') as fAutGephi:
    fAutGephi.write("id\tLabel\r\n")
    fAutGephi.write(strInput)

if __name__ == '__main__':
  print 'This program is PreparaPerGephi, being run by itself'
  #PATH TO FILES
  celaborati = 'Versione3_Multi'
  nEdge = 'EdgeCollabUnifShortPath4'
  pfEdge = join('..', celaborati, nEdge+'.txt')
  print pfEdge
  pfEdgeGephi = join('..', celaborati, nEdge+'Gephi.tsv')
  nAut = 'AutoriCollabUnifShortPath4'
  pfAut = join('..', celaborati, nAut+'.txt')
  pfAutGephi = join('..', celaborati, nAut+'Gephi.tsv')
  preparaPerGephi(pfEdge, pfAut, pfEdgeGephi, pfAutGephi)
  print 'finitoPPGsolo'
else:
  pass
  # print 'I am PreparaPerGephi, being imported from another module'
