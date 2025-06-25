import pytest
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from links import Links


@pytest.fixture
def links_instance():
    """Фикстура для создания экземпляра класса Links"""
    links_file = '../info/links.csv'
    return Links(links_file)


@pytest.fixture
def test_movie_data():
    """Фикстура для загрузки тестовых данных из info.json"""
    with open('../info/info.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def mock_soup_with_data(test_movie_data):
    """Фикстура для создания мока BeautifulSoup с данными"""
    mock_soup = MagicMock()
    mock_script = MagicMock()
    mock_script.string = json.dumps(test_movie_data)
    mock_soup.find.return_value = mock_script
    return mock_soup


class TestLinksGetImdbPytest:
    """Тесты для функции get_imdb класса Links с использованием pytest"""
    
    def test_get_imdb_basic_functionality(self, links_instance, mock_soup_with_data):
        """Базовый тест функциональности get_imdb"""
        movie_ids = ['0113228']
        fields = ['name', 'director']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
            assert 'Grumpier Old Men' in result
    
    def test_get_imdb_multiple_fields(self, links_instance, mock_soup_with_data):
        """Тест получения нескольких полей"""
        movie_ids = ['0113228']
        fields = ['name', 'director', 'genre', 'datePublished', 'contentRating']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
            if result:
                movie_info = result['Grumpier Old Men']
                assert isinstance(movie_info, list)
    
    def test_get_imdb_with_actor_field(self, links_instance, mock_soup_with_data):
        """Тест получения информации об актерах"""
        movie_ids = ['0113228']
        fields = ['name', 'actor']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
            if result:
                movie_info = result['Grumpier Old Men']
                assert isinstance(movie_info, list)
    
    def test_get_imdb_with_aggregate_rating(self, links_instance, mock_soup_with_data):
        """Тест получения рейтинга фильма"""
        movie_ids = ['0113228']
        fields = ['name', 'aggregateRating']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
    
    def test_get_imdb_with_review_data(self, links_instance, mock_soup_with_data):
        """Тест получения данных о рецензии"""
        movie_ids = ['0113228']
        fields = ['name', 'review']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
    
    def test_get_imdb_with_trailer_data(self, links_instance, mock_soup_with_data):
        """Тест получения данных о трейлере"""
        movie_ids = ['0113228']
        fields = ['name', 'trailer']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
    
    def test_get_imdb_with_duration(self, links_instance, mock_soup_with_data):
        """Тест получения длительности фильма"""
        movie_ids = ['0113228']
        fields = ['name', 'duration']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
    
    def test_get_imdb_with_keywords(self, links_instance, mock_soup_with_data):
        """Тест получения ключевых слов"""
        movie_ids = ['0113228']
        fields = ['name', 'keywords']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
    
    def test_get_imdb_with_creator(self, links_instance, mock_soup_with_data):
        """Тест получения информации о создателях"""
        movie_ids = ['0113228']
        fields = ['name', 'creator']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
    
    def test_get_imdb_with_description(self, links_instance, mock_soup_with_data):
        """Тест получения описания фильма"""
        movie_ids = ['0113228']
        fields = ['name', 'description']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
    
    def test_get_imdb_with_url(self, links_instance, mock_soup_with_data):
        """Тест получения URL фильма"""
        movie_ids = ['0113228']
        fields = ['name', 'url']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
    
    @pytest.mark.parametrize("movie_id,expected_padding", [
        ('113228', '0113228'),
        ('114709', '0114709'),
        ('113497', '0113497'),
        ('114885', '0114885'),
    ])
    def test_get_imdb_id_padding(self, links_instance, mock_soup_with_data, movie_id, expected_padding):
        """Параметризованный тест для проверки дополнения ID нулями"""
        fields = ['name']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data) as mock_get_page:
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
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
    
    def test_get_imdb_empty_movies_list(self, links_instance):
        """Тест с пустым списком фильмов"""
        fields = ['name', 'director']
        
        result = links_instance.get_imdb([], fields)
        
        assert result == {}
    
    def test_get_imdb_empty_fields_list(self, links_instance, mock_soup_with_data):
        """Тест с пустым списком полей"""
        movie_ids = ['0113228']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, [])
            
            assert isinstance(result, dict)
    
    def test_get_imdb_no_script_tag(self, links_instance):
        """Тест случая отсутствия script тега"""
        movie_ids = ['0113228']
        fields = ['name', 'director']
        
        mock_soup = MagicMock()
        mock_soup.find.return_value = None
        
        with patch('links.get_page_by_movie', return_value=mock_soup):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert result == {}
    
    def test_get_imdb_invalid_json(self, links_instance):
        """Тест случая некорректного JSON"""
        movie_ids = ['0113228']
        fields = ['name', 'director']
        
        mock_soup = MagicMock()
        mock_script = MagicMock()
        mock_script.string = "invalid json"
        mock_soup.find.return_value = mock_script
        
        with patch('links.get_page_by_movie', return_value=mock_soup):
            with pytest.raises(json.JSONDecodeError):
                links_instance.get_imdb(movie_ids, fields)
    
    def test_get_imdb_result_sorting(self, links_instance, mock_soup_with_data):
        """Тест правильной сортировки результата"""
        movie_ids = ['0113228', '0114709', '0113497']
        fields = ['name']
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            keys = list(result.keys())
            assert keys == sorted(keys, reverse=True)
    
    def test_get_imdb_with_budget_and_gross(self, links_instance, mock_soup_with_data): # FAIL
        """Тест получения бюджета и сборов одновременно"""
        movie_ids = ['0113228']
        fields = ['name', 'budget', 'gross']
        
        mock_box_office = MagicMock()
        mock_box_office.text = "Budget $25,000,000 worldwide $71,000,000 See more"
        
        def side_effect(tag, attrs=None):
            if tag == 'script':
                return mock_soup_with_data.find.return_value
            elif attrs and attrs.get('data-testid') == 'BoxOffice':
                return mock_box_office
            return None
        
        mock_soup_with_data.find.side_effect = side_effect
        
        with patch('links.get_page_by_movie', return_value=mock_soup_with_data):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)


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
        
        with patch('links.get_page_by_movie', return_value=mock_soup):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
    
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
        
        with patch('links.get_page_by_movie', return_value=mock_soup):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)
    
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
        
        with patch('links.get_page_by_movie', return_value=mock_soup):
            result = links_instance.get_imdb(movie_ids, fields)
            
            assert isinstance(result, dict)


if __name__ == '__main__':
    pytest.main([__file__, '-v']) 