#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: rainsty
@file:   test_logger.py
@time:   2019-12-29 14:07:29
@description:
"""

import os
from pyrainsty import logger

base_path = os.path.dirname(__file__)
log_dir_name = 'logs'
log_file_name = 'canal.log'
logger = logger.Logger(base_path, log_dir_name, log_file_name)
logger = logger.get_logger()

logger.info('aaa')
try:
    a = 0/0
except BaseException as e:
    logger.exception(e)
