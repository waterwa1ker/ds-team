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
def movies_instance_default():
    movies_file = f'{project_root}/info/movies.csv'
    return Movies(movies_file)

@pytest.fixture
def movies_instance_with_quotes():
    movies_file = f'{project_root}/info/movies/movies_with_double_quotes.csv'
    return Movies(movies_file)

@pytest.fixture
def dist_by_release_default_expected():
    with open(f'{project_root}/info/movies/dist_by_release.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def dist_by_release_doublequoted_expected():
    with open(f'{project_root}/info/movies/dist_by_release_doublequoted.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def dist_by_genres_default_expected():
    with open(f'{project_root}/info/movies/dist_by_genres.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def dist_by_genres_doublequoted_expected():
    with open(f'{project_root}/info/movies/dist_by_genres_doublequoted.json', 'r', encoding='utf-8') as f:
        return json.load(f)

class TestDistByRelease:
    def test_dist_by_release_default(self, movies_instance_default, movies_instance_with_quotes, dist_by_release_default_expected, dist_by_release_doublequoted_expected):
        result_default = movies_instance_default.dist_by_release()
        assert isinstance(result_default, dict)
        assert len(result_default) == 12
        assert result_default == dist_by_release_default_expected

        result_with_quotes = movies_instance_with_quotes.dist_by_release()
        assert isinstance(result_with_quotes, dict)
        assert len(result_with_quotes) == 11
        assert result_with_quotes == dist_by_release_doublequoted_expected

class TestDistByGenres:
    def test_dist_by_genres_default(self, movies_instance_default, movies_instance_with_quotes, dist_by_genres_default_expected, dist_by_genres_doublequoted_expected):
        result_default = movies_instance_default.dist_by_genres()
        assert isinstance(result_default, dict)
        assert len(result_default) == 14
        assert result_default == dist_by_genres_default_expected

        result_with_quotes = movies_instance_with_quotes.dist_by_genres()
        assert isinstance(result_with_quotes, dict)
        assert len(result_with_quotes) == 11
        assert result_with_quotes == dist_by_genres_doublequoted_expected

class TestMostGenres:
    def test_most_genres_default(self, movies_instance_default, movies_instance_with_quotes):
        expected_data_default = {'Digging Up the Marrow (2014)': 5,
                         'High School Musical (2006)': 5,
                         'Space Buddies (2009)': 4}
        result_default = movies_instance_default.most_genres(3)
        assert isinstance(result_default, dict)
        assert len(result_default) == 3
        assert result_default == expected_data_default

        expected_data_doublequoted = {'Edukators, The (Die Fetten Jahre sind vorbei) (2004)': 4,
                                      'Brave One, The (2007)': 3,
                                      'Getaway, The (1994)': 6}
        result_with_quotes = movies_instance_with_quotes.most_genres(3)
        assert isinstance(result_with_quotes, dict)
        assert len(result_with_quotes) == 3
        assert result_with_quotes == expected_data_doublequoted
    
    def test_most_genres_zero(self, movies_instance_default, movies_instance_with_quotes):
        with pytest.raises(InvalidNumberException) as exc_info:
            movies_instance_default.most_genres(0)
        assert 'Number must be natural number' == exc_info.value.args[0]

        with pytest.raises(InvalidNumberException) as exc_info:
            movies_instance_with_quotes.most_genres(0)
        assert 'Number must be natural number' == exc_info.value.args[0]

    def test_most_genres_negative(self, movies_instance_default, movies_instance_with_quotes):
        with pytest.raises(InvalidNumberException) as exc_info:
            movies_instance_default.most_genres(-7)
        assert 'Number must be natural number' == exc_info.value.args[0]

        with pytest.raises(InvalidNumberException) as exc_info:
            movies_instance_with_quotes.most_genres(-7)
        assert 'Number must be natural number' == exc_info.value.args[0]

    def test_most_genres_parameter_bigger(self, movies_instance_default, movies_instance_with_quotes):
        with pytest.raises(InvalidNumberException) as exc_info:
            movies_instance_default.most_genres(100)
        assert 'Number must be less than length' == exc_info.value.args[0]

        with pytest.raises(InvalidNumberException) as exc_info:
            movies_instance_with_quotes.most_genres(100)
        assert 'Number must be less than length' == exc_info.value.args[0]


if __name__ == "__main__":
    # print(Movies(f'{project_root}/info/movies/movies_with_double_quotes.csv').dist_by_genres())
    pytest.main([__file__, '-v']) 