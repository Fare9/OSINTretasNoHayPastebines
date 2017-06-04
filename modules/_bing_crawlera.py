#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Crawler que buscará en bing URLs de pastebin,
    aun teniendo menos limitaciones que Google, 
    también puede fallar, pero no es perfecto. 

    @author: Fare9
    @mail: farenain9(at)gmail(dot)com
'''


from __base__ import *

import requests
import sys
import re
import time
import random


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


Bing crawler, we could try some advanced search in bing, and It will be
a good script to learn about bing. Code based on TheHarvester 
bing module.

@author: Fare9
@mail: farenain9(at)gmail(dot)com


Ascii art from: https://github.com/syntax-samurai/fsociety
'''

class BingCrawler(Base):

    def __init__(self,verbosity,pages_to_crawl,searches,use_tor):
        '''
            - pages_to_crawl: es normal, crawleamos X páginas de google
        '''
        Base.__init__(self,verbosity,0,use_tor)
        random.seed(None)
        self.pages_to_crawl = pages_to_crawl # maximo 300 puede estar bien

        self.server = "www.bing.com"
        # Un user agent normalito
        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"

        if searches is None:
            self.searches = ["NSA","OSINT","IOC","Malware","Terrorism","ISIS","Anonymous","Exploit"]
        else:
            self.searches = searches

        self.urls_pastebin = set()
        self.total_results = 0
        self.counter = 0
        self.textToFind = '' # buscaremos palabras con un OR, así aparece una u otra

    def run(self):
        '''
            Ejecuta crawler
        '''    
        print logo
        self.print_notification("Bing crawler","Arrancado bing crawler")


        for i in self.searches:
            self.textToFind += str(i) + "+"

            self.process()

            self.counter = 0

            self.textToFind = ''

        self.print_verbosity("[+] URLs PASTEBIN: "+str(self.urls_pastebin),1)

        self.print_notification("Bing crawler","Finalizado bing crawler, se han conseguido "+str(len(self.urls_pastebin))+" tweets")

        return self.urls_pastebin

    def do_search(self):
        try:

            urly = 'https://'+self.server+'/search?q='+self.textToFind+'site%3A+pastebin.com&count=50&first='+str(self.counter)
            self.print_verbosity("URL: "+str(urly),2)
            
            headers = {'User-Agent':self.userAgent}

            # realizamos esperas, pero posiblemente menores que google
            time.sleep(random.randint(0,5))
            r=requests.get(urly,headers=headers)
            time.sleep(random.randint(0,5))

            result = r.content
            #self.print_verbosity("[+] Obtenido de bing: "+str(result),3)

            pastebin_urls = set()
            bsObj =  BeautifulSoup(result,"html5lib")

            # Expresion regular para las URL de pastebin
            regex = r"pastebin.com/[a-zA-Z1-9]{8}" 

            # A continuacion vamos a buscar todas las etiquetas que apunten a pastebin
            self.print_verbosity("[+] Buscando etiquetas con URLs de pastebin",1)
            links = re.findall(regex,result)
            print "total resultados: "+str(links)
            for link in links:
                print link
                pastebin_link = link
                if 'https' not in pastebin_link:
                    pastebin_link = 'https://' + pastebin_link

                self.print_verbosity("[+] Encontrada URL: "+str(pastebin_link),2)
                if self.check_url(pastebin_link):
                    pastebin_urls.add(pastebin_link)
                    time.sleep(0.3)
            return pastebin_urls
        except Exception as e:  
            self.print_verbosity("[-] ERROR SEARCHING BING: "+str(e),0)
            return None

    def process(self):
        while (self.counter < self.pages_to_crawl):
            result = self.do_search()
            if result is not None:
                self.urls_pastebin.update(result)
            self.counter += 50
            self.print_verbosity("[+] Searching: "+str(self.counter)+" results...",2)

if __name__ == '__main__':
    bc = BingCrawler(3,200,None,False)
    print bc.run()