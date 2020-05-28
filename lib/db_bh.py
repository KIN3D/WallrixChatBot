# Автор: Krashe85 vk:@Krashe85
import pymysql.cursors

from jsons.reader import SettingsInType


class Base:
    def __init__(self):
        data = SettingsInType('db')
        self.server = data['server']
        self.user = data['user']
        self.base = data['base']
        self.password = data['pass']

    # подключение к бд
    def connect(self):
        connection = pymysql.connect(host=self.server, user=self.user, password=self.password,
                                     db=self.base, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        return connection

    # чтение таблицы
    def read_record(self, table, sample=False, value="", value_is_equal=""):
        connection = self.connect()
        with connection.cursor() as cursor:
            if sample:
                sql = "SELECT * FROM `{}` WHERE `{}` = %s".format(table, value)
                cursor.execute(sql, (value_is_equal))
            else:
                sql = "SELECT * FROM `{}`".format(table)
                cursor.execute(sql, )
            result = cursor.fetchall()
            return result

    # редактирование записи
    def edit_record(self, value):
        connection = self.connect()
        for i in range(len(value)):
            with connection.cursor() as cursor:
                sql = "UPDATE `{}`.`{}` SET `{}` = '{}' WHERE `{}` = '{}';".format(self.base, value[i]['table'],
                                                                                   value[i]['edit_param'],
                                                                                   value[i]['edit_new_param'],
                                                                                   value[i]['value'],
                                                                                   value[i]['value_is_equal'])
                cursor.execute(sql, )
                connection.commit()
        connection.close()

    # создание записи
    def create_record(self, table, value):
        connection = self.connect()
        param = ""
        key = ""
        for i in value.keys():
            param += "`{}`, ".format(i)
            key += "'{}', ".format(value[i])
        param = param[:len(param) - 2]
        key = key[:len(key) - 2]
        with connection.cursor() as cursor:
            sql = "INSERT INTO `{}` ({}) VALUES ({});".format(table, param, key)
            cursor.execute(sql, )
            result = cursor.fetchone()
            connection.commit()
            connection.close()
            return result

    # Последние N записей
    def last_read_record(self, table, n):
        connection = self.connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM (SELECT * FROM {} ORDER BY id DESC LIMIT {}) t ORDER BY id;".format(table, n)
            cursor.execute(sql,)
            result = cursor.fetchall()
            return result
