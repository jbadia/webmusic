from BeautifulSoup import BeautifulSoup
import re
import urllib
import random
import Artista
import Pista
import Enregistrament

def getLlistaNomIdentArtista():
    return ["Artist","Artist (Group):","Author (group):","Artist (Group)","Artist (Group)","Composer", "Author (group)"]

def getLlistaNomIdentPista():
    return ["Track Group", "Track:", "Track"]

def getLlistaNomIdentEnregistrament():
    return ["Recording"]

def cercar(busqueda):
    webpage="http://webmusicdb.com/search?"
    htmlparse = r'<(.*?)>'
    htmlparse = r'<td bgcolor="#FFFFFF">(.*?)<a href=\"(.*?)\">(.*?)</a>(.*?)</td>$'
    url = urllib.urlopen(webpage+busqueda)
    sopar = BeautifulSoup(url)
    for tag in sopar("td"):
        reg = None
        tag = str(tag).replace('\n', '').strip()
        if str(tag)[:22] == "<td bgcolor=\"#FFFFFF\">":
            tupla = re.findall(htmlparse, str(tag))
            [tupla] = tupla
            try:
                if str(tupla[0]).strip() in getLlistaNomIdentArtista():
                    yield Artista.Artista(tupla[2],tupla[1])
                if str(tupla[0]).strip() in getLlistaNomIdentEnregistrament():
                    yield Enregistrament.Enregistrament(tupla[2],tupla[1])                   
                if str(tupla[0]).strip().split(':')[0] in getLlistaNomIdentPista():
                    yield Pista.Pista(tupla[2],tupla[1],str(tupla[0]).strip().split(':')[1],tupla[3])
            except IndexError: pass

def crearArtista(atribut, info): # perque printa un maleit None
    if atribut in getLlistaNomIdentArtista() : 
        if str(info).find("href") > 0:
            htmlparse = r'<a href="(.*?)">(.*?)</a>$'
            colPage = [ re.findall(htmlparse, html) for html in info ]
            [[colPage]] = colPage
            reg = Artista.Artista(colPage[1], colPage[0])
            return reg
        try:
            resultat =  extreureHref(info)
            if len(resultat) == 0: #TENIR EN COMPTE EL COI D'ESPAIS BUITS
                return
            reg = Artista.Artista(resultat)
            return reg
        except: pass
    return

def rand():
    return str(random.randint(0,1000))

def extreureHref(cadena):
    try:
        [cadena] = cadena
    except ValueError: pass
    if not cadena:
        return ''
    cadena = str(cadena).replace('</a>','')
    htmlparse = r'(.*?)<a href="(.*?)">(.*?)$'
    try:
        [resultat] = re.findall(htmlparse, str(cadena))
    except ValueError: return cadena
    nouCamp = resultat[0] + extreureHref(resultat[2])
    return nouCamp
