#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: rainsty
@file:   test.py
@time:   2019-12-29 11:00:29
@description:
"""

from pyrainsty import connect


def main():
    config = dict(
        host='39.100.82.18',
        port=33306,
        user='root',
        password='qwerty123!@#...',
        database='rainsty',
        charset='utf8'
    )

    mc = connect.MysqlConnect(config)
    mc.create_connect()
    mc.close_connect()
    mc.check_connect()
    state, result = mc.get_data('select * from info_re_basinfo limit 1')
    if not state:
        print(result)

    print(result)
    cursor = mc.get_cursor
    cursor.execute('select * from info_re_basinfo limit 1')
    data = cursor.fetchall()
    for d in data:
        print(d)


if __name__ == '__main__':
    main()
