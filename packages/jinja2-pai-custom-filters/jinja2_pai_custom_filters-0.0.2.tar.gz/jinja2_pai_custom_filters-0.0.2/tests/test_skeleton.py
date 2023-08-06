#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from jinja2_pai_custom_filters.skeleton import fib

__author__ = "pai"
__copyright__ = "pai"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
