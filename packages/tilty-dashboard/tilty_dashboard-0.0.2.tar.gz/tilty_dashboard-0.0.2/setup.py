#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tilty_dashboard',
    description='A live dashboard for the tilty based on Flask-SocketIO',  # noqa
    author='Marcus Young',
    author_email='3vilpenguin@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.0.2',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Flask',
        'Flask-Bootstrap',
        'Flask-Cors',
        'Flask-SQLAlchemy',
        'Flask-SocketIO',
        'Flask-Script',
        'backoff',
        'configobj',
        'gunicorn',
        'Werkzeug==0.15.3',
        'eventlet',
    ]
)
