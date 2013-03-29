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
from moviemood.search import mood_it
from moviemood.funcs import *

M = 2 # Numero de peliculas a desplegar
N = 1 # Numero de peliculas a buscar en la base de datos

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
			movies_to_display = parse_items(movies_to_display)
			#trailers_dict = ast.literal_eval(movies_to_display['trailers'])
			#if trailers_dict['youtube'] != []:
			#	trailer = trailers_dict['youtube'][0]['source']
			#else:
			#	trailer = "N/A"
			return render_to_response('results.html', {
			'movies_to_display' : movies_to_display,
			#'trailer': trailer,
			}, context_instance=RequestContext(request))
			# return HttpResponseRedirect('search_results/') # Redirect after POST
	else:
		form = SearchForm() # An unbound form

	return render(request, 'results.html', {
		'page' : page,
		'form': form,
	}, context_instance=RequestContext(request))

def search_movies(mood):
	movies_to_display = []
	actual_movies = len(movies_to_display)
	# url = ""
	while actual_movies < M:
		act_moods = []
		id = ""

		headers = {"Accept": "application/json"}
		url = None

		while(url is None):
			id = str(randint(0,88099))
			url = "http://api.themoviedb.org/3/movie/" + id + "?api_key=2dc20cff6915def3a6fc5df0dbf7126c&append_to_response=trailers"
			request = Request(url, headers=headers) 
			print "ciclo"
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

		movie_data = json_string.decode('utf-8')
		movie_data = json.loads(movie_data)
		if not movie_data['adult'] and 'vote_average' in movie_data and 'genres' in movie_data:
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
					exists_value('backdrop_path', movie_data)
					exists_value('budget', movie_data)
					exists_value('imdb_id', movie_data)
					exists_value('original_title', movie_data)
					exists_value('overview', movie_data)
					exists_value('popularity', movie_data)
					exists_value('poster_path', movie_data)
					exists_value('release_date', movie_data)
					exists_value('revenue', movie_data)
					exists_value('runtime', movie_data)
					exists_value('tagline', movie_data)
					exists_value('vote_average', movie_data)
					exists_value('vote_count', movie_data)
					exists_value('trailers', movie_data)

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

