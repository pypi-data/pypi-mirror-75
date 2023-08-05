import copy

import dataproperty

from ._csv import CsvTableWriter


class SpaceAlignedTableWriter(CsvTableWriter):
    """
    A table writer class for space aligned format.

        :Example:
            :ref:`example-space-aligned-table-writer`

    .. py:method:: write_table

        |write_table| with space aligned format.

        :Example:
            :ref:`example-space-aligned-table-writer`
    """

    FORMAT_NAME = "space_aligned"

    @property
    def format_name(self) -> str:
        return self.FORMAT_NAME

    def __init__(self) -> None:
        super().__init__()

        self.column_delimiter = "  "
        self.char_cross_point = "  "

        self.is_padding = True
        self.is_formatting_float = True

        self._quoting_flags = copy.deepcopy(dataproperty.NOT_QUOTING_FLAGS)
