#! python3

#in decodedhtml una lista di titoli
#in PapersDEITitoli.txt coppie ID-titoli
#in PaperAutIDFORNASINIAff.txt ID di paper scritti da fornasini


from urllib.request import urlopen
import re

url = "http://www.dei.unipd.it/~fornasini/"
html = urlopen(url)
rawhtml = html.read()
decodedhtml = rawhtml.decode('utf-8').lower()
fhtml = open("PubblicazioniFornasiniHTML.txt", "w")
fhtml.write(decodedhtml)
decodedhtml = decodedhtml.replace("\n"," ")
decodedhtml = decodedhtml.replace("  "," ")
decodedhtml = decodedhtml.replace("  "," ")
decodedhtml = decodedhtml.replace("  "," ")
decodedhtml = decodedhtml.replace(" ","")
decodedhtml = decodedhtml.replace("-","")
decodedhtml = decodedhtml.replace("/","")


#print(decodedhtml)

dtitoli = {}                #dizionario ID-titoli
ftitoli = open("PapersDEITitoli.txt", encoding="utf8") 
for line in ftitoli:
  pezzi = line.split("\t")  #pezzi[0] e' l'ID del paper, pezzi[1] e' il titolo del paper
  ID = pezzi[0]
  titolo = pezzi[1]
  dtitoli.update({ID:titolo})
  
ffornasini = open("PaperAutIDFORNASINIAff.txt")
fmancati = open("TitoliMancati.txt", "w")
hit, miss = 0,0

for line in ffornasini:
  pezzi = line.split("\t")  #pezzi[0] e' l'ID del paper
  #print("String:\t", dtitoli[pezzi[0]])
  titolofravirg = re.search(r'"(.*?)"', dtitoli[pezzi[0]])
  if titolofravirg:
    #print("REG:\t", titolofravirg.group(1))
    titolo = titolofravirg.group(1)
  else:
    #print("NOREG:\t", dtitoli[pezzi[0]])
    titolo = dtitoli[pezzi[0]]
  #print(titolo)
  
  if titolo.lower().replace(" ","").replace("-","").replace("/","") in decodedhtml: hit+=1
  else:
    miss+=1
    #fmancati.write(pezzi[0]+"\t"+dtitoli[pezzi[0]]+"\n")
    fmancati.write(pezzi[0]+"\t"+titolo.lower()+"\n")

print("Hit: ", hit, "\tMiss: ", miss)