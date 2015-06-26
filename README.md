sqlacodegen
=================

*Automatic model code generator for SQLAlchemy*

Fork from <a href="https://pypi.python.org/pypi/sqlacodegen">sqlacodegen</a>. Based off of version 1.1.5.pre2.

__In alpha stage. No plans for further development or support. Just wanted to share my modifications with people facing similar issues.__

What's different:
* Support for Flask-SQLAlchemy syntax using `--flask` option. All this means:
  * SQLAlchemy class is instantiated (i.e. `db = SQLAlchemy()`).
  * Flask-SQLAlchemy columns are used (e.g. `db.Integer`).
  * Metadata is only implicit in tables
* Defaults to generating backrefs in relationships. `--nobackref` still included as option in case backrefs are not wanted. 
* Naming of backrefs is the class name is snake_case (as opposed to CamelCase) and is pluralized if it's Many-to-One or Many-to-Many using <a href="https://pypi.python.org/pypi/inflect">inflect</a>.
* Generate explicit primary joins. I deal with pretty complicated tables that need explicit primary joins.
* If column has a server_default set it to `FetchValue()` instead of trying to determine what that value is. Original code did not set the right server defaults in my set up.
* `--ignorefk` ignores special name columns (e.g. id, inserted, updated) when generating association tables. Original code requires all columns to be foreign keys in order to generate association table. Example: `--ignorefk id,inserted,updated`.
* NOTE: As at 2015-06-26, I removed support for dogpile caching as that aspect of code was never fully developed.
