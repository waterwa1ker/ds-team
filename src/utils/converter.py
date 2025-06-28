from sys import path
from utils.utils import calculate_duration

path.append("..")

class Converter:

	def __init__(self):
		pass

	def convert_to_directors(self, movies_info):

		directors = {}

		for _, director_name_list in movies_info.items():
			director_name = director_name_list[0]
			if director_name in directors:
				directors[director_name] += 1
			else:
				directors[director_name] = 1

		return directors

	def convert_duration(self, movies_info):

		converted_movies_info = {}

		for key, movie_info in movies_info.items():
			movie_duration = movie_info[0]
			converted_movie_duration = calculate_duration(movie_duration)
			converted_movies_info[key] = [movie_info[1], converted_movie_duration]

		return converted_movies_info