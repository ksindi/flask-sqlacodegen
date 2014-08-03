#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, unicode_literals

import functools
import hashlib

from flask_sqlalchemy import BaseQuery
from sqlalchemy import event, select
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.attributes import get_history
from sqlalchemy.orm.interfaces import MapperOption

from dogpile.cache.api import NO_VALUE
from dogpile.cache.region import make_region


def md5_key_mangler(key):
    """
    Encodes SELECT queries (key) into md5 hashes
    """
    if key.startswith('SELECT '):
        key = hashlib.md5(key.encode('ascii')).hexdigest()
    return key


def memoize(obj):
    """
    Local cache of the function return value
    """
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer


cache_config = {
    'backend': 'dogpile.cache.memory',
    'expiration_time': 60,
}

regions = dict(
    default=make_region(key_mangler=md5_key_mangler).configure(**cache_config)
)


class CachingQuery(BaseQuery):
    """
    A Query subclass which optionally loads full results from a dogpile
    cache region.
    """

    def __init__(self, regions, entities, *args, **kw):
        self.cache_regions = regions
        BaseQuery.__init__(self, entities=entities, *args, **kw)

    def __iter__(self):
        """
        override __iter__ to pull results from dogpile
        if particular attributes have been configured.
        """
        if hasattr(self, '_cache_region'):
            return self.get_value(createfunc=lambda: list(BaseQuery.__iter__(self)))
        else:
            return BaseQuery.__iter__(self)

    def _get_cache_plus_key(self):
        """
        Return a cache region plus key.
        """

        dogpile_region = self.cache_regions[self._cache_region.region]
        if self._cache_region.cache_key:
            key = self._cache_region.cache_key
        else:
            key = _key_from_query(self)
        return dogpile_region, key

    def invalidate(self):
        """
        Invalidate the cache value represented by this Query.
        """

        dogpile_region, cache_key = self._get_cache_plus_key()
        dogpile_region.delete(cache_key)

    def get_value(self, merge=True, createfunc=None,
                    expiration_time=None, ignore_expiration=False):
        """
        Return the value from the cache for this query.

        Raise KeyError if no value present and no
        createfunc specified.
        """
        dogpile_region, cache_key = self._get_cache_plus_key()

        assert not ignore_expiration or not createfunc, \
                "Can't ignore expiration and also provide createfunc"

        if ignore_expiration or not createfunc:
            cached_value = dogpile_region.get(cache_key,
                                expiration_time=expiration_time,
                                ignore_expiration=ignore_expiration)
        else:
            cached_value = dogpile_region.get_or_create(
                                cache_key,
                                createfunc,
                                expiration_time=expiration_time)

        if cached_value is NO_VALUE:
            raise KeyError(cache_key)
        if merge:
            cached_value = self.merge_result(cached_value, load=False)

        return cached_value

    def set_value(self, value):
        """
        Set the value in the cache for this query.
        """

        dogpile_region, cache_key = self._get_cache_plus_key()
        dogpile_region.set(cache_key, value)


def query_callable(regions, query_cls=CachingQuery):
    return functools.partial(query_cls, regions)


def _key_from_query(query, qualifier=None):
    """
    Given a Query, create a cache key.
    """

    stmt = query.with_labels().statement
    compiled = stmt.compile()
    params = compiled.params

    return " ".join(
                    [str(compiled)] + 
                    [str(params[k]) for k in sorted(params)])


class FromCache(MapperOption):
    """Specifies that a Query should load results from a cache."""

    propagate_to_loaders = False

    def __init__(self, region="default", cache_key=None):
        """Construct a new FromCache.

        :param region: the cache region.  Should be a
        region configured in the dictionary of dogpile
        regions.

        :param cache_key: optional.  A string cache key
        that will serve as the key to the query.   Use this
        if your query has a huge amount of parameters (such
        as when using in_()) which correspond more simply to
        some other identifier.

        """
        self.region = region
        self.cache_key = cache_key

    def process_query(self, query):
        """Process a Query during normal loading operation."""
        query._cache_region = self


class Cache(object):

    def __init__(self, model, regions, label):
        self.model = model
        self.regions = regions
        self.label = label
        # allow custom pk or default to 'id'
        self.pk = getattr(model, 'cache_pk', 'id')

    def get(self, pk):
        """
        Equivalent to the Model.query.get(pk) but using cache
        """
        return self.model.query.options(self.from_cache(pk=pk)).get(pk)

    def filter(self, order_by='asc', offset=None, limit=None, **kwargs):
        """
        Retrieve all the objects ids then pull them independently from cache.
        kwargs accepts one attribute filter, mainly for relationship pulling.
        offset and limit allow pagination, order by for sorting (asc/desc).
        """
        query_kwargs = {}
        if kwargs:
            if len(kwargs) > 1:
                raise TypeError('filter accept only one attribute for filtering')
            key, value = kwargs.items()[0]
            if key not in self._columns():
                raise TypeError('%s does not have an attribute %s' % self, key)
            query_kwargs[key] = value

        cache_key = self._cache_key(**kwargs)
        pks = self.regions[self.label].get(cache_key)

        if pks is NO_VALUE:
            pks = [o.id for o in self.model.query.filter_by(**kwargs)\
                .with_entities(getattr(self.model, self.pk))]
            self.regions[self.label].set(cache_key, pks)

        if order_by == 'desc':
            pks.reverse()

        if offset is not None:
            pks = pks[pks:]

        if limit is not None:
            pks = pks[:limit]

        keys = [self._cache_key(id) for id in pks]
        for pos, obj in enumerate(self.regions[self.label].get_multi(keys)):
            if obj is NO_VALUE:
                yield self.get(pks[pos])
            else:
                yield obj[0]

    def flush(self, key):
        """
        flush the given key from dogpile.cache
        """
        self.regions[self.label].delete(key)

    @memoize
    def _columns(self):
        return [c.name for c in self.model.__table__.columns if c.name != self.pk]

    @memoize
    def from_cache(self, cache_key=None, pk=None):
        """
        build the from cache option object the the given object
        """
        if pk:
            cache_key = self._cache_key(pk)
        # if cache_key is none, the mangler will generate a MD5 from the query
        return FromCache(self.label, cache_key)

    @memoize
    def _cache_key(self, pk="all", **kwargs):
        """
        Generate a key as query
        format: '<tablename>.<column>[<value>]'

        'user.id[all]': all users
        'address.user_id=4[all]': all address linked to user id 4
        'user.id[4]': user with id=4
        """
        q_filter = "".join("%s=%s" % (k, v) for k, v in kwargs.items()) or self.pk
        return "%s.%s[%s]" % (self.model.__tablename__, q_filter, pk)

    def flush_all(self, obj):
        for column in self._columns():
            added, unchanged, deleted = get_history(obj, column)
            for value in list(deleted) + list(added):
                self.flush(self._cache_key(**{column: value}))
        # flush "all" listing
        self.flush(self._cache_key())
        # flush the object
        self.flush(self._cache_key(getattr(obj, self.pk)))


class CacheableMixin(object):

    @declared_attr
    def cache(cls):  # @NoSelf
        """
        Add the cache features to the model
        """
        return Cache(cls, cls.cache_regions, cls.cache_label)

    @staticmethod
    def _flush_event(mapper, connection, target):
        """
        Called on object modification to flush cache of dependencies
        """
        target.cache._flush_all(target)

    @classmethod
    def __declare_last__(cls):
        """
        Auto clean the caches, including listings possibly associated with
        this instance, on delete, update and insert.
        """
        event.listen(cls, 'before_delete', cls._flush_event)
        event.listen(cls, 'before_update', cls._flush_event)
        event.listen(cls, 'before_insert', cls._flush_event)
