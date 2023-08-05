from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

    setup(name = 'gabi_distribution',
      version = '0.5',
      description = 'Gaussian and Binomial distributions',
      packages = ['gabi_distribution'],
      author = 'Anukool Rathi',
      author_email = 'Anukool.rathi10@gmail.com',
      long_description=long_description,
      zip_safe=False)