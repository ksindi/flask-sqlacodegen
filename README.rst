flask-sqlacodegen
=================

GitHub page:
`flask-sqlacodegen <https://github.com/pwall27/flask-sqlacodegen>`__

Fork of `sqlacodegen <https://pypi.python.org/pypi/sqlacodegen>`__ by
Alex Gronholm. Based off of version 1.1.6.

What's different:

-  Bugfix for "TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'
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

With pip:

::

    pip install -e git://git@github.com:pwall27/flask-sqlacodegen.git#egg=flask-sqlacodegen

Without pip:

::

    git clone https://github.com/pwall27/flask-sqlacodegen.git
    cd flask-sqlacodegen/
    python setup.py install

