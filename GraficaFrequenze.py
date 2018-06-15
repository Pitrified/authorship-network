import matplotlib.pyplot as plt
from bokeh.palettes import Set3, Category20
# import numpy as np
# from matplotlib.ticker import MaxNLocator
# from collections import namedtuple

# def shift(mylist, offset):
  # return [i + offset for i in mylist]

def accorcia(tag):
  return tag.split(' - ')[0]

def graficaFrequenzePerSito(pfComunita, pfGrafico):
  data = {}
  # data = {'elettronica' : {0:12, 5:2},
  #         'automazione' : {1:23, 2:70, 4:2},
  #         'informatica' : {3:32, 4:5, 5:1}
  #         }
  # print(data)
  max_com = 1
  with open(pfComunita, 'rb') as fComunita:
    for line in fComunita:
      freq, com, tag = line.rstrip().split('\t')
      if tag in ['None', 'NA', 'Multipli']: continue
      tag = accorcia(tag)
      # print(tag)
      com = int(com)
      freq = int(freq)
      if com > max_com: max_com = com
      if tag not in data:
        data[tag] = {}
      data[tag][com] = freq

  index = [ [] for _ in range(max_com+1)]
  value = [ [] for _ in range(max_com+1)]
  width = [ [] for _ in range(max_com+1)]

  bin_width = 0.8
  bin_pos = [i + bin_width/2 for i in range(1, len(data)+1)]
  i=1
  for tag in sorted(data, key=lambda x: len(data[x]), reverse=True ):
    # print(tag)
    cf = data[tag]
    bin_step = bin_width / len(cf)
    j=0
    for com in sorted(cf, key=lambda x: cf[x], reverse=True):
      # print(com, cf[com])
      index[com].append(i + bin_step*j + bin_step/2)
      value[com].append(cf[com])
      width[com].append(bin_step)
      j+=1
    i+=1

  # print(index)
  # print(value)
  # print(width)

  fig, ax = plt.subplots()
  opacity = 0.4
  opacity = 1
  colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
  colors = Set3[12]

  for com in range(max_com+1):
    ax.bar(index[com], value[com], width[com], alpha=opacity, color=colors[com%len(colors)], label=com)


  ax.set_xlabel('Comunita\'')
  ax.set_ylabel('Frequenze')
  ax.set_title('Frequenze delle comunita\' generate per comunita\' calcolata')
  # index_shift2 = [i + bar_width  for i in index_all]
  # print(index_shift2)
  ax.set_xticks(bin_pos)
  ax.set_xticklabels([x for x in data], rotation=90)
  # ax.xaxis.set_tick_params(rotation=45)
  # if max_com < 20:
    # ax.legend()

  fig.tight_layout()
  fig.savefig(pfGrafico)
  # plt.show()

def graficaFrequenzePerGenerate(pfComunita, pfGrafico):
  data = {}
  max_tag = 1
  tags = []
  with open(pfComunita, 'rb') as fComunita:
    for line in fComunita:
      freq, com, tag = line.rstrip().split('\t')
      if tag in ['None', 'NA', 'Multipli']: continue
      tag = accorcia(tag)
      com = int(com)
      freq = int(freq)
      if tag not in tags:
        tags.append(tag)
      t = tags.index(tag)
      if t > max_tag: max_tag = t
      if com not in data:
        data[com] = {}
      data[com][t] = freq

      # if com > max_com: max_com = com
      # if tag not in data:
        # data[tag] = {}
      # data[tag][com] = freq


  index = [ [] for _ in range(max_tag+1)]
  value = [ [] for _ in range(max_tag+1)]
  width = [ [] for _ in range(max_tag+1)]
  # print(data)

  bin_width = 0.8
  bin_pos = [i + bin_width/2 for i in range(1, len(data)+1)]
  i=1
  for tag in sorted(data, key=lambda x: len(data[x]), reverse=True ):
    # print(tag)
    cf = data[tag]
    bin_step = bin_width / len(cf)
    j=0
    for com in sorted(cf, key=lambda x: cf[x], reverse=True):
      # print(com, cf[com])
      index[com].append(i + bin_step*j + bin_step/2)
      value[com].append(cf[com])
      width[com].append(bin_step)
      j+=1
    i+=1

  # print(index)
  # print(value)
  # print(width)

  fig, ax = plt.subplots()
  # opacity = 0.4
  opacity = 1
  colors = Category20[20] # ['b', 'g', 'r', 'c', 'm', 'y', 'k']
  colors = Set3[12]

  for tag in range(max_tag+1):
    ax.bar(index[tag], value[tag], width[tag], alpha=opacity, color=colors[tag%len(colors)], label=tags[tag])


  ax.set_xlabel('Comunita\'')
  ax.set_ylabel('Frequenze')
  ax.set_title('Frequenze delle comunita\' scaricate suddivise per comunita\' generate')
  # index_shift2 = [i + bar_width  for i in index_all]
  # print(index_shift2)
  ax.set_xticks(bin_pos)
  ax.set_xticklabels([x for x in data], rotation=90)
  # ax.xaxis.set_tick_params(rotation=45)

  if max_tag < 20:
    ax.legend()
  # leg = ax.legend()
  # leg.loc = (1000,10)

  fig.tight_layout()
  fig.savefig(pfGrafico)
  # plt.show()
if __name__ == '__main__':
  pfComunita = 'ComunitaMergeFrequenza_tutti_distanza_blockmodel_DEI.tsv'
  pfGrafico = 'Grafico_sito_tutti_distanza_blockmodel.pdf'
  graficaFrequenzePerSito(pfComunita, pfGrafico)
  pfGrafico = 'Grafico_generate_tutti_distanza_blockmodel.pdf'
  graficaFrequenzePerGenerate(pfComunita, pfGrafico)
