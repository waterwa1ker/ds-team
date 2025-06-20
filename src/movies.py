from data import Data
from utils.utils import get_class_name

class Movies(Data):
    
    def __init__(self, file_path):
        super().__init__(file_path)
        self.convert_types(get_class_name(self))   