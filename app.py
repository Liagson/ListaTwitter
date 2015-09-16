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

def historial(api, usuario):
	"""
	Primero se lee la id del ultimo tweet que fue registrado en el historial
	La id de este tweet sera devuelta por esta funcion para hacer una busqueda de tweets posteriores
	Se sobreescribe por el ultimo tweet leido en el momento de ejecutar este programa
	"""
	nombre_fichero = ".historial"
	ultimo_tweet_leido = 0

	if os.path.isfile(nombre_fichero):
		try:
			fichero_timeline = open(nombre_fichero, "r+")
		except:
			print "\nError en acceso al historial"
			sys.exit(-1)
		try:
			ultimo_tweet_leido = fichero_timeline.readline()

			fichero_timeline.seek(0)
			fichero_timeline.truncate()
		except:
			print "\nError en lectura de historial"
			sys.exit(-1)
	else:
		try:
			fichero_timeline = open(nombre_fichero, "w")
		except:
			print "\nError en creacion de historial"
			sys.exit(-1)

	public_tweets = api.user_timeline(id = usuario, count = 1)
	ultimo_tweet = public_tweets[0].id
	fichero_timeline.write(str(ultimo_tweet))
	
	fichero_timeline.close()			

	if (ultimo_tweet_leido == 0): 
		return ultimo_tweet
	else: 
		return ultimo_tweet_leido

	def listado_tweets(api, list_usuarios):
		for id_usuario in list_usuarios:
			print "Tweets de", id_usuario, "sin leer:",
			
			id_historial = historial(api, id_usuario)
			if (id_historial != -1):
				public_tweets = api.user_timeline(id = id_usuario, count = 1, since_id = id_historial)
				print len(public_tweets)
				for tweet in public_tweets:
					print tweet.text
		return		

auth = OAuthHandler(credenciales.ckey, credenciales.csecret)
auth.set_access_token(credenciales.atoken, credenciales.asecret)

api = tweepy.API(auth)
list_usuarios = ["ID_AA_Carmack", "romero"]

listado_tweets(api, list_usuarios)





