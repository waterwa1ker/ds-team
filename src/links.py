import json

from data import Data
from utils.utils import get_class_name, convert_duration, get_page_by_movie

class Links(Data):

    def __init__(self, file_path):

        super().__init__(file_path)
        self.convert_types(get_class_name(self))
        
    def get_imdb(self, list_of_movies, list_of_fields):
        """
            Метод возвращает основную информацию о фильме по идентификатору. Например, режиссера, длительность фильма и т.п.
        """
        
        movies_info = self.__get_movie_info(list_of_movies, list_of_fields)

        movies_list = []
        for movie_key, movie_value in movies_info.items():
            tmp = [movie_key, *movie_value]
            movies_list.append(tmp)
        return movies_list

    def top_directors(self, n):
        """
            Метод возвращает словарь, ключами которого являются имена режиссеров, а значения - количество фильмов, выпущенных ими.
        """

        movies_info = self.get_imdb(self.__get_imdb_id(), ['director'])

        directors = self.__convert_to_directors(movies_info)
        return dict(sorted(directors.items(), key=lambda x: x[1], reverse=True)[:n])
            
    def most_expensive(self, n):
        """
            Метод возвращает словарь, ключами которого являются id фильмов, а значения - их бюджет.
        """
        
        budget_dict = self.__get_movie_info(self.__get_imdb_id(), ['budget'])

        return dict(sorted(budget_dict.items(), key=lambda x: x[1], reverse=True)[:n])
    
    def most_profitable(self, n):
        """
            Метод возвращает словарь, ключами которого являются названия фильмов, а значения - отношения мировых сборов к бюджету фильма
        """

        gross_budgets = self.__get_movie_info(self.__get_imdb_id(), ['budget', 'gross', 'name'])
        most_profitable = {k: v[1] / v[0] for k, v in gross_budgets.items()}

        return dict(sorted(most_profitable.items(), key=lambda x: x[1], reverse=True)[:n])
        
    def longest(self, n):
        """
            Метод возвращает словарь, ключами которого явлются названия фильмов, а значениями - их длительность
        """

        movies = self.get_imdb(self.__get_imdb_id(), ['duration', 'name'])
        return dict(sorted(movies.items(), key=lambda x: convert_duration(x[1][0]), reverse = True)[:n])

    def top_cost_per_minute(self, n):
        """
            Метод возвращает словарь, ключами которого являются названия фильмов, а значениями - отношение бюджета к длительности фильма.
        """

        movies = self.__get_movie_info(self.__get_imdb_id(), ['budget', 'duration', 'name'])
        converted_movies = self.__convert_duration(movies)

        print(converted_movies)
        top_cost_movies = {k: round(v[0] / v[1], 2) for k, v in converted_movies.items()}
        return dict(sorted(top_cost_movies.items(), key=lambda x: x[1], reverse=True)[:n])

    def __get_movie_info(self, list_of_movies, list_of_fields):

        movies_info = {}
        RIGHT_MOVIE_ID_LENGTH = 7
        additional_params = ['budget', 'gross']
        
        for movie in list_of_movies:

            # приводим movie_id к правильному значению. Иногда слева нужно добавлять ноль
            movie_id = f"{'0' * (RIGHT_MOVIE_ID_LENGTH - len(str(movie)))}{movie}"

            soup = get_page_by_movie(movie_id)
            script_tag = soup.find('script', {'type': 'application/ld+json'})

            if script_tag:

                movie_info = []
                json_data = json.loads(script_tag.string)
                movie_name = None

                for field in list_of_fields:
                    field_value = json_data.get(field)
                    if field_value and field not in [additional_params, 'name']:
                        movie_info.append(field_value)
                    if field == 'name':
                        movie_name = field_value

                for additional_param in additional_params:
                    if additional_param in list_of_fields:
                        box_office_value = self.__get_info_from_box_office(soup, additional_param)
                        if box_office_value is not None:
                            movie_info.append(box_office_value)

                if movie_name and movie_name not in movies_info and movie_info:
                    movies_info[movie_name] = movie_info
                elif movie_id not in movies_info and movie_info:
                    movies_info[movie_id] = movie_info

        return movies_info

    def __convert_to_directors(self, movies_info):

        directors = {}

        for _, director in movies_info.items():
            director_name = director[0][0]['name']
            if director_name in movies_info:
                directors[director_name] += 1
            else:
                directors[director_name] = 1

        return directors

    def __convert_duration(self, movies_info):

        converted_movies_info = {}

        for key, movie_info in movies_info.items():
            movie_duration = movie_info[0]
            converted_movie_duration = convert_duration(movie_duration)
            converted_movies_info[key] = [movie_info[1], converted_movie_duration]

        return converted_movies_info

    def __get_info_from_box_office(self, soup, info_key):
        box_office_section = soup.find('section', {'data-testid': 'BoxOffice'})
        info_value = None

        if box_office_section is not None:
            box_office_text = box_office_section.text

            if info_key == 'budget':
                start_index = box_office_text.find('Budget') + len('Budget') + 1
                end_index = box_office_text[start_index:].find(' ') + start_index
            else:
                start_index = box_office_text.find('worldwide') + len('worldwide') + 1
                end_index = box_office_text[start_index:].find('See') + start_index

            info_value = box_office_text[start_index:end_index]
            info_value = int(info_value.replace(',', ''))

        return info_value

    def __get_imdb_id(self):
        return list(map(lambda x: x[1], self.data))