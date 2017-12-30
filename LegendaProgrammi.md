# PROGRAMMI

I programmi agiscono all'interno della cartella "\Versione00"

||ExtractAuthorsID.java|
|-|-|
|Input|PersoneDei.txt|
|Database|Authors.txt|
|Output|AutoriDEI.txt|
|Descrizione|cerco i nomi delle PersoneDEI in Authors|
|Commento|ci sono IDaut associati ad omonimi che non sono persone DEI<br/> ci sono IDaut multipli relativi alla stessa persona (nome) DEI|

||ExtractPapersDEI.java|
|-|-|
|Input|AutoriDEI.txt|
|Database|PaperAuthorAffiliations.txt|
|Output|PaperAutAffDEI.txt|
|Descrizione|cerco gli IDaut degli AutoriDEI in PaperAuthorAffiliations|
|Commento|ok|

||EliminaNonPadova.java|
|-|-|
|Input|PadovaPadua.txt|
|Database|PaperAutAffDEI.txt<br/> PapAutAffDEIampi.txt|
|Output|PaperPadovani.txt<br/> PaperPadovaniAmpi.txt|
|Descrizione|filtro il database con gli IDaff padovane in PadovaPadua|
|Commento|molti paper hanno il campo affiliation non compilato, non possono essere identificati in questo modo|

||CreaArchi.java|
|-|-|
|Input|PaperAutAffDEIOrdinatiPAPER<br/> PaperPadovani.txt<br/> PaperPadovaniCompleti.txt|
|Database|-|
|Output|EdgeDEI.txt<br/> EdgePadovani.txt<br/> EdgePadovaniCompleti.txt|
|Descrizione|crea gli edge IDaut1-IDaut2 |
|Commento|ok|
    
||PesaArchi.java|
|-|-|
|Input|EdgeDEI.txt<br/> EdgePadovani.txt<br/> EdgePadovaniCompleti.txt|
|Database|-|
|Output|EdgeDEIPesati1.txt<br/> EdgePadovaniPesati.txt<br/> EdgePadovaniCompletiPesati.txt|
|Descrizione|pesa gli edge IDaut1-IDaut2-peso|
|Commento|ok|

||EstraiAutoriCollab.java|
|-|-|
|Input|EdgeDEIPesati.txt<br/> EdgeCollabPesatiAmpi.txt|
|Database|AutoriDEI.txt<br/> AutoriDEIampi.txt|
|Output|AutoriCollab.txt<br/> AutoriCollabAmpi.txt|
|Descrizione|filtro il database con gli IDaut che compaiono negli edge|
|Commento|considero padovani gli autori che hanno collaborato almeno una volta con un AutoriDEI|

||EstraiAutoriPadovani.java|
|-|-|
|Input|PaperPadovani.txt<br/> PaperPadovaniAmpi.txt|
|Database|AutoriDEI.txt<br/> AutoriDEIampi.txt|
|Output|AutoriPadovani.txt<br/> AutoriPadovaniAmpi.txt|
|Descrizione|filtro il database con gli IDaut che hanno scritto i PaperPadovani|
|Commento|considero padovani gli autori che hanno almeno un paper con affiliation padovana|

||EstraiAutoriPadovaniCompleti.java|
|-|-|
|Input|AutoriPadovani.txt<br/> AutoriPadovaniAmpi.txt|
|Database|PaperAutAffDEI.txt<br/> PapAutAffDEIampi.txt|
|Output|PaperPadovaniCompleti.txt<br/> PaperPadovaniCompletiAmpi.txt|
|Descrizione|cerco gli IDaut degli AutoriPadovani in PaperAutAffDEI|
|Commento|in paper padovani completi sono inclusi paper con affiliation non compilata<br/> il nome del programma non riflette lo scopo|

||CollassaNodi.py|
|-|-|
|Input|AutoriCollabOrdinatiNOMEpoiIDridotto.txt<br/> AutoriPadovaniOrdinatiNOMEpoiID.txt|
|Database|EdgeDEIPesati.txt<br/> EdgePadovaniCompletiPesati.txt|
|Output|EdgeDEIPesatiUnificati.txt<br/> EdgePadovaniCompletiPesatiUnificati.txt|
|Descrizione|IDaut multipli relativi allo stesso nome vengono collassati in un unico IDaut (il primo in ordine)|
|Commento|il nome potrebbe essere riferito a persone diverse<br/>|

||EstraiIDAutoriDEIampi.py|
|-|-|
|Input|PersoneDEI.txt|
|Database|Authors.txt|
|Output|AutoriDEIampi.txt|
|Descrizione|cerco i nomi delle PersoneDEI in Authors con anche tutte le possibili iniziali|
|Commento|ci sono IDaut associati ad omonimi che non sono persone DEI<br/> ci sono IDaut multipli relativi alla stessa persona (nome) DEI<br/> considerando le iniziali il numero di omonimi in sale vistosamente (8379 contro 2135) (il falso positivo prima era solo mario rossi, ora sono tutti gli m rossi, dove m corrisponde a mario ma anche michele, mirko, massimiliana, marina...) (da PersoneDEI ad AutoriDEI x6<br/> da PersoneDEIampie a AutoriDEIampi x11)|

||EstraiPapAutAffDEI.py|
|-|-|
|Input|AutoriDEIampi.txt|
|Database|PaperAuthorAffiliations.txt|
|Output|PapAutAffDEIampi.txt|
|Descrizione|cerco gli IDaut degli AutoriDEIampi in PaperAuthorAffiliations|
|Commento|ok|

||EstraiTitoliPaper.py|
|-|-|
|Input|PapAutAffDEIampi.txt|
|Database|Papers.txt|
|Output|PapersDEITitoliAmpi.txt|
|Descrizione|estraggo i titoli dei paper dei PapAutAffDEIampi|
|Commento|ok|

||CreaEdgeCollab.py|
|-|-|
|Input|PapAutAffDEIampi.txt|
|Database|-|
|Output|EdgeCollabPesatiAmpi.txt|
|Descrizione|crea gli edge pesati IDaut1-IDaut2-peso|
|Commento|ok|

||CollassaNodiAmpi.py|
|-|-|
|Input|EdgeCollabPesatiAmpi.txt<br/> EdgePadovaniCompletiPesatiAmpi.txt|
|Database|PersoneDEI.txt<br/> AutoriCollabAmpiOrdinatiNOMEpoiID.txt<br/> AutoriPadovaniAmpiOrdinatiNOMEpoiID.txt|
|Output|EdgeCollabPesatiAmpiUnificatiBis.txt<br/> EdgePadovaniCompletiPesatiAmpiUnificatiBis.txt|
|Descrizione|collassa i nodi risalendo anche da abbreviazione a nome completo|
|Commento|ok con Bis|

