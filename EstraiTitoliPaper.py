#! python2

#carica da PaperAutAffDEI.txt gli ID dei paper scritti da AutoriDEI
#scorri Papers.txt e se l'ID e' noto copia la riga

spaper = set()

#fpapautaff = open("PaperAutAffDEI.txt", "r")
fpapautaff = open("PapAutAffDEIampi.txt", "r")

for line in fpapautaff:
  pezzi = line.split("\t", 1)
  spaper.add(pezzi[0])

fpapautaff.close()

pat="C:\Users\Pietro\Documents\Universit"+u"\u00E0"+"\Tesi\Programmi\Papers.txt"
fpapers = open(pat, "r")
ltitoli = []

for line in fpapers:
  pezzi = line.split("\t", 1)
  if pezzi[0] in spaper:
    ltitoli.append(line)
    #print line
    
#print ltitoli

#ftitoli = open("PapersDEITitoli.txt", "w")
ftitoli = open("PapersDEITitoliAmpi.txt", "w")
ftitoli.writelines(ltitoli)