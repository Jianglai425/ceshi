import json


class ReadJson:
    def __init__(self, path: str) -> None:
        with open(path, 'r', encoding='utf-8') as f:
            self.__data = json.load(f)

    def get_all_data(self):
        return self.__data
