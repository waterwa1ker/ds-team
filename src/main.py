# line = '55080,"Brave One, The (2007), aaaaaaaa",Crime|Drama|Thriller'.split(',')

# quotes_elements = list(filter(lambda x: '"' in x, line))
# a = list(map(lambda x: line.index(x), quotes_elements))
# print(a)
# print(quotes_elements)
# quotes_elements = ",".join(line)[a[0]:a[1]]

# print(quotes_elements)


line = '55080,Brave One, The (2007), aaaaaaaa,Crime|Drama|Thriller'

name = line[line.index('"') + 1:line.index('"', line.index('"') + 1)]
print(name)