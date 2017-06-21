# authorship-network

## File originali msr.zip ##
#Column number  Column description

Affiliations.txt              2.719.436 lines
1 Affiliation ID
2 Affiliation name

Authors.txt                   123.017.489 lines
1 Author ID
2 Author name

PaperAuthorAffiliations.txt   325.498.063 lines
1 Paper ID
2 Author ID
3 Affiliation ID 
4 Original affiliation name
5 Normalized affiliation name
6 Author sequence number

## File prodotti ##
PersoneDEI.txt
353 nomi autori DEI

Il programma ExtractAuthorsID cerca i nomi degli afferenti DEI all'interno di Authors.txt e produce
AutoriDEI.txt
Con le coppie: ID autore  Nome autore DEI

Il programma ExtractPapersDEI cerca gli ID degli autori DEI all'interno di PaperAuthorAffiliations.txt e produce
PaperAutAffDEI.txt            14.360 righe
con la stessa struttura di PaperAuthorAffiliations.txt
è da notare che di questi paper, 8.907 non hanno il campo affiliation compilato

Il file PaperAutAffDEI viene ordinato per Paper ID, in modo da avere in sequenza 
paper1 autore1
paper1 autore2
paper1 autore3
paper2 autore1
paper2 autore2
che il programma CreaArchi elabora in una lista di archi, producendo
EdgeDEI.txt                   2.413 righe nella forma
autore1 autore2
autore1 autore3
autore2 autore3
autore1 autore2


EdgeDEI viene ordinato, ed in seguito elaborato da PesaArchi, producendo
EdgeDEIPesati.txt             488 righe nella forma
autore1 autore2 2
autore1 autore3 1
autore2 autore3 1

Dal file Affiliation cercando Padova|Padua si ottengono 8.285 istituzioni Padovane salvate in
PadovaPadua.txt
1 Affiliation ID
2 Affiliation name

Dal file PaperAutAffDEI EliminaNonPadova estrae solo i paper con affiliation padovana si ottengono 2.875 paper salvati in
PaperDEIPadovani.txt