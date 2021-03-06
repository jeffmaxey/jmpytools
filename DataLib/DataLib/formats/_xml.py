""" Tablib - XML support.
"""

import xml.etree.ElementTree as ET


class XMLFormat:
    title = 'xml'
    extensions = ('xml',)

    # TODO implement
    # @classmethod
    # def import_set(cls, dset, in_stream):
    #     dset.wipe()

    @classmethod
    def export_set(cls, DataTable):
        root = ET.Element('DataTable')

        for row_index, row in enumerate(DataTable.dict):
            row_node = ET.Element('row')
            tags = DataTable._data[row_index].tags
            if tags:
                row_node.set('tags', ','.join(tags))
            for header, value in row.items():
                value_node = ET.Element(header)
                value_node.text = str(value)
                row_node.append(value_node)

            root.append(row_node)

        return ET.tostring(root).decode()
