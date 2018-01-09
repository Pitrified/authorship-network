#!python2



def estraiPaperPadovaniCompleti(pfPapAutAff, pfAffPad, pfAutoriID, pfPapPad, pfAutPad):
  """
  #estrai paperpadovani per affiliazione se in PadovaPadua
    #(da PapAutAffDEI, devono comunque essere IDaut nella lista)
    #in eliminanonpadova.java
  #estrai autoripadovani
  #estrai paperpadovanicompleti
    #(da PapAutAffDEI prendo i paper scritti da IDaut con almeno un aff padovana)
  """

  # IDaff affiliation padovane
  sAffPad = set()
  with open(pfAffPad, 'rb') as fAffPad:
    for line in fAffPad:
      sAffPad.add(line.split('\t')[0])  #carico IDaff

  sAutPad = set()
  with open(pfPapAutAff, 'rb') as fPapAutAff, open(pfPapPad, 'wb') as fPapPad:
    # IDaut che hanno almeno un paper con affiliation padovana
    for line in fPapAutAff:
      pezzi = line.rstrip().split('\t') #
      if len(pezzi)>=2:           #campo IDaff compilato
        if pezzi[2] in sAffPad:   #paper con aff padovana
          sAutPad.add(pezzi[1])   #carico l'IDaut
    
    # estraggo i paper scritti da autori padovani
    fPapAutAff.seek(0)
    for line in fPapAutAff:
      pezzi = line.rstrip().split('\t')
      if pezzi[1] in sAutPad:     #paper scritto da autore con almeno un aff pad
        fPapPad.write(line)
  
  # autori padovani
  with open(pfAutoriID, 'rb') as fAutoriID, open(pfAutPad, 'wb') as fAutPad:
    for line in fAutoriID:
      if line.split('\t')[0] in sAutPad:
        fAutPad.write(line)
  


if __name__ == '__main__':
  print('This program is EstraiPaperPadovaniCompleti, being run by itself')
  #PATH TO FILES
  celaborati = 'Versione3_Single\\'
  pfPapAutAff = celaborati + 'PapAutAffDEIMacroFull.txt'
  pfAffPad = 'PadovaPadua.txt'
  pfAutoriID = celaborati + 'AutoriDEIMacroFull.txt'
  pfPapPad = celaborati + 'PaperPadovaniCompletiSingolo.txt'
  pfAutPad = celaborati + 'AutoriPadovaniSingolo.txt'
  estraiPaperPadovaniCompleti(pfPapAutAff, pfAffPad, pfAutoriID, pfPapPad, pfAutPad)
  print('finito EPPC solo'.format() )
  
else:
  print 'I am EstraiPaperPadovaniCompleti, being imported from another module'
