#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Clase para obtener la configuración
    de los crawlers a través de un archivo
    de configuración, esto permitirá su 
    modificación durante la ejecución

    @author: Fare9
    @mail: farenain9(at)gmail(dot)com
'''

# Librería para ConfigParser para obtener configuración de un archivo
from ConfigParser import ConfigParser


class PastebinConfig():


    def __init__(self, filename = 'utilities/config.ini'):
        self.options = {}
        self.config = ConfigParser()
        self.config.read(filename)
        for section in self.config.sections():
            self.options[section] = self.getOptions(section)

    def getOptions(self, section):
        """
            Obtiene las opciones de una seccion en formato de diccionario (clave valor)
        """
        options = self.config.options(section)
        params = {}
        for option in options:
            try:
                params[option] = self.config.get(section, option)
            except:
                params[option] = None
        return params

    def __getitem__(self, name):
        return self.options[name]

    def __repr__(self):
        return self.options