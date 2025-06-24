from data import Data
from utils.utils import get_class_name

class Tags(Data):

    def __init__(self, file_path):
        super().__init__(file_path)
        self.convert_types(get_class_name(self))

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict
 where the keys are tags and the values are the number of words inside the tag.
 Drop the duplicates. Sort it by numbers descendingly.
        """
        big_tags = {}

        tags = self.__get_tags()
        for tag in tags:
            big_tags[tag] = len(tag.split(" "))
        return dict(sorted(big_tags.items(), key=lambda x: x[1], reverse=True)[:n])

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        tags = self.__get_tags()

        return list(sorted(tags, key=lambda x: len(x), reverse=True)[:n])

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        # Не понял, что сделать надо. Какой-то тупизм если честно
        
        return big_tags

    def most_popular(self, n):
        """
        The method returns the most popular tags.
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        
        popular_tags = {}
        tags = self.__get_tags()
        for tag in tags:
            if tag in popular_tags:
                popular_tags[tag] += 1
            else:
                popular_tags[tag] = 1
        return dict(sorted(popular_tags.items(), key=lambda x: x[1], reverse=True)[:n])

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        
        tags_with_word = []
        tags = self.__get_tags()
        for tag in tags:
            if word in tag and tag not in tags_with_word:
                tags_with_word.append(tag)
        return list(sorted(tags_with_word))

    def __get_tags(self):
        return list(map(lambda x: x[2], self.data))
