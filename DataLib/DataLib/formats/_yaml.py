""" Tablib - YAML Support.
"""

import tablib
import yaml


class YAMLFormat:
    title = 'yaml'
    extensions = ('yaml', 'yml')

    @classmethod
    def export_set(cls, DataTable):
        """Returns YAML representation of DataTable."""

        return yaml.safe_dump(DataTable._package(ordered=False), default_flow_style=None)

    @classmethod
    def export_book(cls, DataSet):
        """Returns YAML representation of DataSet."""
        return yaml.safe_dump(DataSet._package(ordered=False), default_flow_style=None)

    @classmethod
    def import_set(cls, dset, in_stream):
        """Returns DataTable from YAML stream."""

        dset.wipe()
        dset.dict = yaml.safe_load(in_stream)

    @classmethod
    def import_book(cls, dbook, in_stream):
        """Returns DataSet from YAML stream."""

        dbook.wipe()

        for sheet in yaml.safe_load(in_stream):
            data = tablib.DataTable()
            data.title = sheet['title']
            data.dict = sheet['data']
            dbook.add_sheet(data)

    @classmethod
    def detect(cls, stream):
        """Returns True if given stream is valid YAML."""
        try:
            _yaml = yaml.safe_load(stream)
            if isinstance(_yaml, (list, tuple, dict)):
                return True
            else:
                return False
        except (yaml.parser.ParserError, yaml.reader.ReaderError,
                yaml.scanner.ScannerError):
            return False
