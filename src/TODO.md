# Ошибки которые были найдены и их описание

## Содержание

1. [(FIXED) Проблема при значении параметра n, больше чем количество фильмов в данных](#проблема-при-значении-параметра-n-больше-чем-количество-фильмов-в-данных) \
    1.1. [Описание](#описание) \
    1.2. [Пример](#пример) \
    1.3. [Предложения по фиксу](#предложения-по-фиксу)
2. [(FIXED) Проблема при отрицательном значении параметра n](#проблема-при-отрицательном-значении-параметра-n) \
    2.1. [Описание](#описание-1) \
    2.2. [Пример](#пример-1) \
    2.3. [Предложения по фиксу](#предложения-по-фиксу-1)

3. [Проблема в функции Links.longest() - несоответствие типов](#проблема-в-функции-linkslongest---несоответствие-типов) \
    3.1. [Описание](#описание-2) \
    3.2. [Пример](#пример-2) \
    3.3. [Предложения по фиксу](#предложения-по-фиксу-2) \
    3.4. [P.S.](#ps)
4. [(FIXED) Вопрос по movies.py](#вопрос-по-moviespy) \
    4.1. [Описание](#описание-3) \
    4.2. [В чем собственно вопрос](#в-чем-собственно-вопрос)
5. [(FIXED) Проблема с сортировкой словарей по убыванию](#fixed-проблема-с-сортировкой-словарей-по-убыванию) \
    5.1. [Описание](#описание-4) \
    5.2. [Пример](#пример-3) \
    5.3. [Предложения по фиксу](#предложения-по-фиксу-3)
___

## (FIXED) Проблема при значении параметра n, больше чем количество фильмов в данныхMore actions

### Описание

В функциях

```python
top_directors(self, n)
most_expensive(self, n)
most_profitable(self, n)
longest(self, n)
```

присутствует проблема при их вызове с аргументом ```n > len(data)```.

### Пример

```python
data = 
{
    "1": [100, 1500, "Film1"],
    "2": [1000000, 1111111, "Film2"],
    "3": [500, 499, "Film3"],
    "4": [500, 500, "Film4"],
    "5": [5, 10, "Film5"],
    "6": [7777, 6666, "Film6"],
    "7": [123123, 200000, "Film7"]
}
```

- Всего 7 фильмов, вызываем функцию ```most_profitable```

- Получаем ответ - та же самая ```data```:

```python
links_instance.most_profitable(12)
{
    '1': 15.0,
    '2': 1.111111,
    '3': 0.998,
    '4': 1.0,
    '5': 2.0,
    '6': 0.8571428571428571,
    '7': 1.6243918682943073,
}
```

### Предложения по фиксу

1. Выбрасывать исключение ```Exception("Parameter must be less or equal than the amount of data")```, которое можно будет ловить при тестах
2. Возвращать полную отсортированную ```data```, будто ```n == len(data)```

___

## (FIXED) Проблема при отрицательном значении параметра n

### Описание

В функциях

```python
top_directors(self, n)
most_expensive(self, n)
most_profitable(self, n)
longest(self, n)
```

присутствует проблема при их вызове с отрицательным значением параметра ```n```.

### Пример

```python
data = 
{
    "1": [100, 1500, "Film1"],
    "2": [1000000, 1111111, "Film2"],
    "3": [500, 499, "Film3"],
    "4": [500, 500, "Film4"],
    "5": [5, 10, "Film5"],
    "6": [7777, 6666, "Film6"],
    "7": [123123, 200000, "Film7"]
}
```

- Вызываем функцию most_profitable для ```n < 0```

- Получаем ответ - ```(len(data) + n) % len(data)``` записей в отсортированном виде(хотя в предыдущем случае, где ```n == len(data)``` вывод был не отсортирован):

То есть:

для ```n = -5``` получим 2 записи;
для ```n = -4``` получим 3 записи;
для ```n = -3``` получим 4 записи и т.д.

```python
links_instance.most_profitable(-5)
{
    '1': 15.0,
    '5': 2.0,
}
```

### Предложения по фиксу

1. Выбрасывать исключение ```Exception("Parameter must be greater than zero")```, которое можно будет ловить при тестах
2. Возвращать пустой ответ(вариант не очень, но не упомянуть не мог)

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

## (FIXED) Проблема с сортировкой словарей по убыванию

### Описание

В функциях класса Movies и Tags присутствует проблема: возвращаемый словарь не отсортирован по возрастанию.

### Пример

- Входные данные:

```bash
userId,movieId,tag,timestamp
62,3578,imdb top 250,1528152498
474,7834,Nick and Nora Charles,1137200666
573,4015,bad,1186589039
474,1381,high school,1137374154
474,1197,six-fingered man,1137202999
477,56174,Post apocalyptic,1262795695
474,2391,heist,1138032185
62,104863,zoe kazan,1528843965
477,42422,love,1252377761
567,4144,Unique,1525283560
474,5451,mental illness,1137375287
474,7217,amnesia,1137521621
474,912,start of a beautiful friendship,1137202319
474,1212,Venice,1143683500
474,30812,biopic,1138038949
474,912,start of a beautiful friendship,1137202319
474,912,start of a beautiful friendship,1137202319
474,912,start of a beautiful friendship,1137202319
474,912,start of a beautiful friendship,1137202319
```

- Вызываем функцию и смотрим вывод:

```python
most_words(3)

>>  {
>>      'Nick and Nora Charles': 4,
>>      'imdb top 250': 3,
>>      'start of a beautiful friendship': 5
>>  }
```

По заданию нужно сортировать по убыванию, тут почему-то по возрастанию, причем во всех функциях, где требуется сортировка.

### Предложения по фиксу

Предлагаю использовать ```OrderedDict``` из модуля ```collections```. Так словарь будет упорядоченный(то есть будет хранить порядок вставки элементов в него).

В тестах буду сравнивать с помощью списка кортежей:

1. Превращаю каждый элемент словаря в кортеж (ключ, значение)
2. Засовываю это все в список.
Все это делается с помощью ```list(result.items())```
3. Дальше просто сравниваю с отсортированной ```expected_data``` заранее приведенными к тому же виду

