flask-sqlacodegen
=================

Fork from <a href="https://pypi.python.org/pypi/sqlacodegen">sqlacodegen</a>. Based off of version 1.1.6.

What's different:
* Support for Flask-SQLAlchemy syntax using `--flask` option. All this means:
  * SQLAlchemy class is instantiated (i.e. `db = SQLAlchemy()`).
  * Flask-SQLAlchemy columns are used (e.g. `db.Integer`).
  * Metadata is only implicit in tables.
* Defaults to generating backrefs in relationships. `--nobackref` still included as option in case backrefs are not wanted. 
* Naming of backrefs is class name in snake_case (as opposed to CamelCase) and is pluralized if it's Many-to-One or Many-to-Many using <a href="https://pypi.python.org/pypi/inflect">inflect</a>.
* Generate explicit primary joins. I deal with pretty complicated tables that need explicit primary joins.
* If column has a server_default set it to `FetchValue()` instead of trying to determine what that value is. Original code did not set the right server defaults in my set up.
* `--ignore-cols` ignores special columns (e.g. id, inserted, updated) when generating association tables. Original code requires all columns to be foreign keys in order to generate association table. Example: `--ignore-cols id,inserted,updated`.
