import json
import requests as re
from bs4 import BeautifulSoup as bs

class ImdbRequester:

    def __init__(self):
        pass

    def get_movie_info(self, list_of_movies, list_of_fields):

        movies_info = {}
        RIGHT_MOVIE_ID_LENGTH = 7
        additional_params = ['budget', 'gross']

        for movie in list_of_movies:

            # приводим movie_id к правильному значению. Иногда слева нужно добавлять ноль
            movie_id = f"{'0' * (RIGHT_MOVIE_ID_LENGTH - len(str(movie)))}{movie}"

            soup = self.__get_page_by_movie(movie_id)
            script_tag = soup.find('script', {'type': 'application/ld+json'})

            if script_tag:

                movie_info = []
                json_data = json.loads(script_tag.string)
                movie_name = None

                for field in list_of_fields:
                    field_value = json_data.get(field)
                    if field_value and field not in [additional_params, 'name']:
                        if field == 'director':
                            field_value = field_value[0]['name']
                        movie_info.append(field_value)
                    if field == 'name':
                        movie_name = field_value

                for additional_param in additional_params:
                    if additional_param in list_of_fields:
                        box_office_value = self.__get_info_from_box_office(soup, additional_param)
                        if box_office_value is not None:
                            movie_info.append(box_office_value)

                if movie_name and movie_name not in movies_info and movie_info:
                    movies_info[movie_name] = movie_info
                elif movie_id not in movies_info and movie_info:
                    movies_info[movie_id] = movie_info

        return movies_info


    def __get_info_from_box_office(self, soup, info_key):
        box_office_section = soup.find('section', {'data-testid': 'BoxOffice'})
        info_value = None

        if box_office_section is not None:
            box_office_text = box_office_section.text

            if info_key == 'budget':
                start_index = box_office_text.find('Budget') + len('Budget') + 1
                end_index = box_office_text[start_index:].find(' ') + start_index
            else:
                start_index = box_office_text.find('worldwide') + len('worldwide') + 1
                end_index = box_office_text[start_index:].find('See') + start_index

            info_value = box_office_text[start_index:end_index]
            info_value = int(info_value.replace(',', ''))

        return info_value

    def __get_page_by_movie(movie_id):

        link = f'https://www.imdb.com/title/tt{movie_id}/?ref_=vp_close'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        page = re.get(link, headers=headers)
        soup = bs(page.text, "html.parser")

        return soup
