sqlacodegen
=================

*Automatic model code generator for SQLAlchemy*

Fork from <a href="https://pypi.python.org/pypi/sqlacodegen">sqlacodegen</a>. Based off of version 1.1.5.pre2.

Currently in alpha stage.

What's different:
* Support for Flask-SQLAlchemy using `--flask` option. All this means:
  * SQLAlchemy class is instantiated (i.e. `db = SQLAlchemy()`).
  * Flask-SQLAlchemy columns are used (e.g. `db.Integer`).
  * Metadata is only implicit in tables
* `--dogpile` option supports dogpile caching from <a href="http://www.debrice.com/flask-sqlalchemy-caching/">here</a>. You must have `caching.py` at the same level as your outfile. Note option dependent on flask option.
* Defaults to generating backrefs in relationships. `--nobackref` still included as option in case backrefs are not wanted. 
* Naming of backref is the class name in underscore (CamelCase to camel_case) and is pluralized if it's Many-to-One or Many-to-Many using <a href="https://pypi.python.org/pypi/inflect">inflect</a>.
* Generate explicit primary joins. I deal with pretty complicated tables that need explicit primary joins.
* If column has a server_default set it to `FetchValue()` instead of trying to determine what that value is. Original code did not set the right server defaults -- at least in my set up.
* `--ignorefk` ignores special name columns (e.g. id, inserted, updated) when generating association tables. Original code requires all columns to be foreign keys in order to generate association table. All you have to do is: `--ignorefk id,inserted,updated`.
