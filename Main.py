#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 23/01/2010

@author: jordi
'''

import cmd
import string
import sys
import llibreria


class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.dicObj = {}
        self.prompt = '> '
    
    def do_cercar(self, arg):
        '''Per a poder cercar un terme s'ha de fer de la següent manera:
                cercar nom_artista'''
        for item in llibreria.cercar(arg):
            self.dicObj[item._id] = item
            self.dicObj[item._id].infoLine()
    
    def do_mostrar(self,arg):
        '''Per a poder mostrar la informació d'un article, disc, pista s'ha de fer de la següent manera:
                mostrar id
            ex:
            A     20936 Artist (Group): The Rolling Stones
            > mostrar 20936
                '''
        try:
            for id,element in ( (element._id,element) for element in self.dicObj[arg].info() ):
                self.dicObj[id]=element
        except KeyError:
            print "component no cercat"

    def do_quit(self, arg):
        '''q o quit per a poder sortir'''
        sys.exit(1)

    # shortcuts
    do_q = do_quit

#
# try it out

cli = CLI()
cli.cmdloop()

