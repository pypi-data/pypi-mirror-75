"""Pythonic pipelines."""

__version__ = "0.2.0"
__all__ = (
    "pipeline",
    "tap",
    "remove",
    "keep",
    "each",
    "sort",
    "unique",
)

def pipeline(*fns):
    """Get a function to pipe data through a sequence of transformations."""
    def pipe(data):
        for fn in fns:
            data = fn(data)
        return data
    return pipe

def tap(fn):
    """Execute a step in the pipeline with side effects."""
    def tapper(x):
        fn(x)
        return x
    return tapper

def remove(check):
    """Remove items where `check` succeeds."""
    def remover(it):
        return (x for x in it if not check(x))
    return remover

def keep(check):
    """Remove items where `check` doesn't succeed."""
    def keeper(it):
        return (x for x in it if check(x))
    return keeper

def each(fn):
    """Apply `fn` to each item of an iterable."""
    def mapper(it):
        return (fn(x) for x in it)
    return mapper

def sort(*, key=None, reverse=False):
    """Sort the items (optionally by a key)."""
    def sorter(it):
        return sorted(it, key=key, reverse=reverse)
    return sorter

def unique(key=None):
    """Remove non-unique items from the iterable."""
    def inner(iterable):
        seen = set()
        for item in iterable:
            val = item if not key else key(item)
            if val in seen:
                continue
            seen.add(val)
            yield item
    return inner

def flatten(depth=1, scalar=(str, bytes)):
    """Flatten an iterable by N levels, treating `scalar` values as single."""
    from collections.abc import Iterable

    def flattener(iterable):
        # Don't flatten infinitely, stop if at the recursion limit.
        if depth <= 0:
            yield from iterable
            return

        for item in iterable:
            # Scalar values are values that are normally treated as
            # singular, even though they may be iterable.
            if isinstance(item, scalar) or not isinstance(item, Iterable):
                yield item
                return

            yield from flatten(depth-1)(item)

    return flattener
