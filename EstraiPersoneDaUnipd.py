#!python2

def pnt(nome):
  print('{}\ttipo: {}'.format(nome,  type(eval(nome))  ) )

from bs4 import BeautifulSoup
from urllib import urlopen
import os



def estraiPersoneDaUnipd(pfPersone, url):
  htmldoc = urlopen(url).read()
  soup = BeautifulSoup(htmldoc, 'html.parser')

  with open(pfPersone, 'wb' ) as fPersone:
    for tag in soup.find_all('a'):
      spans = tag.find_all('span')
      if len(spans) == 3:
        nome = spans[0].string.lower()
        cognome = spans[1].string.lower()
        print 'nome: ', nome, '\tcognome: ', cognome
        fPersone.write('{} {}\r\n'.format(nome, cognome))
    

if __name__ == '__main__':
  print 'This program is EstraiPersoneDaUnipd, being run by itself' 
  
  url = 'http://www.dsfarm.unipd.it/category/ruoli/personale-docente'
  # url = 'https://www.dei.unipd.it/lista-docenti'
  
  celaborati = 'Versione3_Multi\\'
  sub = 'Amplia\\'
  sub = ''
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  tag = 'CTF'
  pfPersone = celaborati + sub + 'PersoneNomi' + tag + '.txt'
  
  estraiPersoneDaUnipd(pfPersone, url)