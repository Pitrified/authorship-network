#!python2

from os import makedirs
from os.path import exists, join
from itertools import combinations, product

def creaAbbreviazioni(nome):
  tocchi = nome.split()
  if len(tocchi) == 0:
    print('Nome vuoto molto male')
  elif len(tocchi) == 1:
    return [nome, nome[0]]
  else:
    nt = len(tocchi)# - 1
    ip = product(range(2), repeat=nt)
    print ('nome {} lungo {}'.format(nome, len(tocchi)))
    abbr = []
    for p in ip:
      abb = ''
      for i in range(len(p)):
        if p[i] == 0:
          abb += tocchi[i] + ' '
        else:
          abb += tocchi[i][0] + ' '
      abbr.append(abb)
    print(abbr)
    return abbr


def abbreviaComunitaUnipd(pfPersone, pfAbbreviate):
  with open(pfPersone, 'rb') as fPersone, open(pfAbbreviate, 'wb') as fAbbreviate:
    for line in fPersone:
      pezzi = line.rstrip().split('\t')
      # print(pezzi)
      abbr = creaAbbreviazioni(pezzi[0])
      for a in abbr:
        fAbbreviate.write('{} {}\t{}\r\n'.format(a, pezzi[1], pezzi[2]))


if __name__ == '__main__':
  print 'This program is AbbrebiaComunita, being run by itself'

  celaborati = 'Versione3_Giu'
  sub = ''
  if not exists(join(celaborati, sub)): makedirs(join(celaborati, sub))
  tag = 'GIU'
  pfPersone = join(celaborati, sub, 'PersoneNomiComunita{}.txt'.format(tag))
  pfAbbreviate = join(celaborati, sub, 'PersoneNomiComunitaAbbreviate{}.txt'.format(tag))

  abbreviaComunitaUnipd(pfPersone, pfAbbreviate)
