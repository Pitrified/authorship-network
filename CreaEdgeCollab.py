#! python2

#in PapAutAffDEIampi.txt ho IDpap-IDaut
#carico in dizionario IDpap:IDaut1,IDaut2,IDaut3
#creo gli edge IDaut12;13;23;

def creaEdgeCollab(pfPapAutAff, pfEdgeCollab, dPAA=None):
  """
  in pfPapAutAff ho IDpap-IDaut
  in dPAA carico {IDpap:[IDa1, IDa2, IDa4, IDa3]}
  in pfEdgeCollab creo edge IDa1-2, IDa1-4, IDa1-3, IDa2-4, IDa2-3, IDa3-4 con pesi
  """
  if dPAA is None:
    dPAA = {}
    with open(pfPapAutAff, 'rb') as fPapAutAff:
      for line in fPapAutAff:
        #print line,
        pezzi = line.rstrip().split("\t")
        if not dPAA.has_key(pezzi[0]):    #pezzi[0] : IDpap
          dPAA.update({pezzi[0]:[]})      #se non c'e' la chiave creo lista vuota
        dPAA[pezzi[0]].append(pezzi[1])   #carico pezzi[1] = IDaut nella lista
  #else:
    #print 'arrivato {}'.format(dPAA)

  dEdgeCollab = {}
  for entry in dPAA:
    ledge = dPAA[entry]
    #print len(ledge)
    i=0
    #ptype(ledge)
    while i<len(ledge)-1:
      j=i+1
      while j<len(ledge):
        if ledge[i]<ledge[j]: coppia = ledge[i]+"\t"+ledge[j]
        else: coppia = ledge[j]+"\t"+ledge[i]
        #print coppia
        if not dEdgeCollab.has_key(coppia): dEdgeCollab.update({coppia:1})
        else: dEdgeCollab[coppia]+=1      
        j+=1
      i+=1
  #print dEdgeCollab
    
  with open(pfEdgeCollab, 'wb') as fEdgeCollab: 
    for entry in dEdgeCollab:
      fEdgeCollab.write('{}\t{}\r\n'.format(entry, dEdgeCollab[entry]))
      #fEdgeCollab.write(entry+"\t"+str(dEdgeCollab[entry])+"\n")
  return dEdgeCollab

if __name__ == '__main__':
  print 'This program is CreaEdgeCollab, being run by itself' 
  #PATH TO FILES
  celaborati = 'Versione3_Single\\'
  pfPapAutAff = celaborati + 'PapAutAffDEI.txt'
  pfEdgeCollab = celaborati + 'EdgeCollab.txt'
  creaEdgeCollab(pfPapAutAff, pfEdgeCollab)
  print 'finitoCECsolo'
else:
  print 'I am CreaEdgeCollab, being imported from another module'


##trova i paper che creeranno selfloop
# #controllo duplicati nei IDaut dei paper
# #check solo sugli ID, non considera i nomi
# fpaperloop = open(CARTELLA+"PaperAADALoopBis.txt", "w")
# for entry in dpaa:
  # if len(dpaa[entry]) <> len(set(dpaa[entry])):
    # print "paper con ID duplicati nella lista:", entry, "lista", dpaa[entry]
    # fpaperloop.write("paper con ID duplicati nella lista: "+ entry + " lista: " + str(dpaa[entry]) + "\n")
# fpaperloop.close()
  
