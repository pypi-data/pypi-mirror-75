#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
===============================
HtmlTestRunner
===============================


.. image:: https://img.shields.io/pypi/v/styler_identity.svg
        :target: https://pypi.python.org/pypi/styler_identity

Simple library used to handle user data from JWT tokens


Links:
---------
* `Github <https://github.com/STYLER-Inc/styler-identity>`_
"""

from setuptools import setup, find_packages

requirements = ['pyjwt']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Bruno Toshio Sugano",
    author_email='bruno.sugano@styler.link',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    description="Simple library used to handle user data from JWT tokens",
    install_requires=requirements,
    license="MIT license",
    long_description=__doc__,
    include_package_data=True,
    keywords='styler_identity',
    name='styler_identity',
    packages=find_packages(include=['styler_identity']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/STYLER-Inc/styler-identity',
    version='0.5.1',
    zip_safe=False,
)
