#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Clase base para los crawlers,
    esta clase modelará un poco 
    como deben ser los crawlers,
    incluyendo algunas variables 
    que pueden tener todos

    @author: Fare9
    @mail: farenain9(at)gmail(dot)com
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
from threading import Thread
from torrequest import TorRequest # para tor
from utilities.PastebinConfig import PastebinConfig

import os
import requests
try:
    import notify2
except:
    print "[-] No fue posible importar notify2"
import time

class Base():

    def __init__(self,verbosity=1,time_to_crawl=10,use_tor=False):
        '''
            +   verbosity = nivel de verbosidad en los mensajes
            |
            |---------> verbosity = -1 # nada mensajes, ni de error
            |---------> verbosity =  0 # mensajes de error
            |---------> verbosity =  1 # algo normal, un poco para saber como vamos 
            |---------> verbosity =  2 # aun más mensajes
            |---------> verbosity =  3 # incluye incluso mensajes estupidos
            
            +   time_to_crawl = tiempo que debe durar cada crawler/2

        '''
        self.verbosity = verbosity
        self.time_to_crawl = time_to_crawl
        self.use_tor = use_tor
        try:
            notify2.init("OSINTretasNoHayPastebines")
        except:
            print "[-] No fue posible iniciar notify2"
    def run(self):
        pass

    def print_verbosity(self,message,verbosity_required):
        '''
            Mostramos según verbosidad (importancia)
            del mensaje
        '''
        if self.verbosity >= verbosity_required:
            print message

    def print_notification(self,title,message):
        '''
            Para mostrar mensajes de notificaciones
        '''
        if self.verbosity >= 0:
            argumento = [title,message]
            thread = Thread(target = show_notification, args = [argumento])
            thread.start()

    def check_url(self,url):
        '''
            Método para ver si una URL sigue en pie
            en ese caso la podemos mandar 
        '''
        self.print_verbosity("[+] Checkeando si la URL: "+url+" esta online",3)
        try:
            if "https://" not in url:
                url = "https://"+url

            if not self.use_tor:
                response_code = requests.get(url).status_code
            else:
                with TorRequest() as tr:
                    contador = 0
                    response_code = tr.get(url).status_code
                    while response_code != 200:
                        # en caso de que no responda, puede ser cosa de tor
                        # en ese caso reiniciamos el servicio y esperamos un 
                        # par de segundos
                        os.system("service tor restart")
                        time.sleep(2)
                        response_code = tr.get(url).status_code
                        contador += 1
                        if contador == 3:
                            break
            if response_code == 200:
                self.print_verbosity("[+] EXISTE",3)
                return True
            else:
                self.print_verbosity("[+] NO EXISTE: "+str(response_code),3)
                return False
        except Exception as e:
            self.print_verbosity("[+] NO EXISTE: "+str(e),3)
            return False

def show_notification(args):
    '''
        Para ejecutar en un hilo a parte
    '''
    try:
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
    except:
        pass