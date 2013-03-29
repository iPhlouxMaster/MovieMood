import ast
from django.utils import simplejson

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
		movie.release_date = int(movie.release_date.split('-')[0])
		trailers = ast.literal_eval(str(movie.trailers))['youtube']
		movie.trailers = [trailer['source'] for trailer in trailers]
	return movies