#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Crawler que obtendrá URLs de pastebin en twitter
    esta librería buscará enlaces y los irá metiendo
    en una lista set, ya que normalmente esto puede
    llevar mucho tiempo, haremos que se ejecute un 
    tiempo indicado por el llamador

    Al ser un trabajo de clase aquí tengo valores posibles de usar:
    User Name: OSINTretasNoPastebin
    User: OSINTPastebin
    Password: ojetedevaca
'''

# librerías crawling para javascript (selenium)
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# librerías para procesamiento de html (BeautifulSoup)
from bs4 import BeautifulSoup


# Otras librerías interesantes
import re
import sys
import time

class TwitterCrawler():

    def __init__(self,time_to_crawl,user,password):
        
        self.time_to_crawl = time_to_crawl
        self.user = user
        self.password = password
        self.driver = None
        self.dict_for_tweets = {} # guardaremos el id como la clave, si no tiene ID pues no es tweet
        # los tweets suelen tener un id como stream-item-tweet-854876533420412928
        # al usarlo como clave de diccionario, no se repetirá, guardamos objetos beatufiulsoup 
        # y otra clase ya los procesará

        # cadenas para buscar en twitter
        self.look_for = ["pastebin.com","pastebin.com and anonymous","exploit and pastebin.com"]

    def run(self):
        '''
            Ejecuta crawler
        '''
        retorno = self.start_crawler()
        if retorno is None:
            sys.exit(-1)

        usIn,pssIn = self.get_login_inputs()
        time.sleep(2)
        self.login_twitter(usIn,pssIn)

        for string in self.look_for:
            # buscamos la cadena obtenemos los tweets y lo metemos en nuestro diccionario
            self.look_for_string(string)
            retorno = self.give_me_that_tweets()
            self.dict_for_tweets.update(retorno)

    def start_crawler(self):
        '''
            Empieza el crawler y mete en twitter
        '''
        try:
            print "[+] Starting Twitter"
            self.driver = webdriver.Firefox(executable_path='/opt/geckodriver')
            self.driver.get("https://twitter.com/es")
            self.driver.maximize_window()
            time.sleep(5)
            return 0
        except Exception as e:
            print "[-] ERROR START_CRAWLER: "+str(e)
            return None

    def get_login_inputs(self):
        '''
            Dame los inputs ricos para loguearme
        '''
        userInput = self.driver.find_element_by_xpath("//input[@name='session[username_or_email]']")
        passwordInput = self.driver.find_element_by_xpath("//input[@name='session[password]']")
        
        return userInput,passwordInput
    def login_twitter(self,usIn,pssIn):
        '''
            Finalmente entra en twitter
        '''
        usIn.click()
        usIn.send_keys(self.user)
        pssIn.click()
        pssIn.send_keys(self.password)
        pssIn.send_keys(Keys.ENTER)
        time.sleep(4)

    def look_for_string(self,lookfor):
        '''
            Para buscar dentro de twitter en la cajita de busqueda

        '''
        query_box = self.driver.find_element_by_xpath("//input[@id='search-query']")
        query_box.clear()
        query_box.send_keys(lookfor)
        query_box.send_keys(Keys.ENTER)
        print "[?] Buscando por: "+str(lookfor)
        time.sleep(4)

    def give_me_that_tweets(self):
        '''
            Método para obtener todos los tweets de la actual página

            Algoritmo:
                mientras haya tiempo
                    pillamos toda la web de primeras  <------------------
                    obtenemos los <li> actuales con beautifulsoup       |
                    los metemos en la tabla                             |
                    hacemos scroll --------------------------------------
        '''
        tweetsList = {}
        a = time.time()

        while (time.time()-a) < float(self.time_to_crawl*2): #crawlearemos por un tiempo
                                                             #ya que se hace espera de 2 segundo, pues multiplicamos por 2
                                                             #los segundos que entran por los que salen
            bsObject = BeautifulSoup(self.driver.page_source,"html5lib")
            # obtenemos primero el ol por su id
            print "[+] Obteniendo tweets"
            olTweets = bsObject.find("ol",{"id":"stream-items-id"})

            # ahora obtenemos sus li
            allli = olTweets.findAll("li")

            # ahora pasamos un poco por cada uno quitando bazofia
            # normalmente los tweets tienen el atributo id
            for li in allli:
                if li.has_attr("id"):
                    # directo al diccionario
                    if li["id"] not in tweetsList:
                        print "[+] Insertando tweet con id: "+str(li["id"])
                        tweetsList[str(li["id"])] = li

            # ahora scroll
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        print "[!] Número total de tweets obtenidos: "+str(len(tweetsList))
        return tweetsList

if __name__ == '__main__':
    tc = TwitterCrawler(20,'OSINTPastebin','ojetedevaca')
    tc.run()