import pymysql

from commom.read_config import ReadYaml
from run.data_path import DataPath


class Mysql:
    def __init__(self) -> None:
        self.__db = None
        self.__cursor = None
        y = ReadYaml(DataPath.data_path + "config/yamlData.yaml")
        self.__db = pymysql.connect(user=y.get_value("MySQL.user"), password=y.get_value("MySQL.password"),
                                    host=y.get_value("MySQL.host"), database=y.get_value("MySQL.database"),
                                    port=y.get_value("MySQL.port"), charset=y.get_value("MySQL.charset"))
        self.__cursor = self.__db.cursor()

    def __del__(self):
        if self.__db is not None:
            self.__db.close()
        if self.__cursor is not None:
            self.__cursor.close()

    def select(self, sql: str):
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    def delete(self, sql: str):
        self.__cursor.execute(sql)
        self.__db.commit()
        return self.__cursor.fetchall()
