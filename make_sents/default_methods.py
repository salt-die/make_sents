from functools import wraps

def add_doc(factory):
    """
    Add `doc` keyword argument to factory. If `doc` is provided,
    the factory will add a docstring to the functions it produces.
    """
    @wraps(factory)
    def wrapper(*args, doc=None, **kwargs):
        func = factory(*args, **kwargs)

        if doc is not None:
            func.__doc__ = doc

        return func

    return wrapper

@add_doc
def raise_(error, msg=None):
    """
    Return a function that raises an error with an optional message.
    """
    if msg is None:
        def error_raiser(self):
            raise error()

    else:
        def error_raiser(self):
            raise error(msg)

    return error_raiser

@add_doc
def return_(value):
    def default_value(self):
        return value

    return default_value

@add_doc
def property_(func):
    return property(func)

def DEFAULT_ITER(self):
    """
    Empty generator function.
    """
    return
    yield

def make_init(attrs):
    def __init__(self):
        for attr, val in attrs.items():
            object.__setattr__(self, attr, val)

    return __init__

def DEFAULT_GET(default):
    def __getattr__(self, attr):
        return default

    return __getattr__

def IGNORE_SETATTR(self, attr, value):
    pass

IDENTITY = property_(lambda self: self, doc='Identity.')
READONLY = raise_(AttributeError, msg="can't set attribute")
RETURNNONE = PASS = return_(None)
