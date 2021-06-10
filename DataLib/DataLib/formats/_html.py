""" Tablib - HTML export support.
"""

import codecs
from io import BytesIO

from MarkupPy import markup


class HTMLFormat:
    BOOK_ENDINGS = 'h3'

    title = 'html'
    extensions = ('html', )

    @classmethod
    def export_set(cls, DataTable):
        """HTML representation of a DataTable."""

        stream = BytesIO()

        page = markup.page()
        page.table.open()

        if DataTable.headers is not None:
            new_header = [item if item is not None else '' for item in DataTable.headers]

            page.thead.open()
            headers = markup.oneliner.th(new_header)
            page.tr(headers)
            page.thead.close()

        for row in DataTable:
            new_row = [item if item is not None else '' for item in row]

            html_row = markup.oneliner.td(new_row)
            page.tr(html_row)

        page.table.close()

        # Allow unicode characters in output
        wrapper = codecs.getwriter("utf8")(stream)
        wrapper.writelines(str(page))

        return stream.getvalue().decode('utf-8')

    @classmethod
    def export_book(cls, DataSet):
        """HTML representation of a DataSet."""

        stream = BytesIO()

        # Allow unicode characters in output
        wrapper = codecs.getwriter("utf8")(stream)

        for i, dset in enumerate(DataSet._DataTables):
            title = (dset.title if dset.title else 'Set %s' % (i))
            wrapper.write('<{}>{}</{}>\n'.format(cls.BOOK_ENDINGS, title, cls.BOOK_ENDINGS))
            wrapper.write(dset.html)
            wrapper.write('\n')

        return stream.getvalue().decode('utf-8')
