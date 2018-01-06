#! python2


#in AutoriDEIampi.txt ci sono IDaut-NOMIautori, salvo gli IDaut in un set
#in PaperAuthorAffiliations.txt ci sono IDpap-IDaut-IDaff, se IDaut e' nel set
#salvo in PapAutAffDEIampi.txt

from timeit import default_timer as timer
import io

start = timer()

sidaut = set()


CARTELLA = "Versione2\\"
faut = open(CARTELLA+"AutoriDEIampi.txt")
#carico gli IDaut nel set
for line in faut:
  pezzi = line.split("\t", 1)
  #print pezzi[0]
  sidaut.add(pezzi[0])
  
print 'ci sono {} autori DEI'.format(len(sidaut))
  
#pat="C:\Users\Pietro\Documents\Universit"+u"\u00E0"+"\Tesi\Programmi\PaperAuthorAffiliations.txt"
# pat = "C:\Users\Test\Documents\Tesi\FileRAW\PaperAuthorAffiliations.txt"    #tempo: 172.679247183 righeparsizzate: 288264682
                                                                            # #tempo: 187.196060742 righeparsizzate: 325498062
pat = "C:\Users\Test\Documents\Tesi\FileRAW\PaperAuthorAffiliations5000000.txt"
fid = open(pat, "rb")
# fid = open(pat, "rb", newline='\r\n')

CARTELLA = 'C:\Users\Test\Documents\Linguaggi\Prove\proveFileMulti\PerTesi\\'
fout = open(CARTELLA+"PapAutAffDEIampi5000000Binary.txt", "w") 
# fout = io.open(CARTELLA+"PapAutAffDEIampi5000000Binary.txt", "wb", newline='\r\n') 

#se IDaut nel set copio la linea che descrive il paper
i=0
for line in fid:
  i+=1
  pezzi = line.split("\t")
  #print pezzi[1]
  if pezzi[1] in sidaut:
    fout.write(line.rstrip()+'\n')    #aperto in binery mode non riconosce i newline bene
    #print line,
  
#print sidaut

end = timer()
print 'tempo: {} righeparsizzate: {}'.format(end-start, i)