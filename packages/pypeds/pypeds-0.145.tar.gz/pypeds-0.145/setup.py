#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['pypeds']

package_data = \
{'': ['*'], 'pypeds': ['.ipynb_checkpoints/*']}

install_requires = \
['requests', 'pandas', 'altair', 'dfply', 'numpy', 'xlrd', 'pantab']

setup(name='pypeds',
      version='0.145',
      description='A python package to help facilitate the collection and analysis of education-related datasets. ',
      author='Brock Tibert',
      author_email='btibert3@gmail.com',
      url='https://github.com/Btibert3/pypeds',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      python_requires='>=3.6',
     )
