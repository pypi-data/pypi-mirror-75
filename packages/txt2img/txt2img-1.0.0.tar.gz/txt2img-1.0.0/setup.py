#!/usr/bin/env python

from setuptools import setup

setup(name='txt2img',
      version='1.0.0',
      keywords = ["text", "image"],
      author='Yongping Guo',
      author_email='guoyoooping@163.com',
      description='a python tool to convert the text into a image.',
      long_description=open('README.rst').read(),
      install_requires = ["Pillow-PIL"],
      url='https://github.com/guoyoooping/txt2img',
      license='GPLv3',
      scripts=['txt2img'],
      #packages=[ 'pygnuplot' ],
      #packages = find_packages(),
      )
