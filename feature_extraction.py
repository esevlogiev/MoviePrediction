import numpy as np

from db_manager import DBManager
from constants import Constants

class RatingFeatures:
	def __init__(self, movies):
		self.movies = movies
		self.movies_duration = np.asarray([m.duration for m in movies])
		self.movies_dict = {}
		

	def normalize_duration(self, duration, movies_duration):
		return (duration - movies_duration.mean()) / movies_duration.std()

	def normalize(array):
		return (array - array.mean()) / array.std()

	def genres_average(self, genres):
		movies_dict = self.movies_dict
		genres_average = []

		for genre in genres:
			if not movies_dict.get(genre):
				movies_dict[genre] = \
					np.asarray([m.rating for m in DBManager.get_movies_by_genre(genre)]).mean()

			genres_average.append(movies_dict[genre])

		return np.asarray(genres_average).mean()

	def cast_average(self, cast):
		movies_dict = self.movies_dict
		cast_average = []

		for actor in cast:
			if not movies_dict.get(actor):
				movies_dict[actor] = \
					np.asarray([m.rating for m in DBManager.get_movies_by_actor(actor)]).mean()

			cast_average.append(movies_dict[actor])

		return np.asarray(cast_average).mean()

	def get_movies_count(self):
		return len(self.movies)

	def get_ratings(self):
		return np.asarray([[m.rating] for m in self.movies])

	def get_features(self):
		rows_count, columns_count = Constants.features_count, len(self.movies)
		features = [[0 for x in range(columns_count)] for y in range(rows_count)] 
		movies_dict = self.movies_dict

		for movie in self.movies:
			director = movie.director
			mpaa = movie.motion_picture_rating
			genres = movie.genres
			main_cast = movie.cast[:Constants.main_cast_count]

			if not movies_dict.get(director):
				movies_dict[director] = \
					np.asarray([m.rating for m in DBManager.get_movies_by_director(director)]).mean()
			
			if not movies_dict.get(mpaa):
				movies_dict[mpaa] = \
					np.asarray([m.rating for m in DBManager.get_movies_by_mpaa(mpaa)]).mean()
			
			for (feature, value) in zip(features, [movies_dict[director], movies_dict[mpaa], 
				movie.duration, self.genres_average(genres), self.cast_average(main_cast)]):
				feature.append(value)

		(dir, rat, dur, g, c) = [RatingFeatures.normalize(np.asarray(feature)) for feature in features]
		return np.asarray([list(f) for f in zip(dir, rat, dur, g, c)])