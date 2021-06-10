"""Tablib - LaTeX table export support.

   Generates a LaTeX booktabs-style table from the DataTable.
"""
import re


class LATEXFormat:
    title = 'latex'
    extensions = ('tex',)

    TABLE_TEMPLATE = """\
%% Note: add \\usepackage{booktabs} to your preamble
%%
\\begin{table}[!htbp]
  \\centering
  %(CAPTION)s
  \\begin{tabular}{%(COLSPEC)s}
    \\toprule
%(HEADER)s
    %(MIDRULE)s
%(BODY)s
    \\bottomrule
  \\end{tabular}
\\end{table}
"""

    TEX_RESERVED_SYMBOLS_MAP = dict([
        ('\\', '\\textbackslash{}'),
        ('{', '\\{'),
        ('}', '\\}'),
        ('$', '\\$'),
        ('&', '\\&'),
        ('#', '\\#'),
        ('^', '\\textasciicircum{}'),
        ('_', '\\_'),
        ('~', '\\textasciitilde{}'),
        ('%', '\\%'),
    ])

    TEX_RESERVED_SYMBOLS_RE = re.compile(
        '(%s)' % '|'.join(map(re.escape, TEX_RESERVED_SYMBOLS_MAP.keys())))

    @classmethod
    def export_set(cls, DataTable):
        """Returns LaTeX representation of DataTable

        :param DataTable: DataTable to serialize
        :type DataTable: tablib.core.DataTable
        """

        caption = '\\caption{%s}' % DataTable.title if DataTable.title else '%'
        colspec = cls._colspec(DataTable.width)
        header = cls._serialize_row(DataTable.headers) if DataTable.headers else ''
        midrule = cls._midrule(DataTable.width)
        body = '\n'.join([cls._serialize_row(row) for row in DataTable])
        return cls.TABLE_TEMPLATE % dict(CAPTION=caption, COLSPEC=colspec,
                                     HEADER=header, MIDRULE=midrule, BODY=body)

    @classmethod
    def _colspec(cls, DataTable_width):
        """Generates the column specification for the LaTeX `tabular` environment
        based on the DataTable width.

        The first column is justified to the left, all further columns are aligned
        to the right.

        .. note:: This is only a heuristic and most probably has to be fine-tuned
        post export. Column alignment should depend on the data type, e.g., textual
        content should usually be aligned to the left while numeric content almost
        always should be aligned to the right.

        :param DataTable_width: width of the DataTable
        """

        spec = 'l'
        for _ in range(1, DataTable_width):
            spec += 'r'
        return spec

    @classmethod
    def _midrule(cls, DataTable_width):
        """Generates the table `midrule`, which may be composed of several
        `cmidrules`.

        :param DataTable_width: width of the DataTable to serialize
        """

        if not DataTable_width or DataTable_width == 1:
            return '\\midrule'
        return ' '.join([cls._cmidrule(colindex, DataTable_width) for colindex in
                         range(1, DataTable_width + 1)])

    @classmethod
    def _cmidrule(cls, colindex, DataTable_width):
        """Generates the `cmidrule` for a single column with appropriate trimming
        based on the column position.

        :param colindex: Column index
        :param DataTable_width: width of the DataTable
        """

        rule = '\\cmidrule(%s){%d-%d}'
        if colindex == 1:
            # Rule of first column is trimmed on the right
            return rule % ('r', colindex, colindex)
        if colindex == DataTable_width:
            # Rule of last column is trimmed on the left
            return rule % ('l', colindex, colindex)
        # Inner columns are trimmed on the left and right
        return rule % ('lr', colindex, colindex)

    @classmethod
    def _serialize_row(cls, row):
        """Returns string representation of a single row.

        :param row: single DataTable row
        """

        new_row = [cls._escape_tex_reserved_symbols(str(item)) if item else ''
                   for item in row]
        return 6 * ' ' + ' & '.join(new_row) + ' \\\\'

    @classmethod
    def _escape_tex_reserved_symbols(cls, input):
        """Escapes all TeX reserved symbols ('_', '~', etc.) in a string.

        :param input: String to escape
        """
        def replace(match):
            return cls.TEX_RESERVED_SYMBOLS_MAP[match.group()]
        return cls.TEX_RESERVED_SYMBOLS_RE.sub(replace, input)
