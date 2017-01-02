# -*- coding: utf-8 -*-
"""Provides missing Postgresql types.

Implement mockups for Point and LTree type, but generated models won't work out
of the box: a better way would be to use a package implementing proper classes
which could be imported in the target project.
"""

from sqlalchemy import types as sqltypes
from sqlalchemy.dialects.postgresql.base import ischema_names, PGTypeCompiler


class LTREE(sqltypes.TypeEngine):
    """Postgresql LTREE type mockup."""

    __visit_name__ = 'LTREE'


class POINT(sqltypes.TypeEngine):
    """Postgresql POINT type mockup."""

    __visit_name__ = 'POINT'


ischema_names['ltree'] = LTREE
ischema_names['point'] = POINT

PGTypeCompiler.visit_LTREE = lambda self, type_: 'LTREE'
PGTypeCompiler.visit_POINT = lambda self, type_: 'POINT'
