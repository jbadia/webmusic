#! /usr/bin/env python2.5
# -*- coding: utf-8 -*-

import Artista
import Enregistrament

import llibreria
import re
import urllib
from BeautifulSoup import BeautifulSoup

class Pista(object):

    def __init__(self,nom,url='',numero='',durada=''):
        try:
            self._id = str(url).split('?')[1]
        except: self._id ="?" + llibreria.rand()
        self.nom = nom
        self.url = "http://www.webmusicdb.com" + url
        self.numero = numero
        self.durada = durada
        self.artistes = None # no es fa anar
        self.enregistraments = None # no es fa anar
        self._html = None
        
    
    def infoLine(self):
        print "T    ", self._id, self.nom
    
    def getcodihtml(self):
        if self._html:
            return self._html
        else:
            obj = BeautifulSoup(urllib.urlopen(self.url))
            self._html = str(obj)
            return self._html
    
    def info(self, diccionari=None):
        soupTotaPagina = BeautifulSoup(self.getcodihtml())
        
        generador = ( (seccio,codiSeccio) for (seccio,codiSeccio) in enumerate(soupTotaPagina("p")) if seccio is not 0 )
        
        newObjects=[]
        
        for clau,codi in generador:
            
            soupSeccio = BeautifulSoup(str(codi))
            
            htmlparse = r'<td class="banner" bgcolor="#336699">(.*?)</td>$'
            atribut = [ re.findall(htmlparse,str(line).replace("\n", '')) for posicio,line in enumerate(soupSeccio("td")) if str(line).find("banner") > 0 and posicio == 1]
            [[atribut]] = atribut
            
            print atribut
            
            htmlparse = r'<td bgcolor="#FFFFFF">(.*?)</td>$'
            
            llista = [ re.findall(htmlparse, str(element).replace("\n", '')) for posicio,element in enumerate(soupSeccio("td")) if posicio > 3]
            
            htmlparse = r'<a href="(.*?)">(.*?)</a>$'
            for info in llista:
                if atribut in llibreria.getLlistaNomIdentArtista():
                    if str(info).find("href") > 0:
                        colPage = [ re.findall(htmlparse, html) for html in info ]
                        [[colPage]] = colPage
                        art = Artista.Artista(colPage[1], colPage[0])
                        newObjects.append(art)
                        art.infoLine()
                    else:
                        try:
                            [info] = info
                            art = Artista.Artista(info)
                            art.infoLine()
                        except: pass
                elif atribut in llibreria.getLlistaNomIdentEnregistrament():
                    if str(info).find("href") > 0:
                        colPage = [ re.findall(htmlparse, html) for html in info ]
                        try:
                            [[colPage]] = colPage
                            art = Enregistrament.Enregistrament(colPage[1], colPage[0])
                            newObjects.append(art)
                            art.infoLine()
                        except: pass
                    else:
                        try:
                            [info] = info
                            art = Enregistrament.Enregistrament(info)
                            art.infoLine()
                        except: pass
                else:
                    print "    ", llibreria.extreureHref(info)
        return newObjects    

if __name__ == '__main__':
    obj = Pista("Out of Control","/disp?47806","3."," (07:19)")
    obj.infoLine()
    print
    obj.info()

    
