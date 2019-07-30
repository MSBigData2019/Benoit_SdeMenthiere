#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote
import ssl
from collections import OrderedDict

cache = {}

def getJSON(page):
    params = urlencode({
      'format': 'json',
      'action': 'parse',
      'prop': 'text',
      'redirects': 'true',
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"  # TODO: changer ceci
    # désactivation de la vérification SSL pour contourner un problème sur le
    # serveur d'évaluation -- ne pas modifier
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']
        content = parsed['parse']['text']['*']
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getPage(page):
    #try:
    if page in cache.keys():
        return cache[page]
    else:
        print(page)
        title, content = getRawPage(page)
        soup = BeautifulSoup(content, 'html.parser')
        paragraphs = [x.find_all('p') for x in soup.find_all('div',recursive=False)]
        paragraphs = [item for sublist in paragraphs for item in sublist]
        links = [paragraph.find_all('a', href=True, title=True) for paragraph in paragraphs]
        links = [item for sublist in links for item in sublist]
        links = [a['href'] for a in links]
        links = [link for link in links if link.startswith('/wiki/') and 'redlink=1' not in link and ':' not in link]
        links =  list(OrderedDict.fromkeys(links))
        links = [unquote(link[6:]) for link in links]
        def retirer_frag(link):
            try:
                idx = link.index('#')
                return link[:idx].replace('_',' ')
            except:
                return link.replace('_',' ')
        links = list(map(retirer_frag, links))
        cache[page] = title, links[:10]
        return title, links[:10]
    #except TypeError:
            # La page demandée n'existe pas
    #    return [], None

if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    print("Ça fonctionne !")

    # Voici des idées pour tester vos fonctions :
    # print(getJSON("Utilisateur:A3nm/INF344"))
    print(getPage("Utilisateur:A3nm/INF344"))
    print(getPage("Geoffrey Miller"))
