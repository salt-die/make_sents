from functools import partial

from . import default_methods

MAKE_PARTIAL = type('MAKE_PARTIAL', (), {'__repr__': lambda self: 'MAKE_PARTIAL'})()

def make_sents(cls=MAKE_PARTIAL, *, ):
    """
    A class decorator for building sentinel objects. Alternatively, use `None` as only positional
    argument to produce a sentinel without decorating a class.
    """
    if cls is MAKE_PARTIAL:
        return partial(make_sents, **kwargs)

    if cls is None:
        return _make_sents_from_none(**kwargs)

def _make_sents_from_none(**kwargs):
    """
    Build a sentinel from the ground up.
    """