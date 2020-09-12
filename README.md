# Flask sqlacodegen

Fork of [sqlacodegen](https://pypi.python.org/pypi/sqlacodegen) by Alex Gronholm. Based off of version 1.1.6.

What's different:

* Support for Flask-SQLAlchemy syntax using `--flask` option.
* Defaults to generating backrefs in relationships. `--nobackref` still included as option in case backrefs are not wanted. 
* Naming of backrefs is class name in snake_case (as opposed to CamelCase) and is pluralized if it's Many-to-One or Many-to-Many using [inflect](https://pypi.python.org/pypi/inflect).
* Primary joins are explicit.
* If column has a server_default set it to `FetchValue()` instead of trying to determine what that value is. Original code did not set the right server defaults in my setup.
* `--ignore-cols` ignores special columns when generating association tables. Original code requires all columns to be foreign keys in order to generate association table. Example: `--ignore-cols id,inserted,updated`.
* Uses the command `flask-sqlacodegen` instead of `sqlacodegen`.
* Added support for `--notables` to only generate model classes, even for association tables

## Install

With pip:
```sh
pip install flask-sqlacodegen
```

Without pip:
```sh
git clone https://github.com/ksindi/flask-sqlacodegen.git
cd flask-sqlacodegen/
python setup.py install
```

For contributing:
```sh
git clone https://github.com/ksindi/flask-sqlacodegen.git
python -m venv env
pip install -r requirements.txt
python -m sqlacodegen.main --flask --outfile models.py mysql+pymysql://<username>:<password>@<database-ip>:<port>/<database-name> [--tables <tablenames>] [--notables]
```