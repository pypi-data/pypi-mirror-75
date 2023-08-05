from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(

    name='elucidata',

    version='0.0.3',

    description='A python module to parse source code for retro-documentation',

    long_description=long_description,

    long_description_content_type='text/markdown',

    author='Nicolas Bouillette, Guillaume Hurvois, Julien Mendes, Adam Wang',

    author_email='nbouillette@bi-consulting.com, '
    'ghurvois@bi-consulting.com, '
    'jmendes@bi-consulting.com, '
    'awang@bi-consulting.com',

    url='https://bitbucket.org/bi_labbigdata/parser/src/master/',

    package_dir={"": "elucidata"},
    packages=find_packages('elucidata'),

    python_requires='>=3.7'
)
