import json
import requests as re
from bs4 import BeautifulSoup as bs
import json

from data import Data
from utils.utils import get_class_name, compare_duration

class Links(Data):

    def __init__(self, file_path):

        super().__init__(file_path)
        self.convert_types(get_class_name(self))
        
    def get_imdb(self, list_of_movies, list_of_fields):
        """
            Метод возвращает основную информацию о фильме по идентификатору. Например, режиссера, длительность фильма и т.п.
        """
        
        movies_info = self.__get_movie_info(list_of_movies, list_of_fields)
            
        return dict(sorted(movies_info.items(), key=lambda x: x[0], reverse=True))
        
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

        # Посмотреть еще раз
        
        movies = self.get_imdb(self.__get_imdb_id(), ['duration', 'name'])

        return dict(sorted(movies.items(), key=lambda x: compare_duration(x[1][0]), reverse = True)[:n])

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
     The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """

        movies = self.__get_movie_info(self.__get_imdb_id(), ['budget', 'duration', 'name'])
        return movies

    # Переписать
    def __get_movie_info(self, list_of_movies, list_of_fields):
        
        RIGHT_MOVIE_ID_LENGTH = 7
        
        movies_info = {}
        
        for movie in list_of_movies:

            # приводим movie_id к правильному значению. Иногда слева нужно добавлять ноль
            movie_id = f"{'0' * (RIGHT_MOVIE_ID_LENGTH - len(str(movie)))}{movie}"
        
            link = f'https://www.imdb.com/title/tt{movie_id}/?ref_=vp_close'
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
            
            page = re.get(link, headers = headers)
            soup = bs(page.text, "html.parser")
            script_tag = soup.find('script', {'type': 'application/ld+json'})


            if script_tag:

                movie_info = []

                json_data = json.loads(script_tag.string)

                movie_name = ''
                for field in list_of_fields:
                    field_value = json_data.get(field)
                    if field_value and field not in ['budget', 'gross', 'name']:
                        movie_info.append(field_value)
                    if field == 'name':
                        movie_name = field_value


                if 'budget' in list_of_fields:

                    box_office_section = soup.find('section', {'data-testid': 'BoxOffice'})

                    if box_office_section != None:
                        budget_info = box_office_section.text

                        start_index = budget_info.find('Budget') + len('Budget') + 1
                        end_index = budget_info[start_index:].find(' ') + start_index

                        budget = budget_info[start_index:end_index]
                        budget = budget.replace(',', '')

                        movie_info.append(int(budget))

                if 'gross' in list_of_fields:

                    box_office_section = soup.find('section', {'data-testid': 'BoxOffice'})

                    if box_office_section != None:
                        budget_info = box_office_section.text

                        start_index = budget_info.find('worldwide') + len('worldwide') + 1
                        end_index = budget_info[start_index:].find('See') + start_index

                        gross = budget_info[start_index:end_index]
                        gross = gross.replace(',', '')

                        movie_info.append(int(gross))

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
    
    def __get_imdb_id(self):
        return list(map(lambda x: x[1], self.data))