from sys import path

from constants.body_constants import body_types

path.append("..")

def get_class_name(object):
    return type(object).__name__

def get_list_types(data):
    list_types = []
    for element in data:
        if element.isdigit():
            list_types.append('int')
        else:
            element = element.replace('.', '')
            if element.isdigit():
                list_types.append('float')
            else:
                list_types.append('str')
    return list_types

def get_column_index(header, column_name):
    return header.split(',').index(column_name)

def print_file(header, data):
    print(header)
    for line in data:
        print(line)

def convert_types(body, class_type):
    result = []
    for line in body:
        result_line = []
        for i in range(len(line)):
            right_element_type = body_types[class_type][i]
            if right_element_type == 'int':
                result_line.append(int(line[i]))
            elif right_element_type == 'float':
                result_line.append(float(line[i]))
            else:
                result_line.append(line[i])
        result.append(result_line)
    return result

def compare_duration(duration):
    hours = duration[duration.find('T')+1:duration.find('H')]
    minutes = duration[duration.find('H')+1:duration.find('M')]
    
    return hours * 60 + minutes