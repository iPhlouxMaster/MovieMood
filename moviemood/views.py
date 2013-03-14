import json
import ast
from random import randint
from urllib2 import urlopen
from django.utils import simplejson 
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext, Context

from moviemood.models import Movie, Mood, Movie_Mood
from moviemood.forms import SearchForm

M = 2 # Numero de peliculas a desplegar
N = 1 # Numero de peliculas a buscar en la base de datos

"""
angry_act = 0
happy_act = 0
sad_act = 0
geeky_act = 0
weird_act = 0
relaxed_act = 0
loved_act = 0
curious_act = 0
bored_act = 0
bleh_act = 0
"""

# Moods with genres and weights
moods = [["Angry", 0], ["Happy", 0], ["Sad", 0], ["Geeky", 0], ["Weird", 0], ["Relaxed", 0], ["Loved", 0], ["Curious", 0], ["Scared", 0], ["Bored", 0], ["Bleh", 0]]

angry = {"War":3, "Action":2, "Crime":1}
happy = {"Comedy":3, "Animation":2, "Family":1, "Fantasy":1, "Adventure":1}
sad = {"Drama":3, "Horror":2}
geeky = {"Documentary":3, "Biography":2, "History":1}
weird = {"Scifi":3, "Fantasy":2}
relaxed = {"Adventure":3, "Scifi":2, "Comedy":1}
loved = {"Romance":3, "Musical":2, "Comedy":1}
curious = {"Mystery":3, "Thriller":2, "Crime":1, "Documentary":1, "Horror":1}
scared = {"Horror":3, "Thriller":2, "Mystery":1}


# bored = {} # Cualquier pelicula con mas de 8.5 estrellas
# bleh = {} # Cualquier pelicula

def index(request):
	page = "index"

	return render_to_response('index.html', {
		'page' : page
		}, context_instance=RequestContext(request))

def search_results(request):
	page = "results"
	if request.method == 'POST': # If the form has been submitted...
		form = SearchForm(request.POST) # A form bound to the POST data
		if form.is_valid(): 
			mood = form.cleaned_data['mood']
			movies_to_display = search_movies(mood)
			return render_to_response('results.html', {
			'movies_to_display' : movies_to_display,
			}, context_instance=RequestContext(request))
			# return HttpResponseRedirect('search_results/') # Redirect after POST
	else:
		form = SearchForm() # An unbound form

	return render(request, 'results.html', {
		'page' : page,
		'form': form,
	}, context_instance=RequestContext(request))
	"""
	mood = request.POST.get('search_query','')
	movies_to_display = search_movies(mood)
	return render_to_response('results.html', {
		'movies_to_display' : movies_to_display,
		}, context_instance=RequestContext(request))
	"""

def str_to_dict(json):
	json_string = u''+json
	obj = simplejson.loads(json_string)
	return simplejson.dumps(obj)

def ini_mood_values():
	return [["Angry", 0], ["Happy", 0], ["Sad", 0], ["Geeky", 0], ["Weird", 0], ["Relaxed", 0], ["Loved", 0], ["Curious", 0], ["Scared", 0], ["Bored", 0], ["Bleh", 0]]
	"""
	angry_act = 0
	happy_act = 0
	sad_act = 0
	geeky_act = 0
	weird_act = 0
	relaxed_act = 0
	loved_act = 0
	curious_act = 0
	bored_act = 0
	bleh_act = 0
	"""

def get_total_weight(mood, genres):
	weight = 0
	if mood == "Angry":
		for genre in genres:
			if genre in angry:
				weight += angry[genre]
		return weight
	elif mood == "Happy":
		for genre in genres:
			if genre in happy:
				weight += happy[genre]
		return weight
	elif mood == "Sad":
		for genre in genres:
			if genre in sad:
				weight += sad[genre]
		return weight
	elif mood == "Geeky":
		for genre in genres:
			if genre in geeky:
				weight += geeky[genre]
		return weight
	elif mood == "Weird":
		for genre in genres:
			if genre in weird:
				weight += weird[genre]
		return weight
	elif mood == "Relaxed":
		for genre in genres:
			if genre in relaxed:
				weight += relaxed[genre]
		return weight
	elif mood == "Loved":
		for genre in genres:
			if genre in loved:
				weight += loved[genre]
		return weight
	elif mood == "Curious":
		for genre in genres:
			if genre in curious:
				weight += curious[genre]
		return weight
	elif mood == "Scared":
		for genre in genres:
			if genre in scared:
				weight += scared[genre]
		return weight		
	elif mood == "Bleh":
		weight = 10
		return weight
	return weight

def mood_it(genres):
	moods = ini_mood_values()
	moods[0][1] = get_total_weight(moods[0][0], genres)
	moods[1][1] = get_total_weight(moods[1][0], genres)
	moods[2][1] = get_total_weight(moods[2][0], genres)
	moods[3][1] = get_total_weight(moods[3][0], genres)
	moods[4][1] = get_total_weight(moods[4][0], genres)
	moods[5][1] = get_total_weight(moods[5][0], genres)
	moods[6][1] = get_total_weight(moods[6][0], genres)
	moods[7][1] = get_total_weight(moods[7][0], genres)
	moods[8][1] = get_total_weight(moods[8][0], genres)
	moods[9][1] = get_total_weight(moods[9][0], genres)
	moods[10][1] = get_total_weight(moods[10][0], genres)

	#moods1 = moods

	highest_weights = []
	max_act = []
	while len(highest_weights) < 3:
		max_act = moods[0]
		for i in xrange(len(moods)):
			if i < len(moods) and max_act[1] < moods[i][1]:
				max_act = moods[i]
		highest_weights.append(max_act)
		#for i in highest_weights:
		moods.remove(max_act)

	return highest_weights 		

def search_movies(mood):
	movies_to_display = []
	actual_movies = len(movies_to_display)
	url = ""
	while actual_movies < M:
		act_moods = []
		bored_movie = []
		id = ""

		# Valores default de la pelicula 
		def_runtime = "na"
		def_rating = "na"
		def_genres = "na"
		def_rated = "na"
		def_language = "na"
		def_title = "na"
		def_poster = "na"
		def_imdb_url = "na"
		def_directors = "na"
		def_rating_count = -1
		def_actors = "na"
		def_plot = "na"
		def_year = -1
		def_country = "na"
		def_release_date = "na"
		def_aka = "na"

		id += str(randint(0,2)) + str(randint(0,8))
		for i in xrange(5):
			id += str(randint(0,9))
		url = "http://imdbapi.org/?id=tt" + id
		json_string = urlopen(url).read()
		movie_data = u'' + json_string
		movie_data = ast.literal_eval(movie_data)
		if 'code' not in movie_data and 'rating' in movie_data and 'genres' in movie_data:
			if float(movie_data['rating']) >= 6.5: # Revisa que sea mayor a 6.5 estrellas
				if float(movie_data['rating']) >= 8.5: # Si tiene mas de 8.5 estrellas le agregamos el mood bored
					bored_movie.append("bored")
					act_moods.append(bored_movie)
				try:
					act_movie_in_db = Movie.objects.get(imdb_id=movie_data['imdb_id'])
				except Movie.DoesNotExist:
					act_movie_in_db = None	
				# all_movies = Movie.objects.all() # Siempre hay que volver a recuperar todas las peliculas para el caso de que se agregue varias veces la misma pelicula en la misma busqueda
				if act_movie_in_db == None:
					genres = movie_data['genres']
					#genres = u'' + movie_data['genres']
					# genres = ast.literal_eval(genres)
					act_moods = mood_it(genres)

					# Revisar que existan todos los valores considerados y si no existe darle un valor default
					if 'runtime' not in movie_data:
						movie_data['runtime'] = def_runtime
					if 'rating' not in movie_data:
						movie_data['rating'] = def_rating
					if 'genres' not in movie_data:
						movie_data['genres'] = def_genres
					if 'rated' not in movie_data:						
						movie_data['rated'] = def_rated
					if 'language' not in movie_data:
						movie_data['language'] = def_language
					if 'title' not in movie_data:
						movie_data['title'] = def_title
					if 'poster' not in movie_data:
						movie_data['poster'] = def_poster
					if 'imdb_url' not in movie_data:
						movie_data['imdb_url'] = def_imdb_url
					if 'directors' not in movie_data:
						movie_data['directors'] = def_directors
					if 'rating_count' not in movie_data:						
						movie_data['rating_count'] = def_rating_count
					if 'actors' not in movie_data:
						movie_data['actors'] = def_actors
					if 'plot_simple' not in movie_data:
						movie_data['plot_simple'] = def_plot	
					if 'year' not in movie_data:
						movie_data['year'] = def_year	
					if 'country' not in movie_data:
						movie_data['country'] = def_country
					if 'release_date' not in movie_data:
						movie_data['release_date'] = def_release_date	
					if 'also_known_as' not in movie_data:
						movie_data['also_known_as'] = def_aka																							


					# Agregamos pelicula a bd
					new_movie = Movie(imdb_id=movie_data['imdb_id'], runtime=movie_data['runtime'], rating=movie_data['rating'],
						genres=movie_data['genres'], rated=movie_data['rated'], language=movie_data['language'], title=movie_data['title'],
						poster=movie_data['poster'], imdb_url=movie_data['imdb_url'], directors=movie_data['directors'],
						rating_count=movie_data['rating_count'], actors=movie_data['actors'], plot=movie_data['plot_simple'], year=movie_data['year'],
						country=movie_data['country'], release_date=movie_data['release_date'], aka=movie_data['also_known_as'])
					new_movie.save()

					# Agregamos los moods de la pelicula CLASIFICACION EN BD
					imdb_id_act = Movie.objects.get(imdb_id=movie_data['imdb_id'])
					for act_mood in act_moods:
						mood_act = Mood.objects.get(mood=act_mood[0])
						movie_mood = Movie_Mood()
						movie_mood.movie_id = imdb_id_act
						movie_mood.mood_id = mood_act
						movie_mood.save()

					# Si una de las clasificaciones es igual al mood solicitado se guarda para desplegar
					mood = mood.lower()
					if any(mood == val[0].lower() for val in act_moods):
						movies_to_display.append(imdb_id_act)
						actual_movies += 1
	return movies_to_display

