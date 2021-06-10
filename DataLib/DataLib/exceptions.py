#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
exceptions.py
~~~~~~~~~~~~~

"""


class InvalidDataTableType(Exception):
    """Only DataTables can be added to a DataTable"""


class InvalidDimensions(Exception):
    """Invalid size"""


class InvalidDataTableIndex(Exception):
    """Outside of DataTable size"""


class HeadersNeeded(Exception):
    """Header parameter must be given when appending a column in this DataTable."""


class UnsupportedFormat(NotImplementedError):
    """Format is not supported"""
