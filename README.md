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
### File - Programmi
Formattazione: *FileElaborato.txt* - **Programma.java**

*PersoneDEI.txt*: 353 nomi di afferenti (autori) DEI, scaricati dal [sito del dipartimento](https://www.dei.unipd.it/lista-docenti "Persone | DEI") (Docenti, Assegnisti di ricerca, Collaboratori di ricerca, Dottorandi)

**ExtractAuthorsID.java**: cerca i nomi degli afferenti DEI (*PersoneDEI.txt*) all'interno di *Authors.txt* e produce *AutoriDEI.txt*

**ExtractPapersDEI.java**: cerca gli ID degli autori DEI (*AutoriDEI.txt*) all'interno di *PaperAuthorAffiliations.txt* e produce *PaperAutAffDEI.txt*, 14.360 paper scritti dagli autori del DEI (e da tutti i loro omonimi). Di questi paper, 8.907 non hanno il campo affiliation compilato.

*PaperAutAffDEI.txt* viene ordinato per Paper ID, in modo da avere in sequenza
```
paper1 autore1
paper1 autore2
paper1 autore3
paper2 autore1
paper2 autore2
```
**CreaArchi.java**: elabora una lista di archi, producendo *EdgeDEI.txt* (2.413 archi) nel formato
```
autore1 autore2
autore1 autore3
autore2 autore3
autore1 autore2
```
(escludendo i paper scritti da un singolo autore);

*EdgeDEI.txt* viene ordinato, ed in seguito elaborato da **PesaArchi.java**, producendo *EdgeDEIPesati.txt* (488 archi) nel formato
```
autore1 autore2 2
autore1 autore3 1
autore2 autore3 1
```

Una lista di autori si può estrarre senza considerare le affiliazioni ma cercando tra gli autori quelli che hanno collaborato almeno una volta (ipotizzando sia improbabile che un omonimo autore abbia lavorato con un afferente DEI):

**EstraiAutoriCollab.java** estrae da *AutoriDEI.txt* (che sono 2135) gli autori che compaiono almeno una volta in *EdgeDEIPesati.txt*, salvati in *AutoriCollab.txt* (che sono 247). Circa il 75% degli autori compare nella componente centrale salvata in *EDAT_GiantComp.pdf*

---

Un altro modo per estrarre una lista di autori è tramite le Affiliation:

Filtrando il file *Affiliation.txt* con "Padova|Padua" risultano 8.285 istituzioni Padovane, copiate in *PadovaPadua.txt*

**EliminaNonPadova.java**: cerca gli ID delle affiliation padovane (*PadovaPadua.txt*) all'interno di *PaperAutAffDEI.txt*: risultano 2.875 paper, copiati in *PaperPadovani.txt*.

**EstraiAutoriPadovani.java** estrae da *AutoriDEI.txt* quelli che hanno un paper in *PaperPadovani.txt*: 248 autori salvati in *AutoriPadovani.txt* (prova a rimuovere gli omonimi, che probabilmente non avranno pubblicazioni a Padova, tenendo gli autori con almeno un paper con affiliazione padovana)

**EstraiAutoriPadovaniCompleti.java** estrae da *PaperAutAffDEI.txt* i paper scritti da *AutoriPadovani.txt*, copiati in *PaperPadovaniCompleti.txt*, a cui si applicano **CreaArchi** e **PesaArchi** per generare *EdgePadovaniCompletiPesati.txt*. Il grafo formato da questi archi, caricato in Gephi e manipolato risulta nella componente centrale visualizzabile in *EPCP_GiantComp.pdf*
