#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='jindutiao',
    version='0.2b0',
    author='William Ma',
    author_email='3327821469@qq.com',
    url='https://github.com/theCoder-WM',
    description=u'进度条ProgressBar',
    packages=['jindutiao'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'jindutiao=jindutiao:progress_bar',
        ]
    }
)
