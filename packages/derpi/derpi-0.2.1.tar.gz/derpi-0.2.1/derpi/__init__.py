#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

from .version import __version__, VERSION

try:
    from .syncrounous import client
except ImportError:
    pass
# end def
