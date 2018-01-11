#! python2

import re

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
  celaborati = 'C:\\Users\\Test\\Documents\\Tesi\\authorship-network\\Versione3_Single\\'
  pfEdge = celaborati + 'EdgeCollabUnificati.txt'
  pfAut = celaborati + 'AutoriCollabUnificatiMacro.txt'
  pfEdgeGephi = celaborati + 'EdgeCollabUnificatiGephi.tsv'
  pfAutGephi = celaborati + 'AutoriCollabUnificatiGephi.tsv'
  #pfAutLoop = celaborati + 'AutoriCollabLoop.txt'
  preparaPerGephi(pfEdge, pfAut, pfEdgeGephi, pfAutGephi)
  print 'finitoPPGsolo'
else:
  pass
  # print 'I am PreparaPerGephi, being imported from another module'