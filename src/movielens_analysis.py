from sys import argv
from links import Links
from movies import Movies
import json
from tags import Tags
from ratings import Ratings

if __name__ == '__main__':
    if len(argv) == 5:
        print(Links(argv[1]).top_directors(1))
        #print(Links(argv[1]).longest(2))
        #print(Links(argv[1]).top_cost_per_minute(3))
        #dic = Links(argv[1]).most_expensive(4)
        #dic = Links(argv[1]).get_imdb(['0114709', '0114885', '4912910'], ['director'])
        #print(dic)
        #print(Links(argv[1]).most_profitable(2))
        #print(Movies(argv[2]).dist_by_release())
        #print(Movies(argv[2]).dist_by_genres())
        #print(Movies(argv[2]).most_genres(2))
        #print(Tags(argv[3]).most_words(3))
        #print(Tags(argv[3]).longest(4))
        #print(Tags(argv[3]).most_popular(5))
        #print(Tags(argv[3]).tags_with('m'))

        # ratings = Ratings(argv[4])
        # movies = ratings.Movies(ratings)
        # print(movies.dist_by_year())
        # print(movies.dist_by_rating())
        # print(movies.find_imdb_id_by_movie_id('1'))
        # print(movies.get_movie_id())