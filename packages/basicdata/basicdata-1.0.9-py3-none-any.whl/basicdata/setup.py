#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='basicdata',
    version='1.0.9',
    author='William Ma',
    author_email='3327821469@qq.com',
    url='https://github.com/theCoder-WM',
    description=u'basic data for both Chinese and English  中英文的一些基本数据',
    packages=['basicdata'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'type_of_object=basicdata:type_of_object',
            'is_one_letter=basicdata:is_one_letter',
            'is_all_letter=basicdata:is_all_letter'
            'is_special_symbols=basicdata:is_special_symbols',
            'is_valid_phone_num=basicdata:is_valid_phone_num',
        ]
    }
)
