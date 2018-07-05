#!python2

import matplotlib.pyplot as plt
from bokeh.palettes import Set3, Category20
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

def aggregaValidazione(pftValidation, validation):
  # file tsv
  pfValidation = pftValidation.format('tsv')
  with open(pfValidation, 'wb') as fValidation:
    for strada in sorted(validation.keys()):
      hcv = validation[strada]
      # fValidation.write('{:38}\t{:4.2f}\t{:4.2f}\t{:4.2f}\r\n'.format(strada, hcv[0], hcv[1], hcv[2]) )
      fValidation.write('{:38}\t{:4.2f}\r\n'.format(strada, hcv[2]) )

  # file pdf
  pfValidation = pftValidation.format('pdf')
  fig, ax = plt.subplots()
  colors = Set3[12]
  ax.set_xlabel('Tipologia di esplorazione')
  ax.set_ylabel('V-measure')
  ax.set_title('V-measure delle partizioni')

  # names = sorted( [x for x in validation if re.search(x, 'noNone')])
  names = sorted(validation)
  values = [float(validation[x][2]) for x in names]
  names = [x for x in range(len(values))]
  # names = ['group_a', 'group_b', 'group_c']
  # values = [1, 10, 100]
  print(type(names[0]))
  print(type(values[0]))
  plt.bar(names, values, color=colors)

  fig.savefig(pfValidation)


if __name__ == '__main__':
  pfValidation = ''
  validation = {}
