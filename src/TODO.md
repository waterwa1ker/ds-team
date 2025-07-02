# Ошибки которые были найдены и их описание

## Содержание

1. [Проблема в функции Links.longest() - несоответствие типов](#проблема-в-функции-linkslongest---несоответствие-типов) \
    1.1. [Описание](#описание) \
    1.2. [Пример](#пример) \
    1.3. [Предложения по фиксу](#предложения-по-фиксу) \
    1.4. [P.S.](#ps)

___

## Проблема в функции Links.longest() - несоответствие типов

### Описание

В функции

```python
longest(self, n)
```

присутствует проблема при ее вызове, т.к. она работает с функцией ```get_imdb```, которая возвращает список(!), а не словарь.

### Пример

```python
data = 
{
    "The Shawshank Redemption": ["PT1H33M"],
    "The Godfather": ["PT1H41M"],
    "The Dark Knight": ["PT1H39M"],
    "Pulp Fiction": ["PT2H1M"],
    "Inception": ["PT0H30M"],
    "Goodfellas": ["PT1H59M"],
    "The Silence of the Lambs": ["PT1H12M"],
    "Se7en": ["PT3H7M"],
    "Fight Club": ["PT1H0M"],
    "The Matrix": ["PT1H28M"]
}
```

- Вызов функции с любым параметром дает ошибку

```bash
>       return dict(sorted(movies.items(), key=lambda x: self.converter.convert_duration(x[1][0]), reverse = True)[:n])
E       AttributeError: 'list' object has no attribute 'items'

../links.py:82: AttributeError
======================================================================================================== short test summary info =========================================================================================================
FAILED links_test.py::TestLongest::test_longest_default - AttributeError: 'list' object has no attribute 'items'
```

### Предложения по фиксу

1. исправить функцию, чтобы работала со списком, а не словарем

### P.S.

если вдруг думаешь, что у меня данные неверные, то скорее всего ты ошибаешься, т.к. я мокирую метод get_movie_info, а он возвращает словарь, так что все ок там

___
