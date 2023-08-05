#!/usr/bin/env python

"""
===============================
HtmlTestRunner
===============================


.. image:: https://img.shields.io/pypi/v/styler_middleware.svg
        :target: https://pypi.python.org/pypi/styler_middleware

Utility middlewares for aiohttp web apps.


Links:
---------
* `Github <https://github.com/STYLER-Inc/styler-middleware>`_
"""

from setuptools import setup, find_packages

requirements = ['aiohttp']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Bruno Toshio Sugano",
    author_email='bruno.sugano@styler.link',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    description="Utility middlewares for aiohttp web apps.",
    install_requires=requirements,
    license="MIT license",
    long_description=__doc__,
    include_package_data=True,
    keywords='styler_middleware middleware aiohttp',
    name='styler_middleware',
    packages=find_packages(include=['styler_middleware', 'styler_middleware.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/STYLER-Inc/styler-middleware',
    version='0.3.0',
    zip_safe=False,
)
