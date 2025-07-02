import pytest
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from links import Links
from imdb_requester import ImdbRequester
from exceptions.invalid_number_exception import InvalidNumberException

@pytest.fixture
def links_instance():
    """Фикстура для создания экземпляра класса Links"""
    links_file = '../info/links.csv'
    return Links(links_file)

@pytest.fixture
def imdb_request_instance():
    return ImdbRequester()


@pytest.fixture
def test_movie_data():
    """Фикстура для загрузки тестовых данных для get_imdb из get_imdb.json"""
    with open(f'{project_root}/info/links/get_imdb.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def mock_soup_with_data(test_movie_data):
    """Фикстура для создания мока BeautifulSoup с данными для теста get_imdb"""
    mock_soup = MagicMock()
    mock_script = MagicMock()
    mock_script.string = json.dumps(test_movie_data)
    mock_soup.find.return_value = mock_script
    return mock_soup

@pytest.fixture
def test_movie_data_2():
    """Фикстура для создания данных для теста top_directors"""
    with open(f'{project_root}/info/links/top_directors.json', 'r', encoding='utf-8') as f:
        movie_data = json.load(f)
        return movie_data

@pytest.fixture
def test_movie_data_3():
    """Фикстура для создания данных для теста most_expensive"""
    with open(f'{project_root}/info/links/most_expensive.json', 'r', encoding='utf-8') as f:
        movie_data = json.load(f)
        return movie_data

@pytest.fixture
def test_movie_data_4():
    """Фикстура для создания данных для теста most_profitable"""
    with open(f'{project_root}/info/links/most_profitable.json', 'r', encoding='utf-8') as f:
        movie_data = json.load(f)
        return movie_data

@pytest.fixture
def test_movie_data_5():
    """Фикстура для создания данных для теста longest"""
    with open(f'{project_root}/info/links/longest.json', 'r',encoding='utf-8') as f:
        movie_data = json.load(f)
        return movie_data

@pytest.fixture
def test_movie_data_6():
    """Фикстура для создания данных для теста longest"""
    with open(f'{project_root}/info/links/top_cost_per_minute.json', 'r',encoding='utf-8') as f:
        movie_data = json.load(f)
        return movie_data

class TestLinksGetImdbPytest:
    """Тесты для функции get_imdb класса Links с использованием pytest"""
    
    def test_get_imdb_basic_functionality(self, links_instance, imdb_request_instance, mock_soup_with_data):
        """Базовый тест функциональности get_imdb"""
        movie_ids = ['0113228']
        fields = ['name', 'director']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
            assert 'Grumpier Old Men' in result[0]
    
    def test_get_imdb_multiple_fields(self, links_instance, mock_soup_with_data):
        """Тест получения нескольких полей"""
        movie_ids = ['0113228']
        expected_fields = ['Grumpier Old Men', 'Howard Deutch', ['Comedy', 'Romance'], '1995-12-22', 'PG-13']
        fields = ['name', 'director', 'genre', 'datePublished', 'contentRating']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
            if result:
                movie_info = result[0]
                for item in movie_info:
                    assert item in expected_fields
    
    def test_get_imdb_with_actor_field(self, links_instance, mock_soup_with_data):
        """Тест получения информации об актерах"""
        movie_ids = ['0113228']
        expected_names = ['Walter Matthau', 'Jack Lemmon', 'Ann-Margret']
        fields = ['name', 'actor']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
            if result:
                movie_info = result[0][1]
                for item in movie_info:
                    assert item['name'] in expected_names
    
    def test_get_imdb_with_aggregate_rating(self, links_instance, mock_soup_with_data):
        """Тест получения рейтинга фильма"""
        movie_ids = ['0113228']
        fields = ['name', 'aggregateRating']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
    
    def test_get_imdb_with_review_data(self, links_instance, mock_soup_with_data):
        """Тест получения данных о рецензии"""
        movie_ids = ['0113228']
        fields = ['name', 'review']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
    
    def test_get_imdb_with_trailer_data(self, links_instance, mock_soup_with_data):
        """Тест получения данных о трейлере"""
        movie_ids = ['0113228']
        fields = ['name', 'trailer']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
    
    def test_get_imdb_with_duration(self, links_instance, mock_soup_with_data):
        """Тест получения длительности фильма"""
        movie_ids = ['0113228']
        fields = ['name', 'duration']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
    
    def test_get_imdb_with_keywords(self, links_instance, mock_soup_with_data):
        """Тест получения ключевых слов"""
        movie_ids = ['0113228']
        fields = ['name', 'keywords']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
    
    def test_get_imdb_with_creator(self, links_instance, mock_soup_with_data):
        """Тест получения информации о создателях"""
        movie_ids = ['0113228']
        fields = ['name', 'creator']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
    
    def test_get_imdb_with_description(self, links_instance, mock_soup_with_data):
        """Тест получения описания фильма"""
        movie_ids = ['0113228']
        fields = ['name', 'description']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
    
    def test_get_imdb_with_url(self, links_instance, mock_soup_with_data):
        """Тест получения URL фильма"""
        movie_ids = ['0113228']
        fields = ['name', 'url']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
    
    @pytest.mark.parametrize("movie_id,expected_padding", [
        ('113228', '0113228'),
        ('114709', '0114709'),
        ('113497', '0113497'),
        ('114885', '0114885'),
    ])
    def test_get_imdb_id_padding(self, links_instance, mock_soup_with_data, movie_id, expected_padding):
        """Параметризованный тест для проверки дополнения ID нулями"""
        fields = ['name']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data) as mock_get_page:
            links_instance.get_imdb([movie_id], fields)
            mock_get_page.assert_called_with(expected_padding)
    
    @pytest.mark.parametrize("fields", [
        ['name'],
        ['name', 'director'],
        ['name', 'director', 'genre'],
        ['name', 'director', 'genre', 'actor'],
        ['name', 'director', 'genre', 'actor', 'datePublished'],
    ])
    def test_get_imdb_various_field_combinations(self, links_instance, mock_soup_with_data, fields):
        """Параметризованный тест различных комбинаций полей"""
        movie_ids = ['0113228']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
    
    def test_get_imdb_empty_movies_list(self, links_instance):
        """Тест с пустым списком фильмов"""
        fields = ['name', 'director']
        
        result = links_instance.get_imdb([], fields)
        
        assert result == []
    
    def test_get_imdb_empty_fields_list(self, links_instance, mock_soup_with_data):
        """Тест с пустым списком полей"""
        movie_ids = ['0113228']
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, [])
            
            assert result == []
    
    def test_get_imdb_no_script_tag(self, links_instance):
        """Тест случая отсутствия script тега"""
        movie_ids = ['0113228']
        fields = ['name', 'director']
        
        mock_soup = MagicMock()
        mock_soup.find.return_value = None
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert result == []
    
    def test_get_imdb_invalid_json(self, links_instance):
        """Тест случая некорректного JSON"""
        movie_ids = ['0113228']
        fields = ['name', 'director']
        
        mock_soup = MagicMock()
        mock_script = MagicMock()
        mock_script.string = "invalid json"
        mock_soup.find.return_value = mock_script
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup):
            with pytest.raises(json.JSONDecodeError):
                links_instance.get_imdb(movie_ids, fields)
    
    def test_get_imdb_with_budget_and_gross(self, links_instance, mock_soup_with_data): # FAIL
        """Тест получения бюджета и сборов одновременно"""
        movie_ids = ['0113228']
        fields = ['name', 'budget', 'gross']
        
        mock_box_office = MagicMock()
        mock_box_office.text = "Budget$25,000,000 worldwide$71,000,000 See more"
        
        def side_effect(tag, attrs=None):
            if tag == 'script':
                return mock_soup_with_data.find.return_value
            elif attrs and attrs.get('data-testid') == 'BoxOffice':
                return mock_box_office
            return None
        
        mock_soup_with_data.find.side_effect = side_effect
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)


class TestLinksGetImdbEdgeCases:
    """Тесты граничных случаев для функции get_imdb"""
    
    def test_get_imdb_nonexistent_field(self, links_instance, test_movie_data):
        """Тест запроса несуществующего поля"""
        movie_ids = ['0113228']
        fields = ['name', 'nonexistent_field']
        
        mock_soup = MagicMock()
        mock_script = MagicMock()
        mock_script.string = json.dumps(test_movie_data)
        mock_soup.find.return_value = mock_script
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
    
    def test_get_imdb_null_field_value(self, links_instance):
        """Тест случая, когда поле имеет значение null"""
        movie_data = {
            "name": "Test Movie",
            "director": None,
            "genre": ["Action"]
        }
        
        movie_ids = ['0113228']
        fields = ['name', 'director', 'genre']
        
        mock_soup = MagicMock()
        mock_script = MagicMock()
        mock_script.string = json.dumps(movie_data)
        mock_soup.find.return_value = mock_script
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)
    
    def test_get_imdb_empty_field_value(self, links_instance):
        """Тест случая, когда поле имеет пустое значение"""
        movie_data = {
            "name": "Test Movie",
            "director": "",
            "genre": []
        }
        
        movie_ids = ['0113228']
        fields = ['name', 'director', 'genre']
        
        mock_soup = MagicMock()
        mock_script = MagicMock()
        mock_script.string = json.dumps(movie_data)
        mock_soup.find.return_value = mock_script
        
        with patch('imdb_requester.ImdbRequester._ImdbRequester__get_page_by_movie', return_value=mock_soup):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, list)

class TestTopDirectors:
    """Тесты для проверки функции top_directors"""
    def test_top_directors_default(self, links_instance, test_movie_data_2):
        """Тест на обычное поведение функции"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_2)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_2):
                result = links_instance.top_directors(3)
                assert isinstance(result, dict)
                assert len(result) == 3

                expected_result = [
                    ("Christopher Nolan", 2),
                    ("David Fincher", 2),
                    ("Frank Darabont", 1)
                ]
                assert list(result.items()) == expected_result
    
    def test_top_directors_zero(self, links_instance, test_movie_data_2):
        """Тест при нулевом количестве позиций"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_2)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_2):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.top_directors(0)
                assert 'Number must be natural number' == exc_info.value.args[0]
    
    def test_top_directors_empty_data(self, links_instance):
        """Тест при пустых данных"""
        movie_data = {}
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=[]):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=movie_data):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.top_directors(3)
                assert 'Number must be less than length' == exc_info.value.args[0]
    
    def test_top_directors_negative(self, links_instance, test_movie_data_2):
        """Тест при отрицательном значении параметра"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_2)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_2):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.top_directors(-12)
                assert 'Number must be natural number' == exc_info.value.args[0]
    
    def test_top_directors_parameter_bigger_than_data(self, links_instance, test_movie_data_2):
        """Тест при параметре, который больше входных данных"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_2)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_2):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.top_directors(48)
                assert 'Number must be less than length' == exc_info.value.args[0]

class TestMostExpensive:
    def test_most_expensive_default(self, links_instance, test_movie_data_3):
        """Тест на обычное поведение функции"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_3)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_3):
                expected_result = [
                    ('7', 4000),
                    ('4', 2000),
                    ('2', 1500)
                ]
                result = links_instance.most_expensive(3)
                assert len(result) == 3
                assert list(result.items()) == expected_result
    
    def test_most_expensive_zero(self, links_instance, test_movie_data_3):
        """Тест при нулевом количестве позиций"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_3)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_3):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.most_expensive(0)
                assert 'Number must be natural number' == exc_info.value.args[0]
    
    def test_most_expensive_negative(self, links_instance, test_movie_data_3):
        """Тест при отрицательном параметре"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_3)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_3):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.most_expensive(-7)
                assert 'Number must be natural number' == exc_info.value.args[0]
    
    def test_most_expensive_empty_data(self, links_instance):
        """Тест при пустых данных"""
        movie_info = {}
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=[]):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=movie_info):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.most_expensive(4)
                assert 'Number must be less than length' == exc_info.value.args[0]
    
    def test_most_expensive_parameter_bigger(self, links_instance, test_movie_data_3):
        """Тест при параметре, большем входных данных"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_3)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_3):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.most_expensive(45)
                assert 'Number must be less than length' == exc_info.value.args[0]

class TestMostProfitable:
    def test_most_profitable_default(self, links_instance, test_movie_data_4):
        """Тест на обычное поведение функции"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1', '2', '3', '4', '5', '6', '7']):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_4):
                expected_result = [
                    ('1', 15.0),
                    ('5', 2.0),
                    ('7', 1.6243918682943073)
                ]
                result = links_instance.most_profitable(3)
                assert len(result) == 3
                assert list(result.items()) == expected_result

    def test_most_profitable_zero(self, links_instance, test_movie_data_4):
        """Тест при нулевом количестве позиций"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_4)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_4):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.most_profitable(0)
                assert 'Number must be natural number' == exc_info.value.args[0]
    
    def test_most_profitable_negative(self, links_instance, test_movie_data_4):
        """Тест при отрицательном параметре"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_4)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_4):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.most_profitable(-5)
                assert 'Number must be natural number' == exc_info.value.args[0]
    
    def test_most_profitable_empty_data(self, links_instance):
        """Тест при пустых данных"""
        movie_info = {}
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=[]):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=movie_info):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.most_profitable(3)
                assert 'Number must be less than length' == exc_info.value.args[0]
    
    def test_most_profitable_parameter_bigger(self, links_instance, test_movie_data_4):
        """Тест при параметре, большем входных данных"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_4)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_4):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.most_profitable(12)
                assert 'Number must be less than length' == exc_info.value.args[0]

class TestLongest:
    def test_longest_default(self, links_instance, test_movie_data_5):
        """Тест на обычное поведение функции"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_5)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_5):
                result = links_instance.longest(3)
                assert len(result) == 3
                assert result == 'gay'

    def test_longest_zero(self, links_instance, test_movie_data_5):
        """Тест при нулевом количестве позиций"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_5)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_5):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.longest(0)
                assert 'Number must be natural number' == exc_info.value.args[0]
    
    def test_longest_negative(self, links_instance, test_movie_data_5):
        """Тест при отрицательном параметре"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_5)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_5):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.longest(-5)
                assert 'Number must be natural number' == exc_info.value.args[0]
    
    def test_longest_empty_data(self, links_instance):
        """Тест при пустых данных"""
        movie_info = {}
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=[]):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=movie_info):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.longest(3)
                assert 'Number must be less than length' == exc_info.value.args[0]
    
    def test_longest_parameter_bigger(self, links_instance, test_movie_data_5):
        """Тест при параметре, большем входных данных"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_5)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_5):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.longest(12)
                assert 'Number must be less than length' == exc_info.value.args[0]

class TestTopCostPerMinute:
    def test_top_cost_per_minute_default(self, links_instance, test_movie_data_6):
        """Тест на обычное поведение функции"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_6)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_6):
                expected_result = [
                    ('The Godfather', 1980.2),
                    ('The Shawshank Redemption', 1075.27),
                    ('The Silence of the Lambs', 13.89)
                ]
                result = links_instance.top_cost_per_minute(3)
                assert len(result) == 3
                assert list(result.items()) == expected_result

    def test_top_cost_per_minute_zero(self, links_instance, test_movie_data_6):
        """Тест при нулевом количестве позиций"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_6)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_6):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.top_cost_per_minute(0)
                assert 'Number must be natural number' == exc_info.value.args[0]
    
    def test_top_cost_per_minute_negative(self, links_instance, test_movie_data_6):
        """Тест при отрицательном параметре"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_6)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_6):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.top_cost_per_minute(-5)
                assert 'Number must be natural number' == exc_info.value.args[0]
    
    def test_top_cost_per_minute_empty_data(self, links_instance):
        """Тест при пустых данных"""
        movie_info = {}
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=[]):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=movie_info):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.top_cost_per_minute(3)
                assert 'Number must be less than length' == exc_info.value.args[0]
    
    def test_top_cost_per_minute_parameter_bigger(self, links_instance, test_movie_data_6):
        """Тест при параметре, большем входных данных"""
        with patch.object(links_instance, '_Links__get_imdb_id', return_value=['1'] * len(test_movie_data_6)):
            with patch('imdb_requester.ImdbRequester.get_movie_info', return_value=test_movie_data_6):
                with pytest.raises(InvalidNumberException) as exc_info:
                    links_instance.top_cost_per_minute(12)
                assert 'Number must be less than length' == exc_info.value.args[0]

    
if __name__ == '__main__':
    pytest.main([__file__, '-v']) 