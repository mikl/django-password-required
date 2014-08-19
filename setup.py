#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django-password-required',
    version='0.1.0',
    description='A flexible & capable API layer for Django.',
    author='Mikkel Høgh',
    author_email='mikkel@hoegh.org',
    url='http://github.com/mikl/django-password-required/',
    packages=[
        'password_required',
    ],
    package_data={
        'password_required': ['templates/*'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)

