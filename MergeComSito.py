#!python2

def mergeComSito(pfMod, pfAbbreviate, pfMerge):
  with open(pfMod, 'rb') as fMod, open(pfAbbreviate, 'rb') as fAbbreviate, open(pfMerge, 'wb') as fMerge:
    dAbbr = {'Label' : ['Comunita']}
    for line in fAbbreviate:
      pezzi = line.rstrip().split('\t')
      if pezzi[0] in dAbbr:
        # print('{} incontrato di nuovo,\nprima {}\nora   {}'.format(pezzi[0], dAbbr[pezzi[0]], pezzi[1]))
        if pezzi[1] not in dAbbr[pezzi[0]]:
          dAbbr[pezzi[0]].append(pezzi[1])
          # print(dAbbr[pezzi[0]])
      else:
        dAbbr[pezzi[0]] = [pezzi[1]]
    for line in fMod:
      com = 'NA'
      pezzi = line.rstrip().split('\t')
      if pezzi[1] in dAbbr:
        # print('{} {}'.format(pezzi[1], dAbbr[pezzi[1]]))
        if len(dAbbr[pezzi[1]]) == 1:
          com = dAbbr[pezzi[1]][0]
        else:
          com = 'Multipli'
      fMerge.write('{}\t{}\t{}\t{}\r\n'.format(pezzi[0], pezzi[1], pezzi[2], com))

def analizzaComunita(pfMerge, pfFreq):
  with open(pfMerge, 'rb') as fMerge, open(pfFreq, 'wb') as fFreq:
    dCoppie = {}
    for line in fMerge:
      pezzi = line.rstrip().split('\t')
      coppia = '{}\t{}'.format(pezzi[2], pezzi[3])
      if coppia in dCoppie:
        dCoppie[coppia] += 1
      else:
        dCoppie[coppia] = 1
    for coppia in dCoppie:
      # print('{}\t{}'.format(dCoppie[coppia], coppia))
      fFreq.write('{}\t{}\r\n'.format(dCoppie[coppia], coppia))

def comunitaMergeAnalizza(pfMod, pfAbbreviate, pfMerge, pfFreq):
  # prende un file di comunita ID Nome Comunita
  # prende un file di Nomi ComunitaDalSito
  # conta le frequenze delle coppie Comunita-ComunitaDalSito
  mergeComSito(pfMod, pfAbbreviate, pfMerge)
  analizzaComunita(pfMerge, pfFreq)


if __name__ == '__main__':
  # print('This program is MergeComSito, being run by itself')

  tag = 'GIU'
  pfAbbreviate = 'PersoneNomiComunitaAbbreviate{}.txt'.format(tag)
  pfMod = 'AutoriCollabClasse_padovani_distanza.tsv'
  pfMerge = 'AutoriCollabClasseMergeComunita_padovani_distanza.tsv'
  pfFreq = 'FrequenzaMergeComunita_padovani_distanza.tsv'

  comunitaMergeAnalizza(pfMod, pfAbbreviate, pfMerge, pfFreq)

