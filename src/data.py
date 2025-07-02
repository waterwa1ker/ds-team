from utils.file_parser import FileParser
from utils.utils import get_class_name, convert_types

class Data:

    def __init__(self, file_path):

        self.data = []

        self.file_parser = FileParser()

        self.file_parser.file_exists(file_path)
        self.file_parser.file_empty(file_path)
        
        self.__open_file(file_path)

    def __open_file(self, file_path):
        with open(file_path, 'r') as f:
            header = f.readline().replace('\n', '')
            self.file_parser.check_headers(get_class_name(self), header)
            self.header = header
            for line in f:
                line = line.replace('\n', '')
                line_list = line.split(',')
                if '"' in line:
                    name = line[line.index('"') + 1:line.index('"', line.index('"') + 1)]
                    line_list = [line_list[0], name, line_list[-1]]
                # [line_list[0], tmp, line_list[-1]]
                self.file_parser.check_body_line(get_class_name(self), line_list)
                self.data.append(line_list)

    def convert_types(self, class_name):
        self.data = convert_types(self.data, class_name)