import ast
import datetime
from django.utils import simplejson
from django.conf import settings

from moviemood.models import *

def set_cookie(response, key, value, days_expire = 7):
	if days_expire is None:
		max_age = 365 * 24 * 60 * 60  #one year
	else:
		max_age = days_expire * 24 * 60 * 60 
	expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
	response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

def str_to_dict(json):
	json_string = u''+json
	obj = simplejson.loads(json_string)
	return simplejson.dumps(obj)

def exists_value(value, movie_data):
	# Valores default de la pelicula 
	def_str = "N/A"
	def_int = -1
	numeric_values = ['budget', 'revenue', 'vote_count']

	if value not in numeric_values:
		if value not in movie_data or movie_data[value] == None:
							movie_data[value] = def_str
	else: 
		if value not in movie_data or movie_data[value] == None:
							movie_data[value] = def_int

def parse_items(movies):
	for movie in movies:
		movie.genres = ast.literal_eval(str(movie.genres))
		if movie.release_date != "N/A":
			movie.release_date = int(movie.release_date.split('-')[0])
		trailers = ast.literal_eval(str(movie.trailers))['youtube']
		movie.trailers = [trailer['source'] for trailer in trailers]
	return movies

def parse_item(movie):
	movie.genres = ast.literal_eval(str(movie.genres))
	if movie.release_date != "N/A":
		movie.release_date = int(movie.release_date.split('-')[0])
	trailers = ast.literal_eval(str(movie.trailers))['youtube']
	movie.trailers = [trailer['source'] for trailer in trailers]
	return movie

#Clasifica las peliculas en la bd que sean 'Bored' (Con criterio de 8.5 estrellas hacia arriba)
def classify_bored():
	count = 0
	try:
		movies = Movie.objects.all()
		for movie in movies:
			if movie.vote_average != "N/A" and float(movie.vote_average) >= 8.5:
				count += 1
				mood_act = Mood.objects.get(mood="Bored")
				movie_mood = Movie_Mood()
				movie_mood.movie_id = movie
				movie_mood.mood_id = mood_act
				movie_mood.save()
	except Movie.DoesNotExist:
		raise Http404
	return count