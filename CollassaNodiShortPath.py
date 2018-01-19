#!python2

import snap
from itertools import combinations, product
from timeit import default_timer as timer


def creaAbbreviazioni(autNome, dAbbreviazioni):
  # creo tutte le abbreviazioni dal nome
  # labbr = [] # lista di abbreviazioni da questo nome 
  # caricate in dAbbreviazioni
  tocchi = autNome.split()
  # print tocchi, len(tocchi), len(tocchi[0]), tocchi[0][0]
  if not dAbbreviazioni.has_key(autNome):
    if len(tocchi) == 0:  # manca
      pass
      # print('Nome vuoto molto male')
    elif len(tocchi) == 1:  # singolo
      dAbbreviazioni.update({autNome:[]})
    elif len(tocchi) == 2:
      if len(tocchi[0]) <> 1:
        dAbbreviazioni.update({autNome:[tocchi[0][0]+' '+tocchi[1]]})
      else:
        dAbbreviazioni.update({autNome:[]})
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
      # print sa
      dAbbreviazioni.update({autNome:[x for x in sa]})
      pass 
  else:
    # print 'visto gia {} lista {}'.format(autNome, dAbbreviazioni[autNome])
    pass
  pass

def checkNome(autNome, daNomeAbb, dAbbreviazioni):
  fullnames = []
  labbr = []
  for entry in dAbbreviazioni:
    if autNome in dAbbreviazioni[entry]:
      fullnames.append(entry)
      for x in dAbbreviazioni[entry]:
        if x not in labbr:
          labbr.append(x)
  longest = ''
  for name in fullnames:
    if len(name) > len(longest):
      longest = name
  if daNomeAbb.has_key(longest):
    for abb in labbr:
      if abb not in daNomeAbb[longest]:
        daNomeAbb[longest].append(abb)
  else:
    if longest <> '':
      daNomeAbb.update({longest:labbr})
    else:
      daNomeAbb.update({autNome:[]})
  # print 'fulln: {} labbr: {} autNome: {} longest: {}'.format(fullnames, labbr, autNome, longest)
      

def collassaNodiShortPath(pfAutNum, pfAbbr, pfDatiPaj):
  #edge e autori non collassati
  UGraph = snap.LoadPajek(snap.PUNGraph, pfDatiPaj) 

  with open(pfAutNum, 'rb') as fAutNum:
    # load nomi id num
    daID   = {} # {id : numero, nome}
    daNum  = {} # {numero : id, nome}
    daNome = {} # {nome : (id, num)}
    for line in fAutNum:
      pezzi = line.rstrip().split('\t')
      autID = pezzi[0]
      autNum = int(pezzi[1])
      autNome = pezzi[2]
      daID.update({autID:[autNum, autNome]})
      daNum.update({autNum:[autID, autNome]})
      daNome.update({autNome:[autID, autNum]})
    # print('daID: {}\n\ndaNum: {}\n\ndaNome: {}'.format(daID, daNum, daNome))
  
    fAutNum.seek(0)
    start = timer()
    dAbbreviazioni = {} # {con cani cose:[c c cose, con c cose, c cani cose]}
    for line in fAutNum:
      pezzi = line.rstrip().split('\t')
      autNome = pezzi[2]
      creaAbbreviazioni(autNome, dAbbreviazioni)
    end = timer()
    # print 'creaAbbreviazioni in {}'.format(end-start)
    # print 'dAbbreviazioni: {}'.format(dAbbreviazioni)
    
    daNomeAbb = {}  # {fullest name:[abbreviazioni che incontro...]}
    fAutNum.seek(0)
    for line in fAutNum:
      pezzi = line.rstrip().split('\t')
      autNome = pezzi[2]
      checkNome(autNome, daNomeAbb, dAbbreviazioni)
    # print '\ndaNomeAbb: {}'.format(daNomeAbb)
    
    daNomiNum = {} # {nomefull:[numeri di id legati al nome]}
    for nome in daNomeAbb:
      # print 'nome {}'.format(nome)
      daNomiNum.update({nome:[daNome[nome][1]]})
      for abb in daNomeAbb[nome]:
        if abb in daNome: # tendenzialmente sempre
          if daNome[abb][1] in daNomiNum[nome]:
            pass
            # print 'avevo gia visto abb {} con nome {} e daNome[abb][1] {}'.format(abb, nome, daNome[abb][1])
          else:
            daNomiNum[nome].append(daNome[abb][1])
    # print '\ndaNomiNum: {}'.format(daNomiNum)

    lenfreq = {}
    dacollassare = []
    i = -1
    maxhops = 10 
    for nome in daNomiNum:
      new = True
      if len(daNomiNum[nome]) > 1:
        print 'nome: {}\tdaNomiNum[nome]: {}'.format(nome, daNomiNum[nome])
        for src, dst in combinations(daNomiNum[nome], 2):
          # src = daNomiNum[nome][0]
          # dst = daNomiNum[nome][1]
          srcname = daNum[src][1]
          dstname = daNum[dst][1]
          # print type(src), type(dst)
          lenshopa = snap.GetShortPath(UGraph, src, dst)
          print 'da {}\ta {}\tlen {}\tsrcname {}\tdstname {}'.format(src, dst, lenshopa, srcname, dstname)
          if lenshopa in lenfreq: lenfreq[lenshopa] += 1
          else: lenfreq.update({lenshopa:1})
          if lenshopa <= maxhops:
            if new: # devo creare nuovo set 
              new = False
              i += 1
              dacollassare.append(set())
            dacollassare[i].add(src)
            dacollassare[i].add(dst)
    print 'dacollassare: {}'.format(dacollassare)
    print 'lenfreq {}'.format(lenfreq)

if __name__ == '__main__':
  print 'This program is CollassaNodiShortPath, being run by itself' 
  #PATH TO FILES
  celaborati = 'Versione3_Multi\\'
  pfDatiPaj = celaborati + 'AutoriEdgeSNAP.paj'
  pfAutNum = celaborati + 'AutoriIdNumNomi.txt'  # ID e Numero e Nome
  pfAbbr = celaborati + 'PersoneDEIabbr.txt'
  collassaNodiShortPath(pfAutNum, pfAbbr, pfDatiPaj)
  
"""


# ho nomi ed abbreviazioni mescolati
# creo {c cose:[]}
#      {con c cose:[c c cose]}
#      {con cani cose:[c c cose, con c cose, c cani cose]}
# scorro nomi ed abbreviazioni
# - se sono nelle liste delle abbreviazioni 'c c cose'
# - so il nome che le ha generate? forse ne trovo piu di una
# - prendo la piu lunga
# ora che ho {con cani cose: con c cose}
# creo {con cani cose:[numeriiii...]}

def creaAbbreviazioni(autNome, dAbbreviazioni):
  # creo tutte le abbreviazioni dal nome
  # labbr = [] # lista di abbreviazioni da questo nome 
  # caricate in dAbbreviazioni
  tocchi = autNome.split()
  # print tocchi, len(tocchi), len(tocchi[0]), tocchi[0][0]
  if not dAbbreviazioni.has_key(autNome):
    if len(tocchi) == 0:  # manca
      pass
      # print('Nome vuoto molto male')
    elif len(tocchi) == 1:  # singolo
      dAbbreviazioni.update({autNome:[]})
    elif len(tocchi) == 2:
      if len(tocchi[0]) <> 1:
        dAbbreviazioni.update({autNome:[tocchi[0][0]+' '+tocchi[1]]})
      else:
        dAbbreviazioni.update({autNome:[]})
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
      # print sa
      dAbbreviazioni.update({autNome:[x for x in sa]})
      pass # itertools product
    # if len(tocchi) == 3:
      # if len(tocchi[0]) <> 1 and len(tocchi[1]) <> 1:
        # a1 = tocchi[0][0]+' '+tocchi[1][0]+' '+tocchi[2]
        # a2 = tocchi[0]   +' '+tocchi[1][0]+' '+tocchi[2]
        # a3 = tocchi[0][0]+' '+tocchi[1]   +' '+tocchi[2]
        # sa = set((a1,a2,a3))
        # dAbbreviazioni.update({autNome:[x for x in sa]})
      # else:
        # dAbbreviazioni.update({autNome:[]})
  else:
    # print 'visto gia {} lista {}'.format(autNome, dAbbreviazioni[autNome])
    pass
  pass

def checkNome(autNome, daNomeAbb, dAbbreviazioni):
  fullnames = []
  labbr = []
  for entry in dAbbreviazioni:
    if autNome in dAbbreviazioni[entry]:
      fullnames.append(entry)
      for x in dAbbreviazioni[entry]:
        if x not in labbr:
          labbr.append(x)
  longest = ''
  for name in fullnames:
    if len(name) > len(longest):
      longest = name
  if daNomeAbb.has_key(longest):
    for abb in labbr:
      if abb not in daNomeAbb[longest]:
        daNomeAbb[longest].append(abb)
  else:
    if longest <> '':
      daNomeAbb.update({longest:labbr})
    else:
      daNomeAbb.update({autNome:[]})
  # print 'fulln: {} labbr: {} autNome: {} longest: {}'.format(fullnames, labbr, autNome, longest)
  # print ''.format(labbr)
      
      # # tutte le entry abbreviate ???
  # # print autNome, fullnames
  # # if len(fullnames) > 1: print autNome, fullnames
  # fn = ''
  # abb= ''
  # if len(fullnames) == 0:
    # # daNomeAbb.update({autNome:[]})
    # fn  = autNome
    # abb = ''
  # if len(fullnames) == 1:
    # # daNomeAbb.update({fullnames[0]:autNome})
    # fn  = fullnames[0]
    # abb = autNome
  # if len(fullnames) >  1:
    # longest = ''
    # for name in fullnames:
      # if len(name) > len(longest):
        # longest = name
    # # daNomeAbb.update({longest:autNome})
    # fn  = longest
    # abb = autNome
    # # print autNome, longest
    # # ma se longest, autNome, fullnames[0] ci sono gia nel dizionario ???
  # if daNomeAbb.has_key(fn):
    # daNomeAbb[fn].add(abb)
  # else:
    # daNomeAbb.update({fn:set(abb)})
  # pass
  

#edge e autori non collassati
UGraph = snap.LoadPajek(snap.PUNGraph, 'AutoriEdgeSNAP.paj') 

pfAutNum = 'AutoriIdNumNomi.txt'  # ID e Numero e Nome
# pfAut = 'AutoriCollabMacro.txt'   #non collassati
# pfEdge = 'EdgeCollabMacro.txt'

with open(pfAutNum, 'rb') as fAutNum: # , open(pfAut, 'rb') as fAut:
  daID  = {} # {id : numero}
  daNum = {} # {numero : id}
  daNome = {} # {nome : (id, num)}
  for line in fAutNum:
    pezzi = line.rstrip().split('\t')
    autID = pezzi[0]
    autNum = int(pezzi[1])
    autNome = pezzi[2]
    daID.update({autID:[autNum, autNome]})
    daNum.update({autNum:[autID, autNome]})
    daNome.update({autNome:[autID, autNum]})
    
  fAutNum.seek(0)
  start = timer()
  dAbbreviazioni = {} # {con cani cose:[c c cose, con c cose, c cani cose]}
  for line in fAutNum:
    pezzi = line.rstrip().split('\t')
    autNome = pezzi[2]
    creaAbbreviazioni(autNome, dAbbreviazioni)
  end = timer()
  print 'creaAbbreviazioni in {}'.format(end-start)
  print 'dAbbreviazioni: {}'.format(dAbbreviazioni)
  
  daNomeAbb = {}  # {fullest name:[abbreviazioni che incontro...]}
  fAutNum.seek(0)
  for line in fAutNum:
    pezzi = line.rstrip().split('\t')
    autNome = pezzi[2]
    checkNome(autNome, daNomeAbb, dAbbreviazioni)
  print '\ndaNomeAbb: {}'.format(daNomeAbb)
  
  daNomiNum = {} # {nomefull:[numeri di id legati al nome]}
  for nome in daNomeAbb:
    # print 'nome {}'.format(nome)
    daNomiNum.update({nome:[daNome[nome][1]]})
    for abb in daNomeAbb[nome]:
      if abb in daNome:
        daNomiNum[nome].append(daNome[abb][1])
  print '\ndaNomiNum: {}'.format(daNomiNum)

  lenfreq = {}
  for nome in daNomiNum:
    if len(daNomiNum[nome]) > 1:
      print '{}'.format(daNomiNum[nome])
      for src, dst in combinations(daNomiNum[nome], 2):
        # src = daNomiNum[nome][0]
        # dst = daNomiNum[nome][1]
        srcname = daNum[src][1]
        dstname = daNum[dst][1]
        # print type(src), type(dst)
        lenshopa = snap.GetShortPath(UGraph, src, dst)
        print 'da {}\ta {}\tlen {}\tsrcname {}\tdstname {}'.format(src, dst, lenshopa, srcname, dstname)
      if lenshopa in lenfreq: lenfreq[lenshopa] += 1
      else: lenfreq.update({lenshopa:1})
  print 'lenfreq {}'.format(lenfreq)
  
  
# scorro nodi a gruppi di omonimi
# calcolo tutte le distanze tra omonimi
# scopro cose

"""
