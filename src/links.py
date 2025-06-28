from data import Data
from imdb_requester import ImdbRequester
from utils.utils import get_class_name, get_class_column
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

        movies_info = self.imdb_requester.get_movie_info(self.__get_imdb_id(), ['director'])

        directors = self.converter.convert_to_directors(movies_info)
        return dict(sorted(directors.items(), key=lambda x: x[1], reverse=True)[:n])
            
    def most_expensive(self, n):
        """
            Метод возвращает словарь, ключами которого являются id фильмов, а значения - их бюджет.
        """
        
        budget_dict = self.imdb_requester.get_movie_info(self.__get_imdb_id(), ['budget'])

        return dict(sorted(budget_dict.items(), key=lambda x: x[1], reverse=True)[:n])
    
    def most_profitable(self, n):
        """
            Метод возвращает словарь, ключами которого являются названия фильмов, а значения - отношения мировых сборов к бюджету фильма
        """

        gross_budgets = self.imdb_requester.get_movie_info(self.__get_imdb_id(), ['budget', 'gross', 'name'])
        most_profitable = {k: v[1] / v[0] for k, v in gross_budgets.items()}

        return dict(sorted(most_profitable.items(), key=lambda x: x[1], reverse=True)[:n])
        
    def longest(self, n):
        """
            Метод возвращает словарь, ключами которого явлются названия фильмов, а значениями - их длительность
        """

        movies = self.get_imdb(self.__get_imdb_id(), ['duration', 'name'])
        return dict(sorted(movies.items(), key=lambda x: self.converter.convert_duration(x[1][0]), reverse = True)[:n])

    def top_cost_per_minute(self, n):
        """
            Метод возвращает словарь, ключами которого являются названия фильмов, а значениями - отношение бюджета к длительности фильма.
        """

        movies = self.imdb_requester.get_movie_info(self.__get_imdb_id(), ['budget', 'duration', 'name'])
        converted_movies = self.converter.convert_duration(movies)

        top_cost_movies = {k: round(v[0] / v[1], 2) for k, v in converted_movies.items()}
        return dict(sorted(top_cost_movies.items(), key=lambda x: x[1], reverse=True)[:n])

    def __get_imdb_id(self):
        return get_class_column(get_class_name(self), 'imdbId')