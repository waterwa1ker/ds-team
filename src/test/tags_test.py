import pytest
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from tags import Tags
from exceptions.invalid_number_exception import InvalidNumberException

@pytest.fixture
def tags_instance_default():
    tags_file = f"{project_root}/info/tags.csv"
    return Tags(tags_file)

class TestMostWords:
    def test_most_words_default(self, tags_instance_default):
        expected_data = [
            ('start of a beautiful friendship', 5),
            ('Nick and Nora Charles', 4),
            ('imdb top 250', 3)
        ]
        result = tags_instance_default.most_words(3)
    
        assert isinstance(result, dict)
        assert len(result) == 3
        assert list(result.items()) == expected_data
    
    def test_most_words_zero(self, tags_instance_default):
        with pytest.raises(InvalidNumberException) as exc_info:
            tags_instance_default.most_words(0)
        assert 'Number must be natural number' == exc_info.value.args[0]

    def test_most_words_negative(self, tags_instance_default):
        with pytest.raises(InvalidNumberException) as exc_info:
            tags_instance_default.most_words(-7)
        assert 'Number must be natural number' == exc_info.value.args[0]

    def test_most_words_parameter_bigger(self, tags_instance_default):
        with pytest.raises(InvalidNumberException) as exc_info:
            tags_instance_default.most_words(100)
        assert 'Number must be less than length' == exc_info.value.args[0]

if __name__ == "__main__":
    pytest.main([__file__, '-v']) 
