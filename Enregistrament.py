#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 20/01/2010

@author: jordi
'''

import Artista
import Pista

import llibreria
import re
import urllib
from BeautifulSoup import BeautifulSoup

class Enregistrament(object):

    def __init__(self,nom,url=''):
        try:
            self._id = str(url).split('?')[1]
        except: self._id ="?" + llibreria.rand()
        self.nom = nom
        self.url = "http://www.webmusicdb.com" + url
        self.pistes = None
        self.artistes = None
        self._html = None
    
    def infoLine(self):
        print "R    ", self._id, self.nom
    
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
            #llista = [ re.findall(htmlparse, str(element).replace("\n", '')) for posicio,element in enumerate(soupSeccio("td")) if posicio > 3 and posicio != 0]
            
            llista = [ re.findall(htmlparse, str(element).replace("\n", '')) for posicio,element in enumerate(soupSeccio("td")) if posicio > 3]
            
            #llista = llista[1:]
            for info in llista:
                if atribut in llibreria.getLlistaNomIdentArtista() :
                    if str(info).find("href") > 0:
                        htmlparse = r'<a href="(.*?)">(.*?)</a>$'
                        colPage = [ re.findall(htmlparse, html) for html in info ]
                        try:
                            [[colPage]] = colPage
                            reg = Artista.Artista(colPage[1], colPage[0])
                            newObjects.append(reg)
                            reg.infoLine()
                        except: pass
                    else:
                        try:
                            [info] = info
                            reg = Artista.Artista(info)
                            reg.infoLine()
                        except: pass
                elif atribut in llibreria.getLlistaNomIdentPista():
                    if str(info).find("href") > 0:
                        htmlparse = r'^(.*?)<a href="(.*?)">(.*?)</a>(.*?)$'
                        colPage = [ re.findall(htmlparse,str(html).split('by')[0]) for html in info ]
                        try:
                            [[colPage]] = colPage
                            reg = Pista.Pista(colPage[2], colPage[1], colPage[0], colPage[3])
                            newObjects.append(reg)
                            reg.infoLine()
                        except: pass
                    else:
                        try:
                            [info] = info
                            reg = Pista.Pista(info)
                            reg.infoLine()
                        except: pass
                else:
                    print "    ", llibreria.extreureHref(info)
        return newObjects         
    
if __name__ == '__main__':
    obj = Enregistrament("Revolver","/disp?88731")
    #obj = Enregistrament("Artist (Group): The Beatles","/disp?74")
    obj.infoLine()
    print
    obj.info()

    