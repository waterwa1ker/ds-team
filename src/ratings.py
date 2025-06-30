from data import Data
from links import Links
from utils.utils import get_class_name, get_class_column

class Ratings(Data):

    def __init__(self, file_path):
        super().__init__(file_path)
        self.convert_types(get_class_name(self))
        
    class Movies:    
        
        def __init__(self, ratings):
            self.ratings = ratings
        
        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            
            ratings_by_year = {}
            timestamps = self.__get_timestamp()
            years = map(lambda x: self.__find_year_from_timestamp(x), timestamps)
            
            for year in years:
                if year in ratings_by_year:
                    ratings_by_year[year] += 1
                else:
                    ratings_by_year[year] = 1
            return dict(sorted(ratings_by_year.items(), key=lambda x: x[1], reverse=True))
        
        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
         Sort it by ratings ascendingly.
            """
            
            ratings_distribution = {}
            ratings = self.__get_rating()
            for rating in ratings:
                if rating in ratings_distribution:
                    ratings_distribution[rating] += 1
                else:
                    ratings_distribution[rating] = 1
            return dict(sorted(ratings_distribution.items(), key=lambda x: x[1], reverse=True))
        
        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
     Sort it by numbers descendingly.
            """
            top_movies = {}

            movie_ids = self.__get_movie_id()
            imdb_ids = list(map(lambda x: self.__find_imdb_id_by_movie_id(str(x)), movie_ids))

            links = Links('info/links.csv')
            movies = links.get_imdb(imdb_ids, ['datePublished', 'name'])
            print(movies)

            return top_movies
        
        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            return top_movies
        
        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
          Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            return top_movies


        def get_movie_id(self):
            return get_class_column(get_class_name(self.ratings), 'movieId', self.ratings.data)

        def __get_timestamp(self):
            return get_class_column(get_class_name(self.ratings), 'timestamp', self.ratings.data)
        
        def __get_rating(self):
            return get_class_column(get_class_name(self.ratings), 'rating', self.ratings.data)
        
        # это не совсем точно
        def __find_year_from_timestamp(self, timestamp):
            YEAR_FROM = 1970
            return YEAR_FROM + (timestamp // 60 // 60 // 24 // 365)
        
        def __find_imdb_id_by_movie_id(self, movie_id):
            file_path = 'info/links.csv'
            imdb_id = None
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.replace('\n', '')
                    line_list = line.split(',')
                    line_movie_id = line_list[0]
                    if movie_id == line_movie_id:
                        imdb_id = line_list[1]
                        break
            return imdb_id
                        

    class Users:
        """
        In this class, three methods should work. 
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
     Inherit from the class Movies. Several methods are similar to the methods from it.
        """