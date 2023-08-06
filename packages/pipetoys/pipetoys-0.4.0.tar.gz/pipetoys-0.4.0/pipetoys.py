"""Pythonic pipelines."""

__version__ = "0.4.0"
__all__ = (
    "pipeline",
    "tap",
    "remove",
    "keep",
    "each",
    "sort",
    "unique",
    "flatten",
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
        from collections.abc import Hashable

        hashables = set()
        unhashables = []

        for item in iterable:
            value = item if not key else key(item)

            if isinstance(value, Hashable):
                if value in hashables:
                    continue
                hashables.add(value)
            else:
                if value in unhashables:
                    continue
                unhashables.append(value)

            yield item

    return inner


def flatten(depth=1, *, scalar=(str, bytes)):
    """Flatten an iterable (of mixed depth) by N levels.

    `scalar` types are treated as single, even if iterable.
    """
    def flattener(iterable):
        from collections.abc import Iterable

        if depth <= 0:
            yield from iterable
            return

        for item in iterable:
            if isinstance(item, Iterable) and not isinstance(item, scalar):
                yield from flatten(depth-1, scalar=scalar)(item)
            else:
                yield item

    return flattener
