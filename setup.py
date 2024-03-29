import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import sqlacodegen


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


extra_requirements = ()
if sys.version_info < (2, 7):
    extra_requirements = ('argparse',)

setup(
    name='flask-sqlacodegen',
    description='Automatic model code generator for SQLAlchemy with Flask support',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    version=sqlacodegen.version,
    author='Kamil Sindi',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Topic :: Database',
        'Topic :: Software Development :: Code Generators',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords=['sqlalchemy', 'sqlacodegen', 'flask'],
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=(
        "SQLAlchemy >= 2.0",
        "inflect >= 4.0.0",
    ) + extra_requirements,
    tests_require=['pytest', 'pytest-pep8'],
    cmdclass={'test': PyTest},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'flask-sqlacodegen=sqlacodegen.main:main'
        ]
    }
)
