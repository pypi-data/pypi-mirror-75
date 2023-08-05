from distutils.core import setup
from setuptools import find_packages

setup(name='TSvho',  # 包名
      version='0.0.2',  # 版本号
      description='Useful package for time series data',
      long_description='',
      author='Vincent Ho',
      author_email='',
      url='',
      license='MIT',
      install_requires=[],
      classifiers=[
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Intended Audience :: Developers'
      ],
      packages=find_packages(),
      include_package_data=True,
      platforms="any"
      )
# !/usr/bin/env python