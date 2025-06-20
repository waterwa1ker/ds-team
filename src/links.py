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
            
        sorted_movies_info = sorted(movies_info, key=lambda x: x[0], reverse=True)
        return sorted_movies_info
        
    def top_directors(self, n):
        """
            Метод возвращает словарь, ключами которого являются имена режиссеров, а значения - количество фильмов, выпущенных ими.
        """
        
        director_dict = {}
        
        directors = self.get_imdb(self.__get_imdb_id(), ['director'])
        for director in directors:
            director_name = director[1][0]['name']
            if director_name in director_dict:
                director_dict[director_name] += 1
            else:
                director_dict[director_name] = 1
        return sorted(director_dict.items(), key=lambda x: x[1], reverse=True)[:n]
            

        
    def most_expensive(self, n):
        """
            Метод возвращает словарь, ключами которого являются id фильмов, а значения - их бюджет.
        """
        
        budget_dict = self.__get_budgets()
                
        return sorted(budget_dict.items(), key=lambda x: int(x[1]), reverse=True)[:n]
    
    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
     Sort it by the difference descendingly.
        """
        return profits
        
    def longest(self, n):
        """
            Метод возвращает словарь, ключами которого явлются названия фильмов, а значениями - их длительность
        """
        
        movies_dict = {}
        
        movies = self.get_imdb(self.__get_imdb_id(), ['duration', 'name'])
        movies = list(filter(lambda x: x[1] != None, movies))
        
        for movie in movies:
            movie_name = movie[2]
            if movie_name not in movies_dict:
                movies_dict[movie_name] = movie[1]
        sorted_movies = sorted(movies_dict.items(), key=lambda x: compare_duration(x[1]), reverse = True)
        return sorted_movies[:n]
        
    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
     The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        return costs
    
    def __get_movie_info(self, list_of_movies, list_of_fields):
        
        RIGHT_MOVIE_ID_LENGTH = 7
        
        movies_info = []
        
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
                json_data = json.loads(script_tag.string)
                
                movie_info = [movie_id]
                
                for field in list_of_fields:
                    movie_info.append(json_data.get(field))
                
                movies_info.append(movie_info)
        
        return movies_info
              
    
    def __get_budgets(self):
        
        RIGHT_MOVIE_ID_LENGTH = 7
        budget_dict = {}
        
        for movie in self.data:
        
            movie = movie[1]
            
            movie_id = f"{'0' * (RIGHT_MOVIE_ID_LENGTH - len(str(movie)))}{movie}"
            
            link = f'https://www.imdb.com/title/tt{movie_id}/?ref_=vp_close'
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
            
            page = re.get(link, headers = headers)
            soup = bs(page.text, "html.parser")
            
            box_office_section = soup.find('section', {'data-testid': 'BoxOffice'})
            if box_office_section != None:
                budget_info = box_office_section.text

                start_index = budget_info.find('Budget') + len('Budget') + 1 
                end_index = budget_info[start_index:].find(' ') + start_index    
                
                budget = budget_info[start_index:end_index]
                budget = budget.replace(',', '')
                
                if movie_id not in budget_dict:
                    budget_dict[movie_id] = budget
        return budget_dict
    
    def __get_imdb_id(self):
        return list(map(lambda x: x[1], self.data))