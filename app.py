"""
Si el programa no ejecuta probar con (por este orden):
$> pip install tweepy
$> pip install requests[security]
$> apt-get install libffi-dev libssl-dev
"""

import credenciales
import os.path
import tweepy, sys
from tweepy import OAuthHandler

list_usuarios = ["ID_AA_Carmack", "romero"] #Esta es la lista de usuarios a seguir (no son vinculados a tu cuenta de twitter)

def apertura_fichero():
	"""
	Abre/Crea un fichero y devuelve el file descriptor
	"""

	nombre_fichero = ".historial"
	cond_nuevo = False
	if os.path.isfile(nombre_fichero):
		try:
			fichero_timeline = open(nombre_fichero, "r+")
		except:
			print "\nError en acceso al historial"
			sys.exit(-1)
	else:
		try:
			fichero_timeline = open(nombre_fichero, "w")
			cond_nuevo = True
		except:
			print "\nError en creacion de historial"
			sys.exit(-1)
	
	return fichero_timeline, cond_nuevo

def procesado_historial(api, usuario, fichero_timeline, cond_nuevo):
	"""
	En cada linea del historial viene "usuario id_ultimo_tweet_leido"
	Se busca en el fichero la linea de historial que pertenezca al usuario
	Se devuelve la id de ese ultimo tweet leido y un string con "usuario ultimo_tweet"
	Si no se encuentra o el fichero esta vacio, se considera 
	como ultimo tweet leido al ultimo escrito por el usuario
	"""
	usuario_coincide = False

	while not usuario_coincide and not cond_nuevo:
		linea_fichero_historial = fichero_timeline.readline().split()
		if (linea_fichero_historial[0] == usuario):
			usuario_coincide = True
		if (len(linea_fichero_historial) == 0):
			cond_nuevo = True
			usuario_coincide = True

	public_tweets = api.user_timeline(id = usuario, count = 1)
	ultimo_tweet = public_tweets[0].id

	if cond_nuevo:
		ultimo_tweet_leido = ultimo_tweet
		salida = usuario + " " + str(ultimo_tweet) + "\n"
	else:
		ultimo_tweet_leido = int(linea_fichero_historial[1])
		salida = usuario + " " + linea_fichero_historial[1] + "\n"
		
	fichero_timeline.seek(0)
	return ultimo_tweet_leido, salida

def escritura_historial(fichero, lista):
	fichero.truncate()

	for linea in lista:
		try:
			fichero.write(linea)
		except:
			print "\n Error en escritura de historial"
			sys.exit(-1)
	fichero.close()

def listado_tweets(api, list_usuarios):
	fichero_timeline, cond_nuevo = apertura_fichero()
	v_linea = []
	for id_usuario in list_usuarios:
		print "* Tweets de", id_usuario, "sin leer:",
		
		id_historial, linea = procesado_historial(api, id_usuario, fichero_timeline, cond_nuevo)
		v_linea.append(linea)
		public_tweets = api.user_timeline(id = id_usuario, count = 1, since_id = id_historial)
		print len(public_tweets)
		for tweet in public_tweets:
			print tweet.text
	escritura_historial(fichero_timeline, v_linea)
	return		

auth = OAuthHandler(credenciales.ckey, credenciales.csecret)
auth.set_access_token(credenciales.atoken, credenciales.asecret)

api = tweepy.API(auth)
listado_tweets(api, list_usuarios)





