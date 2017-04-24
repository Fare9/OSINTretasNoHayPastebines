# OSINTretasNoHayPastebines

Trabajo de OSINT para la asignatura de seguridad en sistemas distribuidos.
Estos scripts buscarán cadenas y expresiones regulares en páginas de pastebin.
Como pastebin no es muy amigable, y no suele darnos muchos URLs para hacer esto
buscaremos URLs de pastebin en otras fuentes "públicas", por ejemplo:

## osintpastebin
consola para ejecución de comandos de la herramienta, hay comandos para 
establecer variables, mostrarlas, cargar módulos, ejecutarlos y realizar
las búsquedas dentro de pastebin.

archivo: osintpastebin.py

## twitter
dentro de twitter se buscarán cadenas de texto y se irán obteniendo tweets
después estos tweets se analizarán para obtener las URLs de pastebin

archivo crawler: modules/_twitter_crawlera.py

## pastebin
este crawler buscará en ciertas partes de la página de pastebin enlaces,
no da mucho pero bueno menos es nada

archivo crawler: modules/_pastebin_crawlera.py

## BING
futuro crawler para buscar enlaces en bing a través de búsquedas avanzadas.

futuro archivo crawler: modules/_bing_crawlera.py

## Google
futuro crawler para buscar enlaces en google a través de búsquedas avanzadas.

futuro archivo crawler: modules/_google_crawlera.py

### Requerimientos

Python 2.7
geckodriver dentro de la carpeta opt
selenium
bs4
notify2