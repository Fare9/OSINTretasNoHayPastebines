#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Crawler que obtendrá de la página de pastebin
    todas las URLs posibles a obtener, estas
    no son muchas, pero podemos conseguir las actuales
    tendencias y las URLs que aparecen más actuales

    @author: Fare9
    @mail: farenain9(at)gmail(dot)com
'''

from __base__ import *

import requests
import re

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

class PastebinCrawler(Base):

    def __init__(self,verbosity,urls_to_search):
        '''
            No argumentos propios
        '''
        Base.__init__(self,verbosity,0)
        self.urls_pastebin = set()

        if urls_to_search is None:
            self.urls_to_search = ["https://pastebin.com/archive","https://pastebin.com/trends"]
        else:
            self.urls_to_search = urls_to_search


    def run(self):
        '''
            Ejecuta el crawler
        '''
        print logo

        self.print_notification("Pastebin Crawler","Arrancado pastebin crawler")

        for page in self.urls_to_search:
            text = self.get_web_page(page)
            if text is None:
                return None
            self.urls_pastebin.update(self.get_pastebin_urls(text))


        self.print_verbosity("[+] URLs PASTEBIN: "+str(self.urls_pastebin),1)

        self.print_notification("Pastebin crawler","Finalizado pastebin crawler, se han conseguido "+str(len(self.urls_pastebin))+" tweets")
        return self.urls_pastebin

    def get_web_page(self,web_page):
        '''
            Obtener toda la página web de pastebin
            y luego empezar a obtener enlaces
        '''
        try:
            response = requests.get(web_page)
            if response.status_code == 200:
                return response.text
            else:
                self.print_verbosity("[-] ERROR GET_WEB_PAGE response status not 200")
                return None
        except Exception as e:
            self.print_verbosity("[-] ERROR GET_WEB_PAGE: "+str(e),0)
            return None

    def get_pastebin_urls(self,text):
        '''
            Obtener las urls de pastebin dentro de pastebin.
        '''
        pastebin_urls = set()
        try:
            bsObject = BeautifulSoup(text,"html5lib")
            regex = r"\/[a-zA-Z1-9]{8}"

            # primero vamos a obtener las tendencias
            self.print_verbosity("[+] Obteniendo enlaces tendencias de pastebin",1)
            tableTrends = bsObject.find("table",{"class":'maintable'})
            for link in tableTrends.findAll('a',href=re.compile(regex)):
                if '/u/' in str(link):
                    continue
                self.print_verbosity("[+] Obteniendo enlace de: "+str(link),2)

                if 'href' in link.attrs:
                    url = "pastebin.com" + link['href']
                    self.print_verbosity("[!] Enlace obtenido: "+str(url),3)

                    if self.check_url(url):
                        pastebin_urls.add(url)

            # ahora vamos a obtener los enlaces que aparecen a la derecha
            self.print_verbosity("[+] Obteniendo enlaces nuevos de pastebin",1)
            ulNew = bsObject.find('ul',{'class':'right_menu'})
            for link in ulNew.findAll('a',href=re.compile(regex)):
                if '/u/' in str(link):
                    continue
                self.print_verbosity("[+] Obteniendo enlace de: "+str(link),2)
                if 'href' in link.attrs:
                    url = "pastebin.com" + link['href']
                    self.print_verbosity("[!] Enlace obtenido: "+str(url),3)

                    if self.check_url(url):
                        pastebin_urls.add(url)

            return pastebin_urls
        except Exception as e:
            self.print_verbosity("[-] ERROR GET_PASTEBIN_URLS: "+str(e),0)
            return None

if __name__ == '__main__':
    pc = PastebinCrawler(3,None)
    pc.run()