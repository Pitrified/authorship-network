#!python2

def pnt(nome):
  print('{}\ttipo: {}'.format(nome,  type(eval(nome))  ) )

from bs4 import BeautifulSoup
from urllib import urlopen
import os



def estraiPersoneDaUnipd(pfPersone, url):
  # htmldoc = unicode(urlopen(url).read(), 'utf-8')
  with open('PersoneSPGIhtml.html', 'rb') as f:
    htmldoc = f.read()
  soup = BeautifulSoup(htmldoc, 'html.parser')

  with open(pfPersone, 'wb' ) as fPersone:
    for tag in soup.find_all('a'):
      spans = tag.find_all('span')
      if len(spans) == 3:
        nome = spans[0].string.lower()
        cognome = spans[1].string.lower()
        print 'nome: ', nome, '\tcognome: ', cognome
        fPersone.write('{} {}\r\n'.format(nome, cognome).decode('utf-8'))


if __name__ == '__main__':
  print 'This program is EstraiPersoneDaUnipd, being run by itself'

  url = 'http://www.dsfarm.unipd.it/category/ruoli/personale-docente'
  url = 'https://www.biologia.unipd.it/dipartimento/persone/docenti/'
  url = 'http://www.spgi.unipd.it/category/ruoli/personale-docente'
  # url = 'https://www.dei.unipd.it/lista-docenti'

  celaborati = 'Versione3_Multi\\'
  sub = 'Amplia\\'
  sub = ''
  if not os.path.exists(celaborati + sub): os.makedirs(celaborati + sub)
  tag = 'SPGI'
  pfPersone = celaborati + sub + 'PersoneNomi' + tag + '.txt'

  estraiPersoneDaUnipd(pfPersone, url)
