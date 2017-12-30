#! python2


#in AutoriDEIampi.txt ci sono IDaut-NOMIautori, salvo gli IDaut in un set
#in PaperAuthorAffiliations.txt ci sono IDpap-IDaut-IDaff, se IDaut e' nel set
#salvo in PapAutAffDEIampi.txt

sidaut = set()
faut = open("AutoriDEIampi.txt")
for line in faut:
  pezzi = line.split("\t", 1)
  #print pezzi[0]
  sidaut.add(pezzi[0])
  
#pat="C:\Users\Pietro\Documents\Universit"+u"\u00E0"+"\Tesi\Programmi\PaperAuthorAffiliations.txt"
pat = "C:\Users\Test\Documents\Tesi\FileRAW\PaperAuthorAffiliations.txt"
fid = open(pat, "r")
fout = open("PapAutAffDEIampi.txt", "w") 

for line in fid:
  pezzi = line.split("\t")
  #print pezzi[1]
  if pezzi[1] in sidaut:
    fout.write(line)
    #print line,
  
#print sidaut

