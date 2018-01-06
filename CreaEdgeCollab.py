#! python2

#in PapAutAffDEIampi.txt ho IDpap-IDaut
#carico in dizionario IDpap:IDaut1,IDaut2,IDaut3
#creo gli edge IDaut1.2;13;23;

CARTELLA = "Versione2\\"

def ptype(obj):
  print obj, " - ", type(obj)


dpaa = {} #carico il dizionario {paper:[a1,a2,a4,a3]}
fpaa = open(CARTELLA+"PapAutAffDEIampi.txt")
#fpaa = open(CARTELLA+"PaperPadovaniCompletiAmpi.txt")
for line in fpaa:
  pezzi = line.split("\t")
  if not dpaa.has_key(pezzi[0]): dpaa.update({pezzi[0]:[]})     #se non c'e' la chiave creo lista vuota
  dpaa[pezzi[0]].append(pezzi[1])
  #ptype(dpaa[pezzi[0]])
fpaa.close()
#print dpaa

#controllo duplicati nei IDaut dei paper
#check solo sugli ID, non considera i nomi
fpaperloop = open(CARTELLA+"PaperAADALoopBis.txt", "w")
for entry in dpaa:
  if len(dpaa[entry]) <> len(set(dpaa[entry])):
    print "paper con ID duplicati nella lista:", entry, "lista", dpaa[entry]
    fpaperloop.write("paper con ID duplicati nella lista: "+ entry + " lista: " + str(dpaa[entry]) + "\n")
    
fpaperloop.close()
  

#creo edge a1a2,a1a4,a1a3,a2a4,a2a3,a3a4 pesati
dedgepesati = {}
for entry in dpaa:
  ledge = dpaa[entry]
  #print len(ledge)
  i=0
  #ptype(ledge)
  while i<len(ledge)-1:
    j=i+1
    while j<len(ledge):
      if ledge[i]<ledge[j]: coppia = ledge[i]+"\t"+ledge[j]
      else: coppia = ledge[j]+"\t"+ledge[i]
      #print coppia
      if not dedgepesati.has_key(coppia): dedgepesati.update({coppia:1})
      else: dedgepesati[coppia]+=1      
      j+=1
    i+=1
#print dedgepesati

fedge = open(CARTELLA+"EdgeCollabPesatiAmpiBis.txt", "w")
#fedge = open(CARTELLA+"EdgePadovaniCompletiPesatiAmpiBis.txt", "w")
for entry in dedgepesati:
  fedge.write(entry+"\t"+str(dedgepesati[entry])+"\n")
fedge.close()
