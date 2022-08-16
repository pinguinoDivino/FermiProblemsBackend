from django.core.cache import cache
from functools import wraps

import copy


def make_hash(obj):
    """Make a hash from an arbitrary nested dictionary, list, tuple or
    set.

    """
    if isinstance(obj, set) or isinstance(obj, tuple) or isinstance(obj, list):
        return hash(tuple([make_hash(e) for e in obj]))

    elif not isinstance(obj, dict):
        return hash(obj)

    new_obj = copy.deepcopy(obj)
    for k, v in new_obj.items():
        new_obj[k] = make_hash(v)

    return hash(tuple(frozenset(new_obj.items())))


def cached(function, hours=24):
    @wraps(function)
    def get_cache_or_call(*args, **kwargs):

        # known bug: if the function returns None, we never save it in
        # the cache
        cache_key = make_hash((function.__module__ + function.__name__,
                               args, kwargs))

        cached_result = cache.get(cache_key)
        if cached_result is None:
            result = function(*args)
            cache.set(cache_key, result, 60 * 60 * hours)
            return result
        else:
            return cached_result

    return get_cache_or_call
