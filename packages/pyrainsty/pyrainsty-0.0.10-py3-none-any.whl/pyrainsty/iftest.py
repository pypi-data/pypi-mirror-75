#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: rainsty
@file:   iftest.py
@time:   2019-12-29 15:00:29
@description: interface test
"""

import json
import requests


class InterfaceTest(object):
    """
    example:
        from pyrainsty.iftest import InterfaceTest

        test_host = '127.0.0.1'
        test_port = 5000
        version = 'v1.0.20'


        class APITest(InterfaceTest):

            def configuration(self, path='/configuration/'):
                return self.get_request(path=path, title='配置-获取配置信息')


        if __name__ == '__main__':
            api = APITest('http://{}:{}/api/'.format(test_host, test_port), version)
            api.configuration()

    """
    def __init__(self, base_url, version='', username=None, password=None, is_login=False):
        self.base_url = base_url + version if version else ''
        self.username = username
        self.password = password
        self.token = ''
        self.is_login = is_login
        self.login()

    @property
    def headers(self):
        return {'content-type': 'application/json', 'Http-Authorization': self.token, 'Connection': 'close'}

    def content(self, path=None, method=None, payload=None, title=None, request_desc=None, resp_data=None):
        print('')
        print('# {}'.format(title))
        print('')
        print('* 地址: **{}**  '.format(path))
        print('* 请求: **{}**  '.format(method.upper()))
        if payload:
            print('* 参数:  ')
            print('')
            print('```')
            print(json.dumps(payload, ensure_ascii=False, indent=4))
            print('```')
            print('')
            print('* 参数说明:  ')
            print('')
            print('''|参数|类型|说明|是否必填|备注|\n|---|---|---|---|---|''')
            for k, v in payload.items():
                print('''|{}|{}||0|无|'''.format(k, str(type(v)).split('\'')[1].split('\'')[0]))
        if request_desc:
            print(request_desc)
        print('')
        print('* 返回值:  ')
        print('')
        print('```')
        print(json.dumps(resp_data, ensure_ascii=False, indent=4))
        print('```')
        print('')
        if 'data' in resp_data:
            error = None
            try:
                error = resp_data['data'][0].items()
                print('* 返回值说明  ')
                print('')
                print('''|参数|类型|说明|备注|\n|---|---|---|---|''')
                if isinstance(resp_data['data'], dict):
                    for k, v in resp_data['data'].items():
                        print('''|{}|{}||无|'''.format(k, str(type(v)).split('\'')[1].split('\'')[0]))
                elif isinstance(resp_data['data'], list):
                    for k, v in resp_data['data'][0].items():
                        print('''|{}|{}||无|'''.format(k, str(type(v)).split('\'')[1].split('\'')[0]))
            except BaseException as e:
                print(e, error)

    def get_request(self, path=None, payload=None, request_desc=None, title=None):
        print('')
        print(self.base_url + path)
        response = requests.get(
            url=self.base_url + path, params=payload, headers=self.headers)
        response_data = response.json()
        self.content(
            path=path, method='get', payload=payload, title=title,
            resp_data=response_data, request_desc=request_desc)
        return response_data

    def post_request(self, path=None, payload=None, request_desc=None, title=None):
        print('')
        print(self.base_url + path)
        response = requests.post(
            url=self.base_url + path, data=json.dumps(payload), headers=self.headers)
        response_data = response.json()
        self.content(
            path=path, method='post', payload=payload, title=title,
            resp_data=response_data, request_desc=request_desc)
        return response_data

    def put_request(self, path=None, payload=None, request_desc=None, title=None):
        print('')
        print(self.base_url + path)
        response = requests.put(
            url=self.base_url + path, data=json.dumps(payload), headers=self.headers)
        response_data = response.json()
        self.content(
            path=path, method='put', payload=payload, title=title,
            resp_data=response_data, request_desc=request_desc)
        return response_data

    def del_request(self, path=None, payload=None, request_desc=None, title=None):
        print('')
        print(self.base_url + path)
        response = requests.delete(
            url=self.base_url + path, data=json.dumps(payload), headers=self.headers)
        response_data = response.json()
        self.content(
            path=path, method='delete', payload=payload, title=title,
            resp_data=response_data, request_desc=request_desc)
        return response_data

    def login(self, path='/login'):
        """You can override this method..."""
        if self.is_login:
            print('')
            print(self.base_url + path)
            payload = dict(
                username=self.username if self.username else 'admin',
                password=self.password if self.password else '123456'
            )
            response = requests.post(
                url=self.base_url + path, data=json.dumps(payload), headers=self.headers)
            response_data = response.json()
            self.token = response_data.get('token', '')
            print(self.token)
        else:
            print('No login...')
