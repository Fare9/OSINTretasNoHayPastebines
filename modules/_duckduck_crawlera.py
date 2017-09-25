#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Crawler que buscará en Duck Duck Go URLs de pastebin,
    este crawler puede fallar en caso de que se imponga
    alguna restricción, es posible el uso de TOR al 
    contrario que Google, ya que Duck Duck Go, permite 
    el uso de TOR.

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

from torrequest import TorRequest # para tor

logo = logo_base % ('''Duck Duck go crawler to get pastebin URLs, we could try to do some
advanced search from Duck Syntax.''')

class DuckDuckCrawler(Base):

    def __init__(self,verbosity,time_to_crawl,use_tor,searches):
        '''
            - pages_to_crawl: es normal, crawleamos X páginas de duck duck go
        '''
        Base.__init__(self,verbosity,0,use_tor)
        # Un user agent normalito
        self.time_to_crawl = time_to_crawl
        self.use_tor = use_tor
        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        if searches is None:
            options = PastebinConfig()['DuckDuckGo']
            self.searches = options['searches'].split(",")
        else:
            self.searches = searches

        self.urls_pastebin = set()
        self.driver = None

    def run(self):
        '''
            Ejecuta el crawler
        '''
        print logo
        self.print_notification("DuckDuckGo crawler","Arrancado duckduckgo crawler")

        self.do_search()

        self.checkea_urls()

        self.print_verbosity("[+] URLs PASTEBIN: "+str(self.urls_pastebin),1)
        self.print_notification("DuckDuckGo crawler","Finalizado duck duck go crawler, se han obtenido "+str(len(self.urls_pastebin))+" urls")

    def do_search(self):
        try:
            for search in self.searches:
                self.start_crawler(search_string=search)
                self.search_for_urls()
        except Exception as e:
            raise

    def start_crawler(self,search_string):
        '''
            Empieza el crawler y mete en duckduckgo
        '''
        try:
            print "[+] Starting Duck Duck Go"
            caps = webdriver.DesiredCapabilities().FIREFOX
            caps["marionette"] = False
            self.driver = webdriver.Firefox(executable_path='/opt/geckodriver',capabilities = caps)
            self.driver.get("https://duckduckgo.com/?q="+search_string+"+site%3Apastebin.com&kp=-2&atb=v61-4&ia=web")
            self.driver.maximize_window()
            time.sleep(5)
            return 0
        except Exception as e:
            raise
            self.print_verbosity("[-] ERROR START_CRAWLER: "+str(e),0)
            return None

    def search_for_urls(self):
        '''
            Busca URLs hasta que el tiempo finalice
        '''
        

        id_search = "r1-%d"
        counter = 0
        errors = 0
        
        bsObject = BeautifulSoup(self.driver.page_source,"html5lib")
        a = time.time()
        while (time.time()-a) < float(self.time_to_crawl*2):
            self.print_verbosity("[+] Obteniendo urls",1)
            if errors > 3:
                break
            # buscamos los enlaces por su div que tiene el id r1-<numero>
            # una vez no haya más, bajamos a ver si seguimos encontrando
            # si no sigue encontrando, pues fuera
            div = bsObject.find("div",{"id":id_search % (counter)})
            # si no existe intentamos bajar para ver si es que ha cargado la página
            # y volvemos a obtener el código de la web
            if not div:
                self.print_verbosity("[+] No hay div avanzamos con scroll",2)
                errors += 1
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                bsObject = BeautifulSoup(self.driver.page_source,"html5lib")
            else:
                # si se ha obtenido respuesta, entonces obtenemos la URL y se añade al carro
                errors = 0 # reiniciamos puesto que ha habido uno correcto
                a_tag = div.find("a",{"class":"result__a"})
                url = str(a_tag['href'])
                self.print_verbosity("[+] Insertando url: "+str(url),2)
                self.urls_pastebin.add(url)
                counter += 1

        self.driver.quit()

    def checkea_urls(self):
        urls = self.urls_pastebin
        for url in urls:
            if not self.check_url(url):
                self.urls_pastebin.remove(url)