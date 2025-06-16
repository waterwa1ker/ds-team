from sys import argv
from collections import Counter
import requests as re
from bs4 import BeautifulSoup as bs
import json

from file_parser import FileParser
from utils import get_class_name, get_column_index, print_file, convert_types


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
The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
     Sort it by movieId descendingly.
        """
        
        RIGHT_MOVIE_ID_LENGTH = 7
        
        for movie in list_of_movies:

            # приводим movie_id к правильному значению. Иногда слева нужно добавлять ноль
            movie_id = f"{'0' * (RIGHT_MOVIE_ID_LENGTH - len(str(movie)))}{movie}"
            print(movie_id)
        
            link = f'https://www.imdb.com/title/tt{movie_id}/?ref_=vp_close'
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
            
            page = re.get(link, headers = headers)
            soup = bs(page.text, "html.parser")
            script_tag = soup.find('script', {'type': 'application/ld+json'})
            
            movies_info = []
            
            if script_tag:
                json_data = json.loads(script_tag.string)
                
                movie_info = f"'{movie_id}', "
                
                for field in list_of_fields:
                    movie_info = f"{movie_info}, '{json_data.get(field)[0]}'"
                
                movies_info.append(movie_info)
            
        print(movies_info)
        return movies_info
        
    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        
        RIGHT_MOVIE_ID_LENGTH = 7
        
        director_dict = {}
        
        for element in self.data:
            
            # приводим movie_id к правильному значению. Иногда слева нужно добавлять ноль
            movie_id = f"{'0' * (RIGHT_MOVIE_ID_LENGTH - len(str(element[1])))}{element[1]}"
            link = f'https://www.imdb.com/title/tt{movie_id}/?ref_=vp_close'
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
            
            page = re.get(link, headers = headers)
            soup = bs(page.text, "html.parser")
            script_tag = soup.find('script', {'type': 'application/ld+json'})
            
            if script_tag:
                json_data = json.loads(script_tag.string)
                # может быть так, что у режиссеров одинаковые имя и фамилия, так что целесообразнее сделать через url
                director_url = json_data.get('director')[0]['name']
                if director_url not in director_dict:
                    director_dict[director_url] = 1
                else:
                    director_dict[director_url] += 1
                    
        sorted_director_dict = sorted(director_dict.items(), key=lambda x : x[1], reverse=True)    
        print(sorted_director_dict[:n])
        
        return sorted_director_dict
        
    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        return budgets
        
    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
     Sort it by the difference descendingly.
        """
        return profits
        
    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
     Sort it by runtime descendingly.
        """
        return runtimes
        
    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
     The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        return costs



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
        #Links(argv[1]).top_directors(3)
        Links(argv[1]).get_imdb(['0114709', '0113497'], ['description', 'genre'])