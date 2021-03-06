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


    @author: Fare9
    @mail: farenain9(at)gmail(dot)com
'''


from modules.__base__ import *
from utilities.common_variables import logo_base

# Otras librerías interesantes
import re
import sys
import time


logo = logo_base % ('''Twitter crawler to get pastebin URLs, you can change verbosity and time to crawl
this crawler is one of the modules for the OSINT tool OSINTretasNoHayPastebines,
you can use it and modify it.''')

class TwitterCrawler(Base):

    def __init__(self,verbosity,time_to_crawl,use_tor,user,password,look_for):
        '''
            +   user = nombre de usuario en twitter
            +   password = password en twitter
            +   look_for = cadenas que mirar
        '''
        Base.__init__(self,verbosity,time_to_crawl,use_tor)
        self.user = user
        self.password = password
        self.driver = None
        self.dict_for_tweets = {} # guardaremos el id como la clave, si no tiene ID pues no es tweet
        # los tweets suelen tener un id como stream-item-tweet-854876533420412928
        # al usarlo como clave de diccionario, no se repetirá, guardamos objetos beatufiulsoup 

        self.urls_pastebin = []
        # cadenas para buscar en twitter
        if look_for is None:
            options = PastebinConfig()['Twitter']
            self.look_for = options["searches"].split(",")
        else:
            self.look_for = look_for

    def run(self):
        '''
            Ejecuta crawler
        '''
        print logo
        self.print_notification("Twitter crawler","Arrancado twitter crawler")

        retorno = self.start_crawler()
        if retorno is None:
            return None

        usIn,pssIn = self.get_login_inputs()
        if usIn is None or pssIn is None:
            return None

        time.sleep(2)
        retorno = self.login_twitter(usIn,pssIn)
        if retorno is None:
            return None

        for string in self.look_for:
            # buscamos la cadena obtenemos los tweets y lo metemos en nuestro diccionario
            self.look_for_string(string)
            retorno = self.give_me_that_tweets()
            self.dict_for_tweets.update(retorno)

        # después buscaremos en el contenido las URLs de pastebin
        self.urls_pastebin = self.get_pastebin_urls(self.dict_for_tweets)
        self.print_verbosity("[+] URLs PASTEBIN: "+str(self.urls_pastebin),1)

        self.print_notification("Twitter crawler","Finalizado twitter crawler, se han conseguido "+str(len(self.urls_pastebin))+" tweets")
        self.driver.quit()
        return self.urls_pastebin

    def start_crawler(self):
        '''
            Empieza el crawler y mete en twitter
        '''
        try:
            print "[+] Starting Twitter"
            caps = webdriver.DesiredCapabilities().FIREFOX
            caps["marionette"] = False
            self.driver = webdriver.Firefox(executable_path='/opt/geckodriver',capabilities = caps)
            self.driver.get("https://twitter.com/es")
            self.driver.maximize_window()
            time.sleep(5)
            return 0
        except Exception as e:
            self.print_verbosity("[-] ERROR START_CRAWLER: "+str(e),0)
            return None

    def get_login_inputs(self):
        '''
            Dame los inputs ricos para loguearme
        '''
        try:
            userInput = self.driver.find_element_by_xpath("//input[@name='session[username_or_email]']")
            passwordInput = self.driver.find_element_by_xpath("//input[@name='session[password]']")
            
            return userInput,passwordInput
        except Exception as e:
            self.print_verbosity("[-] ERROR GET_LOGIN_INPUTS: "+str(e),0)
            return None,None

    def login_twitter(self,usIn,pssIn):
        '''
            Finalmente entra en twitter
        '''
        try:
            usIn.click()
            usIn.send_keys(self.user)
            pssIn.click()
            pssIn.send_keys(self.password)
            pssIn.send_keys(Keys.ENTER)
            time.sleep(4)
            return 0
        except Exception as e:
            self.print_verbosity("[-] ERROR LOGIN_TWITTER: "+str(e),0)
            return None

    def look_for_string(self,lookfor):
        '''
            Para buscar dentro de twitter en la cajita de busqueda

        '''
        query_box = self.driver.find_element_by_xpath("//input[@id='search-query']")
        query_box.clear()
        query_box.send_keys(lookfor)
        query_box.send_keys(Keys.ENTER)
        self.print_verbosity("[?] Buscando por: "+str(lookfor),1)
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

        self.print_verbosity("[+] Obteniendo tweets",1)
        while (time.time()-a) < float(self.time_to_crawl*2): #crawlearemos por un tiempo
                                                             #ya que se hace espera de 2 segundo, pues multiplicamos por 2
                                                             #los segundos que entran por los que salen
            bsObject = BeautifulSoup(self.driver.page_source,"html5lib")
            # obtenemos primero el ol por su id
            olTweets = bsObject.find("ol",{"id":"stream-items-id"})

            # ahora obtenemos sus li
            allli = olTweets.findAll("li")

            # ahora pasamos un poco por cada uno quitando bazofia
            # normalmente los tweets tienen el atributo id
            for li in allli:
                if li.has_attr("id"):
                    # directo al diccionario
                    if li["id"] not in tweetsList:
                        self.print_verbosity("[+] Insertando tweet con id: "+str(li["id"]),2)
                        tweetsList[str(li["id"])] = li

            # ahora scroll
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        self.print_verbosity("[!] Número total de tweets obtenidos: "+str(len(tweetsList)),1)
        return tweetsList

    def get_pastebin_urls(self,tweets):
        '''
            Obtener las url de pastebin a base de expresión 
            regular, eso de las regex parecía potentillo
        '''
        pastebin_urls = set() # un set, así no se repiten
        for tweet in tweets:
            # como es un li, obtenemos el text
            self.print_verbosity("[+] Buscando URL para el tweet: "+tweet,2)
            tweet_text = tweets[tweet].find("p").get_text()
            # para buscar los enlaces normales
            regex = r"pastebin\.com/[a-zA-Z1-9]{8}"
            enlaces = re.findall(regex,tweet_text)
            # para buscar los enlaces raw, y los limpiamos
            regex = r"pastebin\.com/raw/[a-zA-Z1-9]{8}"
            enlacesraw = re.findall(regex,tweet_text)
            for i in range(len(enlacesraw)):
                enlacesraw[i] = enlacesraw[i].replace("/raw","")

            enlaces += enlacesraw

            self.print_verbosity("[!] Enlaces encontrados: "+str(enlaces),3)
            for enlace in enlaces:
                if self.check_url(enlace):
                    pastebin_urls.add(enlace)

        return pastebin_urls

if __name__ == '__main__':
    tc = TwitterCrawler(3,5,'OSINTPastebin','ojetedevaca',None)
    tc.run()