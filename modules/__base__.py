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

class Base():

    def __init__(self,verbosity=1,time_to_crawl=10):
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

    def run(self):
        pass

    def print_verbosity(self,message,verbosity_required):
        '''
            Mostramos según verbosidad (importancia)
            del mensaje
        '''
        if self.verbosity >= verbosity_required:
            print message