#!python2

from bokeh.palettes import Set3, Category20
from itertools import groupby
import matplotlib.pyplot as plt
import re

def getComClu(pfMerge):
  allcom = []
  allclu = []
  allcomnn = []
  allclunn = []
  com2num = {}
  comviste = 0
  with open(pfMerge, 'rb')as fMerge:
    for line in fMerge:
      pezzi = line.rstrip().split('\t')
      clu = pezzi[2]
      com = pezzi[3]
      # print(com, clu)
      if com not in com2num:
        com2num[com] = comviste
        comviste += 1
      if not com == 'None':
        com = com2num[com]
        allcomnn.append(com)
        allclunn.append(clu)
      allcom.append(com)
      allclu.append(clu)
  return allcom, allclu, allcomnn, allclunn

def spezzachiavi(x):
  # print('{} di tipo {}'.format(x, type(x) ) )
  sp = x[0:2]
  su = x[2:4]
  sc = x[4:6]
  return '{}{}'.format(sp, su)

def spezzacom(x):
  # print('{} di tipo {}'.format(x, type(x) ) )
  sp = x[0:2]
  su = x[2:4]
  sc = x[4:6]
  return '{}'.format(sc)

def autolabel(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 0.90*height,
                # '%d' % height,
                '{:4.2f}'.format(height),
                ha='center', va='bottom')

def autolabelVertical(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2. + 0.08,
                # 0.85*height,
                height - 0.05,
                '{:4.2f}'.format(height),
                rotation='vertical',
                fontsize='x-small',
                ha='center', va='bottom')


def aggregaValidazione(pftValidation, validation):
  # GENERALE
  sv = '_generale'
  # file tsv
  pfValidation = pftValidation.format(sv, 'tsv')
  with open(pfValidation, 'wb') as fValidation:
    for strada in sorted(validation.keys()):
      hcv = validation[strada]
      # fValidation.write('{:38}\t{:4.2f}\t{:4.2f}\t{:4.2f}\r\n'.format(strada, hcv[0], hcv[1], hcv[2]) )
      # fValidation.write('{:38}\t{:4.2f}\r\n'.format(strada, hcv[2]) )
      fValidation.write('{:8}\t{:4.2f}\r\n'.format(strada, hcv[2]) )

  # file pdf
  pfValidation = pftValidation.format(sv, 'pdf')
  fig, ax = plt.subplots()
  # colors = Set3[12]
  # colors = Set3[7]
  colors = Set3[6]
  ax.set_xlabel('Tipologia di esplorazione')
  ax.set_ylabel('V-measure')
  ax.set_title('V-measure delle partizioni')

  # names = sorted( [x for x in validation if re.search(x, 'noNone')])
  names = sorted(validation)
  values = [float(validation[x][2]) for x in names]
  ind = [x for x in range(len(values))]
  # names = ['group_a', 'group_b', 'group_c']
  # values = [1, 10, 100]
  # print(type(names[0]))
  # print(type(values[0]))
  # plt.bar(ind, values, color=colors)
  rects = ax.bar(ind, values, color=colors)
  autolabelVertical(ax, rects)
  # print(names)
  plt.xticks(ind, names, rotation='vertical')
  # plt.xticks(ind, names)#, rotation='vertical')

  fig.tight_layout()
  fig.savefig(pfValidation)
  plt.close(fig)

  # AGGREGATO PER PaNo, PaDi, PaEd, TuNo, TuDi, TuEd
  sv = '_Unione'
  # print('validation {}'.format(validation) )
  # spezzetto le chiavi
  gruppi = []
  chiavi = []
  for k, g in groupby(sorted(validation), key=lambda x:spezzachiavi(x) ):
    gruppi.append(list(g))
    chiavi.append(k)
  cg = zip(chiavi, gruppi)

  # aggrego i valori
  pfValidation = pftValidation.format(sv, 'tsv')
  with open(pfValidation, 'wb') as fValidation:
    names = []
    values = []
    for c in cg:
      # print(c)
      names.append(c[0] ) # ci appendo la chiave PaNo
      tot = 0
      for cv in c[1]:     # itero PaNoBl, PaNoGi...
        vm = validation[cv][2]  # estraggo la v-measure
        tot += vm
      values.append( float(tot) / len(c[1]) )
      fValidation.write('{}\t{}\r\n'.format(c[0], float(tot) / len(c[1]) ) )

  ind = [x for x in range(len(values))]
  fig, ax = plt.subplots()
  ax.set_xlabel('Tipologia di esplorazione')
  ax.set_ylabel('V-measure')
  ax.set_title('V-measure - aggregate per tipologia estrazione')
  # plt.bar(ind, values, color=colors)
  rects = ax.bar(ind, values, color=colors)
  autolabel(ax, rects)
  plt.xticks(ind, names, rotation='vertical')
  fig.tight_layout()
  pfValidation = pftValidation.format(sv, 'pdf')
  fig.savefig(pfValidation)


  # AGGREGATO PER Bl, Gi, Cl, Zb, Zc, Zg
  sv = '_Comunita'
  # print('validation {}'.format(validation) )
  # spezzetto le chiavi
  gruppi = []
  chiavi = []
  for k, g in groupby(sorted(validation, key=lambda x:spezzacom(x)), key=lambda x:spezzacom(x) ):
    gruppi.append(list(g))
    chiavi.append(k)
  cg = zip(chiavi, gruppi)

  # aggrego i valori
  pfValidation = pftValidation.format(sv, 'tsv')
  with open(pfValidation, 'wb') as fValidation:
    names = []
    values = []
    for c in cg:
      # print(c)
      names.append(c[0] ) # ci appendo la chiave PaNo
      tot = 0
      for cv in c[1]:     # itero PaNoBl, PaNoGi...
        vm = validation[cv][2]  # estraggo la v-measure
        tot += vm
      values.append( float(tot) / len(c[1]) )
      fValidation.write('{}\t{}\r\n'.format(c[0], float(tot) / len(c[1]) ) )

  ind = [x for x in range(len(values))]
  fig, ax = plt.subplots()
  ax.set_xlabel('Tipologia di esplorazione')
  ax.set_ylabel('V-measure')
  ax.set_title('V-measure - aggregate per comunita\'')
  # plt.bar(ind, values, color=colors)
  rects = ax.bar(ind, values, color=colors)
  plt.xticks(ind, names, rotation='vertical')
  autolabel(ax, rects)
  fig.tight_layout()
  pfValidation = pftValidation.format(sv, 'pdf')
  fig.savefig(pfValidation)

if __name__ == '__main__':
  pfValidation = ''
  validation = {}


