# OSINTretasNoHayPastebines

Trabajo de OSINT para la asignatura de seguridad en sistemas distribuidos.
Estos scripts buscarán cadenas y expresiones regulares en páginas de pastebin.
Como pastebin no es muy amigable, y no suele darnos muchos URLs para hacer esto
buscaremos URLs de pastebin en otras fuentes "públicas", por ejemplo:

## twitter
dentro de twitter se buscarán cadenas de texto y se irán obteniendo tweets
después estos tweets se analizarán para obtener las URLs de pastebin

archivo crawler: modules/twitter_crawlera.py

## pastebin
es verdad que no vale para mucho, pero intentaremos tirar de su API y de la 
navegación en sus propios enlaces de pastebin, ya veremos a ver que tal.

## Ideas
pueden darme ideas, las que sea, para eso estamos....
