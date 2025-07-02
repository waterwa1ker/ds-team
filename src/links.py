from collections import OrderedDict
from data import Data
from imdb_requester import ImdbRequester
from utils.utils import get_class_name, get_class_column, is_number_natural, is_number_less_than_length
from utils.converter import Converter

class Links(Data):

    def __init__(self, file_path):

        super().__init__(file_path)
        self.convert_types(get_class_name(self))

        self.imdb_requester = ImdbRequester()
        self.converter = Converter()

    def get_imdb(self, list_of_movies, list_of_fields):
        """
            Метод возвращает основную информацию о фильме по идентификатору. Например, режиссера, длительность фильма и т.п.
        """
        
        movies_info = self.imdb_requester.get_movie_info(list_of_movies, list_of_fields)

        movies_list = []
        for movie_key, movie_value in movies_info.items():
            tmp = [movie_key, *movie_value]
            movies_list.append(tmp)
        return sorted(movies_list, key=lambda x: x[0], reverse=True)

    def top_directors(self, n):
        """
            Метод возвращает словарь, ключами которого являются имена режиссеров, а значения - количество фильмов, выпущенных ими.
        """

        is_number_natural(n)

        movies_info = self.imdb_requester.get_movie_info(self.__get_imdb_id(), ['director'])

        directors = self.converter.convert_to_directors(movies_info)

        is_number_less_than_length(n, len(directors))
        return OrderedDict(dict(sorted(directors.items(), key=lambda x: x[1], reverse=True)[:n]))
            
    def most_expensive(self, n):
        """
            Метод возвращает словарь, ключами которого являются id фильмов, а значения - их бюджет.
        """

        is_number_natural(n)
        
        budget_dict = self.imdb_requester.get_movie_info(self.__get_imdb_id(), ['budget'])

        is_number_less_than_length(n, len(budget_dict))
        return OrderedDict(dict(sorted(budget_dict.items(), key=lambda x: x[1], reverse=True)[:n]))
    
    def most_profitable(self, n):
        """
            Метод возвращает словарь, ключами которого являются названия фильмов, а значения - отношения мировых сборов к бюджету фильма
        """

        GROSS_INDEX = 1
        BUDGET_INDEX = 0

        is_number_natural(n)

        gross_budgets = self.imdb_requester.get_movie_info(self.__get_imdb_id(), ['budget', 'gross', 'name'])
        most_profitable = {k: v[GROSS_INDEX] / v[BUDGET_INDEX] for k, v in gross_budgets.items()}

        is_number_less_than_length(n, len(most_profitable))
        return OrderedDict(dict(sorted(most_profitable.items(), key=lambda x: x[1], reverse=True)[:n]))

    # Че за индексы тут, надо вспомнить
    def longest(self, n):
        """
            Метод возвращает словарь, ключами которого явлются названия фильмов, а значениями - их длительность
        """

        is_number_natural(n)

        movies = self.imdb_requester.get_movie_info(self.__get_imdb_id(), ['duration', 'name'])

        is_number_less_than_length(n, len(movies))
        return OrderedDict(dict(sorted(movies.items(), key=lambda x: self.converter.convert_duration(x[1][0]), reverse = True)[:n]))

    def top_cost_per_minute(self, n):
        """
            Метод возвращает словарь, ключами которого являются названия фильмов, а значениями - отношение бюджета к длительности фильма.
        """

        BUDGET_INDEX = 0
        DURATION_INDEX = 1

        is_number_natural(n)

        movies = self.imdb_requester.get_movie_info(self.__get_imdb_id(), ['budget', 'duration', 'name'])
        converted_movies = self.converter.convert_duration(movies)

        top_cost_movies = {k: round(v[BUDGET_INDEX] / v[DURATION_INDEX], 2) for k, v in converted_movies.items()}

        is_number_less_than_length(n, len(top_cost_movies))
        return OrderedDict(dict(sorted(top_cost_movies.items(), key=lambda x: x[1], reverse=True)[:n]))

    def __get_imdb_id(self):
        return get_class_column(get_class_name(self), 'imdbId', self.data)