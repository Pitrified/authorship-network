# authorship-network

### File originali msr.zip
```
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
```
### File elaborati
In *PersoneDEI.txt* si trovano i 353 nomi autori DEI, scaricati dal [sito del dipartimento](https://www.dei.unipd.it/lista-docenti "Persone | DEI") (Docenti, Assegnisti di ricerca, Collaboratori di ricerca, Dottorandi).

Il programma **ExtractAuthorsID** cerca i nomi degli afferenti DEI all'interno di *Authors.txt* e produce *AutoriDEI.txt*, mantenedo la struttura di *Authors.txt*.

Il programma **ExtractPapersDEI** cerca gli ID degli autori DEI all'interno di *PaperAuthorAffiliations.txt* e produce *PaperAutAffDEI.txt*, 14.360 paper scritti dagli autori del DEI (e da tutti i loro omonimi) con la stessa struttura di *PaperAuthorAffiliations.txt*. Di questi paper, 8.907 non hanno il campo affiliation compilato.

Il file *PaperAutAffDEI.txt* viene ordinato per Paper ID, in modo da avere in sequenza
```
paper1 autore1
paper1 autore2
paper1 autore3
paper2 autore1
paper2 autore2
```
che il programma **CreaArchi** elabora in una lista di archi, producendo *EdgeDEI.txt*, 2.413 archi
```
autore1 autore2
autore1 autore3
autore2 autore3
autore1 autore2
```
*EdgeDEI.txt* viene ordinato, ed in seguito elaborato da **PesaArchi**, producendo *EdgeDEIPesati.txt*, 488 archi
```
autore1 autore2 2
autore1 autore3 1
autore2 autore3 1
```
Filtrando il file *Affiliation.txt* con "Padova|Padua" risultano 8.285 istituzioni Padovane salvate in *PadovaPadua.txt*, che mantiene la struttura di *Affiliation.txt*.

Dal file *PaperAutAffDEI.txt* il programma **EliminaNonPadova** estrae solo i paper con affiliation padovana: risultano 2.875 paper salvati in *PaperPadovani.txt*.

Il programma **EstraiAutoriPadovani** estrae da *AutoriDEI.txt* quelli che hanno un paper in *PaperPadovani.txt*, 248 autori salvati in *AutoriPadovani.txt*