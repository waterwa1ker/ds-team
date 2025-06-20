import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from links import Links

def test_get_imdb_1():
    
    file_path = 'info/links.csv'
    field = ['name']
    movies = ['0114709']
    excepted_result = [['0114709', 'Toy Story']]
    
    links = Links(file_path)
    
    result = links.get_imdb(movies, field)
    
    assert excepted_result == result
    
def test_get_imdb_2():
    
    file_path = 'info/links.csv'
    fields = ['duration', 'datePublished']
    movies = ['0114709', '0113228']
    excepted_result = [['0114709', 'PT1H21M', '1995-11-22'], ['0113228', 'PT1H41M', '1995-12-22']]
    
    links = Links(file_path)
    
    result = links.get_imdb(movies, fields)
    
    assert excepted_result == result
    