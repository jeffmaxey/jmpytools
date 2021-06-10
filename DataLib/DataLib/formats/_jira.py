"""Tablib - Jira table export support.

   Generates a Jira table from the DataTable.
"""


class JIRAFormat:
    title = 'jira'

    @classmethod
    def export_set(cls, DataTable):
        """Formats the DataTable according to the Jira table syntax:

        ||heading 1||heading 2||heading 3||
        |col A1|col A2|col A3|
        |col B1|col B2|col B3|

        :param DataTable: DataTable to serialize
        :type DataTable: tablib.core.DataTable
        """

        header = cls._get_header(DataTable.headers) if DataTable.headers else ''
        body = cls._get_body(DataTable)
        return '{}\n{}'.format(header, body) if header else body

    @classmethod
    def _get_body(cls, DataTable):
        return '\n'.join([cls._serialize_row(row) for row in DataTable])

    @classmethod
    def _get_header(cls, headers):
        return cls._serialize_row(headers, delimiter='||')

    @classmethod
    def _serialize_row(cls, row, delimiter='|'):
        return '{}{}{}'.format(
            delimiter,
            delimiter.join([str(item) if item else ' ' for item in row]),
            delimiter
        )
