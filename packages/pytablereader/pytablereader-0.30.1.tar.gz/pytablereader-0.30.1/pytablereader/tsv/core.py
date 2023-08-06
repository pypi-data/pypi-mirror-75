"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from .._validator import FileValidator, TextValidator
from ..csv.core import CsvTableFileLoader, CsvTableTextLoader


class TsvTableFileLoader(CsvTableFileLoader):
    """
    Tab separated values (TSV) format file loader class.

    :param str file_path: Path to the loading TSV file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s``.
    """

    @property
    def format_name(self):
        return "tsv"

    def __init__(self, file_path):
        super().__init__(file_path)

        self.delimiter = "\t"

        self._validator = FileValidator(file_path)


class TsvTableTextLoader(CsvTableTextLoader):
    """
    Tab separated values (TSV) format text loader class.

    :param str text: TSV text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(format_name)s%(format_id)s``.
    """

    @property
    def format_name(self):
        return "tsv"

    def __init__(self, text):
        super().__init__(text)

        self.delimiter = "\t"

        self._validator = TextValidator(text)
