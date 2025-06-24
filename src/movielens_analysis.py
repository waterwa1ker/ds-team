from sys import argv
from links import Links
from movies import Movies
import json
from tags import Tags

if __name__ == '__main__':
    if len(argv) == 5:
        #print(Links(argv[1]).top_directors(2))
        #print(Links(argv[1]).longest(2))
        #print(Links(argv[1]).top_cost_per_minute(3))
        #dic = Links(argv[1]).most_expensive(4)
        #dic = Links(argv[1]).get_imdb(['0114709', '0113497', '0114709'], ['budget'])
        #print(Links(argv[1]).most_profitable(2))
        #print(Movies(argv[2]).dist_by_release())
        #print(Movies(argv[2]).dist_by_genres())
        #print(Movies(argv[2]).most_genres(2))
        print(Tags(argv[3]).most_words(3))
        print(Tags(argv[3]).longest(4))
        print(Tags(argv[3]).most_popular(5))
        print(Tags(argv[3]).tags_with('m'))