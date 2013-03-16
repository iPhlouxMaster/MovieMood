import json
import ast
import re
from random import randint
from urllib2 import Request, urlopen
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

def str_to_dict(json):
	json_string = u''+json
	obj = simplejson.loads(json_string)
	return simplejson.dumps(obj)

def ini_mood_values():
	return [["Angry", 0], ["Happy", 0], ["Sad", 0], ["Geeky", 0], ["Weird", 0], ["Relaxed", 0], ["Loved", 0], ["Curious", 0], ["Scared", 0], ["Bored", 0], ["Bleh", 0]]

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
		id = ""

		# Valores default de la pelicula 
		def_adult = "N/A"
		def_backdrop_path = "N/A"
		def_budget = -1
		def_genres = "N/A"
		def_imdb_id = "N/A"
		def_original_title = "N/A"
		def_overview = "N/A"
		def_popularity = "N/A"
		def_poster_path = "N/A"
		def_release_date = "N/A"
		def_revenue = -1
		def_runtime = "N/A"
		def_tagline = "N/A"
		def_vote_average = "N/A"
		def_vote_count = -1
		def_trailers = "N/A"

		headers = {"Accept": "application/json"}
		url = None

		while(url is None):
			id = str(randint(0,88099))
			url = "http://api.themoviedb.org/3/movie/" + id + "?api_key=2dc20cff6915def3a6fc5df0dbf7126c&append_to_response=trailers"
			request = Request(url, headers=headers) 
			try: 
			    json_string = urlopen(request).read()
			    continue
			except Exception:
				url = None
			    #import traceback
			    #checksLogger.error('generic exception: ' + traceback.format_exc())
			"""
			except urllib2.HTTPError, e:
			    checksLogger.error('HTTPError = ' + str(e.code))
			except urllib2.URLError, e:
			    checksLogger.error('URLError = ' + str(e.reason))
			except urllib2.HTTPException, e:
			    checksLogger.error('HTTPException')
			""" 

		"""
		json_obj = json.loads(json_string)
		for key, value in json_obj.items():
			json_obj[key] = str(value)
		json_obj['adult'] = "" + str(json_obj['adult'])
		if json_obj['adult'] == "False":
			json_obj['adult'] = "False"
		json_obj['belongs_to_collection'] = ""
		json_obj = json.dumps(json_string)
		"""
		movie_data = json_string.decode('utf-8')
		movie_data = json.loads(movie_data)
		if 'status_code' not in movie_data and not movie_data['adult'] and 'vote_average' in movie_data and 'genres' in movie_data:
			if float(movie_data['vote_average']) >= 6.5: # Revisa que sea mayor a 6.5 estrellas
				if float(movie_data['vote_average']) >= 8.5: # Si tiene mas de 8.5 estrellas le agregamos el mood bored
					act_moods.append("bored")
				try:
					act_movie_in_db = Movie.objects.get(tmdb_id=movie_data['id'])
				except Movie.DoesNotExist:
					act_movie_in_db = None	
				# all_movies = Movie.objects.all() # Siempre hay que volver a recuperar todas las peliculas para el caso de que se agregue varias veces la misma pelicula en la misma busqueda
				if act_movie_in_db == None:
					genres = [genre['name'] for genre in movie_data['genres']]
					act_moods = mood_it(genres)

					# Revisar que existan todos los valores considerados y si no existe darle un valor default
					if 'backdrop_path' not in movie_data or movie_data['backdrop_path'] == None:
						movie_data['backdrop_path'] = def_backdrop_path
					if 'budget' not in movie_data or movie_data['budget'] == None:
						movie_data['budget'] = def_budget
					if 'imdb_id' not in movie_data or movie_data['imdb_id'] == None:						
						movie_data['imdb_id'] = def_imdb_id
					if 'original_title' not in movie_data or movie_data['original_title'] == None:
						movie_data['original_title'] = def_original_title
					if 'overview' not in movie_data or movie_data['overview'] == None:
						movie_data['overview'] = def_overview
					if 'popularity' not in movie_data or movie_data['popularity'] == None:
						movie_data['popularity'] = def_popularity
					if 'poster_path' not in movie_data or movie_data['poster_path'] == None:
						movie_data['poster_path'] = def_poster_path
					if 'release_date' not in movie_data or movie_data['release_date'] == None:
						movie_data['release_date'] = def_release_date
					if 'revenue' not in movie_data or movie_data['revenue'] == None:						
						movie_data['revenue'] = def_revenue
					if 'runtime' not in movie_data or movie_data['runtime'] == None:
						movie_data['runtime'] = def_runtime
					if 'tagline' not in movie_data or movie_data['tagline'] == None:
						movie_data['tagline'] = def_tagline	
					if 'vote_average' not in movie_data or movie_data['vote_average'] == None:
						movie_data['vote_average'] = def_vote_average
					if 'vote_count' not in movie_data or movie_data['vote_count'] == None:
						movie_data['vote_count'] = def_vote_count
					if 'trailers' not in movie_data or movie_data['trailers'] == None:
						movie_data['trailers'] = def_trailers

					# Agregamos pelicula a bd
					new_movie = Movie(tmdb_id=movie_data['id'], backdrop_path=movie_data['backdrop_path'], budget=movie_data['budget'],
						genres=genres, imdb_id=movie_data['imdb_id'], original_title=movie_data['original_title'], overview=movie_data['overview'],
						popularity=movie_data['popularity'], poster_path=movie_data['poster_path'], release_date=movie_data['release_date'],
						revenue=movie_data['revenue'], runtime=movie_data['runtime'], tagline=movie_data['tagline'], vote_average=movie_data['vote_average'],
						vote_count=movie_data['vote_count'], trailers=movie_data['trailers'])
					new_movie.save()

					# Agregamos los moods de la pelicula CLASIFICACION EN BD
					imdb_id_act = Movie.objects.get(tmdb_id=movie_data['id'])
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

