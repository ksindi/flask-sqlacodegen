flask-sqlacodegen
=================

* Automatic model code generator for SQLAlchemy *

Fork from <a href="https://pypi.python.org/pypi/sqlacodegen">sqlacodegen</a>. Based off of version 1.1.5.pre2.

What's different:
* Support for Flask-SQLAlchemy.
* Support for dogpile caching from <a href="http://www.debrice.com/flask-sqlalchemy-caching/">here</a>
* Defaults to generating backrefs in relationships. `--nobackref` still included as option in case backrefs are not wanted. 
* Naming of backref is the class name in underscore (CamelCase to camel_case) and is pluralized if it's Many-to-One or Many-to-Many using <a href="https://pypi.python.org/pypi/inflect">inflect</a>.
* Generate explicit primary joins. I deal with pretty complicated tables that need explicit primary joins.
* If column has a server_default set it to FetchValue() instead of trying to determine what that value is. Original code did not set the right server defaults in my set up.
* When generating association tables, I ignore special name columns *id*, *inserted*, *updated* when checking whether all columns have foreign keys as all my association tables have those columns.
