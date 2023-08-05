#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: rainsty
@file:   ifparams.py
@time:   2020-01-16 15:36:29
@description: interface params check
"""

import re
import datetime


class ParamError(BaseException):
    """
    Common base class for all non-exit exceptions.
    """

    def __init__(self, *args, **kwargs):
        self.desc = args[0]
        self.name = kwargs.get('name', None)
        self.value = kwargs.get('value', None)


class IfParamsCheck(object):
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
        h = ICP.check_in_regex(name='h', value='127.6.0.1a', _regex=ICP.get_regex_str('ipv4'))

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

    """

    def __init__(self):
        self.param_error = ParamError

    @staticmethod
    def get_regex_str(key=None):
        _dict = dict(
            ipv4=r'((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)',
        )
        if key:
            return _dict.get(key, '')
        return _dict

    def _not_in_value_range_error(self, name=None, _range=None):
        return self.param_error('The value of {} not in {}.'.format(name, _range))

    def _not_range_error(self):
        return self.param_error('The type of str param _range is not found.')

    def _not_in_value_list_error(self, name=None, _list=None):
        return self.param_error('The value of {} not in {}.'.format(name, _list))

    def _not_list_error(self):
        return self.param_error('The type of list param _list is not found.')

    def _not_str_type_error(self):
        return self.param_error('The type of param is not str.')

    def _not_regex_error(self):
        return self.param_error('The regex is not None.')

    def _not_regex_result_error(self):
        return self.param_error('The regex is not result.')

    def _check_range(self, _range=None):
        if not _range:
            raise self._not_range_error()
        _range = _range.strip()
        _range_result = re.sub(r'[ ]|[(]|[)]|[\[]|[\]]', '', _range)
        _range_result = _range_result.split(',')
        return _range, _range_result

    def _check_list(self, _list=None):
        if not _list:
            raise self._not_list_error()
        return _list

    def _check_regex(self, value=None, _regex=None):
        if not _regex:
            raise self._not_regex_error()
        result = re.match(_regex, value)
        if result:
            return result.group()
        else:
            return None

    def check_int(self, name=None, value=None):
        """
        :desc   a = ICP.check_int(name='a', value='1')

        :param name: The param`s name.
        :param value: The param`s value.
        :return: int(param)
        """
        try:
            value = int(value)
            return value
        except BaseException as e:
            raise self.param_error('ParamError: {}'.format(e), name=name, value=value)

    def check_float(self, name=None, value=None, length=None):
        """
        :desc   b = ICP.check_float(name='b', value='11.0940001')

        :param name: The param`s name.
        :param value: The param`s value.
        :param length: The length
        :return: int(param)
        """
        try:
            if length:
                value = float('%.{}f'.format(length) % float(value))
            else:
                value = float(value)
            return value
        except BaseException as e:
            raise self.param_error('ParamError: {}'.format(e), name=name, value=value)

    def check_range_int(self, name=None, value=None, _range=None):
        """
        :desc   c = ICP.check_range_int(name='c', value='10', _range='(1, 10]')

        :param name: The param`s name.
        :param value: The param`s value.
        :param _range: '(1, 2]'
        :return: int(param)
        """
        try:

            value = int(value)

            _range, _range_result = self._check_range(_range)

            if _range[0] == '(':
                if value <= int(_range_result[0]):
                    raise self._not_in_value_range_error(name=name, _range=_range)

            if _range[0] == '[':
                if value < int(_range_result[0]):
                    raise self._not_in_value_range_error(name=name, _range=_range)

            if _range[-1] == ')':
                if value >= int(_range_result[1]):
                    raise self._not_in_value_range_error(name=name, _range=_range)

            if _range[-1] == ']':
                if value > int(_range_result[1]):
                    raise self._not_in_value_range_error(name=name, _range=_range)

            return value
        except BaseException as e:
            raise self.param_error('ParamError: {}'.format(e), name=name, value=value)

    def check_range_float(self, name=None, value=None, length=None, _range=None):
        """
        :desc   d = ICP.check_range_float(name='d', value='10.1', length=10, _range='(1, 10.11)')

        :param name: The param`s name.
        :param value: The param`s value.
        :param length: The length
        :param _range: '(1, 2]'
        :return: int(param)
        """
        try:
            if not _range:
                raise self._not_range_error()

            if length:
                value = float('%.{}f'.format(length) % float(value))
            else:
                value = float(value)

            _range, _range_result = self._check_range(_range)

            if _range[0] == '(':
                if value <= float(_range_result[0]):
                    raise self._not_in_value_range_error(name=name, _range=_range)

            if _range[0] == '[':
                if value < float(_range_result[0]):
                    raise self._not_in_value_range_error(name=name, _range=_range)

            if _range[-1] == ')':
                if value >= float(_range_result[1]):
                    raise self._not_in_value_range_error(name=name, _range=_range)

            if _range[-1] == ']':
                if value > float(_range_result[1]):
                    raise self._not_in_value_range_error(name=name, _range=_range)

            return value
        except BaseException as e:
            raise self.param_error('ParamError: {}'.format(e), name=name, value=value)

    def check_datetime_format(self, name=None, value=None, _format='%Y-%m-%d %H:%M:%S'):
        """
        :desc   e = ICP.check_datetime_format(name='e', value='2020-01-01', _format='%Y-%m-%d')

        :param name: The param`s name.
        :param value: The param`s value.
        :param _format:
        :return: int(param)
        """
        try:
            _value = datetime.datetime.strptime(value, _format)
            return value
        except BaseException as e:
            raise self.param_error('ParamError: {}'.format(e), name=name, value=value)

    def check_in_list(self, name=None, value=None, _list=None):
        """
        :desc   f = ICP.check_in_list(name='f', value=1, _list=[1, 2, 3])

        :param name: The param`s name.
        :param value: The param`s value.
        :param _list:
        :return: int(param)
        """
        try:
            _list = self._check_list(_list)
            if value not in _list:
                raise self._not_in_value_list_error(name=name, _list=_list)
            return value
        except BaseException as e:
            raise self.param_error('ParamError: {}'.format(e), name=name, value=value)

    def check_in_regex(self, name=None, value=None, _regex=None):
        """
        :desc   g = ICP.check_in_regex(name='g', value='aaa', _regex=r'a.*')

        :param name: The param`s name.
        :param value: The param`s value.
        :param _regex
        :return: int(param)
        """
        try:
            if not isinstance(value, str):
                raise self._not_str_type_error()

            result = self._check_regex(value=value, _regex=_regex)
            if result != value:
                raise self._not_regex_result_error()
            return value
        except BaseException as e:
            raise self.param_error('ParamError: {}'.format(e), name=name, value=value)
