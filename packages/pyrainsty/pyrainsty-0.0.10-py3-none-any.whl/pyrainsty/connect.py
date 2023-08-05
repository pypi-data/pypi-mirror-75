#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: rainsty
@file:   connect.py
@time:   2019-12-29 10:06:29
@description: connect data source
"""

import pymysql


class MysqlConnect(object):
    """
    example:
        from pyrainsty import connect
        config = dict(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            database='test',
            charset='utf8'
        )

        mc = connect.MysqlConnect(config)
        mc.create_connect()
        state, result = mc.get_data('select * from test.test limit 1')
        if not state:
            print('error')
        else:
            print(result)
    """

    def __init__(self, _config, **kwargs):
        self.__config = _config
        self.__kwargs = kwargs
        self.__conn = None
        self.__cursor = None

    @property
    def get_conn(self):
        return self.__conn

    @property
    def get_cursor(self):
        return self.__cursor

    def create_connect(self):
        self.__conn = pymysql.Connection(**self.__config, **self.__kwargs)
        self.__cursor = self.__conn.cursor()

    def check_connect(self):
        try:
            self.__conn.ping()
        except (AttributeError,):
            self.create_connect()

    def close_connect(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__conn:
            self.__conn.close()
        self.__cursor = None
        self.__conn = None

    def __del__(self):
        self.close_connect()

    def get_data(self, sql, params=None):
        try:
            self.check_connect()
            if params:
                self.__cursor.execute(sql, params)
            else:
                self.__cursor.execute(sql)

            _data = self.__cursor.fetchall()
            _column = self.__cursor.description

            _result = [dict(zip([column[0] for column in _column], data)) for data in _data]
            return True, _result
        except BaseException as _e:
            return False, _e

    def exec_cmd(self, sql, params=None):
        try:
            self.check_connect()
            if params:
                self.__cursor.executemany(sql, params)
            else:
                self.__cursor.execute(sql)
            self.__conn.commit()
            return True, None
        except BaseException as _e:
            self.__conn.rollback()
            return False, _e
