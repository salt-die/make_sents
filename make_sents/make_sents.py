from enum import Enum
from functools import partial
from inspect import isgeneratorfunction, signature

from . import default_methods


class SentOptions(str, Enum):
    IGNORE = "ignore"
    READONLY = "readonly"
    DEFAULT = "default"


MAKE_PARTIAL = type('MAKE_PARTIAL', (), {'__repr__': lambda self: 'MAKE_PARTIAL'})()
NO_GET = type('NO_GET', (), {'__repr__': lambda self: 'NO_GET'})()

def make_sents(
    cls=MAKE_PARTIAL,
    /,
    *,
    repr="SENTINEL",
    str=None,
    setattr=SentOptions.READONLY,
    getattr=NO_GET,
    iter=None,
    attrs=None,
    methods=None,
    abc=None,
    name='SENTINEL',
):
    """
    A class decorator for building sentinel objects. Alternatively, use `None` as only positional
    argument to produce a sentinel without decorating a class.
    """
    kwargs = locals().copy()
    kwargs.pop('cls')

    if cls is MAKE_PARTIAL:
        return partial(make_sents, **kwargs)

    if cls is None:
        return make_sents((abc or type)(name, (), { }), **kwargs)

    if repr is not None:
        cls.__repr__ = default_methods.return_(repr)

    if str is not None:
        cls.__str__ = default_methods.return_(str)

    if setattr == SentOptions.IGNORE:
        cls.__setattr__ = default_methods.IGNORE_SETATTR
    elif setattr == SentOptions.READONLY:
        cls.__setattr__ = default_methods.READONLY
    elif setattr is not None:
        cls.__setattr__ = setattr

    if callable(getattr):
        cls.__getattr__ = getattr
    elif getattr is not NO_GET:
        cls.__getattr__ = default_methods.DEFAULT_GET(getattr)

    if iter == SentOptions.DEFAULT:
        cls.__iter__ = default_methods.DEFAULT_ITER
    elif iter is not None:
        cls.__iter__ = iter

    if attrs is not None:
        cls.__init__ = default_methods.make_init(attrs)

    namespace = { }

    if abc is not None:
        METHOD_TEMPLATE = f'def {{}}{{}}:\n    return\n    {{}}\n'
        for method_name in abc.__abstractmethods__:
            method = getattr(abc, method_name)
            source = METHOD_TEMPLATE.format(method_name, signature(method), 'yield' if isgeneratorfunction(method) else '')
            exec(source, globals(), namespace)

    if methods is not None:
        namespace |= methods

    for name, method in namespace.items():
        setattr(cls, name, method)

    return cls()
