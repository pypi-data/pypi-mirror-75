#!/usr/bin/env python

from distutils.core import setup

setup(name='amz_query',
      version='1.0',
      description='request method for amazon spider',
      author='morbosohex',
      packages=['amz_query'],
      install_requires=[          # 添加了依赖的 package
        'beautifulsoup4',
        'six',
        'requests',
        'loguru',
        'lxml',
        'html5lib'
    ])