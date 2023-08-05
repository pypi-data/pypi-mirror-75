#!/usr/bin/env python

from distutils.core import setup

setup(name='am_get',
      version='2.0',
      description='request method for amazon spider',
      author='morbosohex',
      packages=['am_get'],
      install_requires=[          # 添加了依赖的 package
        'beautifulsoup4',
        'six',
        'requests',
        'loguru',
        'lxml',
        'html5lib'
    ])