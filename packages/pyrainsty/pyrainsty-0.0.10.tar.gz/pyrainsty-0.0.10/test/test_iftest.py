#!/usr/bin/python
# encoding: utf-8

"""
@author: rainsty
@file:   test_configuration.py
@time:   2019-09-30 10:44
@description:
"""

from pyrainsty.iftest import InterfaceTest

test_host = '39.100.82.18'
test_port = 31480
version = 'v1.0.20'


class APITest(InterfaceTest):

    def configuration(self, path='/configuration/'):
        return self.get_request(path=path, title='配置-获取配置信息')


if __name__ == '__main__':
    api = APITest('http://{}:{}/api/'.format(test_host, test_port), version)
    api.configuration()
