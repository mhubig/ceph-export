#!/usr/bin/env python

from setuptools import setup


with open('README.md') as f:
    long_description = f.read()

required = [
    'click>=6.7',
    'delegator.py>=0.1.0'
]

setup(
    name='ceph-export.py',
    version='0.1.0',
    license='MIT',
    description='Simple app to export rbd images from a ceph pool, based on the last snapshot.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Markus Hubig',
    author_email='mhubig@gmail.com',
    url='https://github.com/mhubig/ceph-export',
    py_modules=['export'],
    install_requires=required,
    setup_requires=['setuptools>=38.6.0'],
    entry_points={
        'console_scripts': [
            'ceph-export=export:cli',
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ]
)
