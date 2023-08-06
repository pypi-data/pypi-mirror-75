#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2_pai_custom_filters import __version__

import re
from jinja2.ext import Extension

__author__ = "pai"
__copyright__ = "pai"
__license__ = "mit"

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def snake_case(value):
    return value.lower().replace(' ', '_').replace('-', '_')

def camel_case(value):
    name = snake_case(value)

    return ''.join(word.title() for word in name.split('_'))


class Jinja2PaiCustomFilters(Extension):
    def __init__(self, environment):
        super(Jinja2PaiCustomFilters, self).__init__(environment)
        environment.filters['snake_case'] = snake_case
        environment.filters['camel_case'] = camel_case
