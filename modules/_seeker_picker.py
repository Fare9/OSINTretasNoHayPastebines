#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Clase para la búsqueda de los patrones
    en los enlaces de Pastebin, este es llamado
    por el usuario al añadir patrones de búsqueda 
    o expresiones regulares.

    Lo que devolverá será un diccionario para cada
    uno de los patrones de búsqueda, con el valor
    que aparezca y el enlace al pastebin que aparezca
'''
from utilities.common_variables import logo_base

logo = logo_base % ('''Module to search in pastebin webpages some strings, regEx, names, emails...''')


import sys
import os

import requests
import notify2
import time
import re
from threading import Thread
from torrequest import TorRequest # para tor

class Seeker_Picker():

    def __init__(self,verbosity,pastebin_urls,regExs,emails,names,dnis,cadenas,use_tor):
        self.verbosity = verbosity
        self.pastebin_urls = pastebin_urls
        self.regExs = regExs
        self.emails = emails
        self.names = names
        self.dnis = dnis
        self.cadenas = cadenas
        self.use_tor = use_tor
        notify2.init("OSINTretasNoHayPastebines")
        self.retorned_dict = []

    def run(self):
        ''' Método principal '''
        print logo

        self.print_verbosity("[+] Starting module to check for your queries",1)

        self.seek_and_pick()

        self.print_verbosity("[+] Finished module, returning dictionary",1)

        self.print_notification("Seeker_picker","Finished module")

        self.print_verbosity("Se devuelve: "+str(self.retorned_dict),1)

        return self.retorned_dict

    def print_verbosity(self,message,verbosity_required):
        '''
            Mostramos según verbosidad (importancia)
            del mensaje
        '''
        if self.verbosity >= verbosity_required:
            print message

    def seek_and_pick(self):
        ''' FUNCIÓN PARA BUSCAR DENTRO DE CADA ENLACE DE PASTEBIN USO SIN TOR '''

        for url in self.pastebin_urls:

            self.print_verbosity("[+] Requesting for pastebin url: "+url,3)
            if 'raw' not in url: # obtenemos la URL raw ya que así será más sencillo
                if ('http://' not in url) and ('https://' not in url):
                    urlRaw = 'https://' + url.split('/')[0] + "/raw/" + url.split('/')[1]
                else:
                    urlRaw = 'https://pastebin.com/raw/'+url.split('pastebin.com/')[1]

            self.print_verbosity("[+] Requesting for pastebin raw url: "+urlRaw,3)

            try:
                if self.use_tor:
                    with TorRequest() as tr:
                        contador = 0 
                        response = tr.get(urlRaw)
                        while response.status_code != 200:
                            # en caso de que no responda, puede ser cosa de tor
                            # en ese caso reiniciamos el servicio y esperamos un 
                            # par de segundos
                            os.system("service tor restart")
                            time.sleep(2)
                            response = tr.get(urlRaw)
                            contador += 1
                            if contador == 3:
                                break
                        if contador == 3:
                            continue
                else:
                    response = requests.get(urlRaw)
            except Exception as e:
                self.print_verbosity("[-] Failed to get url: "+str(url)+" error: "+str(e),2)
                continue

            code_page = response.text

            if response.status_code == 200: # si la vuelta es 200 perfecto

                self.print_verbosity("[+] URL: "+url+" get 200 code",2)

                # buscamos expresiones regulares
                for regEx in self.regExs:
                    pattern = re.compile(regEx)

                    retorno = pattern.match(code_page)

                    if retorno is not None:
                        self.retorned_dict.append({'type':'regex',regEx:url})
                # Fin de las expresiones regulares

                # buscamos emails
                for email in self.emails:
                    if email in code_page:
                        self.retorned_dict.append({'type':'mail',email:url})
                        
                # Fin de los emails
                # buscamos nombres
                for name in self.names:
                    if name in code_page:
                        self.retorned_dict.append({'type':'name',name:url})
                        
                # Fin de nombres
                # DNIs
                for dni in self.dnis:
                    if dni in code_page:
                        self.retorned_dict.append({'type':'dni',dni:url})
                        
                # Fin DNIs
                # Cadenas
                for cadena in self.cadenas:
                    if cadena in code_page:
                        self.retorned_dict.append({'type':'string',cadena:url})
                # Fin Cadenas

            else:
                self.print_verbosity("[-] ERROR URL: "+url+" get "+str(response.status_code)+" code",0)

    def print_notification(self,title,message):
        '''
            Para mostrar mensajes de notificaciones
        '''
        if self.verbosity >= 0:
            argumento = [title,message]
            thread = Thread(target = show_notification, args = [argumento])
            thread.start()

def show_notification(args):
    '''
        Para ejecutar en un hilo a parte
    '''
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

if __name__=='__main__':

    sk = Seeker_Picker(3,['pastebin.com/skQpwccy','pastebin.com/DLy22Puw'],[],[],[],[],['malware','exploit','IOC','pass','password','WWE','MOVIES'],True)

    print sk.run()