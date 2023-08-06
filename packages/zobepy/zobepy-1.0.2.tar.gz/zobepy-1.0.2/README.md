
zobepy
======

zobepy - zobe's unsorted library.

This is an unsorted library made by zobe.


usage
=====


pip
---

    pip install zobepy


import
------

    import zobepy

and use

    efb = zobepy.BinarySizeFormatter(3000)
    print(bsf.get())


test
====

prerequisites

    pip install -e '.[dev]'

unittest

    python -m unittest discover

pytest

    pytest

tox

    tox

watch htmlcov/index.html for coverage after tox


build document
==============

prerequisites

    pip install -e '.[doc]'

make

    cd docs
    make html
