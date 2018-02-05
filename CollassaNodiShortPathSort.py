#!python2

import snap
from itertools import combinations, product
from operator import itemgetter
from timeit import default_timer as timer
from os.path import join

def abbrevia(nome):
  # restituisce il nome abbreviato
  tocchi = nome.split()
  if len(tocchi) == 1:
    return nome
  else:
    abb = ''
    for t in tocchi[:-1]:
      abb += t[0] + ' '
    abb += tocchi[-1]
    # print('nome {} abbreviato {} '.format(nome, abb))
    return abb


def abbUguali(nameSort):
  # genera liste di autNome che hanno abbreviazione uguale
  abbruguali = [nameSort[0]] # autNomi con cognomi uguali
  for i in range(len(nameSort) - 1):
    cog = nameSort[i].rsplit(' ', 1)[1]
    # if nameSort[i+1].rsplit(' ', 1)[1] == cog:
    if abbrevia(nameSort[i+1]) == abbrevia(nameSort[i]):
      abbruguali.append(nameSort[i+1])
    else:
      yield abbruguali
      abbruguali = [nameSort[i+1]]
  yield abbruguali


def creaAbb(autNome): #, daNome):
  # creo tutte le abbreviazioni da autNome
  tocchi = autNome.split()
  # print tocchi, len(tocchi), len(tocchi[0]), tocchi[0][0]
  if len(tocchi) == 0:  # manca
    print('Nome vuoto molto male')
    return None
  elif len(tocchi) == 1:  # singolo
    return set([autNome])
  else:
    nt = len(tocchi) - 1
    ip = product(range(2), repeat=nt)
    # print 'nome da {} {} {}'.format(len(tocchi), autNome, nt)
    sa = set() # set di abbreviazioni
    for p in ip:
      # print 'p in ip {}'.format(p),
      abb = ''
      for i in range(len(p)):
        if p[i] == 0:
          abb += tocchi[i][0] + ' '
        else:
          abb += tocchi[i] + ' '
      abb += tocchi[len(tocchi)-1]
      sa.add(abb)
      # print abb
    # print('autNome: {} sa: {}'.format(autNome, sa))
    return sa


def ssd(a, b):
  if a < b: return (a, b)
  else: return (b, a)


def collassaNodiShortPath(pfAutINN, pfDatiPaj, pfEdgeUnif, pfAutUnif, maxhops):
  #edge e autori non collassati
  with open(pfAutINN, 'rb') as fAutINN:
    # load nomi id num
    daID   = {} # {id : numero, nome}
    daNum  = {} # {numero : id, nome}
    daNome = {} # {nome : ([id, id...], [num, num...])}
    for line in fAutINN:
      pezzi = line.rstrip().split('\t')
      autID = pezzi[0]
      autNum = int(pezzi[1])
      autNome = pezzi[2]
      daID.update({autID:[autNum, autNome]})
      daNum.update({autNum:[autID, autNome]})
      if autNome in daNome:
        # print('gia visto nome {} lista {}'.format(autNome, daNome[autNome]))
        daNome[autNome][0].append(autID)
        daNome[autNome][1].append(autNum)
      else:
        daNome.update({autNome:[[autID], [autNum]]})
    # print('daID: {}\ndaNum: {}\ndaNome: {}'.format(daID, daNum, daNome))

  # nameSort = [ ..., 'n s cog', 'n sec cog', 'nom sec cog', ... ]
  nameSort = sorted(daNome.keys(), key=lambda x: '{} {}'.format(x.rsplit(' ', 1)[1], x.rsplit(' ', 1)[0]))
  # for n in nameSort: print n

  UGraph = snap.LoadPajek(snap.PUNGraph, pfDatiPaj)
  lenfreq = {}
  dacollassare = {}
  cdc = {} # coppie da collassare {nome: [[src, dst], ...]}
  # maxhops = 2
  tsdc = []
  for au in abbUguali(nameSort):
    # print au
    numeri = []
    for nome in au:
      numeri.extend(daNome[nome][1])
    # print numeri
    coppie = []
    # scoppie = set()
    for src, dst in combinations(numeri, 2):
      lenshopa = snap.GetShortPath(UGraph, src, dst)
      # print 'da {}\ta {}\tlen {}'.format(src, dst, lenshopa)
      if lenshopa in lenfreq: lenfreq[lenshopa] += 1
      else: lenfreq[lenshopa] = 1
      if lenshopa > 0 and lenshopa <= maxhops:
        coppie.append(ssd(src, dst))
        # scoppie.add(ssd(src, dst))
    # if len(coppie) > 100:
      # print 'au {}\nlen {:3} coppie: {}'.format(au, len(coppie), coppie)
      # print 'au {}\nlen {:3} scoppie: {}'.format(au, len(scoppie), scoppie)
    if len(coppie) == 0: # non ho coppie
      # print 'no coppie'
      sdc = []
    elif len(coppie) == 1:
      # print 'una coppia'
      sdc = [set(coppie[0])]
    else:
      sdc = [set(coppie[0])] # set da collassare [set(1,3,5), set(2,7)]
      for coppia in coppie[1:]: # salto la prima
        a = coppia[0]
        b = coppia[1]
        posA, posB = -1, -1
        for i in range(len(sdc)):
          if a in sdc[i]: posA = i
          if b in sdc[i]: posB = i
        if posA == -1 and posB == -1: # entrambi MAI visti
          sdc.append(set(coppia))
        elif posA <> -1 and posB == -1: # a in sdc[posA]
          sdc[posA].add(b)              # aggiungo b che non avevo mai visto
        elif posA == -1 and posB <> -1:
          sdc[posB].add(a)
        else:
          sdc[posA] |= sdc[posB]
          if posA <> posB: del sdc[posB]
      # if len(sdc) > 1: print 'len {} sdc {}'.format(len(sdc), sdc)
    tsdc.extend(sdc)
  print 'lenfreq {}'.format(lenfreq)

  autUniti = {} # {nomelungo: [set(num da collassare), IDlungo, numlungo]}
  for s in tsdc:
    # print s
    # print [daNum[x] for x in s]
    setleader =  max([daNum[x] for x in s], key=itemgetter(1))
    # print setleader
    autUniti[setleader[1]] = (s, setleader[0], daID[setleader[0]][0])
  print autUniti

  dEdgeUnif = {}
  with open(pfDatiPaj, 'rb') as fDatiPaj:
    line = ''
    while line <> '*Edges': line = fDatiPaj.readline().rstrip() # brucio linee
    line = fDatiPaj.readline().rstrip() # brucio linee
    while line <> '':
      # print line
      pezzi = line.split()
      a = int(pezzi[0])
      b = int(pezzi[1])
      w = int(pezzi[2])
      for nome in autUniti:
        if a in autUniti[nome][0]:
          a = autUniti[nome][2]
        if b in autUniti[nome][0]:
          b = autUniti[nome][2]

      if ssd(a,b) in dEdgeUnif:
        dEdgeUnif[ssd(a,b)] += w
      else:
        dEdgeUnif[ssd(a,b)] = w
      line = fDatiPaj.readline().rstrip()
    print 'len(dEdgeUnif) {} dEdgeUnif {}'.format(len(dEdgeUnif), dEdgeUnif)

  sAutUnif = set()
  with open(pfEdgeUnif, 'wb') as fEdgeUnif:
    for edge in dEdgeUnif:
      a = edge[0]
      b = edge[1]
      sAutUnif.add(a)
      sAutUnif.add(b)
      w = dEdgeUnif[edge]
      fEdgeUnif.write('{}\t{}\t{}\r\n'.format(a, b, w))

  with open(pfAutUnif, 'wb') as fAutUnif:
    for a in sAutUnif:
      fAutUnif.write('{}\t{}\r\n'.format(a, daNum[a][1]))

if __name__ == '__main__':
  # print 'This program is CollassaNodiShortPathSort, being run by itself'
  # PATH TO FILES
  celaborati = 'Versione3_Multi'
  pfDatiPaj = join(celaborati, 'AutoriEdgeCollabSNAP.paj')
  pfAutINN = join(celaborati, 'AutoriCollabIdNumNomi.txt') # ID e Numero e Nome
  pfEdgeUnif = join(celaborati, 'EdgeCollabUnifShortPath4.txt')
  pfAutUnif = join(celaborati, 'AutoriCollabUnifShortPath4.txt')
  maxhops = 4
  start = timer()
  collassaNodiShortPath(pfAutINN, pfDatiPaj, pfEdgeUnif, pfAutUnif, maxhops)
  end = timer()
  print 'CollassaNodiShortPathSort in {}'.format(end-start)
