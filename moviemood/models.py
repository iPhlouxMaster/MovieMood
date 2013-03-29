from django.db import models

# Create your models here.
class Movie(models.Model):
	id = models.AutoField(primary_key=True)
	backdrop_path = models.CharField(max_length=100)
	budget = models.IntegerField()
	genres = models.CharField(max_length=300)
	tmdb_id = models.IntegerField()
	imdb_id = models.CharField(max_length=15)
	original_title = models.CharField(max_length=200)
	overview = models.CharField(max_length=1000)
	popularity = models.CharField(max_length = 50)
	poster_path = models.CharField(max_length = 150)
	release_date = models.CharField(max_length = 25)
	revenue = models.IntegerField()
	runtime = models.CharField(max_length = 300)
	tagline = models.CharField(max_length = 1000)
	vote_average = models.CharField(max_length = 50)
	vote_count = models.IntegerField()
	trailers = models.CharField(max_length = 800)
 
	def __unicode__(self):
		return self.original_title

	"""
	imdb_id = models.CharField(max_length=10) # String de la forma /^tt\d+$/
	runtime = models.CharField(max_length=500)
	rating = models.CharField(max_length=20)	# Float entre 0.0 y 10.0
	genres = models.CharField(max_length=200) # Lista de generos
	rated = models.CharField(max_length=5) # Categoria de pelicula ej. 'R' = Restringida
	language = models.CharField(max_length=200) # Lista de idiomas de la pelicula
	title = models.CharField(max_length=150) # Nombre de la pelicula
	poster = models.CharField(max_length=200)
	imdb_url = models.CharField(max_length=200)
	directors = models.CharField(max_length=200)
	rating_count = models.IntegerField() # Numero de personas que han rateado la pelicula
	actors = models.CharField(max_length=800)
	plot = models.CharField(max_length=800)
	year = models.IntegerField()
	country = models.CharField(max_length=100)
	release_date = models.CharField(max_length=8)
	aka = models.CharField(max_length=150) # Also Known As
	"""


class Mood(models.Model):
	id = models.AutoField(primary_key=True)
	mood = models.CharField(max_length=40)

	def __unicode__(self):
		return self.mood

class Movie_Mood(models.Model):
	id = models.AutoField(primary_key=True)
	movie_id = models.ForeignKey(Movie)
	mood_id = models.ForeignKey(Mood)

