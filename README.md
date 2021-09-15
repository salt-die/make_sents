# make_sents

A class decorator or stand alone function for building sentinel objects.

Creating a sentinel in-line is as simple as:
```py
In [2]: from make_sents import make_sents

In [3]: MYSENT = make_sents(None)
```
`None` is a required positional arg when `make_sents` is not used as a decorator.

It will have a default `repr`.
```py
In [4]: MYSENT
Out[4]: SENTINEL
```

And attributes can't be set:
```py
In [5]: MYSENT.a = 1
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-5-f93bbce6924f> in <module>
----> 1 MYSENT.a = 1

~\Documents\Python\make_sents\make_sents\default_methods.py in _READONLY(self, attr, value)
     61     A __setattr__ implementation that raises an AttributeError.
     62     """
---> 63     raise AttributeError("can't set attribute")
     64
     65 def _make_init(attrs: dict):

AttributeError: can't set attribute
```

`make_sents` can also be used to decorate a class. As a decorator, `make_sents` will add any number of default methods or attributes and instantiate and return the sentinal:

```py
In [7]: @make_sents(getattr=None, setattr='ignore', repr='EMPTY_NODE')
   ...: class EMPTY_NODE:
   ...:     def iter_nodes(self):
   ...:         return
   ...:         yield
   ...:

In [8]: EMPTY_NODE
Out[8]: EMPTY_NODE

In [9]: for leaf in EMPTY_NODE.iter_nodes():
   ...:     print(leaf)
   ...:

In [10]: EMPTY_NODE.a = 10  # This does nothing as `setattr` option is `ignore`.

In [11]: EMPTY_NODE.b  # Value provided to `getattr` is returned (None).

```

As a decorator, the parenthesis are optional if no kwargs are supplied:
```py
In [12]: @make_sents
    ...: class EMPTY_NODE:
    ...:     def iter_nodes(self):
    ...:         return
    ...:         yield
    ...:

In [13]: EMPTY_NODE
Out[13]: SENTINEL
```

Of course, above can be in-lined:
```py
In [14]: from make_sents import DEFAULT_ITER, make_sents
    ...: EMPTY_NODE = make_sents(None, methods={'iter_nodes': DEFAULT_ITER})
```
