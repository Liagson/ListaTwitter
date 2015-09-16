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
	Primero se lee la id del ultimo tweet que fue registrado en el historial
	La id de este tweet sera devuelta por esta funcion para hacer una busqueda de tweets posteriores
	Se sobreescribe por el ultimo tweet leido en el momento de ejecutar este programa
	"""
	usuario_coincide = False

	while not usuario_coincide and not cond_nuevo:
		linea_fichero_historial = fichero_timeline.readline().split()
		if (linea_fichero_historial[0] == usuario):
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
		fichero.write(linea)

	fichero.close()

def listado_tweets(api, list_usuarios):
	fichero_timeline, cond_nuevo = apertura_fichero()
	v_linea = []
	for id_usuario in list_usuarios:
		print "Tweets de", id_usuario, "sin leer:",
		
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
list_usuarios = ["ID_AA_Carmack", "romero"]

listado_tweets(api, list_usuarios)





