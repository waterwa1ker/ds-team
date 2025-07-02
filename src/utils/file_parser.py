from os import path as os_path
from sys import path

from utils.utils import get_list_types, convert_types
from constants.body_constants import headers, columns, body_types

path.append("..")

class FileParser:

    def __init__(self):
        pass

    def file_exists(self, file_path):
        
        if not os_path.isfile(file_path):
            raise Exception(f'File {file_path} not exists')

    def file_empty(self, file_path):

        TO_BITS = 8

        if os_path.getsize(file_path) * TO_BITS == 0:
            raise Exception(f'File {file_path} is empty')


    def check_headers(self, class_type, header):

        if headers[class_type] != header:
            raise Exception(f'Invalid header: for {class_type} class headers should be {headers[class_type]}')

    def check_column_name(self, class_type, column_name):

        try:
            columns[class_type].index(column_name)
        except:
            raise Exception(f"Column {column_name} isn't store in {class_type}.csv")

    def check_body_line(self, class_type, body_list):

        is_correct_data_len = len(body_list) == len(body_types[class_type])
        if not is_correct_data_len:
            raise Exception(f'Data should contain {len(body_types[class_type])} elements in line, {len(body_list), body_list}')

        tuple_types = get_list_types(body_list)
        is_correct_types = tuple_types == body_types[class_type]
        if not is_correct_types:
            raise Exception(f'Incorrect type in line {body_list}')