PYMETRICK
=========
Pymetrick version 0.53.0

Mini marco de desarrollo web basado en Python 3.6+ ( TODO EN UNO ), al disponer de todos los módulos necesarios para cualquier desarrollo web (templates, session/cookies, routing de solicitudes, gestión MySQL y SQLite, rst - reStructuredText, identificación de conexiones, tratamiento de imagenes, tratamiento de correos,...etc) permite prescindir de librerias ajenas a las librerías estándar de PYTHON, aunque el uso de librerías externas no se excluye completamente.

No dispone de un servidor de aplicaciones. Por lo que los desarrollos realizados, deberán configurarse con mod_wsgi si se ejecutan en el servidor Apache 2 o bien adaptarlos a otros servidores de aplicaciones disponibles ( CherryPy, Tornado, waitress,... ).

Se aceptan contribuciones de codigo que permitan la adaptación a desarrollos empresariales, con igual licencia que PYMETRICK.


INDICE DE MODULOS
-----------------

- TEMPLATE o cómo interpretar plantillas .tpl y transformarlas en HTML5
- DEVICE o cómo identificar accesos con dispositivos, navegadores, motores e idiomas.
- ROUTING o cómo manipular direcciones HTTP a funciones ( controller )
- IMAGE o cómo gestionar imagenes
- SQLDB y DB_SQLITE o cómo gestionar BB.DD.
- SESSION o como identificar usuarios y seguridad de acceso
- MAIL tratamiento de correo
- EXCHEQUER tratamiento fiscal e identificación (NIF/CIF/NIE/VAT)
- HELPERS o gestión de utilidades universales de uso común
- RST o reStructuredText gestiona el formato de textos convirtiendolo en html
- COMMON o dónde identificar valores universales
- FPDF generación de documentos PDF
- FIRESTORE acceso a GOOGLE FIRESTORE


TEMPLATE
--------

Realiza la gestión de plantillas ( con extensión .tpl ), generando código HTML5. Similar a JINJA2 pero mucho más simple.

A continuación se identifica código para realizar plantillas :

<% ..... %>    
Se puede introducir cualquier tipo de información, si los datos se separan con el carácter | se enviará como una lista de elementos o si además, los elementos están separados por clave valor con = se enviará un diccionario. La información enviada entre estas etiquetas, se procesará en función del primer elemento. Si no pudiera ser procesado por el primer elemento, se incluirá igual que si se hubiera incluído entre etiquetas {%literal%} {%endliteral%}.
Por ejemplo, para incluir en el bloque \<head\>

             <%title|Prueba Html5%>
             <%author|Fco.Javier Tamarit%>
             <%description|Prueba Html5%>
             <%script|../../web/js/jquery.min.js||text/javascript%>
             <%script|../../web/js/jquery-ui.min.js||text/javascript%>

o para incluir en el bloque \<body\>

             <%type="hidden"|id="sessionID"|value=""%>
             <%type="number"|id="numero"|label="Numero"|placeholder="Introduzca numero"|br=""%>
             <%type="tel"|id="telefono"|label="Telefono"|placeholder="Introduzca telefono"|br=""%>
             <%type="submit"|id="s"|value="Acceso"|size=10%>
             <%type="submit"|id="r"|value="Registrarse"%>

{% ..... %}    
Separa la información por bloques, el inicio de bloque se nombrará como {%block body%} y el final como {%endblock body%}. Esto creará una etiqueta \<body\> y al finalizar, otra etiqueta \</body\>. Los bloques permitidos son html, head, body, footer, article, section, aside, form, header, hgroup, table, nav.
Algunos bloques pueden incluir información en su etiqueta inicial como :

             {%block html|lang="es"%}
             {%block body|onload="MideScreen()"%}
             {%block form|id="Login",method="POST",action="/input"%}

Observe que los parámetros estan separados de la etiqueta mediante |

Los bloques iniciados y no cerrados, se cerrarán de forma automática al finalizar el proceso de la plantilla.

{%literal%} .....  {%endliteral%}
La información incluida entre estas dos etiquetas, no tendrá ninguna tranformación, se incluirá exactamente como se haya introducido.

             {%literal%}
             script type="text/javascript">  
                 document.createElement("nav"); 
                 document.createElement("header"); 
                 document.createElement("footer"); 
                 document.createElement("section"); 
                 document.createElement("article"); 
                 document.createElement("aside"); 
                 document.createElement("hgroup");
             </script
             {%endliteral%}



<--!  .....  -->  
La información contenida entre estas dos etiquetas, se entenderá que corresponde a un comentario y no se procesará en el código resultado.

{%extend fichero_template.tpl%}
La etiqueta {%extend se empleará para incluir un fichero con formato de plantilla en la plantilla que se está procesando. De forma que no se repita el mismo código en todas las plantillas y pueda unificarse en un solo fichero de plantilla externo. El nombre de fichero no puede contener espacios.

{%merge fichero_externo.txt%}
La etiqueta {%merge también importa un fichero externo, pero su contenido no será procesado y se incluirá tal cual se importe. El nombre de fichero no puede contener espacios.


{{  .....  }}  
Los datos incluídos entre doble llave, se consideran variables o funciones a procesar, que igualmente deben devolver un valor.
             
DEVICE
------

A partir del 'user-agent' proporcionado por el cliente, es posible identificar : S.O., navegador, motor, idiomas admitidos, dispositivo origen y adaptar la respuesta.

ROUTING
-------

Con su ayuda, se construyen las reglas de actuación ante las posibles solicitudes de los clientes, permitiendo respuestas flexibles en función de parámetros dinámicos.

Importar routing:

from pymetrick.routing import *

Primero debe crear una ruta al subdominio de la siguiente forma :

        rules_web = Map(default_subdomain='www',redirect_defaults='/')

        Las rutas a páginas se crean de la siguiente forma :

        rules_web.add(rule='/login',controller='login')
        rules_web.add(rule='/login/nada',controller='login')
        rules_web.add(rule='/login/nada/todo',controller='login')
        rules_web.add(rule='/registro',controller='registro')
        rules_web.add(rule='/prueba',controller='prueba')

        Ahora, cuando busque una ruta debe indicarlo como :

        rules_web.match('login')
        rules_web.match('/login/nada/todo')
        rules_web.match('/varios')

        esto ejecutara el controlador parametrizado.

        Si la ruta obtenida del cliente, contiene datos del tipo
        '/auth?user=javier&passw=tonto'
        se eliminaran para evaluar correctamente la ruta

        Y si no existe la ruta, devolvera 404 y podremos redirigirlo
        if rules_web.match('/no_existe')=="404":
           rules_web.match('/')
        ''')

IMAGE
-----

Este módulo permite la adaptación o manipulación de las imágenes a cualquier necesidad, desde el peso de las imágenes hasta su formato.

Importar Image:

from pymetrick.image import *

Utilidades con imagenes :
        image_size(__path__) Comprueba las dimensiones de la imagen.

        image_resize(__path__,__factor__=1,__resized_path__='') Convierte fichero de imagen a un tamaño diferente, ademas es posible cambiar el tipo de imagen de png, jpeg o gif a otro cuando se renombra el fichero de imagen resultante.

        strip_metadata(image_path,newImage=None) Elimina los metadatos EXIF de una imagen, guardando en el mismo nombre de imagen o bien en otra imagen nueva.

        image2html('logo.png') Devuelve una imagen en base64 como un string de forma que se pueda utilizar como imagen embebida en css o html.

        image2base64('logo.png') Devuelve una imagen en base64 extendido  ( file_name$string_base64).

        image_download('http://nadadenada.com/coche.png', '/img/coche_2.png') Descarga una imagen desde una url con <urllib> y permite renombrar el fichero.

        image_checksums('logo.png') Devuelve un hash como un string que identifica la imagen para ser comparada con otras imagenes.

        image_compare(file1,file2) Devuelve 0 si las imagenes comparadas son iguales, en caso contrario devolvera un valor distinto de 0.
        
        image_qrcode('/home/content.png'logo.png') Devuelve datos/informacion en formato qrcode como imagen png

SQLDB 
--------

Gestión de la conexión con BB.DD. como MySQL (MYSQL.CONNECTOR), PostgreSQL (PSYCOPG2) y SQLite.

Incluye funciones dirigidas a conexión, reconexión, así como la creación, modificación, eliminación y utilidades de BB.DD.,tablas, indices,...

SESSION
-------

Identifica las conexiones de clientes mediante JSON WEB TOKENS stateless authentication, que se intercambian entre el 
servidor WEB y el cliente a través de :
                HTTP_COOKIE
                HTTP_X_AUTHORIZATION or X_REQUEST_WITH
                HTTP_HOST
                HTTP_CLIENT_IP o HTTP_X_FORWARDED_FOR o REMOTE_ADDR

Incorpora también funciones de encriptación y generación de passwords

MAIL
-----

Con el módulo MAIL se gestiona el correo electrónico. Condición necesaria es disponer de un servidor SMTP y POP3 o IMAP

Parámetros necesarios :  

    sendMail()        Enviar mail e incorporar ficheros adjuntos si fuera necesario
        _sender       - str  -  enviado desde
        _to           - list -  enviar a
        _cc           - list -  enviar copias
        _bcc          - list -  enviar copias ocultas
        _subject      - str  -  asunto
        _text         - str  -  text/plain del mensaje
        _html         - str  -  text/html  del mensaje
        _user         - str  -  usuario
        _password     - str  -  password
        _smtpserver   - str  -  servidor
        _port         - str  -  puerto
        _files        - list -  ficheros adjuntos
        _output       - str  -  el contenido del mensaje se grabara como un fichero

    getMail()         Recepción de mail desde POP3|IMAP
        _user         - str  -  usuario
        _password     - str  -  password
        _imapserver   - str  -  servidor IMAP
        _pop3server   - str  -  servidor POP3
        _port         - str  -  puerto
        _criteria     - str  -   
                        ALL - devuelve todos los mensajes que coinciden con el resto del criterio
                        ANSWERED - coincide con los mensajes con la bandera \\ANSWERED establecida
                        BCC "cadena" - coincide con los mensajes con "cadena" en el campo Bcc:
                        BEFORE "fecha" - coincide con los mensajes con Date: antes de "fecha"
                        BODY "cadena" - coincide con los mensajes con "cadena" en el cuerpo del mensaje
                        CC "cadena" - coincide con los mensajes con "cadena" en el campo Cc:
                        DELETED - coincide con los mensajes borrados
                        FLAGGED - coincide con los mensajes con la bandera \\FLAGGED establecida (algunas veces referidos como Importante o Urgente)
                        FROM "cadena" - coincide con los mensajes con "cadena" en el campo From:
                        KEYWORD "cadena" - coincide con los mensajes con "cadena" como palabra clave
                        NEW - coincide con los mensajes nuevos
                        OLD - coincide con los mensajes antiguos
                        ON "fecha" - coincide con los mensajes con Date: coincidiendo con "fecha"
                        RECENT - coincide con los mensajes con la bandera \\RECENT establecida
                        SEEN - coincide con los mensajes que han sido leídos (la bandera \\SEEN esta estabecido)
                        SINCE "fecha" - coincide con los mensajes con Date: despues de "fecha"
                        SUBJECT "cadena" - coincide con los mensajes con "cadena" en Subject:
                        TEXT "cadena" - coincide con los mensajes con el texto "cadena"
                        TO "cadena" - coincide con los mensajes con "cadena" en To:
                        UNANSWERED - coincide con los mensajes que no han sido respondidos
                        UNDELETED - coincide con los mensajes que no están eliminados
                        UNFLAGGED - coincide con los mensajes que no tienen bandera
                        UNKEYWORD "cadena" - coincide con los mensajes que no tienen la palabra clave "cadena"
                        UNSEEN - coincide con los mensajes que aun no han sido leidos
        _outputdir    - str  -

    deleteIMAP()      Eliminar mail de servidor IMAP
        _user         - str  -  usuario
        _password     - str  -  password
        _imapserver   - str  -  servidor IMAP
        _port         - str  -  puerto
        _folder       - str  -  carpeta a tratar

    timeZone(zona)

EXCHEQUER
---------

Con el módulo EXCHEQUER pueden introducirse datos identificativos fiscales en las transacciones comerciales, así como validar
las identificaciones aportadas según reglas de cada país.

HELPERS
-------

Se admiten todas las clases o funciones que por su funcionalidad, puedan compartirse entre los restantes módulos o no tengan un fín funcional asociado a los restantes módulos.

             
RST o reStructuredText
----------------------

A partir de ficheros con extension .rst y codificados como un reStructuredText se obtienen ficheros HTML5 completos o HTML5 parciales que completarán otros ficheros HTML5 principales.


COMMON
------

Proporciona listas de valores universales para todos los módulos.

FPDF
------

Producción de documentos en formato PDF. Este módulo es una actualización del original FPDF versión 1.7.1 en el que se han incluído EAN13, UPC_A y funciones auxiliares para producir 
códigos de barras no incluídos en la versión previa. 

FIRESTORE
---------

Incorpora un nuevo módulo dirigido a realizar la operativa con la base de datos GOOGLE FIRESTORE: DATABASE y STORAGE. Esto permite realizar autenticación, disponer de una base
de datos NO SQL y ficheros para entornos sin recursos backend o dirigidos a dispositivos móviles.

VERSIONES
---------

Las versiones estables se indicarán con número de versión par. Las versiones en desarrollo y que incorporen características experimentales se numerarán con versión impar.


Ver 0.01     21/09/2012  Licencia GPLv3  - en desarrollo -
    Las pruebas de desarrollo se realizan sobre un ordenador RASPBERRY PI  512Mb RAM, 1 GHz CPU y tarjeta SD de 64Gb con una evolución satisfactoria. El objetivo es desarrollar una librería simple y funcional.
    El entorno hardware de desarrollo se complementa con un servidor MySQL 5 y servidor web APACHE 2 con mod_wsgi.

Ver 0.02     20/08/2015  Licencia GPLv3  - versión estable -

Ver 0.48.4   15/12/2018  Licencia GPLv3  - versión estable -

Ver 0.50.0   31/10/2019  Licencia GPLv3  - versión estable -

Ver 0.52.0   09/05/2020  Licencia GPLv3  - versión estable -    

CREDITOS O COLABORACIONES
-------------------------

Cualquier desarrollo que se incorpore a un módulo o la introducción de nuevos desarrollos deben ser aprobados antes de formar parte de la libreria, debiendo respetar la licencia GPLv3. El reconocimiento de los desarrolladores que colaboren a mejorar la librería se incorporará en la cabecera 'CREDITS' de los módulos afectados por sus desarrollos.
