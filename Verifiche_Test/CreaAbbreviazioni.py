#!python2

from itertools import product

def creaAbbreviazioni(pfPersone, pfAbbr):
  with open(pfPersone, 'rb') as fPersone, open(pfAbbr, 'wb') as fAbbr:
    for line in fPersone:
      autNome = line.rstrip()
      tocchi = autNome.split()
      nt = len(tocchi) - 1
      if nt == -1:
        print('linea vuota molto male')
      elif nt == 0:
        pass # solo cognome, non abbreviabile
        # fAbbr.write('{}\r\n'.format(autNome))
      else:
        for p in product(range(2), repeat=nt): # 000, 001, ..., 111
          abb = ''
          for i in range(len(p)):
            if p[i] == 0:
              abb += tocchi[i][0] + ' '
            else:
              abb += tocchi[i] + ' '
          abb += tocchi[len(tocchi)-1]
          fAbbr.write('{}\t{}\r\n'.format(autNome, abb))

if __name__ == '__main__':
  print 'This program is CreaAbbreviazioni, being run by itself' 
  #PATH TO FILES
  celaborati = '..\\Versione3_Multi\\'
  pfPersone = celaborati + 'PersoneDEI.txt'
  pfAbbr = celaborati + 'PersoneDEIabbr.txt'
  creaAbbreviazioni(pfPersone, pfAbbr)
  