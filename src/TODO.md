# Ошибки которые были найдены и их описание

## Содержание

1. [Проблема в функции Links.longest() - несоответствие типов](#проблема-в-функции-linkslongest---несоответствие-типов) \
    1.1. [Описание](#описание) \
    1.2. [Пример](#пример) \
    1.3. [Предложения по фиксу](#предложения-по-фиксу) \
    1.4. [P.S.](#ps)
2. [Вопрос по movies.py](#вопрос-по-moviespy) \
    2.1. [Описание](#описание-1) \
    2.2. [В чем собственно вопрос](#в-чем-собственно-вопрос)
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

## Вопрос по movies.py

### Описание

Функции

```python
dist_by_release()
dist_by_genres()
```

тестил по одному разу, по файлу info/movies.csv.

Функцию

```python
most_genres(n)
```

тестил чуть поболее, но тоже не особо.

### В чем собственно вопрос

```pytest-cov``` говорит мне, что покрытие 100%:

```bash
Name                                                                                  Stmts   Miss  Cover
---------------------------------------------------------------------------------------------------------
/Users/antonylo/Desktop/projects/ds-team/src/constants/body_constants.py                  3      0   100%
/Users/antonylo/Desktop/projects/ds-team/src/data.py                                     21      0   100%
/Users/antonylo/Desktop/projects/ds-team/src/exceptions/invalid_number_exception.py       3      0   100%
/Users/antonylo/Desktop/projects/ds-team/src/imdb_requester.py                           55      6    89%
/Users/antonylo/Desktop/projects/ds-team/src/links.py                                    52      1    98%
/Users/antonylo/Desktop/projects/ds-team/src/movielens_analysis.py                        9      9     0%
/Users/antonylo/Desktop/projects/ds-team/src/movies.py                                   39      0   100% <<<<<< вот тут
/Users/antonylo/Desktop/projects/ds-team/src/ratings.py                                  61     61     0%
/Users/antonylo/Desktop/projects/ds-team/src/tags.py                                     40     40     0%
/Users/antonylo/Desktop/projects/ds-team/src/utils/converter.py                          21      0   100%
/Users/antonylo/Desktop/projects/ds-team/src/utils/file_parser.py                        31      9    71%
/Users/antonylo/Desktop/projects/ds-team/src/utils/utils.py                              44      3    93%
links_test.py                                                                           385      4    99%
movies_test.py                                                                           54      1    98%
---------------------------------------------------------------------------------------------------------
TOTAL                                                                                   818    134    84%
```

и мне с этим тяжело согласиться, так как я не тестил функции на невалидные данные.

Вот собственно и вопрос. Нужно ли мне тестить функции на хуевых данных? Или у тебя просто такие данные на этапе конструктора нахуй посылаются?