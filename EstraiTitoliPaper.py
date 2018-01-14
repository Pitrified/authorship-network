#! python2

#carica da PaperAutAffDEI.txt gli ID dei paper scritti da AutoriDEI
#scorri Papers.txt e se l'ID e' noto copia la riga

CARTELLA = "Versione2\\"

spaper = set()

#fpapautaff = open(CARTELLA+"PaperAutAffDEI.txt", "r")
fpapautaff = open(CARTELLA+"PapAutAffDEIampi.txt", "r")

for line in fpapautaff:
  pezzi = line.split("\t", 1)
  spaper.add(pezzi[0])

fpapautaff.close()

pat="..\FileRAW\Papers.txt"
fpapers = open(pat, "r")
ltitoli = []

for line in fpapers:
  pezzi = line.split("\t", 1)
  if pezzi[0] in spaper:
    ltitoli.append(line)
    #print line
    
#print ltitoli

#ftitoli = open(CARTELLA+"PapersDEITitoli.txt", "w")
ftitoli = open(CARTELLA+"PapersDEITitoliAmpi.txt", "w")
ftitoli.writelines(ltitoli)
ftitoli.close()



