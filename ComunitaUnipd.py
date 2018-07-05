#!python2

from bs4 import BeautifulSoup
from urllib import urlopen
import os
from os.path import join

def estraiComunitaUnipd(url, pfPersone):
  print(url)
  # htmldoc = unicode(urlopen(url).read(), 'utf-8')
  # htmldoc = urlopen(url).read()
  # with open('listaassegnisti.html', 'rb') as f:
  with open(url, 'rb') as f:
    htmldoc = f.read()
  soup = BeautifulSoup(htmldoc, 'html.parser')
  # print(soup.prettify().encode('raw_unicode_escape'))
  # body_tag = soup.body
  # print(body_tag, type(body_tag))
  # for child in body_tag.children:
    # print(child.name, type(child))

  # for l in soup.find_all('li'):
    # print([n.name for n in l.contents])
    # for link in l.find_all('a'):
      # print(link.get('href'))
    # print(l.contents)
    # print('')

  with open(pfPersone, 'ab' ) as fPersone:
    for tag in soup.find_all('a'):
      spans = tag.find_all('span')
      if len(spans) == 3:
        # cognome = spans[0].string.encode('utf-8').lower()
        # nome = spans[1].string.encode('utf-8').lower()
        cognome = spans[0].string.lower()
        nome = spans[1].string.lower()
        perurl = 'http://www.dei.unipd.it{}'.format(tag.get('href'))
        print('{} {} {}'.format(nome.encode('utf-8'), cognome.encode('utf-8'), perurl))
        # classe = 'prova'
        # fPersone.write('{}\t{}\t{}\r\n'.format(nome, cognome, classe))
        # fPersone.write('{}\t{}\t{}\r\n'.format(nome.encode('utf-8'), cognome.encode('utf-8'), classe))
        perhtml = urlopen(perurl).read()
        persoup = BeautifulSoup(perhtml, 'html.parser')
        ps = persoup.find_all('p')
        for p in ps:
          # print(p.attrs)
          if u'class' in p.attrs and u'dati-anagrafici-classe' in p.attrs[u'class']:
            classe = p.string
            print(classe)
            fPersone.write('{}\t{}\t{}\r\n'.format(nome.encode('utf-8'), cognome.encode('utf-8'), classe))
          # if p.class == 'dati-anagrafici-classe':
            # print(p.string)


if __name__ == '__main__':
  print 'This program is ComunitaUnipd, being run by itself'
  listurl = [
             'http://www.dei.unipd.it/lista-docenti',
             'http://www.dei.unipd.it/lista-assegnisti-ricerca',
             'http://www.dei.unipd.it/lista-collaboratori-ricerca',
             'http://www.dei.unipd.it/lista-dottorandi']
  listurl = [
             'listadocenti.html',
             'listaassegnisti.html',
             'listacollaboratori.html',
             'listadottorandi.html']


  celaborati = 'Versione3_Giu'
  sub = ''
  if not os.path.exists(join(celaborati, sub)): os.makedirs(join(celaborati, sub))
  tag = 'GIU'
  pfPersone = join(celaborati, sub, 'PersoneNomiComunita{}.txt'.format(tag))

  with open(pfPersone, 'wb' ) as fPersone:
    pass

  for url in listurl:
    print('Analizzo {}'.format(url))
    estraiComunitaUnipd(url, pfPersone)
