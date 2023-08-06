#!/usr/bin/env python
"""Dump to know what it is."""

import inspect
import sys
import typing

"""Callback function definition as dump_class

Parameters
----------
target : object
    The target object you want to dump.
indent : int
    Depth to indent
no_print : bool
    If False(Default), immediately output by print().
    If True, no output. Use return value.
public_only : bool
    Ignore methods starts with '_' when True.
Returns
-------
str
    Dump result text.
"""
DumpClassCallback = typing.Callable[[object, int, bool, bool], str]


def dump_class(target: object,
               indent: int = 0,
               no_print: bool = False,
               public_only: bool = True
               ) -> str:
    """Dump class information.

    Parameters
    ----------
    target : object
        The target object you want to dump.
    indent : int
        Depth to indent
    no_print : bool
        If False(Default), immediately output by print().
        If True, no output. Use return value.
    public_only : bool
        Ignore methods starts with '_' when True.

    Returns
    -------
    str
        Dump result text.

    """
    tp: type

    if inspect.isclass(target):
        tp = typing.cast(type, target)
    else:
        tp = target.__class__

    s = 'description of {}.{}:'
    s = '  ' * indent + s.format(tp.__module__, tp.__name__)
    dump_string = s + '\n'
    s = '  ' * (indent + 1) + '__hash__: {}'.format(_get_hash_string(tp))
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__doc__: {}'.format(tp.__doc__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__qualname__: {}'.format(tp.__qualname__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__module__: {}'.format(tp.__module__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__name__: {}'.format(tp.__name__)
    dump_string += s + '\n'

    s = 'methods of {}.{}:'
    s = '  ' * indent + s.format(tp.__module__, tp.__name__)
    dump_string += s + '\n'
    s = dump_methods(target, indent + 1, True, public_only)
    s = s.rstrip('\n')
    dump_string += s

    if no_print is False:
        print(dump_string)
    return dump_string + '\n'


def dump_class_simple(target: object,
                      indent: int = 0,
                      no_print: bool = False,
                      public_only: bool = True) -> str:
    """Dump class information (simple).

    A function like dump_class but no output of methods.

    Parameters
    ----------
    target : object
        The target object you want to dump.
    indent : int
        Depth to indent
    no_print : bool
        If False(Default), immediately output by print().
        If True, no output. Use return value.
    public_only : bool
        Ignore methods starts with '_' when True.

    Returns
    -------
    str
        Dump result text.

    """
    tp: type
    if inspect.isclass(target):
        tp = typing.cast(type, target)
    else:
        tp = target.__class__

    s = 'description of {}.{}:'
    s = '  ' * indent + s.format(tp.__module__, tp.__name__)
    dump_string = s + '\n'
    s = '  ' * (indent + 1) + '__hash__: {}'.format(_get_hash_string(tp))
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__doc__: {}'.format(tp.__doc__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__qualname__: {}'.format(tp.__qualname__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__module__: {}'.format(tp.__module__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__name__: {}'.format(tp.__name__)
    dump_string += s

    if no_print is False:
        print(dump_string)
    return dump_string + '\n'


def dump_class_dummy(target: object,
                     indent: int = 0,
                     no_print: bool = False,
                     public_only: bool = True) -> str:
    """Pseudo implementation of DumpClassCallback outputs and returns nothing.

    Parameters
    ----------
    target: object
    indent: int
    no_print: bool
    public_only : bool

    Returns
    -------
    str
        Always empty string

    """
    return ''


def dump_class_tree(target: object,
                    max_depth: int = 10,
                    no_print: bool = False,
                    indent: int = 0,
                    dump_class_callback: DumpClassCallback = dump_class_dummy,
                    public_only: bool = True) -> str:
    """Dump class information, and its ancestors.

    Dumps class tree only by default.

    Set dump_class() or any to dump_class_callback
    to dump with descriptions of the class.
    Or use dump_class_tree_verbose().

    Parameters
    ----------
    target : object
        The target you want to dump.
    max_depth : int, default 10
        Maximum number of ascending.
        Smaller number suppresses output simple.
    no_print: bool, default False
        Set True suspends all print() call.
        Get dump result from return value.
    indent: int, default 0
        Indent result text.
    dump_class_callback: DumpClassCallback, default dump_class_dummy
        Set output function for classes.
        Default function outputs nothing.
        Set dump_class_simple or dump_class
        to get detail for classes.
    public_only : bool
        Ignore methods starts with '_' when True.

    Returns
    -------
    str
        Dump result text.
    """
    return _dump_class_tree_internal(
        target,
        max_depth,
        indent,
        None,
        dump_class_callback,
        no_print,
        public_only)


def dump_class_tree_verbose(target: object,
                            max_depth: int = 10,
                            no_print: bool = False,
                            indent: int = 0,
                            public_only: bool = True) -> str:
    """Dump class information, and its ancestors.

    Unlike dump_class_tree(), this uses dump_class().
    (Default class dumper of dump_class_tree() is dump_class_dummy(),
    which dumps nothing.)

    Parameters
    ----------
    target : object
        The target you want to dump.
    max_depth : int, default 10
        Maximum number of ascending.
        Smaller number suppresses output simple.
    no_print: bool, default False
        Set True suspends all print() call.
        Get dump result from return value.
    indent: int, default 0
        Indent result text.
    public_only : bool
        Ignore methods starts with '_' when True.

    Returns
    -------
    str
        Dump result text.
    """
    return _dump_class_tree_internal(
        target,
        max_depth,
        indent,
        None,
        dump_class,
        no_print,
        public_only)


def _dump_class_tree_internal(target: object, depth: int = 10, indent: int = 0,
                              duplication_checker: dict = None,
                              dump_class_callback: DumpClassCallback = dump_class,
                              no_print: bool = False,
                              public_only: bool = True):
    dump_string = ''

    if depth <= 0:
        return dump_string

    if inspect.isclass(target) is False:
        target = target.__class__
    target = typing.cast(type, target)

    if duplication_checker is None:
        duplication_checker = dict()

    target_hash = _get_hash_string(target)
    if target_hash == '':
        target_hash = target.__module__ + '.' + target.__name__
    if target_hash in duplication_checker:
        # already dumped class
        duplication_checker[target_hash] += 1
        return dump_string

    duplication_checker[target_hash] = 0

    s = '  ' * indent + '{}.{}:'.format(target.__module__, target.__name__)
    dump_string += s + '\n'
    if no_print is False:
        print(s)

    dump_string += dump_class_callback(target, indent + 1, no_print, public_only)

    target_bases: list = list()
    if hasattr(target, '__bases__') and target.__bases__:
        target_bases = list(target.__bases__)
        try:
            target_bases.remove(object)
        except ValueError:
            pass

    if len(target_bases) > 0:
        s = '{} parent(s) found for [{}.{}]'
        s = s.format(len(target_bases), target.__module__, target.__name__)
        s = '  ' * (indent + 1) + s
        dump_string += s + '\n'
        if no_print is False:
            print(s)
        for c in target_bases:
            s = '  ' * (indent + 2) + '[{}.{}]'.format(c.__module__, c.__name__)
            dump_string += s + '\n'
            if no_print is False:
                print(s)

        for c in target_bases:
            c_hash = _get_hash_string(c)
            if c_hash in duplication_checker:
                # already dump class
                # s = '  '*(indent+2) + 'skipped - already dumped'
                # dump_string += s + '\n'
                # if no_print is False:
                #     print(s)
                duplication_checker[c_hash] += 1
                continue
            dump_string += _dump_class_tree_internal(
                c, depth - 1, indent + 1, duplication_checker,
                dump_class_callback,
                no_print,
                public_only)
    else:
        s = '  ' * (indent + 1) + 'have no parents'
        dump_string += s + '\n'
        if no_print is False:
            print(s)

    return dump_string


def _get_hash_string(target):
    """Calculate Object hash.

    Parameters
    ----------
    target
        An object. It must have __hash__ method.

    Returns
    -------
        The hash string.

    """
    try:
        a = target.__hash__(target)
        b = a % ((sys.maxsize + 1) * 2)
    except TypeError:
        return ''

    return str(b)


def dump_methods(target, indent: int = 0, no_print: bool = False, public_only: bool = True):
    """Dump methods of a class.

    Parameters
    ----------
    target : object
        The target you want to dump. Class or Instance is acceptable.
    indent : int
        Depth to indent
    no_print : bool
        If False(Default), immediately output by print().
        If True, no output. Use return value.
    public_only : bool
        Ignore methods starts with '_' when True.

    Returns
    -------
    str
        Dump result text.

    """
    dump_string = ''

    if False is inspect.isclass(target) \
            and isinstance(target, object):
        target = target.__class__
    if False is inspect.isclass(target):
        return dump_string

    for a in inspect.classify_class_attrs(target):
        if a.kind == 'method':
            attr = getattr(target, a.name)
            # target_class = target
            # if a.defining_class:
            #     target_class = a.defining_class
            attr = getattr(a.defining_class, a.name)
            signature = None
            try:
                signature = inspect.signature(attr)
            except ValueError:
                pass
            s = a.name
            if public_only:
                if s.startswith('_'):
                    continue
            if signature is not None:
                s += str(signature)

            if len(dump_string) > 0:
                dump_string += '\n'
            s = '  ' * indent + s
            dump_string += s

    if no_print is False:
        print(dump_string)

    return dump_string + '\n'


if __name__ == '__main__':
    print(dump_class_tree(True))
