#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 20/01/2010

@author: jordi
'''

import Enregistrament

import re
import llibreria
import urllib
from BeautifulSoup import BeautifulSoup

class Artista(object):

    def __init__(self,nom='',url=''):
        try:
            self._id = str(url).split('?')[1]
        except: self._id ="?" + llibreria.rand()
        self.nom = nom
        self.url = "http://www.webmusicdb.com" + url
        self.artistes = None    #no es fa anar
        self.enregistaments = None  # no es fa anar
        self._html = None
    
    def infoLine(self):
        '''Mètode que ens mostra part de la informació de l'objecte sense accedir a la pàgina'''
        print "A    ", self._id, self.nom
    
    def getcodihtml(self):
        '''funció que obté el codi html i l'emmagatzema, per a produir la descarrega una vegada'''
        if self._html:
            return self._html
        else:
            obj = BeautifulSoup(urllib.urlopen(self.url))
            self._html = str(obj)
            return self._html
    
    def iterTagPagina(self):
        '''iterador dels atributs de la pàgina'''
        soupTotaPagina = BeautifulSoup(self.getcodihtml())
        
        generador = ( (seccio,codiSeccio) for (seccio,codiSeccio) in enumerate(soupTotaPagina("p")) if seccio is not 0 )
        
        for clau,codi in generador:
            
            soupSeccio = BeautifulSoup(str(codi))
            
            htmlparse = r'<td class="banner" bgcolor="#336699">(.*?)</td>$'
            atribut = [ re.findall(htmlparse,str(line).replace("\n", '')) for posicio,line in enumerate(soupSeccio("td")) if str(line).find("banner") > 0 and posicio == 1]
            [[atribut]] = atribut
            
            yield atribut
    
    def info(self, diccionari=None):
        '''Mètode que ens permet obtenir la informació d'una pàgina HTML del tipus d'Artista'''
        soupTotaPagina = BeautifulSoup(self.getcodihtml())
        
        # obtenim les seccions per p de la pàgina web i descartem la primera, no interessa
        generador = ( (seccio,codiSeccio) for (seccio,codiSeccio) in enumerate(soupTotaPagina("p")) if seccio is not 0 )
        
        # objectes que es crearan i volem mantenir en cache
        newObjects=[]
        
        for clau,codi in generador: # parsegem les seccions que ens interessen
            
            soupSeccio = BeautifulSoup(str(codi))
            
            # busquem el titol de l'atibuts, estan en un td amb bgcolor="#336699"
            htmlparse = r'<td class="banner" bgcolor="#336699">(.*?)</td>$'
            atribut = [ re.findall(htmlparse,str(line).replace("\n", '')) for posicio,line in enumerate(soupSeccio("td")) if str(line).find("banner") > 0 and posicio == 1]
            [[atribut]] = atribut
            
            print atribut
            
            # optenim la llista d'informació que conté l'atribut
            htmlparse = r'<td bgcolor="#FFFFFF">(.*?)</td>$'
            #llista = [ re.findall(htmlparse, str(element).replace("\n", '')) for posicio,element in enumerate(soupSeccio("td")) if posicio > 3 and posicio != 0]
            llista = [ re.findall(htmlparse, str(element).replace("\n", '')) for posicio,element in enumerate(soupSeccio("td")) if posicio > 3]
            
            # parsegem cada un dels td's del atribut segons el tipus d'atribut
            #llista = llista[1:] # descartem el primer
            htmlparse = r'<a href="(.*?)">(.*?)</a>$'
            for info in llista:
                # artista
                if atribut in llibreria.getLlistaNomIdentArtista():
                    # artistes amb url
                    if str(info).find("href") > 0:
                        colPage = [ re.findall(htmlparse, html) for html in info ]
                        [[colPage]] = colPage
                        art = Artista(colPage[1], colPage[0])
                        newObjects.append(art)
                        art.infoLine()
                    # artistes sense url
                    else:
                        try:
                            [info] = info
                            art = Artista(info)
                            art.infoLine()
                        except: pass
                # enregistraments
                elif atribut in llibreria.getLlistaNomIdentEnregistrament():
                    # enregistraments amb url
                    if str(info).find("href") > 0:
                        colPage = [ re.findall(htmlparse, html) for html in info ]
                        try:
                            [[colPage]] = colPage
                            art = Enregistrament.Enregistrament(colPage[1], colPage[0])
                            newObjects.append(art)
                            art.infoLine()
                        except: pass
                    # enregistaments sense url
                    else:
                        try:
                            [info] = info
                            art = Enregistrament.Enregistrament(info)
                            art.infoLine()
                        except: pass
                # altres tipus d'atributs
                else:
                    print "    ", llibreria.extreureHref(info)
        
        return newObjects           
    
    def getListOfAtributes(self):
        '''Obtenció dels atributs declarats en la classe'''
        return self.__dict__.keys()
    
    def pairValues(self):
        '''Obtenció d'un iterador amb els atributs i valor d'aquests de la classe'''
        return self.__dict__.itervalues()
    
if __name__ == '__main__':
    obj = Artista("Artist (Group): The Rolling Stones","/disp?20936")
    #obj = Artista("Artist (Group): The Beatles","/disp?74")
    obj.infoLine()
    print
    obj.info()
    

    