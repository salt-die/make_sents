def raise_(error, msg=None, doc=None):
    """
    Return a method that raises an error with an optional message.
    """
    if msg is None:
        def error_raiser(self):
            raise error()

    else:
        def error_raiser(self):
            raise error(msg)

    if doc is not None:
        error_raiser.__doc__ = doc

    return error_raiser

def return_(value, doc=None):
    """
    Return a method that will return `value`.
    """
    def default_value(self):
        return value

    if doc is not None:
        default_value.__doc__ = doc

    return default_value

def DEFAULT_ITER(self):
    """
    Empty generator function.
    """
    return
    yield

def DEFAULT_GET(default):
    """
    Return a __getattr__ implementation that will return `default`.
    """
    def __getattr__(self, attr):
        return default

    return __getattr__

def IGNORE_SETATTR(self, attr, value):
    """
    A __setattr__ implementation that does nothing.
    """
    pass

def READONLY(self, attr, value):
    """
    A __setattr__ implementation that raises an AttributeError.
    """
    raise AttributeError("can't set attribute")

@property
def IDENTITY(self):
    """
    Identity property.
    """
    return self

def make_init(attrs: dict):
    """
    Return an __init__ method that calls object's `__setattr__` on each
    item of attrs.
    """
    def __init__(self):
        for attr, val in attrs.items():
            object.__setattr__(self, attr, val)

    return __init__

RETURN_NONE = PASS = return_(None)
