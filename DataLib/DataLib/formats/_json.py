""" Tablib - JSON Support
"""
import decimal
import json
from uuid import UUID

import tablib


def serialize_objects_handler(obj):
    if isinstance(obj, (decimal.Decimal, UUID)):
        return str(obj)
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return obj


class JSONFormat:
    title = 'json'
    extensions = ('json', 'jsn')

    @classmethod
    def export_set(cls, DataTable):
        """Returns JSON representation of DataTable."""
        return json.dumps(DataTable.dict, default=serialize_objects_handler)

    @classmethod
    def export_book(cls, DataSet):
        """Returns JSON representation of DataSet."""
        return json.dumps(DataSet._package(), default=serialize_objects_handler)

    @classmethod
    def import_set(cls, dset, in_stream):
        """Returns DataTable from JSON stream."""

        dset.wipe()
        dset.dict = json.load(in_stream)

    @classmethod
    def import_book(cls, dbook, in_stream):
        """Returns DataSet from JSON stream."""

        dbook.wipe()
        for sheet in json.load(in_stream):
            data = tablib.DataTable()
            data.title = sheet['title']
            data.dict = sheet['data']
            dbook.add_sheet(data)

    @classmethod
    def detect(cls, stream):
        """Returns True if given stream is valid JSON."""
        try:
            json.load(stream)
            return True
        except (TypeError, ValueError):
            return False
