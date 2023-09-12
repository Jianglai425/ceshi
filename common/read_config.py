import yaml


class ReadYaml:

    def __init__(self, path: str) -> None:
        """
        根据路径读取yaml文件
        :param path:
        """
        with open(path, 'r', encoding='utf-8') as f:
            self.__result = yaml.load(f.read(), Loader=yaml.FullLoader)

    def get_value(self, key: str):
        key_list = key.split(".")
        if len(key_list) == 1:
            return self.__result.get(key_list[0])
        else:
            data = self.__result.get(key_list[0])
            for i in range(1, len(key_list)):
                data = data.get(key_list[i])
            return data

    def get_all_yaml(self):
        return self.__result

    def print_yaml_file(self):
        print(self.__result)
