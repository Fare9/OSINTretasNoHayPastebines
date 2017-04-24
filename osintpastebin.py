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
from modules import _pastebin_crawlera
from modules import _twitter_crawlera

import os
import signal
import sys
import time

'''
    Objetos que tendrán los crawlers
    con las variables que tenemos
    globales.
'''
twitter_crawler = None
pastebin_crawler =  None




'''
    Variables globales a modificar,
    estas variables serán modificadas
    por la consola con el comando:

        set <variable> valores
'''
verbosity = 1               # verbosidad del programa
time_to_crawl = 10          # tiempo de crawling
pastebin_urls = set()       # urls de pastebin
regExs = None               # expresiones regulares a buscar
emails = None               # emails a buscar
names  = None               # nombres a buscar
dnis   = None               # Documentos de identidad a buscar
cadenas = None              # strings a buscar
prompt = "OSINTPASTEBIN >> "
variables = ["verbosity","time_crawl","regExs","emails","names","dnis","cadenas","prompt","urls","crawlers"]

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
logo = """
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XX                                                                          XX
XX   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMMssssssssssssssssssssssssssMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMss'''                          '''ssMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMyy''                                    ''yyMMMMMMMMMMMM   XX
XX   MMMMMMMMyy''                                            ''yyMMMMMMMM   XX
XX   MMMMMy''                                                    ''yMMMMM   XX
XX   MMMy'                                                          'yMMM   XX
XX   Mh'                                                              'hM   XX
XX   -                                                                  -   XX
XX                                                                          XX
XX   ::                                                                ::   XX
XX   MMhh.        ..hhhhhh..                      ..hhhhhh..        .hhMM   XX
XX   MMMMMh   ..hhMMMMMMMMMMhh.                .hhMMMMMMMMMMhh..   hMMMMM   XX
XX   ---MMM .hMMMMdd:::dMMMMMMMhh..        ..hhMMMMMMMd:::ddMMMMh. MMM---   XX
XX   MMMMMM MMmm''      'mmMMMMMMMMyy.  .yyMMMMMMMMmm'      ''mmMM MMMMMM   XX
XX   ---mMM ''             'mmMMMMMMMM  MMMMMMMMmm'             '' MMm---   XX
XX   yyyym'    .              'mMMMMm'  'mMMMMm'              .    'myyyy   XX
XX   mm''    .y'     ..yyyyy..  ''''      ''''  ..yyyyy..     'y.    ''mm   XX
XX           MN    .sMMMMMMMMMss.   .    .   .ssMMMMMMMMMs.    NM           XX
XX           N`    MMMMMMMMMMMMMN   M    M   NMMMMMMMMMMMMM    `N           XX
XX            +  .sMNNNNNMMMMMN+   `N    N`   +NMMMMMNNNNNMs.  +            XX
XX              o+++     ++++Mo    M      M    oM++++     +++o              XX
XX                                oo      oo                                XX
XX           oM                 oo          oo                 Mo           XX
XX         oMMo                M              M                oMMo         XX
XX       +MMMM                 s              s                 MMMM+       XX
XX      +MMMMM+            +++NNNN+        +NNNN+++            +MMMMM+      XX
XX     +MMMMMMM+       ++NNMMMMMMMMN+    +NMMMMMMMMNN++       +MMMMMMM+     XX
XX     MMMMMMMMMNN+++NNMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMNN+++NNMMMMMMMMM     XX
XX     yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy     XX
XX   m  yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy  m   XX
XX   MMm yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy mMM   XX
XX   MMMm .yyMMMMMMMMMMMMMMMM     MMMMMMMMMM     MMMMMMMMMMMMMMMMyy. mMMM   XX
XX   MMMMd   ''''hhhhh       odddo          obbbo        hhhh''''   dMMMM   XX
XX   MMMMMd             'hMMMMMMMMMMddddddMMMMMMMMMMh'             dMMMMM   XX
XX   MMMMMMd              'hMMMMMMMMMMMMMMMMMMMMMMh'              dMMMMMM   XX
XX   MMMMMMM-               ''ddMMMMMMMMMMMMMMdd''               -MMMMMMM   XX
XX   MMMMMMMM                   '::dddddddd::'                   MMMMMMMM   XX
XX   MMMMMMMM-                                                  -MMMMMMMM   XX
XX   MMMMMMMMM                                                  MMMMMMMMM   XX
XX   MMMMMMMMMy                                                yMMMMMMMMM   XX
XX   MMMMMMMMMMy.                                            .yMMMMMMMMMM   XX
XX   MMMMMMMMMMMMy.                                        .yMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMy.                                    .yMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMs.                                .sMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMss.           ....           .ssMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMNo         oNNNNo         oNMMMMMMMMMMMMMMMMMMMM   XX
XX                                                                          XX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    .o88o.                               o8o                .
    888 `"                               `"'              .o8
   o888oo   .oooo.o  .ooooo.   .ooooo.  oooo   .ooooo.  .o888oo oooo    ooo
    888    d88(  "8 d88' `88b d88' `"Y8 `888  d88' `88b   888    `88.  .8'
    888    `"Y88b.  888   888 888        888  888ooo888   888     `88..8'
    888    o.  )88b 888   888 888   .o8  888  888    .o   888 .    `888'
   o888o   8""888P' `Y8bod8P' `Y8bod8P' o888o `Y8bod8P'   "888"      d8'
                                                                     .o...P'

Welcome to the OSINTretasNoHayPastebines console, if you don't know what to do
please, enter "help" command.

@author: Fare9
@mail: farenain9(at)gmail(dot)com


Ascii art from: https://github.com/syntax-samurai/fsociety
"""


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
'''



bad_variable = '''
        
        Las siguientes variables pueden ser modificadas
        con los siguientes valores:
            + prompt: prompt que mostrar en la consola, si se deja en blanco usamos el normal

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

'''
bad_show = '''

        Las siguientes variables pueden ser consultadas:

            + verbosity: verbosidad del programa, cuanta información mostrar

            + time_crawl: tiempo para realizar crawling en algunos plugins

            + regExs: expresiones regulares que buscar en pastebin

            + emails: emails a buscar dentro de pastebin

            + names: Nombres a buscar dentro de pastebin

            + dnis: documentos de identidad a buscar

            + cadenas: una cadena cualquiera en pastebin

            + urls: las urls ya sacadas de pastebin

            + crawlers: crawlers disponibles
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
    global verbosity,time_to_crawl,regExs,emails,names,dnis,cadenas,prompt

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
                    regExs = [transform_args(command_list[3:])]
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
                    emails = [transform_args(command_list[3:])]
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
                    names = [transform_args(command_list[3:])]
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
                    dnis = [transform_args(command_list[3:])]
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
                    cadenas = [transform_args(command_list[3:])]
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
            #variables = ["verbosity","time_crawl","regExs","emails","names","dnis","cadenas","prompt","pastebin_urls"]
            if variable_to_show == "verbosity":
                print "verbosity="+str(verbosity)

            elif variable_to_show == "time_crawl":
                print "time to crawl="+str(time_to_crawl)

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
                print "\t- twitter_crawler"
                print "\t- pastebin_crawler"

            else:
                print bad_show
                return -1
    except IndexError:
        print "[-] Número de argumentos no valido"
        print bad_show
        return -1


def main():
    '''
        funcion principal que ejecutará la shell
        esta luego mandará los valores
    '''
    
    

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

        if command.strip().startswith("set"):
            try:
                _set_variables(command.strip())
            except Exception as e:
                print "[-] Error en la shell: "+str(e)

        if command.strip().startswith("show"):
            try:
                _show_variables(command.strip())
            except Exception as e:
                print "[-] Error en la shell: "+str(e)

        elif command.strip().startswith("clear"):
            os.system("clear")

        else:
            if command.strip().startswith("help"):
                print total_help
            else:
                print "[-] El comando ejecutado no existe, prueba con help"

        command = str(raw_input(OKBLUE + prompt + ENDC))


if __name__ == '__main__':
    main()