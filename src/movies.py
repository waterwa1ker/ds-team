from data import Data
from utils.utils import get_class_name, is_number_natural, is_number_less_than_length, get_class_column

class Movies(Data):
    
    def __init__(self, file_path):
        super().__init__(file_path)
        self.convert_types(get_class_name(self))

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """

        years_dict = {}

        movie_titles = self.__get_movie_titles()
        years = []
        for movie_title in movie_titles:
            year = movie_title[movie_title.rfind('(')+1:movie_title.rfind(')')]
            years.append(year)
        for year in years:
            if year not in years_dict:
                years_dict[year] = 1
            else:
                years_dict[year] += 1

        return dict(sorted(years_dict.items(), key=lambda x: x[1], reverse=True))

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
     Sort it by counts descendingly.
        """

        genres_dict = {}

        movies_genres = '|'.join(self.__get_movie_genres()).split('|')
        for movie_genre in movies_genres:
            if movie_genre not in genres_dict:
                genres_dict[movie_genre] = 1
            else:
                genres_dict[movie_genre] += 1
        return dict(sorted(genres_dict.items(), key=lambda x: x[1], reverse=True))

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """

        is_number_natural(n)

        movies = {}
        for movie in self.data:
            movie_name = movie[1]
            movie_genres = movie[2].split('|')
            movies[movie_name] = len(movie_genres)

        is_number_less_than_length(n, len(movies))
        return dict(sorted(movies.items(), key=lambda x: x[1], reverse=True)[:n])

    def __get_movie_titles(self):
        return get_class_column(get_class_name(self), 'title', self.data)

    def __get_movie_genres(self):
        return get_class_column(get_class_name(self), 'genres', self.data)
