#!python2

from graph_tool.all import *
from random import randint
from numpy import sqrt, log

def disegnaGrafo(pfGT, pfOut, pfClassi):
  g = Graph(directed=False)
  v_id = g.new_vertex_property('string')
  v_nome = g.new_vertex_property('string')
  v_label = g.new_vertex_property('string')
  # e_weight = g.new_edge_property('int')
  e_weight = g.new_edge_property('float')
  e_text = g.new_edge_property('string')
  e_color = g.new_edge_property('int')

  with open(pfGT, 'rb') as fPaj:
    line = fPaj.readline().rstrip()
    N = int(line.split(' ')[1])
    # print(N)
    for i in range(N):
      line = fPaj.readline().rstrip()
      # print(line)
      num = int(line.split('\t')[0]) # graphtool parte da 0
      nome = line.split('\t')[1]
      idaut = line.split('\t')[2]
      # print(num, nome)
      v = g.add_vertex()
      v_nome[v] = nome
      v_id[v] = idaut
    lineadiintestazioneedge = fPaj.readline()
    for line in fPaj:
      pz = line.rstrip().split()
      src = int(pz[0])
      dst = int(pz[1])
      wei = int(pz[2])
      e = g.add_edge(g.vertex(src), g.vertex(dst) )
      e_weight[e] = wei
      if wei > 5:
        e_text[e] = wei

  deg = g.degree_property_map('total', e_weight)
  # deg = g.degree_property_map("in")
  # deg.a = 4 * (sqrt(deg.a) * 0.5 + 0.4)
  deg.a = 2 * (sqrt(deg.a) * 0.3 + 0.4)
  # deg.a = 1 * (sqrt(sqrt(deg.a)) * 0.2 + 0.4)
  # deg.a = 1 * (log(deg.a) * 0.2 + 0.4)
  degoriginale = g.degree_property_map('total', e_weight)
  e_norm = g.new_edge_property('float')
  e_norm.a = 2 * (sqrt(e_weight.a) * 0.2 + 0.1)

  state = minimize_blockmodel_dl(g)
  com = state.get_blocks()
  print('Numero di comunita minimize_blockmodel_dl {}'.format(max(com.a)))

  # estetica grafo
  for e in g.edges():
    if deg[e.source()] > deg[e.target()]:
      e_color[e] = com[e.source()]
    else:
      e_color[e] = com[e.target()]
  for v in g.vertices():
    if degoriginale[v] > 20:
      v_label[v] = v_nome[v].title()


  pos = sfdp_layout(g, eweight=e_weight,
              # p=8,
              K = 10000,
              C = 1.6,
              )
  graph_draw(g, pos=pos,
             vertex_size=deg,
             vertex_text=v_label,
             vertex_text_position = 1,
             vertex_font_size=5,
             # vertex_color=com,
             vertex_fill_color=com,
             edge_pen_width=e_norm,
             edge_text=e_text,
             edge_font_size=5,
             edge_color=e_color,
             output_size=(1500, 1500), output=pfOut.format(''), # tutto il grafo
             )

  lc = label_largest_component(g)
  g.set_vertex_filter(lc)

  pos = sfdp_layout(g, eweight=e_weight,
              # p=8,
              K = 10000,
              C = 1.6,
              )
  graph_draw(g, pos=pos,
             vertex_size=deg,
             vertex_text=v_label,
             vertex_text_position = 1,
             vertex_font_size=5,
             # vertex_color=com,
             vertex_fill_color=com,
             edge_pen_width=e_norm,
             edge_text=e_text,
             edge_font_size=5,
             edge_color=e_color,
             output_size=(1500, 1500), output=pfOut.format('_gc'), # solo componente centrale
             )

  with open(pfClassi, 'wb') as fClassi:
    for v in g.vertices():
      fClassi.write('{}\t{}\t{}\r\n'.format(v_id[v], v_nome[v], com[v]) )

  # nodes properties:
  # font_size, size, fill_color, color
  # edges
  # color, pen_width, text, font_size
  # for v in list(g.vertices()):#[0:5]:
    # print('comunita {}'.format(com[v]))
  # for e in list(g.edges())[0:50]:
    # print('peso {}'.format(e_weight[e]) )


if __name__ == '__main__':
  # print('disegnaGrafo eseguito da solo')
  # pfEdge = 'EdgeUnificatiGephi_padovani_distanza_DEI.tsv'
  # pfAutori = 'AutoriUnificatiGephi_padovani_distanza_DEI.tsv'
  pfGT = 'AutoriEdgeCollab_padovani_DEI.tsv'
  pfOut = 'padovani.pdf'
  pfClassi = 'AutoriComunitaGT.tsv'

  disegnaGrafo(pfGT, pfOut, pfClassi)



