#!python2

import snap
from itertools import combinations, product
from timeit import default_timer as timer
from os.path import join

def creaAbbreviazioni(autNome, dAbbreviazioni, daNome):
  # creo tutte le abbreviazioni dal nome
  # labbr = [] # lista di abbreviazioni da questo nome
  # caricate in dAbbreviazioni
  tocchi = autNome.split()
  # print tocchi, len(tocchi), len(tocchi[0]), tocchi[0][0]
  if not dAbbreviazioni.has_key(autNome):
    if len(tocchi) == 0:  # manca
      # pass
      print('Nome vuoto molto male')
    elif len(tocchi) == 1:  # singolo
      dAbbreviazioni.update({autNome:[autNome]})
    else:
      nt = len(tocchi) - 1
      ip = product(range(2), repeat=nt)
      # print 'nome da {} {} {}'.format(len(tocchi), autNome, nt)
      sa = set()
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
      dAbbreviazioni.update({autNome:[x for x in sa]})
  else:
    print 'visto gia {} lista {}'.format(autNome, dAbbreviazioni[autNome])
    pass


def checkNome(autNome, daNomeAbb, dAbbreviazioni, daNome):
  fullnames = []
  labbr = []
  for entry in dAbbreviazioni:
    if autNome in dAbbreviazioni[entry]:
      fullnames.append(entry)
      for x in dAbbreviazioni[entry]:
        if x not in labbr and x in daNome:
          labbr.append(x)
  longest = max(fullnames, key=len)
  # for name in fullnames:
    # if len(name) > len(longest):
      # longest = name

  if longest not in daNomeAbb:
    daNomeAbb[longest] = labbr
    # for abb in labbr:
      # if abb not in daNomeAbb[longest]:
        # daNomeAbb[longest].append(abb)
  else:
    pass
    # print('gia visto longest {} con daNomeAbb[longest] {} labbr attuale {}'.format(longest, daNomeAbb[longest], labbr))
    # if longest <> '':
      # daNomeAbb.update({longest:labbr})
    # else:
      # daNomeAbb.update({autNome:[]})
  # print 'fulln: {} labbr: {} autNome: {} longest: {}'.format(fullnames, labbr, autNome, longest)


def ssd(a, b):
  if a < b: return [a, b]
  else: return [b, a]


def collassaNodiShortPath(pfAutNum, pfDatiPaj):
  #edge e autori non collassati
  UGraph = snap.LoadPajek(snap.PUNGraph, pfDatiPaj)
  with open(pfAutNum, 'rb') as fAutNum:
    # load nomi id num
    daID   = {} # {id : numero, nome}
    daNum  = {} # {numero : id, nome}
    daNome = {} # {nome : ([id, id...], [num, num...])}
    for line in fAutNum:
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
    print('daID: {}\ndaNum: {}\ndaNome: {}'.format(daID, daNum, daNome))
    # fAutNum.seek(0)
    # start = timer()
    dAbbreviazioni = {} # {con cani cose:[c c cose, con c cose, c cani cose, con cani cose]}
    # ma anche {con c cose:[c c cose, con c cose]}
    # for line in fAutNum:
    for autNome in daNome:
      # pezzi = line.rstrip().split('\t')
      # autNome = pezzi[2]
      creaAbbreviazioni(autNome, dAbbreviazioni, daNome)
    # end = timer()
    # print 'creaAbbreviazioni in {}'.format(end-start)
    print 'dAbbreviazioni: {}'.format(dAbbreviazioni)

    daNomeAbb = {}  # {fullest name:[abbreviazioni che incontro...]}
    # fAutNum.seek(0)
    # for line in fAutNum:
      # pezzi = line.rstrip().split('\t')
      # autNome = pezzi[2]
    for autNome in daNome:
      checkNome(autNome, daNomeAbb, dAbbreviazioni, daNome)
    print 'daNomeAbb: {}'.format(daNomeAbb)

    daNomiNum = {} # {nomefull:[numeri di id legati al nome]}
    for nome in daNomeAbb:
      # print 'nome {}'.format(nome)
      daNomiNum[nome] = daNome[nome][1]
      for abb in daNomeAbb[nome]:
        if abb in daNome: # tendenzialmente sempre
          for num in daNome[abb][1]:
            if num not in daNomiNum[nome]:
              daNomiNum[nome].append(num)
            else:
              # print 'avevo gia visto abb {} con nome {} e daNome[abb][1] {}'.format(abb, nome, daNome[abb][1])
              pass
        else:
          print('non trovata {} in daNome'.format(abb))
          pass
    print 'daNomiNum: {}'.format(daNomiNum)
    # for nome in daNomiNum:
      # print('nome {} sue abb {}'.format(nome, [daNum[x][1] for x in daNomiNum[nome]]))
    lenfreq = {}
    dacollassare = {}
    cdc = {} # coppie da collassare {nome: [[src, dst], ...]}
    maxhops = 2
    for nome in daNomiNum:
      if len(daNomiNum[nome]) > 1:
        # print 'nome: {}\tdaNomiNum[nome]: {}'.format(nome, daNomiNum[nome])
       for src, dst in combinations(daNomiNum[nome], 2):
          srcname = daNum[src][1]
          dstname = daNum[dst][1]
          # print type(src), type(dst)
          lenshopa = snap.GetShortPath(UGraph, src, dst)

          # print 'da {}\ta {}\tlen {}\tsrcname {}\tdstname {}'.format(src, dst, lenshopa, srcname, dstname)
          if lenshopa in lenfreq: lenfreq[lenshopa] += 1
          else: lenfreq.update({lenshopa:1})
          if lenshopa <= maxhops:
            if nome not in cdc:
              dacollassare[nome] = set([src, dst])
              cdc[nome] = [ssd(src, dst)]
            else:
              dacollassare[nome].add(src)
              dacollassare[nome].add(dst)
              cdc[nome].append(ssd(src, dst))
    print 'len {} dacollassare: {}'.format(len(dacollassare), dacollassare)
    print 'len {} cdc: {}'.format(len(cdc), cdc)
    print 'lenfreq {}'.format(lenfreq)
    # for nome in dacollassare:
      # if len(dacollassare[nome]) <> len(daNomiNum[nome]):
        # t = 'nome {}\tlen(daco) {}\tlen daNONU {} daco {} daNONU {}'
        # print t.format(nome, len(dacollassare[nome]), len(daNomiNum[nome]), dacollassare[nome], daNomiNum[nome])
    uomo = 'w han'
    # uomo = 'carlo ferrari'
    uomo = 'guangyuan liu'
    print 'dacollassare[{}]: {}'.format(uomo, dacollassare[uomo])
    ccf = cdc[uomo]
    # ccf = [ [2,3], [1,2], [1,4], [3,4], [5,6], [5,7], [5,1] ]
    # ccf = [ [5,6], [3,5], [4,5] ]
    # ccf = [ [5,6], [3,5], [4,5], [3,6] ]
    print 'len(ccf): {} ccf {}'.format(len(ccf), ccf)
    # ccf = [[x[0],x[1]] for x in set((y[0],y[1]) for y in ccf)]
    # print 'len(ccf): {} ccf {}'.format(len(ccf), ccf)
    # src = ccf[0][0]
    # nodi = {src:[]}
    # for coppia in ccf:
      # print coppia
      # if src == coppia[0]:
        # nodi[src].append(coppia[1])
      # else:
        # src = coppia[0]
        # if src in nodi:
          # nodi[src].append(coppia[1])
        # else:
          # nodi[src] = [coppia[1]]
    # for n in nodi:
      # print('{} {}'.format(n, nodi[n]))
    acf = ccf
    for i in range(len(acf)):
      src = acf[i][0]
      dst = acf[i][1]
      # for j in range(i, len(acf)):
      for j in range(len(acf)):
        if acf[j][0] == dst:
          acf[j][0] = src
          print 'i:{} j:{} src:{} dst:{} acf:{}'.format(i, j, src, dst, ccf)
    print acf

    met = set()
    bcf = ccf
    stot = set()        # tutti gli autNum
    for coppia in bcf:
      stot |= set(coppia)
    tot = len(stot) # numero di autNum da vedere
    print 'len(stot) {}'.format(tot)

    i = 0
    gruppi = [set(bcf[0])]
    # while len(met) < tot:

    for coppia in bcf:
      if coppia[0] in gruppi[i] or coppia[1] in gruppi[i]:
        print 'aggiungo {}'.format(coppia)
        gruppi[i] |= set(coppia)
        met |= set(coppia)
    print gruppi


if __name__ == '__main__':
  print 'This program is CollassaNodiShortPath, being run by itself'
  #PATH TO FILES
  celaborati = 'Versione3_Multi'
  pfDatiPaj = join(celaborati, 'AutoriEdgeSNAP.paj')
  pfAutNum = join(celaborati, 'AutoriIdNumNomi.txt') # ID e Numero e Nome
  collassaNodiShortPath(pfAutNum, pfDatiPaj)
