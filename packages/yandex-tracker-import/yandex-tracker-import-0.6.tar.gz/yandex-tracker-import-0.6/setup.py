# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='yandex-tracker-import',
    version='0.6',
    author='Vladimir Koljasinskij',
    author_email='smosker@yandex-team.ru',
    license='BSD-3-Clause',
    description='move all your content to another organization',
    long_description=read('README.rst'),
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3.7',
                 ],
    keywords='yandex-tracker import',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'yandex_tracker_client',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'yandex-tracker-import = yandex_tracker_import.cli.main:cli',
        ]
    },
)
