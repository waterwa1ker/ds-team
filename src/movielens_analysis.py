from sys import argv
from links import Links

if __name__ == '__main__':
    if len(argv) == 5:
        #print(Links(argv[1]).top_directors(2))
        #print(Links(argv[1]).longest(2))
        #print(Links(argv[1]).most_expensive(4))
        print(Links(argv[1]).get_imdb(['0114709', '0113497', '0114709'], ['director']))