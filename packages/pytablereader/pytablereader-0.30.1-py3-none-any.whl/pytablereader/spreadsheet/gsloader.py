"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import typepy
from tabledata import TableData

from .._constant import TableNameTemplate as tnt
from .._validator import TextValidator
from ..error import APIError, OpenError
from .core import SpreadSheetLoader


class GoogleSheetsTableLoader(SpreadSheetLoader):
    """
    Concrete class of Google Spreadsheet loader.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(sheet)s``.

    :param str file_path: Path to the Google Sheets credential JSON file.

    :Dependency Packages:
        - `gspread <https://github.com/burnash/gspread>`_
        - `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`_
        - `oauth2client <https://pypi.org/project/oauth2client>`_
        - `pyOpenSSL <https://pypi.org/project/pyOpenSSL>`_

    :Examples:
        :ref:`example-gs-table-loader`
    """

    @property
    def _sheet_name(self):
        return self._worksheet.title

    @property
    def _row_count(self):
        return self._worksheet.row_count

    @property
    def _col_count(self):
        return self._worksheet.col_count

    def __init__(self, file_path=None, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(file_path, quoting_flags, type_hints, type_hint_rules)

        self.title = None
        self.start_row = 0

        self._validator = TextValidator(file_path)

        self.__all_values = None

    def load(self):
        """
        Load table data from a Google Spreadsheet.

        This method consider :py:attr:`.source` as a path to the
        credential JSON file to access Google Sheets API.

        The method automatically search the header row start from
        :py:attr:`.start_row`. The condition of the header row is that
        all of the columns have value (except empty columns).

        :return:
            Loaded table data. Return one |TableData| for each sheet in
            the workbook. The table name for data will be determined by
            :py:meth:`~.GoogleSheetsTableLoader.make_table_name`.
        :rtype: iterator of |TableData|
        :raises pytablereader.DataError:
            If the header row is not found.
        :raises pytablereader.OpenError:
            If the spread sheet not found.
        """

        import gspread
        from oauth2client.service_account import ServiceAccountCredentials

        self._validate_table_name()
        self._validate_title()

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.source, scope)

        gc = gspread.authorize(credentials)
        try:
            for worksheet in gc.open(self.title).worksheets():
                self._worksheet = worksheet
                self.__all_values = [row for row in worksheet.get_all_values()]

                if self._is_empty_sheet():
                    continue

                try:
                    self.__strip_empty_col()
                except ValueError:
                    continue

                value_matrix = self.__all_values[self._get_start_row_idx() :]
                try:
                    headers = value_matrix[0]
                    rows = value_matrix[1:]
                except IndexError:
                    continue

                self.inc_table_count()

                yield TableData(
                    self.make_table_name(),
                    headers,
                    rows,
                    dp_extractor=self.dp_extractor,
                    type_hints=self._extract_type_hints(headers),
                )
        except gspread.exceptions.SpreadsheetNotFound:
            raise OpenError("spreadsheet '{}' not found".format(self.title))
        except gspread.exceptions.APIError as e:
            raise APIError(e)

    def _is_empty_sheet(self):
        return len(self.__all_values) <= 1

    def _get_start_row_idx(self):
        row_idx = 0
        for row_values in self.__all_values:
            if all([typepy.is_not_null_string(value) for value in row_values]):
                break

            row_idx += 1

        return self.start_row + row_idx

    def _validate_title(self):
        if typepy.is_null_string(self.title):
            raise ValueError("spreadsheet title is empty")

    def _make_table_name(self):
        self._validate_title()

        kv_mapping = self._get_basic_tablename_keyvalue_mapping()
        kv_mapping[tnt.TITLE] = self.title
        try:
            kv_mapping[tnt.SHEET] = self._sheet_name
        except AttributeError:
            kv_mapping[tnt.SHEET] = ""

        return self._expand_table_name_format(kv_mapping)

    def __strip_empty_col(self):
        from simplesqlite import connect_memdb
        from simplesqlite.query import Attr, AttrList

        con = connect_memdb()

        tmp_table_name = "tmp"
        headers = ["a{:d}".format(i) for i in range(len(self.__all_values[0]))]
        con.create_table_from_data_matrix(tmp_table_name, headers, self.__all_values)
        for col_idx, header in enumerate(headers):
            result = con.select(select=Attr(header), table_name=tmp_table_name)
            if any([typepy.is_not_null_string(record[0]) for record in result.fetchall()]):
                break

        strip_headers = headers[col_idx:]
        if typepy.is_empty_sequence(strip_headers):
            raise ValueError()

        result = con.select(select=AttrList(strip_headers), table_name=tmp_table_name)
        self.__all_values = result.fetchall()
