sqlacodegen
===========

*Automatic model code generator for SQLAlchemy*

Fork from <a href="https://pypi.python.org/pypi/sqlacodegen">sqlacodegen</a>.

What's different:
* Defaults to generating backrefs in relationships. 
    * `--nobackref` included as option in case backrefs are not wanted. 
    * Naming of backref is the class name in underscore (CamelCase to camel_case) and is pluralized if it's Many-to-One or Many-to-Many using <a href="https://pypi.python.org/pypi/inflect">inflect</a>.
* Generate explicit primary joins. I deal with pretty complicated tables that need explicit primary joins.
    * TODO: Don't do this as default and create `--withprijoin` as an option?
    * TODO: Maybe just need to modify code to better check if primary join is needed?
* Support for Flask-SQLAlchemy so that the proper declarative base is included. 
    * Use `--withflask` as an option.
* When generating association tables, I ignore special name columns *id*, *inserted*, *updated* when checking whether all columns have foreign keys as all my association tables have those columns. This is probably not standard for most users.

I hope to do a Pull Request once modifications are more modular.

Still in alpha stage.
