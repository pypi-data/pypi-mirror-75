from setuptools import setup, Extension
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))+'/gammahill_distributions'
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
      long_description = f.read()

setup(name='gammahill_distributions',
      version='0.2',
      description='Gaussian distribution',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Solomon Igori',
      author_email='igorisolomon@gmail.com',
      packages=['gammahill_distributions'],
      zip_safe=False)
