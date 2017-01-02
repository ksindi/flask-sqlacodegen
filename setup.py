# -*- coding: utf-8 -*-
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
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Topic :: Database',
        'Topic :: Software Development :: Code Generators',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['sqlalchemy', 'sqlacodegen', 'flask'],
    license='MIT',
    packages=find_packages(exclude=['tests']),
    setup_requires=[
        'setuptools_scm >= 1.15.0'
    ],
    install_requires=(
        'SQLAlchemy >= 0.6.0',
        'inflect >= 0.2.0'
    ),
    extras_require={
        ':python_version == "2.6"': ['argparse']
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'flask-sqlacodegen=sqlacodegen.main:main'
        ]
    }
)
