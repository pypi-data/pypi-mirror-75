# file: ezmysql.py
# Author: eamonn
import pyodbc


class SqlServerOdbc(object):

    def __init__(self, host, user, password, database):

        conn_info = 'DRIVER={SQL Server};DATABASE=%s;SERVER=%s;UID=%s;PWD=%s' % (database, host, user, password)
        self.cnxn = pyodbc.connect(conn_info)
        self.cursor = self.cnxn.cursor()

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.cnxn:
            self.cnxn.close()

    def get(self, sqlStr, *args):
        """
        获取一条查询结果
        :param sqlStr:
        :return:
        """
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        self.cursor.execute(sqlStr, *args)
        return self.cursor.fetchone()

    def get_dict(self, sqlStr, *args):
        """
        导出一条查询结果，并转成字典类型
        :param sqlStr:
        :param args:
        :return:
        """
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        rows = self.get(sqlStr, *args)
        columns = [column[0] for column in self.cursor.description]
        return dict(zip(columns, rows))

    def query(self, sqlStr, *args, max_count=None):
        """
        获取全部查询结果
        :param sqlStr:
        :param max_count: 查询数据量
        :return:
        """
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        self.cursor.execute(sqlStr, *args)
        if max_count:
            return self.cursor.fetchmany(max_count)
        return self.cursor.fetchall()

    def query_dict(self, sqlStr, *args, max_count=None):
        """
        导出全部查询结果，并转成字典类型
        :param sqlStr:
        :param args:
        :param max_count:
        :return:
        """
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        results = list()
        rows = self.query(sqlStr, *args, max_count=max_count)
        columns = [column[0] for column in self.cursor.description]
        for row in rows:
            results.append(dict(zip(columns, row)))
        return results

    def query_page(self, sqlStr, *args, page_size=100, page=0):
        """
        获取分页查询结果
        :param sqlStr:
        :param page: 页码
        :param page_size: 页码大小
        :return:
        """
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        self.cursor.execute(sqlStr, *args)
        self.cursor.skip(page * page_size)
        return self.cursor.fetchmany(page_size)

    def count(self, sqlStr, *args):
        """
        获取查询条数
        :param sqlStr:
        :return:
        """
        import re
        pattern = re.compile("SELECT (.*?) FROM", re.IGNORECASE)
        result = re.findall(pattern, sqlStr)[0]
        sqlStr = sqlStr.replace(result, "count(0)")
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        self.cursor.execute(sqlStr, *args)
        return self.cursor.fetchone()[0]

    def execute(self, sqlStr, *args):
        """
        执行sql语句
        :param sqlStr:
        :param args:
        :return:
        """
        if "%s" in sqlStr:
            sqlStr = sqlStr.replace("%s", "?")
        cnt = self.cursor.execute(sqlStr, *args).rowcount
        self.cnxn.commit()
        return cnt

    def insert(self, table_name, item):
        """
        插入数据
        :param table_name:  数据表名
        :param item: 字典类型数据
        :return:
        """
        keys, values = zip(*item.items())
        sqlStr = None
        try:
            sqlStr = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, ",".join(keys), ",".join(["?"] * len(values)))
            self.execute(sqlStr, *values)
        except Exception as e:
            print(sqlStr)
            print(e)

    def insert_many(self, table_name, items):
        """
        插入多条数据
        :param table_name: 数据表名
        :param items: 列表类型数据
        :return:
        """
        if isinstance(items, list):
            for item in items:
                self.insert(table_name, item)

    def update(self, table_name, updates, search):
        """
        更新数据
        :param table_name: 表名
        :param updates:需要更新的字段
        :param search:查询条件
        :return:
        """
        upsets = []
        values = []
        for k, v in updates.items():
            s = '%s=?' % k
            upsets.append(s)
            values.append(v)
        upsets = ' , '.join(upsets)

        searchsets = []
        for k, v in dict(search).items():
            s = "%s='%s'" % (k, v)
            searchsets.append(s)
        searchsets = ' and '.join(searchsets)

        sqlStr = f'UPDATE %s SET %s WHERE {searchsets}' % (
            table_name,
            upsets
        )
        self.execute(sqlStr, *values)
