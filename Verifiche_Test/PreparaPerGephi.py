#! python2

# import re
from os import getcwd
from os.path import dirname
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
  pardir = dirname(getcwd())
  print pardir
  celaborati = 'Versione3_Multi'
  nEdge = 'EdgeCollabUnifShortPath4'
  pfEdge = join(pardir, celaborati, nEdge+'.txt')
  # print pfEdge
  pfEdgeGephi = join(pardir, celaborati, nEdge+'Gephi.tsv')
  nAut = 'AutoriCollabUnifShortPath4'
  pfAut = join(pardir, celaborati, nAut+'.txt')
  pfAutGephi = join(pardir, celaborati, nAut+'Gephi.tsv')
  preparaPerGephi(pfEdge, pfAut, pfEdgeGephi, pfAutGephi)
  print 'finitoPPGsolo'
else:
  pass
  # print 'I am PreparaPerGephi, being imported from another module'
