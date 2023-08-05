#!/usr/bin/env python

from distutils.core import setup

setup(name='amget',
      version='1.1',
      description='request method for amazon spider',
      author='morbosohex',
      packages=['amget'],
      install_requires=[          # 添加了依赖的 package
        'beautifulsoup4',
        'six',
        'requests',
        'loguru',
        'lxml',
        'html5lib'
    ])