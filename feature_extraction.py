import numpy as np

from db_manager import DBManager
from constants import Constants

class RatingFeatures:
	def __init__(self, movies):
		self.movies = movies
		self.movies_duration = np.asarray([m.duration for m in movies])
		self.movies_dict = {}

	def average_youtube_likes(self):
		movies_with_likes = np.asarray([m.you_tube_trailer_info.likeCount for m in self.movies if m.you_tube_trailer_info])
		movies_with_dislikes = np.asarray([m.you_tube_trailer_info.dislikeCount for m in self.movies if m.you_tube_trailer_info])

		return [movies_with_likes.mean(), movies_with_dislikes.mean()]

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
					np.asarray([m.rating for m in [m for m in self.movies if genre in m.genres]]).mean()

			genres_average.append(movies_dict[genre])

		return np.asarray(genres_average).mean()

	def cast_average(self, cast, totalAverage):
		movies_dict = self.movies_dict
		cast_average = []

		for actor in cast:
			if not movies_dict.get(actor):
				movies_dict[actor] = \
					np.asarray([m.rating for m in [m for m in self.movies if actor in m.cast]]).mean()

			cast_average.append(movies_dict[actor])

		return np.asarray(cast_average).mean() if totalAverage else cast_average

	def get_movies_count(self):
		return len(self.movies)

	def get_ratings(self):
		return np.asarray([[m.rating] for m in self.movies])

	def normalize_all_features(self, features):
		mean_std_values = [[f.mean(), f.std()] for f in np.asarray(features).transpose()]
		normalized_features = []

		for feature in features:
			normalized_features.append([ (feature[i] - mean_std_values[i][0]) / mean_std_values[i][1] \
				for i in range(0, len(feature)) ])

		return normalized_features

	def get_features(self, to_normalize = False, total_cast_average = False):
		features = []
		movies_dict = self.movies_dict

		for movie in self.movies:
			director = movie.director
			mpaa = movie.motion_picture_rating
			genres = movie.genres
			main_cast = movie.cast[:Constants.main_cast_count]

			if not movies_dict.get(director):
				movies_dict[director] = \
					np.asarray([m.rating for m in [m for m in self.movies if m.director == director]]).mean()
			
			if not movies_dict.get(mpaa):
				movies_dict[mpaa] = \
					np.asarray([m.rating for m in [m for m in self.movies if m.motion_picture_rating == mpaa]]).mean()

			features.append([movies_dict[director], movies_dict[mpaa],self.genres_average(genres)] + \
				self.cast_average(main_cast, total_cast_average))

		return self.normalize_all_features(features) if to_normalize else features