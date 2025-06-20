from utils.file_parser import FileParser
from utils.utils import get_class_name, get_column_index, print_file, convert_types

class Data:

    def __init__(self, file_path):

        self.data = []

        self.file_parser = FileParser()

        self.file_parser.file_exists(file_path)
        self.file_parser.file_empty(file_path)
        
        self.__open_file(file_path)


    def sort_by_column(self, column_name, reverse = False):
        self.file_parser.check_column_name(get_class_name(self), column_name)

        column_index = get_column_index(self.header, column_name)
        tmp_data = sorted(self.data, key = lambda x: x[column_index], reverse = reverse)
        print_file(self.header, tmp_data) #do we need this???

    def __open_file(self, file_path):
        with open(file_path, 'r') as f:
            header = f.readline().replace('\n', '')
            self.file_parser.check_headers(get_class_name(self), header)
            self.header = header
            for line in f:
                line = line.replace('\n', '')
                line_list = line.split(',')
                self.file_parser.check_body_line(get_class_name(self), line_list)
                self.data.append(line_list)

    def convert_types(self, class_name):
        self.data = convert_types(self.data, class_name)