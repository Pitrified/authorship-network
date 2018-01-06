#! python2

import re

def ptype(obj):
  print obj, " - ", type(obj)

def processaNodi(nome, est=".txt"):
  fullname = dir+"\\"+nome+est
  finput = open(fullname, "r")
  strInput = finput.read()
  finput.close()

  fullnameout = dir+"\\"+nome+".tsv"
  foutput = open(fullnameout, "w")
  foutput.write("id\tLabel\n")          #aggiunge la riga iniziale
  foutput.write(strInput)
  foutput.close()
  
def processaEdge(nome, est=".txt"):
  fullname = dir+"\\"+nome+est
  finput = open(fullname, "r")
  strInput = finput.read()
  finput.close()

  strOutput = strInput.replace("\n","\tUndirected\n")     #gli edge sono Undirected
  #strOutput = re.sub("\n","\tUndirected\n", strInput)

  fullnameout = dir+"\\"+nome+".tsv"
  foutput = open(fullnameout, "w")
  foutput.write("Source\tTarget\tWeight\tType\n")         #aggiunge la riga iniziale
  foutput.write(strOutput)
  foutput.close()


dir = r'C:\Users\Test\Documents\Tesi\authorship-network\Versione2'    #cartella in cui lavora

processaNodi("AutoriPadovaniAmpiUnificatiBis")
processaNodi("AutoriCollabAmpiUnificatiBis")
#processaNodi("AutoriPadovaniAmpi")
#processaNodi("AutoriCollabAmpi")

processaEdge("EdgePadovaniCompletiPesatiAmpiUnificatiBis")
processaEdge("EdgeCollabPesatiAmpiUnificatiBis")

