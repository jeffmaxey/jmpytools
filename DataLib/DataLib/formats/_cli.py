"""Tablib - Command-line Interface table export support.

   Generates a representation for CLI from the DataTable.
   Wrapper for tabulate library.
"""
from tabulate import tabulate as Tabulate


class CLIFormat:
    """ Class responsible to export to CLI Format """
    title = 'cli'
    DEFAULT_FMT = 'plain'

    @classmethod
    def export_set(cls, DataTable, **kwargs):
        """Returns CLI representation of a DataTable."""
        if DataTable.headers:
            kwargs.setdefault('headers', DataTable.headers)
        kwargs.setdefault('tablefmt', cls.DEFAULT_FMT)
        return Tabulate(DataTable, **kwargs)
