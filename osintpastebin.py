#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Intento de consola para poder establecer 
    valores así como para ejecutar los plugins
    y obtener los valores para buscar en los 
    enlaces de pastebin.
'''


'''
    Librerías que importar 
'''
from modules._pastebin_crawlera import PastebinCrawler
from modules._twitter_crawlera import TwitterCrawler
from modules._seeker_picker import Seeker_Picker
from modules._google_crawlera import GoogleCrawler
from modules._bing_crawlera import BingCrawler
from utilities.common_variables import logo_base
import os
import signal
import sys
import time
import pprint
import numpy # para guardar los datos
import json  # para guardar los datos

logo = logo_base % ('''Welcome to the OSINTretasNoHayPastebines console, if you don't know what to do
please, enter "help" command.''')


'''
    Variables globales a modificar,
    estas variables serán modificadas
    por la consola con el comando:

        set <variable> valores
'''
pastebin_urls = set()       # urls de pastebin
regExs = []                 # expresiones regulares a buscar
emails = []                 # emails a buscar
names  = []                 # nombres a buscar
dnis   = []                 # Documentos de identidad a buscar
cadenas = []                # strings a buscar
reconocimientos = []        # lo que hemos encontrado en pastebin

verbosity = 1               # verbosidad del programa
time_to_crawl = 10          # tiempo de crawling
use_tor = False             # usar o no TOR
userTwitter = None          # usuario de twitter
passTwitter = None          # password de twitter
pages_to_crawl = 100        # Nº de URLs a buscar con google
prompt = "OSINTPASTEBIN >> "
variables = ["use_tor","verbosity","time_crawl","regExs","emails","names","dnis",
            "cadenas","prompt","urls","crawlers","twitterUser","twitterPassword","reconocimientos",
            "pages_to_crawl"]

'''
    Variables de los módulos a cargar,
    estos serán usados con load y
    run. Carga con las variables 
    setteadas

    load <modulo> 
'''
seeker_picker = None
twitter_crawler = None
pastebin_crawler = None
google_crawler = None
bing_crawler = None
crawlers = ["twitter","pastebin","google","bing"]



'''
    Variables de uso general
'''
OKBLUE = '\033[94m'
ENDC = '\033[0m'

'''
    Ayudas que podran servir al usuario,
    estas seran cadenas indicando 
    que cosas puede hacer el usuario
'''




total_help = '''
    
    Bienvenido a OSINTretasNoHayPastebines, supongo que habrás escrito help,
    si no, no estarías aquí. Bien te voy a contar un poco los comandos 
    que tenemos por aquí.

        - set: establece valor a una de las variables del programa, para
        conocer las variables disponibles, ejecuta "set" sin argumentos.
        Ejemplo:    set prompt nuevo_prompt >> 

        - show: muestra el valor de las variables actuales, así como de los 
        módulos que actualmente tiene el programa. Para conocer las variables
        disponibles, ejecuta "show" sin argumentos.
        Ejemplo:    show verbosity

        - load: carga módulos con las variables setteadas, existen variables 
        con valores por defecto.
        Ejemplo:    load twitter

        - search: Busca los patrones y cadenas indicadas con set dentro del
        código de las URL de pastebein.
        Ejemplo:    search

        - save: Guarda los datos de urls o de reconocimientos de pastebin en
        archivos para mantener persistencia.
        Ejemplo: save urls

        - get: Obtiene las urls guardadas en un archivo, así tenemos persistencia
        ante las URLs las cuales lleva tiempo conseguir.
        Ejemplo: get archivo_urls.npy
'''

bad_variable = '''
        
        Las siguientes variables pueden ser modificadas
        con los siguientes valores:
            + prompt: prompt que mostrar en la consola, si se deja en blanco usamos el normal

            + use_tor: usar o no la red tor para checkear las URLs

            ejemplo: set use_tor true

            + verbosity: verbosidad del programa, cuanta información mostrar
            |
            |------------> -1 = No mostrar nada de información
            |------------>  0 = Mostrar errores mínimo
            |------------>  1 = Mostrar mínimo de información, para ver como va
            |------------>  2 = Mostrar algo más de información
            |------------>  3 = Mucha información de todo lo que se hace

            ejemplo: set verbosity -1

            + time_crawl: tiempo para realizar crawling en algunos plugins

            ejemplo: set time_crawl 20

            + regExs: expresiones regulares que buscar en pastebin
            |
            |------------> f <path_to_file> = coger expresiones regulares de archivo
            |------------> d <expresion_regular> = expresión regular directa

            ejemplo: set regExs d exploit MacOS[0-9]{2}

            + emails: emails a buscar dentro de pastebin
            |
            |------------> f <path_to_file> = coger emails de archivo
            |------------> d <email> = email directo

            ejemplo: set emails d fulanito@detal.com

            + names: Nombres a buscar dentro de pastebin
            |
            |------------> f <path_to_file> = coger nombres de archivo
            |------------> d <nombre> = nombre directo

            ejemplo: set nombre d Mr.bean

            + dnis: documentos de identidad a buscar
            |
            |------------> f <path_to_file> = coger documentos de archivo
            |------------> d <documento> = documento directo

            ejemplo: set dnis "11111111A"

            + cadenas: una cadena cualquiera en pastebin
            |
            |------------> f <path_to_file> = coger cadenas de archivo
            |------------> d <cadena> = cadena directa

            ejemplo: set cadenas archivo.pdf

            + twitterUser: usuario para twitter

            + twitterPassword: password para twitter

            + pages_to_crawl: número de páginas a buscar por google o bing
'''

bad_show = '''

        Las siguientes variables pueden ser consultadas:
            + use_tor: uso o no de tor en el check de urls

            + verbosity: verbosidad del programa, cuanta información mostrar

            + time_crawl: tiempo para realizar crawling en algunos plugins

            + regExs: expresiones regulares que buscar en pastebin

            + emails: emails a buscar dentro de pastebin

            + names: Nombres a buscar dentro de pastebin

            + dnis: documentos de identidad a buscar

            + cadenas: una cadena cualquiera en pastebin

            + urls: las urls ya sacadas de pastebin

            + crawlers: crawlers disponibles

            + twitterUser: Usuario para twitter

            + twitterPassword: Password para twitter

            + reconocimientos: URLs encontradas que matchean con expresiones y cadenas dadas

            + pages_to_crawl: Número de URLs a buscar por google o bing
'''

bad_load = '''

        Los siguientes módulos pueden ser cargados:

            - twitter: módulo que ejecuta crawling en twitter para conseguir
            enlaces de pastebin.
            Ejemplo:    load twitter
            - pastebin: módulo que ejecuta crawling en pastebin para conseguir
            unos pocos enlaces de pastebin.
            Ejemplo:    load pastebin
            - google: módulo que ejecuta crawling en google para conseguir
            enlaces de pastebin.
            Ejemplo:    load google
            - bing: módulo que ejecuta crawling en bing para conseguir
            enlaces de pastebin.
            Ejemplo:    load bing
'''

bad_save = '''
        Las siguientes opciones valen para save:

            - urls: guarda las urls encontradas.
            Usa un formato de numpy para guardarlo mejor.
            Ejemplo: save urls
            - founds: guarda los reconocimientos encontrados en pastebin.
            Usa formato JSON para usarlo con otras herramientas.
            Ejemplo: save founds
'''
'''
    Funciones a utilizar
'''

def signal_handler(signal, frame):
    '''
        Método para evitar el uso de CTRL-C y que pete el programa
    '''
    print('\n\nGracias por utilizar OSINTretasNoHayPastebines')
    sys.exit(0)


def transform_args(args):
    '''
        metodo para transformar una lista en una cadena
    '''
    cadena = ''
    for arg in args:
        cadena += str(arg) + " "

    cadena = cadena.strip()
    return cadena

def _set_variables(command):
    '''
        Funcion para establecer los valores
    '''
    global use_tor,verbosity,time_to_crawl,regExs,emails,names,dnis,cadenas,prompt,userTwitter,passTwitter,pages_to_crawl

    command_list = command.split(" ") 
    # tomaremos ya que el primer comando es set
    # segundo la variable a tomar
    # los demás dependerán de la variable

    try:

        variable_to_change = str(command_list[1])

        if variable_to_change not in variables:
            print "[-] La variable "+variable_to_change+" no es una variable a modificar"
            print bad_variable
            return -1

        else: 
            if variable_to_change == "verbosity":
                try:
                    verbosidad = int(command_list[2])
                    if verbosidad < -1 or verbosidad > 3:
                        print "[-] Verbosidad debe estar entre -1 y 3"
                        print bad_variable
                        return -1
                    else:
                        verbosity = verbosidad
                except:
                    print "[-] La verbosidad debe ser un número"
                    print bad_variable
                    return -1

            elif variable_to_change == "pages_to_crawl":
                try:
                    pages_to_crawl = int(command_list[2])
                    if pages_to_crawl < 0 or pages_to_crawl > 300:
                        print "[-] Pages_to_crawl debe estar entre 0 y 300"
                        print bad_variable
                        return -1
                except:
                    print "[-] pages_to_crawl debe ser un número"
                    print bad_variable
                    return -1

            elif variable_to_change == "use_tor":
                if command_list[2] == "true":
                    use_tor = True
                elif command_list[2] == "false":
                    use_tor = False
                else:
                    print "[-] use_tor debe ser True o False"

            elif variable_to_change == 'time_crawl':
                try:
                    tiempo = int(command_list[2])
                    time_to_crawl = tiempo
                except:
                    print "[-] El número debe ser un entero"
                    print bad_variable
                    return -1

            elif variable_to_change == "prompt":
                if len(command_list) == 2:
                    prompt = "OSINTPASTEBIN >> "
                else:
                    prompt = transform_args(command_list[2:])
                    prompt += " "

            elif variable_to_change == "twitterUser":
                userTwitter = transform_args(command_list[2:])

            elif variable_to_change == "twitterPassword":
                passTwitter = transform_args(command_list[2:])

            # variables que aceptan ficheros
            elif variable_to_change == "regExs":
                if str(command_list[2]) == "f":
                    archivo = str(command_list[3])
                    try:
                        f_regEx = open(archivo,'rb')
                    except:
                        print "[-] El archivo "+archivo+" no existe"
                        return -1
                    data = f_regEx.readlines()
                    f_regEx.close()
                    regExs = []
                    regExs = data
                elif str(command_list[2]) == "d":
                    regExs = command_list[3:]
                else:
                    print "[-] Comando no valido"
                    print bad_variable
                    return -1

            elif variable_to_change == "emails":
                if str(command_list[2]) == "f":
                    archivo = str(command_list[3])
                    try:
                        f_regEx = open(archivo,'rb')
                    except:
                        print "[-] El archivo "+archivo+" no existe"
                        return -1
                    data = f_regEx.readlines()
                    f_regEx.close()
                    emails = []
                    emails = data
                elif str(command_list[2]) == "d":
                    emails = command_list[3:]
                else:
                    print "[-] Comando no valido"
                    print bad_variable
                    return -1

            elif variable_to_change == "names":
                if str(command_list[2]) == "f":
                    archivo = str(command_list[3])
                    try:
                        f_regEx = open(archivo,'rb')
                    except:
                        print "[-] El archivo "+archivo+" no existe"
                        return -1
                    data = f_regEx.readlines()
                    f_regEx.close()
                    names = []
                    names = data
                elif str(command_list[2]) == "d":
                    names = command_list[3:]
                else:
                    print "[-] Comando no valido"
                    print bad_variable
                    return -1

            elif variable_to_change == "dnis":
                if str(command_list[2]) == "f":
                    archivo = str(command_list[3])
                    try:
                        f_regEx = open(archivo,'rb')
                    except:
                        print "[-] El archivo "+archivo+" no existe"
                        return -1
                    data = f_regEx.readlines()
                    f_regEx.close()
                    dnis = []
                    dnis = data
                elif str(command_list[2]) == "d":
                    dnis = command_list[3:]
                else:
                    print "[-] Comando no valido"
                    print bad_variable
                    return -1

            elif variable_to_change == "cadenas":
                if str(command_list[2]) == "f":
                    archivo = str(command_list[3])
                    try:
                        f_regEx = open(archivo,'rb')
                    except:
                        print "[-] El archivo "+archivo+" no existe"
                        return -1
                    data = f_regEx.readlines()
                    f_regEx.close()
                    cadenas = []
                    cadenas = data
                elif str(command_list[2]) == "d":
                    cadenas = command_list[3:]
                else:
                    print "[-] Comando no valido"
                    print bad_variable
                    return -1

    except IndexError:
        print "[-] Número de argumentos no valido"
        print bad_variable

def _show_variables(command):
    '''
        Método para mostrar las variables que tenemos
    '''
    try:
        command_list = command.split(" ")

        variable_to_show = command_list[1]

        if variable_to_show not in variables:
            print "[-] La variable "+variable_to_show+" no está en las variables del programa"
            print bad_show
            return -1
        else: 

            if variable_to_show == "verbosity":
                print "verbosity="+str(verbosity)
            elif variable_to_show == "use_tor":
                if use_tor:
                    print "use_tor=true"
                else:
                    print "use_tor=false"
            elif variable_to_show == "time_crawl":
                print "time to crawl="+str(time_to_crawl)

            elif variable_to_show == "twitterUser":
                print "Usuario twitter="+str(userTwitter)

            elif variable_to_show == "twitterPassword":
                print "Contraseña twitter="+str(passTwitter)

            elif variable_to_show == "regExs":
                print "Lista de expresiones regulares: "
                for regex in regExs:
                    print "\t- "+regex

            elif variable_to_show == "emails":
                print "Lista de mails: "
                for mail in emails:
                    print "\t- "+mail

            elif variable_to_show == 'names':
                print "Lista de nombres: "
                for name in names:
                    print "\t- "+name

            elif variable_to_show == 'dnis':
                print "Lista de DNIs: "
                for dni in dnis:
                    print "\t- "+dni

            elif variable_to_show == 'cadenas':
                print "Lista de cadenas: "
                for cadena in cadenas:
                    print "\t- "+cadena

            elif variable_to_show == 'urls':
                print "Lista de urls de pastebin: "
                for url in pastebin_urls:
                    print "\t- "+url

            elif variable_to_show == 'crawlers':
                print "Lista de crawlers: "
                for element in crawlers:
                    print "\t- "+str(element)

            elif variable_to_show == 'reconocimientos':
                pprint.pprint(reconocimientos)

            elif variable_to_show == 'pages_to_crawl':
                print "pages_to_crawl="+str(pages_to_crawl)

            else:
                print bad_show
                return -1
    except IndexError:
        print "[-] Número de argumentos no valido"
        print bad_show
        return -1

def _load_crawlers(command):
    '''
        Función para cargar los crawlers con los objetos.
    '''
    global twitter_crawler,pastebin_crawler,google_crawler,bing_crawler

    try:
        command_list = command.split(" ")

        crawler = command_list[1]

        if crawler not in crawlers:
            print "[-] El módulo "+crawler+" no está en los módulos del programa"
            print bad_load
            return -1
        else:
            #crawlers = ["twitter","pastebin"]
            if crawler == "twitter":
                if userTwitter is None or passTwitter is None:
                    print "[-] Credenciales para twitter son necesarias"
                    return -1
                twitter_crawler = TwitterCrawler(verbosity,time_to_crawl,use_tor,userTwitter,passTwitter,None)

            elif crawler == "pastebin":
                pastebin_crawler = PastebinCrawler(verbosity,use_tor,None,time_to_crawl)

            elif crawler == "google":
                google_crawler = GoogleCrawler(verbosity,pages_to_crawl,None,use_tor)

            elif crawler == "bing":
                bing_crawler = BingCrawler(verbosity,pages_to_crawl,None,use_tor)

    except IndexError:
        print "[-] Número de argumentos no valido"
        print bad_load
        return -1

def _run_crawlers(command):
    '''
        Funcion para ejecutar los crawlers
    '''
    try:
        command_list = command.split(" ")

        crawler = command_list[1]

        if crawler not in crawlers:
            print "[-] El módulo "+crawler+" no está en los módulos del programa"
            print bad_load
            return -1
        else:
            if crawler == "twitter":
                try:
                    pastebin_urls.update(twitter_crawler.run())
                except Exception as e:
                    print "[-] Error al ejecutar crawler de twitter: "+str(e)
            elif crawler == "pastebin":
                try:
                    pastebin_urls.update(pastebin_crawler.run())
                except  Exception as e:
                    print "[-] Error al ejecutar crawler de pastebin: "+str(e)
            elif crawler == "google":
                try:
                    pastebin_urls.update(google_crawler.run())
                except Exception as e:
                    print "[-] Error al ejecutar crawler de google: "+str(e)
            elif crawler == "bing":
                try:
                    pastebin_urls.update(bing_crawler.run())
                except Exception as e:
                    print "[-] Error al ejecutar crawler de bing: "+str(e)
    except IndexError:
        print "[-] Número de argumentos no valido"
        return -1

def _save_data(command):
    '''
        Función para guardar los datos del programa
        tanto las URLs como los resultados de seeker picker
    '''
    try:
        command_list = command.split(" ")

        what_save = command_list[1]

        if what_save == "urls":
            name = "urls_"+time.strftime("%Y-%m-%d_%H:%M")+".npy"
            print "[!] Las urls se guardaran en %s" % (name)
            aux = numpy.array(list(pastebin_urls))
            aux.dump(open(name,'wb'))

        elif what_save == "founds":
            name = "founds_"+time.strftime("%Y-%m-%d_%H:%M")+".json"
            print "[!] Lo encontrado se guardará en %s" % name
            with open(name,'wb') as outfile:
                json.dumps(reconocimientos,outfile)
        else:
            print bad_save
    except IndexError:
        print "[-] Número de argumentos no valido"
        print bad_save
        return -1

def _get_data(command):
    '''
        Función para cargar los datos de URL desde un 
        archivo
    '''
    global pastebin_urls
    try:
        command_list = command.split(" ")

        filenpy = command_list[1]

        if os.path.isfile(filenpy):
            try:
                aux = list(numpy.load(open(filenpy,'rb')))
                pastebin_urls.update(aux)
            except Exception as e:
                print "[-] ERROR cargando datos: "+str(e)
                print "USAGE: get <urls file>"
                return -1
        else:
            print "USAGE: get <urls file>"
            return -1
    except Exception as e:
        print "[-] Número de argumentos no valido"
        print "USAGE: get <urls file>"
        return -1


def main():
    '''
        funcion principal que ejecutará la shell
        esta luego mandará los valores
    '''
    global reconocimientos
    

    os.system("clear")
    try:
        for c in logo.split("\n"):
                print c
                time.sleep(0.2)
    except:
        os.system("clear")
        print logo

    signal.signal(signal.SIGINT, signal_handler)

    command = str(raw_input(OKBLUE + prompt + ENDC))

    while command.strip().lower() not in ["exit","quit"]:

        if command.startswith("set"):
            try:
                _set_variables(command)
            except Exception as e:
                print "[-] Error en la shell: "+str(e)

        elif command.startswith("show"):
            try:
                _show_variables(command)
            except Exception as e:
                print "[-] Error en la shell: "+str(e)

        elif command.startswith("clear"):
            os.system("clear")

        elif command.startswith("load"):
            try:
                _load_crawlers(command)
            except Exception as e:
                print "[-] Error en la shell: "+str(e)

        elif command.startswith("run"):
            try:
                _run_crawlers(command)
            except Exception as e:
                print "[-] Error en la shell: "+str(e)

        elif command.startswith("search"):
            #try:
            seeker_picker = Seeker_Picker(verbosity,pastebin_urls,regExs,emails,names,dnis,cadenas,use_tor)
            reconocimientos = seeker_picker.run()
            #except Exception as e:
            #    print "[-] Error en la shell: "+str(e)

        elif command.startswith("save"):
            try:
                _save_data(command)
            except Exception as e:
                print "[-] Error en la shell: "+str(e)

        elif command.startswith("get"):
            try:
                _get_data(command)
            except Exception as e:
                print "[-] Error en la shell: "+str(e)
        else:
            if command.startswith("help"):
                print total_help
            else:
                print "[-] El comando ejecutado no existe, prueba con help"

        command = str(raw_input(OKBLUE + prompt + ENDC))


if __name__ == '__main__':
    main()