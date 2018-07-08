#! python2

# import re
from os import getcwd
from os.path import dirname
from os.path import join
from os.path import abspath

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
  pardir = abspath(dirname(dirname(__file__) ) ) # dir(file)=aut/ver; dd(f)=aut
  # print pardir
  celaborati = join('elaborato', 'DatiGrafiElaborato')
  tag = '_DEI'

  pftEdgeCollab = join(pardir, celaborati, 'EdgeCollab_padovani{{}}{}.{{}}'.format(tag))
  pftAutCollab  = join(pardir, celaborati, 'AutoriCollab_padovani{{}}{}.{{}}'.format(tag))
  pftEdgeCollab = join(pardir, celaborati, 'EdgeCollab_tutti{{}}{}.{{}}'.format(tag))
  pftAutCollab  = join(pardir, celaborati, 'AutoriCollab_tutti{{}}{}.{{}}'.format(tag))
  # print(pftEdgeCollab, pftAutCollab)
  pfEdge = pftEdgeCollab.format('', 'txt')
  pfAut = pftAutCollab.format('', 'txt')
  pfEdgeGephi = pftEdgeCollab.format('_Gephi', 'tsv')
  pfAutGephi = pftAutCollab.format('_Gephi', 'tsv')

  preparaPerGephi(pfEdge, pfAut, pfEdgeGephi, pfAutGephi)
  print 'finitoPPGsolo'
else:
  pass
  # print 'I am PreparaPerGephi, being imported from another module'
