# -*- coding: utf-8 -*-
"""Distutils setup file, used to install or test 'flask-sqlacodegen'."""
import textwrap

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='flask-sqlacodegen',
    description='Automatic model generator for SQLAlchemy with Flask support',
    long_description=readme,
    use_scm_version=True,
    author='Kamil Sindi',
    url='https://github.com/ksindi/flask-sqlacodegen',
    keywords=['sqlalchemy', 'sqlacodegen', 'flask'],
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=(
        'SQLAlchemy >= 0.6.0',
        'inflect >= 0.2.0',
    ),
    setup_requires=[
        'pytest-runner',
        'setuptools_scm >= 1.15.0',
        'sphinx_rtd_theme',
    ],
    tests_require=[
        'pytest',
        'pytest-flake8',
    ],
    extras_require={
        ':python_version == "2.6"': ['argparse']
    },
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'flask-sqlacodegen=sqlacodegen.main:main'
        ]
    },
    classifiers=textwrap.dedent("""
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        License :: OSI Approved :: MIT License
        Environment :: Console
        Topic :: Database
        Topic :: Software Development :: Code Generators
        Programming Language :: Python
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.2
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
    """).strip().splitlines()
)
