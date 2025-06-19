from sys import argv
import requests as re
from bs4 import BeautifulSoup as bs
import json

from file_parser import FileParser
from utils import get_class_name, get_column_index, print_file, convert_types, compare_duration


class Data:

    def __init__(self, file_path):

        self.data = []

        self.file_parser = FileParser()

        self.file_parser.file_exists(file_path)
        self.file_parser.file_empty(file_path)
        
        self.__open_file(file_path)


    def sort_by_column(self, column_name, reverse = False):
        self.file_parser.check_column_name(get_class_name(self), column_name)

        column_index = get_column_index(self.header, column_name)
        tmp_data = sorted(self.data, key = lambda x: x[column_index], reverse = reverse)
        print_file(self.header, tmp_data) #do we need this???

    def count_values_by_column(self, column_name):
        pass

    def __open_file(self, file_path):
        with open(file_path, 'r') as f:
            header = f.readline().replace('\n', '')
            self.file_parser.check_headers(get_class_name(self), header)
            self.header = header
            for line in f:
                line = line.replace('\n', '')
                line_list = line.split(',')
                self.file_parser.check_body_line(get_class_name(self), line_list)
                self.data.append(line_list)

    def convert_types(self, class_name):
        self.data = convert_types(self.data, class_name)


class Links(Data):

    def __init__(self, file_path):

        super().__init__(file_path)
        self.convert_types(get_class_name(self))
        
    def get_imdb(self, list_of_movies, list_of_fields):
        """
            Метод возвращает основную информацию о фильме по идентификатору. Например, режиссера, длительность фильма и т.п.
        """
        
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
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        
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
    
    def __get_imdb_id(self):
        return list(map(lambda x: x[1], self.data))



class Tags(Data):

    def __init__(self, file_path):
        super().__init__(file_path)
        self.convert_types(get_class_name(self))
    


class Ratings(Data):

    def __init__(self, file_path):
        super().__init__(file_path)
        self.convert_types(get_class_name(self))
        
    
class Movies(Data):
    
    def __init__(self, file_path):
        super().__init__(file_path)
        self.convert_types(get_class_name(self))    
    


if __name__ == '__main__':
    if len(argv) == 5:
        #print(Links(argv[1]).top_directors(2))
        #print(Links(argv[1]).longest(2))
        print(Links(argv[1]).most_expensive(4))
        #print(Links(argv[1]).get_imdb(['0114709', '0113497', '0114709'], ['director']))