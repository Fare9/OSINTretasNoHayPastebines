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

from modules.__base__ import *
from utilities.common_variables import logo_base

import requests
import re
import time

logo = logo_base % ('''Pastebin crawler to get some URLs from mainpage, we can't take too much, 
but maybe it's something''')

class PastebinCrawler(Base):

    def __init__(self,verbosity,use_tor,urls_to_search,time_to_crawl):
        '''
            No argumentos propios
        '''
        Base.__init__(self,verbosity,time_to_crawl,use_tor)
        self.urls_pastebin = set()

        if urls_to_search is None:
            options = PastebinConfig()['Pastebin']
            self.urls_to_search = options['searches'].split(",")
        else:
            self.urls_to_search = urls_to_search


    def run(self):
        '''
            Ejecuta el crawler
        '''
        print logo

        self.print_notification("Pastebin Crawler","Arrancado pastebin crawler")

        actualTime = time.time()


        for page in self.urls_to_search:

            text = self.get_web_page(page)
            if text is None:
                return None
            self.urls_pastebin.update(self.get_pastebin_urls(text))
            if self.time_to_crawl != -1:
                if (time.time() - actualTime) >= float(self.time_to_crawl):
                    break

        self.print_verbosity("[+] URLs PASTEBIN: "+str(self.urls_pastebin),1)

        self.print_notification("Pastebin crawler","Finalizado pastebin crawler, se han conseguido "+str(len(self.urls_pastebin))+" tweets")
        return self.urls_pastebin

    def get_web_page(self,web_page):
        '''
            Obtener toda la página web de pastebin
            y luego empezar a obtener enlaces
        '''
        try:
            if not self.use_tor:
                response = requests.get(web_page)
            else:
                with TorRequest() as tr:
                    response = tr.get(web_page)
            if response.status_code == 200:
                return response.text
            else:
                self.print_verbosity("[-] ERROR GET_WEB_PAGE response status not 200: "+str(web_page),0)
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

            # para buscar distintas index en la página de usuario
            user_page_regex = r"\/u/.+/[0-9]+"
            for link in bsObject.findAll('a',href=re.compile(user_page_regex)):
                user_link = "https://pastebin.com" + link['href']
                if user_link not in self.urls_to_search:
                    self.print_verbosity("[+] Añadido a urls_to_search: "+str(user_link),3)
                    self.urls_to_search.append(user_link)

            # primero vamos a obtener las tendencias
            self.print_verbosity("[+] Obteniendo enlaces tendencias de pastebin",1)
            tableTrends = bsObject.find("table",{"class":'maintable'})
            for link in tableTrends.findAll('a',href=re.compile(regex)):
                if '/u/' in str(link):

                    user_link = "https://pastebin.com" + link['href']
                    if user_link not in self.urls_to_search:
                        self.print_verbosity("[+] Añadido a urls_to_search: "+str(user_link),3)
                        self.urls_to_search.append(user_link)

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
                    user_link = "https://pastebin.com" + link['href']
                    if user_link not in self.urls_to_search:
                        self.print_verbosity("[+] Añadido a urls_to_search: "+str(user_link),3)
                        self.urls_to_search.append(user_link)
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