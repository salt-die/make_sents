from functools import partial
from importlib import import_module
from inspect import isgeneratorfunction, signature

from . import default_methods

MAKE_PARTIAL = type('MAKE_PARTIAL', (), {'__repr__': lambda self: 'MAKE_PARTIAL'})()
NO_GET = type('NO_GET', (), {'__repr__': lambda self: 'NO_GET'})()

def make_sents(
    cls=MAKE_PARTIAL,
    /,
    *,
    repr="SENTINEL",
    str=None,
    setattr='readonly',
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

    Parameters
    ----------
    cls : None | type
        The decorated class. To in-line a sentinel, one can use None. Positional argument only.
    repr : str | None, default: 'SENTINEL'
        The string returned by __repr__. If repr is None, no __repr__ is added.
    str : str | None, default: 'SENTINEL'
        The string returned by __str__. If str is None, no __str__ is added.
    setattr : 'readonly' | 'ignore' | Callable | None, default: 'readonly'
        The __setattr__ of the sentinel. `'readonly'` option creates a __setattr__
        that raises an AttributeError. `'ignore'` creates a __setattr__
        that does nothing.
    getattr : Callable | ANY | None, default: NO_GET
        If getattr is a callable it will be the __getattr__. Any other value will create
        a __getattr__ that always returns that value.
    iter : 'default' | Callable | None, default: None
        The `__iter__` implementation. `'default'` will add a default implementation.
    attrs : None | dict, default: None
        A dictionary of attributes of the sentinel.
    methods : None | dict, default: None
        A dictionary of methods of the sentinel.
    abc : None | ABC, default: None
        An abstract base class. Abstract methods in abc will be given default implementations
        in the sentinel.
    name : str, default: 'SENTINEL'
        The class name of the sentinel. Ignored when decorating a class.
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

    if setattr == 'ignore':
        cls.__setattr__ = default_methods._IGNORE_SETATTR
    elif setattr == 'readonly':
        cls.__setattr__ = default_methods._READONLY
    elif setattr is not None:
        cls.__setattr__ = setattr

    if callable(getattr):
        cls.__getattr__ = getattr
    elif getattr is not NO_GET:
        cls.__getattr__ = default_methods._DEFAULT_GET(getattr)

    if iter == 'default':
        cls.__iter__ = default_methods.DEFAULT_ITER
    elif iter is not None:
        cls.__iter__ = iter

    if attrs is not None:
        cls.__init__ = default_methods._make_init(attrs)

    namespace = { }

    if abc is not None:
        METHOD_TEMPLATE = f'def {{}}{{}}:\n    return\n    {{}}\n'
        for method_name in abc.__abstractmethods__:
            method = __builtins__['getattr'](abc, method_name)
            source = METHOD_TEMPLATE.format(method_name, signature(method), 'yield' if isgeneratorfunction(method) else '')
            exec(source, globals(), namespace)

    if methods is not None:
        namespace |= methods

    for name, method in namespace.items():
        __builtins__['setattr'](cls, name, method)

    return cls()
