#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Crawler que buscará en Google URLs de Pastebin,
    este crawler puede fallar debido a las limitaciones
    que imponga Google, así como no será posible el uso
    de TOR, ya que Google pediría un captcha

    @author: Fare9
    @mail: farenain9(at)gmail(dot)com
'''

from modules.__base__ import *
from utilities.common_variables import logo_base

import requests
import sys
import re
import time
import random


logo = logo_base % ('''Google crawler to get pastebin URLs, we could try to do some
advanced search from Google Dorks. Code based on TheHarvester 
google module.''')

class GoogleCrawler(Base):

    def __init__(self,verbosity,pages_to_crawl,searches,use_tor):
        '''
            - pages_to_crawl: es normal, crawleamos X páginas de google
        '''
        Base.__init__(self,verbosity,0,use_tor)
        random.seed(None)
        self.pages_to_crawl = pages_to_crawl # maximo 300 puede estar bien

        self.server = "www.google.com"
        self.hostname = "www.google.com"
        # Un user agent normalito
        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        if searches is None:
            options = PastebinConfig()['Google']
            self.searches = options['searches'].split(",")
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
        self.print_notification("Google crawler","Arrancado google crawler")


        for i in self.searches:
            self.textToFind += str(i) + "+"

        if self.textToFind[-1] == "+":
            self.textToFind = self.textToFind[:-1]

        self.process()

        self.print_verbosity("[+] URLs PASTEBIN: "+str(self.urls_pastebin),1)

        self.print_notification("Google crawler","Finalizado google crawler, se han conseguido "+str(len(self.urls_pastebin))+" tweets")

        return self.urls_pastebin

    def do_search(self):
        try:
            urly = "https://www.google.es/search?num="+str(100)+"&start="+str(self.counter)+"&as_q=&as_epq=&as_oq="+self.textToFind+"&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=pastebin.com&as_occt=title&safe=images&as_filetype=&as_rights="
            
            self.print_verbosity("[+] URL a buscar: "+urly,3)
            headers = {'User-Agent':self.userAgent}

            #realizamos esperas para evitar problemas con google
            time.sleep(random.randint(0,10))
            r=requests.get(urly,headers=headers)
            time.sleep(random.randint(0,10))


            result = r.content 
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
            self.print_verbosity("[-] ERROR SEARCHING GOOGLE: "+str(e),0)
            return None 

    def process(self):
        while (self.counter < self.pages_to_crawl):
            result = self.do_search()
            if result is not None:
                self.urls_pastebin.update(result)
            self.counter += 100
            self.print_verbosity("[+] Searching: "+str(self.counter)+" results...",2)

if __name__ == '__main__':
    gc = GoogleCrawler(3,300,None,False)
    print gc.run()