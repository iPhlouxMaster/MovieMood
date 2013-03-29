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

#genres = ['Comedy', 'Adventure', 'Action']
 
def mood_it(genres):
	moods = ini_mood_values()
	for val in xrange(len(moods)):
		moods[val][1] = get_total_weight(moods[val][0], genres)
	#moods1 = moods

	highest_weights = []
	max_act = []
	# print moods
	while moods and len(highest_weights) < 3:
		max_act = moods[0]
		print "max_act: " + str(max_act)
		for i in xrange(len(moods)):
			if i+1 < len(moods) and max_act[1] < moods[i+1][1]:
				max_act = moods[i+1]
				# print "max_act: " + str(max_act)
		if max_act[1] != 0:
			highest_weights.append(max_act)
		#for i in highest_weights:
		moods.remove(max_act)

	return highest_weights