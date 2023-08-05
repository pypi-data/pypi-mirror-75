#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: rainsty
@file:   test_ifparams.py
@time:   2020-01-16 15:44:29
@description:
"""

from pyrainsty import ifparams

try:
    ICP = ifparams.IfParamsCheck()

    a = ICP.check_int(name='a', value='1')
    b = ICP.check_float(name='b', value='11.0940001')
    c = ICP.check_range_int(name='c', value='10', _range='(1, 10]')
    d = ICP.check_range_float(name='d', value='10.11', _range='(1, 10.11]')
    e = ICP.check_datetime_format(name='e', value='2020-01-01', _format='%Y-%m-%d')
    f = ICP.check_in_list(name='f', value=1, _list=[1, 2, 3])
    g = ICP.check_in_regex(name='g', value='aaa', _regex=r'a.*')
    h = ICP.check_in_regex(name='h', value='127.6.0.10', _regex=ICP.get_regex_str('ipv4'))

    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)
    print(g)
    print(h)
    print(ifparams.IfParamsCheck.__doc__)
except ifparams.ParamError as e:
    print(e.name)
    print(e.desc)
