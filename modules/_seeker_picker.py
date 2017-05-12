#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Clase para la búsqueda de los patrones
    en los enlaces de Pastebin, este es llamado
    por el usuario al añadir patrones de búsqueda 
    o expresiones regulares.

    Lo que devolverá será un diccionario para cada
    uno de los patrones de búsqueda, con el valor
    que aparezca y el enlace al pastebin que aparezca
'''

logo = '''
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XX                                                                          XX
XX   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMMssssssssssssssssssssssssssMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMss'''                          '''ssMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMyy''                                    ''yyMMMMMMMMMMMM   XX
XX   MMMMMMMMyy''                                            ''yyMMMMMMMM   XX
XX   MMMMMy''                                                    ''yMMMMM   XX
XX   MMMy'                                                          'yMMM   XX
XX   Mh'                                                              'hM   XX
XX   -                                                                  -   XX
XX                                                                          XX
XX   ::                                                                ::   XX
XX   MMhh.        ..hhhhhh..                      ..hhhhhh..        .hhMM   XX
XX   MMMMMh   ..hhMMMMMMMMMMhh.                .hhMMMMMMMMMMhh..   hMMMMM   XX
XX   ---MMM .hMMMMdd:::dMMMMMMMhh..        ..hhMMMMMMMd:::ddMMMMh. MMM---   XX
XX   MMMMMM MMmm''      'mmMMMMMMMMyy.  .yyMMMMMMMMmm'      ''mmMM MMMMMM   XX
XX   ---mMM ''             'mmMMMMMMMM  MMMMMMMMmm'             '' MMm---   XX
XX   yyyym'    .              'mMMMMm'  'mMMMMm'              .    'myyyy   XX
XX   mm''    .y'     ..yyyyy..  ''''      ''''  ..yyyyy..     'y.    ''mm   XX
XX           MN    .sMMMMMMMMMss.   .    .   .ssMMMMMMMMMs.    NM           XX
XX           N`    MMMMMMMMMMMMMN   M    M   NMMMMMMMMMMMMM    `N           XX
XX            +  .sMNNNNNMMMMMN+   `N    N`   +NMMMMMNNNNNMs.  +            XX
XX              o+++     ++++Mo    M      M    oM++++     +++o              XX
XX                                oo      oo                                XX
XX           oM                 oo          oo                 Mo           XX
XX         oMMo                M              M                oMMo         XX
XX       +MMMM                 s              s                 MMMM+       XX
XX      +MMMMM+            +++NNNN+        +NNNN+++            +MMMMM+      XX
XX     +MMMMMMM+       ++NNMMMMMMMMN+    +NMMMMMMMMNN++       +MMMMMMM+     XX
XX     MMMMMMMMMNN+++NNMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMNN+++NNMMMMMMMMM     XX
XX     yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy     XX
XX   m  yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy  m   XX
XX   MMm yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy mMM   XX
XX   MMMm .yyMMMMMMMMMMMMMMMM     MMMMMMMMMM     MMMMMMMMMMMMMMMMyy. mMMM   XX
XX   MMMMd   ''''hhhhh       odddo          obbbo        hhhh''''   dMMMM   XX
XX   MMMMMd             'hMMMMMMMMMMddddddMMMMMMMMMMh'             dMMMMM   XX
XX   MMMMMMd              'hMMMMMMMMMMMMMMMMMMMMMMh'              dMMMMMM   XX
XX   MMMMMMM-               ''ddMMMMMMMMMMMMMMdd''               -MMMMMMM   XX
XX   MMMMMMMM                   '::dddddddd::'                   MMMMMMMM   XX
XX   MMMMMMMM-                                                  -MMMMMMMM   XX
XX   MMMMMMMMM                                                  MMMMMMMMM   XX
XX   MMMMMMMMMy                                                yMMMMMMMMM   XX
XX   MMMMMMMMMMy.                                            .yMMMMMMMMMM   XX
XX   MMMMMMMMMMMMy.                                        .yMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMy.                                    .yMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMs.                                .sMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMss.           ....           .ssMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMNo         oNNNNo         oNMMMMMMMMMMMMMMMMMMMM   XX
XX                                                                          XX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    .o88o.                               o8o                .
    888 `"                               `"'              .o8
   o888oo   .oooo.o  .ooooo.   .ooooo.  oooo   .ooooo.  .o888oo oooo    ooo
    888    d88(  "8 d88' `88b d88' `"Y8 `888  d88' `88b   888    `88.  .8'
    888    `"Y88b.  888   888 888        888  888ooo888   888     `88..8'
    888    o.  )88b 888   888 888   .o8  888  888    .o   888 .    `888'
   o888o   8""888P' `Y8bod8P' `Y8bod8P' o888o `Y8bod8P'   "888"      d8'
                                                                     .o...P'


Pastebin crawler to get some URLs from mainpage, we can't take too much, 
but maybe it's something

@author: Fare9
@mail: farenain9(at)gmail(dot)com


Ascii art from: https://github.com/syntax-samurai/fsociety
'''


import sys
import os

import requests
import notify2
import time
import re
from threading import Thread


class Seeker_Picker():

    def __init__(self,verbosity,pastebin_urls,regExs,emails,names,dnis,cadenas,use_tor):
        self.verbosity = verbosity
        self.pastebin_urls = pastebin_urls
        self.regExs = regExs
        self.emails = emails
        self.names = names
        self.dnis = dnis
        self.cadenas = cadenas
        self.use_tor = use_tor
        notify2.init("OSINTretasNoHayPastebines")
        self.retorned_dict = {}

    def run(self):
        ''' Método principal '''
        print logo

        self.print_verbosity("[+] Starting module to check for your queries",1)

        self.seek_and_pick()

        self.print_verbosity("[+] Finished module, returning dictionary",1)

        self.print_notification("Seeker_picker","Finished module")

    def print_verbosity(self,message,verbosity_required):
        '''
            Mostramos según verbosidad (importancia)
            del mensaje
        '''
        if self.verbosity >= verbosity_required:
            print message

    def seek_and_pick(self):
        ''' FUNCIÓN PARA BUSCAR DENTRO DE CADA ENLACE DE PASTEBIN USO SIN TOR '''

        for url in self.pastebin_urls:

            self.print_verbosity("[+] Requesting for pastebin url: "+url,3)
            if 'raw' not in url: # obtenemos la URL raw ya que así será más sencillo
                urlRaw = 'https://' + url.split('/')[0] + "/raw/" + url.split('/')[1]

            self.print_verbosity("[+] Requesting for pastebin raw url: "+urlRaw,3)

            try:
                if use_tor:
                    with TorRequest() as tr:
                        response = tr.get(urlRaw)
                else:
                    response = requests.get(urlRaw)
            except Exception as e:
                self.print_verbosity("[-] Failed to get url: "+str(url),2)
                continue

            code_page = str(response.text)

            if response.status_code == 200: # si la vuelta es 200 perfecto

                self.print_verbosity("[+] URL: "+url+" get 200 code",2)

                # buscamos expresiones regulares
                self.retorned_dict['regExs'] = {}
                for regEx in self.regExs:
                    pattern = re.compile(regEx)

                    retorno = pattern.match(code_page)

                    if retorno is not None:
                        try:
                            if type(self.retorned_dict['regExs'][regEx]) == 'list': 
                                #si no es una lista o no es nada saltará error, y lo crearemos como una lista
                                self.retorned_dict['regExs'][regEx].append(url)
                        except:
                            # esto saltará con la primera URL
                            self.retorned_dict['regExs'][regEx] = []
                            self.retorned_dict['regExs'][regEx].append(url)
                # Fin de las expresiones regulares

                # buscamos emails
                self.retorned_dict['emails'] = {}
                for email in self.emails:
                    if email in code_page:
                        try:
                            if type(self.retorned_dict['emails'][email]) == 'list':
                                self.retorned_dict['emails'][email].append(url)
                        except:
                            self.retorned_dict['emails'][email] = []
                            self.retorned_dict['emails'][email].append(url)
                # Fin de los emails
                # buscamos nombres
                self.retorned_dict['names'] = {}
                for name in self.names:
                    if name in code_page:
                        try:
                            if type(self.retorned_dict['names'][name]) == 'list':
                                self.retorned_dict['names'][name].append(url)
                        except:
                            self.retorned_dict['names'][name] = []
                            self.retorned_dict['names'][name].append(url)
                # Fin de nombres
                # DNIs
                self.retorned_dict['DNIs'] = {}
                for dni in self.dnis:
                    if dni in code_page:
                        try:
                            if type(self.retorned_dict['DNIs'][dni]) == 'list':
                                self.retorned_dict['DNIs'][dni].append(url)
                        except:
                            self.retorned_dict['DNIs'][dni] = []
                            self.retorned_dict['DNIs'][dni].append(url)
                # Fin DNIs
                # Cadenas
                self.retorned_dict['strings'] = {}
                for cadena in cadenas:
                    if cadena in code_page:
                        try:
                            if type(self.retorned_dict['strings'][cadena]) == 'list':
                                self.retorned_dict['strings'][cadena].append(url)
                        except:
                            self.retorned_dict['strings'][cadena] = []
                            self.retorned_dict['strings'][cadena].append(url)
                # Fin Cadenas
            else:
                self.print_verbosity("[-] ERROR URL: "+url+" get "+str(response.status_code)+" code",0)

    def print_notification(self,title,message):
        '''
            Para mostrar mensajes de notificaciones
        '''
        if self.verbosity >= 0:
            argumento = [title,message]
            thread = Thread(target = show_notification, args = [argumento])
            thread.start()

def show_notification(args):
    '''
        Para ejecutar en un hilo a parte
    '''
    title = args[0]
    message = args[1]
    n = notify2.Notification(title,
                     message,
                     "Pastebin"   # Icon name
                    )
    n.show()
    time.sleep(3)
    n.close()
    return