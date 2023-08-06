"""Pythonic pipelines."""

__version__ = "0.1.0"
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
    def inner(x):
        fn(x)
        return x
    return inner

def remove(check):
    """Remove items where the check succeeds."""
    def inner(it):
        return (x for x in it if not check(x))
    return inner

def keep(check):
    """Remove items where the check doesn't succeed."""
    def inner(it):
        return (x for x in it if check(x))
    return inner

def each(fn):
    """Get the result of `fn` for each item."""
    def inner(it):
        return (fn(x) for x in it)
    return inner

def sort(*, key=None, reverse=False):
    """Sort the items."""
    def inner(it):
        return sorted(it, key=key, reverse=reverse)
    return inner

def unique(check=hash):
    """Remove non-unique items from the iterable."""
    def inner(iterable):
        seen = set()
        for item in iterable:
            val = check(item)
            if val in seen:
                continue
            seen.add(val)
            yield item
    return inner
