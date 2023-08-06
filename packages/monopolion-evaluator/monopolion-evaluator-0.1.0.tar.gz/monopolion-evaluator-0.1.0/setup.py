#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='monopolion-evaluator',
    version='0.1.0',
    license='MIT',
    description='Neural net to predict winning probability in Monopoly',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Matt Miermans',
    author_email='m.miermans@gmail.com',
    url='https://github.com/miermans/monopolion-evaluator',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://monopolion-evaluator.readthedocs.io/',
        'Changelog': 'https://monopolion-evaluator.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/miermans/monopolion-evaluator/issues',
    },
    keywords=[
        'monopoly', 'ai', 'machine learning', 'neural network', 'deep learning'
    ],
    python_requires='>=3.6, <4',
    install_requires=[
        'tensorflow==2.2.0',
        'protobuf>=3.12.0',
        'numpy>=1.18.0,<1.19.0',
        'pandas>=1.0.0',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            'monopolion-evaluator = monopolion_evaluator.cli:main',
        ]
    },
)
