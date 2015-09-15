# ListaTwitter

##Descripción
Una manera rápida de seguir los últimos tweets de un usuario desde la terminal de linux

##Instrucciones
1. Tener python instalado. En linux suele venir ya instalado.
2. Instalar la libreria tweep:
  * `pip install tweepy`
3. Ejecutar en la terminal de linux:
  * `python app.py`
  
Si aparecen errores se deberá seguramente a un problema de librerias de python.
Para ello se deberá probar a instalar estos paquetes:
  * `pip install requests[security]`
  * `apt-get install libffi-dev libssl-dev`
  
##Credenciales
Por razones de seguridad, el fichero credenciales.py no ha sido incluido al repositorio por contener las claves privadas.
Es necesario para poder acceder a la API tener en el mismo directorio que el programa.
Éste deberá de contener las siguentes variables:

a. La consumer key (**ckey**) 

b. El consumer secret (**csecret**) 

c. El access token (**atoken**) 

d. El access secret (**asecret**)

Los valores de dichas variables son dados por [twitter](https://dev.twitter.com) y basta con tener cuenta de twitter para poder solicitarlos.
