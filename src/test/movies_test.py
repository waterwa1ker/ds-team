import pytest
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from movies import Movies
from exceptions.invalid_number_exception import InvalidNumberException

@pytest.fixture
def movies_instance():
    movies_file = f'{project_root}/info/movies.csv'
    return Movies(movies_file)

@pytest.fixture
def dist_by_release_expected_data():
    with open(f'{project_root}/info/movies/dist_by_release.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def dist_by_genres_expected_data():
    with open(f'{project_root}/info/movies/dist_by_genres.json', 'r', encoding='utf-8') as f:
        return json.load(f)

class TestDistByRelease:
    def test_dist_by_release_default(self, movies_instance, dist_by_release_expected_data):
        result = movies_instance.dist_by_release()
        assert isinstance(result, dict)
        assert len(result) == 12
        assert result == dist_by_release_expected_data

class TestDistByGenres:
    def test_dist_by_genres_default(self, movies_instance, dist_by_genres_expected_data):
        result = movies_instance.dist_by_genres()
        assert isinstance(result, dict)
        assert len(result) == 14
        assert result == dist_by_genres_expected_data

class TestMostGenres:
    def test_most_genres_default(self, movies_instance):
        expected_data = {'Digging Up the Marrow (2014)': 5,
                         'High School Musical (2006)': 5,
                         'Space Buddies (2009)': 4}
        result = movies_instance.most_genres(3)
        assert isinstance(result, dict)
        assert len(result) == 3
        assert result == expected_data
    
    def test_most_genres_zero(self, movies_instance):
        with pytest.raises(InvalidNumberException) as exc_info:
            movies_instance.most_genres(0)
        assert 'Number must be natural number' == exc_info.value.args[0]

    def test_most_genres_negative(self, movies_instance):
        with pytest.raises(InvalidNumberException) as exc_info:
            movies_instance.most_genres(-7)
        assert 'Number must be natural number' == exc_info.value.args[0]

    def test_most_genres_parameter_bigger(self, movies_instance):
        with pytest.raises(InvalidNumberException) as exc_info:
            movies_instance.most_genres(100)
        assert 'Number must be less than length' == exc_info.value.args[0]

if __name__ == "__main__":
    # print(Movies(f'{project_root}/info/movies.csv').most_genres(3))
    pytest.main([__file__, '-v']) 