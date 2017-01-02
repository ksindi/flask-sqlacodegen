Flask Sqlacodegen: SQLAlchemy Model Generator
=============================================

.. image:: https://travis-ci.org/ksindi/flask-sqlacodegen.svg?branch=master
    :target: https://travis-ci.org/ksindi/flask-sqlacodegen
    :alt: Build Status

.. image:: https://readthedocs.org/projects/flask-sqlacodegen/badge/?version=latest
    :target: http://flask-sqlacodegen.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Fork of `sqlacodegen <https://pypi.python.org/pypi/sqlacodegen>`__ by
Alex Gronholm. Based off of version 2.0.0.

What's different:

-  Support for Flask-SQLAlchemy syntax using ``--flask`` option.
-  Defaults to generating backrefs in relationships. ``--nobackref``
   still included as option in case backrefs are not wanted.
-  Naming of backrefs is class name in snake\_case (as opposed to
   CamelCase) and is pluralized if it's Many-to-One or Many-to-Many
   using `inflect <https://pypi.python.org/pypi/inflect>`__.
-  Primary joins are explicit.
-  If column has a server\_default set it to ``FetchValue()`` instead of
   trying to determine what that value is. Original code did not set the
   right server defaults in my setup.
-  ``--ignore-cols`` ignores special columns when generating association
   tables. Original code requires all columns to be foreign keys in
   order to generate association table. Example:
   ``--ignore-cols id,inserted,updated``.
-  Uses the command ``flask-sqlacodgen`` instead of ``sqlacodegen``.


Install
-------

::

    pip install flask-sqlacodegen

Usage
-----

::

    flask-sqlacodegen mysql+musqldb://uname:passwd@localhost/dbname --flask

Testing
-------

::

    make test

License
-------

MIT
