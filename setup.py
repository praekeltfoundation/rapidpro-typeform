#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('requirements.txt') as req_file:
    requirements = req_file.read().split('\n')

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('VERSION') as fp:
    version = fp.read().strip()

setup(
    name='rapidform',
    version=version,
    description="rapidform",
    long_description=readme,
    author="Simon de Haan",
    author_email='simon@praekelt.org',
    url='https://github.com/praekeltfoundation/rapidpro-typeform',
    packages=[
        'rapidform',
    ],
    package_dir={'rapidform':
                 'rapidform'},
    extras_require={},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='rapidpro typeform',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ]
)
