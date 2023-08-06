# file: ezmssql.py
# Author: eamonn
import pymssql


class SqlServer(object):
    """A lightweight wrapper around SqlServer.
    """

    def __init__(self, host, user, password, database):
        self.__conn_list = pymssql.connect(host=host, user=user, password=password, database=database,
                                         charset="utf8")
        self.__conn_dict = pymssql.connect(host=host, user=user, password=password, database=database,
                                         charset="utf8", as_dict=True)

    def execute(self, sql, *parameters, **kwparameters):
        with self.__conn_list.cursor() as cursor:
            cursor.execute(sql, kwparameters or parameters)
            self.__conn_list.commit()

    def get(self, sql, values=None):
        with self.__conn_list.cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone()

    def get_dict(self, sql, values=None):
        with self.__conn_dict.cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone()

    def query(self, sql, values=None):
        with self.__conn_list.cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchall()

    def query_dict(self, sql, values=None):
        with self.__conn_dict.cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchall()

    def __insert(self, sql, values=None):
        with self.__conn_list.cursor() as cursor:
            cursor.execute(sql, values)
            self.__conn_list.commit()

    def insert(self, table_name, item):
        keys, values = zip(*item.items())
        try:
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, ",".join(keys), ",".join(["%s"] * len(values)))
            self.__insert(sql, values)
        except Exception as e:
            print(sql)
            print(e)

    def insert_many(self, table_name, items):
        if isinstance(items, list):
            for item in items:
                self.insert(table_name, item)

    def update(self, table_name, updates, search):
        upsets = []
        values = []
        for k, v in updates.items():
            s = '%s=%%s' % k
            upsets.append(s)
            values.append(v)
        upsets = ' , '.join(upsets)

        searchsets = []
        for k, v in dict(search).items():
            s = "%s='%s'" % (k, v)
            searchsets.append(s)
        searchsets = ' and '.join(searchsets)


        sql = f'UPDATE %s SET %s WHERE {searchsets}' % (
            table_name,
            upsets
        )
        self.execute(sql, *values)

