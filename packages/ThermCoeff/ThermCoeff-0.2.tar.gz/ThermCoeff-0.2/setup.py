# Read the "README.rst" for project description
with open('README.rst', 'r', encoding='utf8') as f:
    readme = f.read()
    
from setuptools import setup, Extension
from ThermCoeff import __version__

setup(
    name='ThermCoeff',
    version=__version__,
    author='Lorenzo Capponi',
    author_email='lorenzocapponi@outlook.it',
    description='Module for thermoelastic coefficient identification',
    url='https://github.com/LolloCappo/ThermCoeff',
    py_modules=['ThermCoeff'],
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires = ['numpy','pyLIA>=0.6']
)
