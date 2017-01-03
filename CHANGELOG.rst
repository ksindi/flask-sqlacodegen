.. :changelog:

Changelog
=========

Releases
--------

v0.2.0 (2017-01-03)
~~~~~~~~~~~~~~~~~~~

* Major refactor large thanks to sqlacodegen rewrite.
* Naming has changed.
* CLI changes:
  * ``tables`` is space separated instead of comma separated. Example: ``--tables Table1 Table2``
  * ``ignore-cols`` is not space separated instead of comma separated. Example: ``--ignore-cols id inserted updated``
  * ``fetch-value`` is a new option change server default to FetchValue;
it only works for non primary keys.

v1.1.6 (2016-06-30)
~~~~~~~~~~~~~~~~~~~

* Parity with sqlacodegen.
