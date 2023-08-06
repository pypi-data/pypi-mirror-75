"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import os
import platform
from concurrent.futures import ProcessPoolExecutor
from decimal import Decimal
from textwrap import dedent

import pytest
from path import Path
from pytablewriter import dumps_tabledata
from tabledata import TableData

import pytablereader as ptr
from pytablereader import InvalidTableNameError
from pytablereader.interface import AbstractTableReader

from ._common import TYPE_HINT_RULES, fifo_writer


Data = collections.namedtuple("Data", "value expected")

test_data_empty = Data("""""", [TableData("tmp", [], [])])
test_data_single_01 = Data(
    dedent(
        """\
        {"attr_b": 4, "attr_c": "a", "attr_a": 1}
        {"attr_b": 2.1, "attr_c": "bb", "attr_a": 2}
        {"attr_b": 120.9, "attr_c": "ccc", "attr_a": 3}
        """
    ),
    [
        TableData(
            "json_lines1",
            ["attr_b", "attr_c", "attr_a"],
            [
                {"attr_a": 1, "attr_b": 4, "attr_c": "a"},
                {"attr_a": 2, "attr_b": 2.1, "attr_c": "bb"},
                {"attr_a": 3, "attr_b": 120.9, "attr_c": "ccc"},
            ],
        )
    ],
)
test_data_single_02 = Data(
    dedent(
        """\
        {"attr_a": 1}
        {"attr_b": 2.1, "attr_c": "bb"}
        """
    ),
    [
        TableData(
            "json_lines1",
            ["attr_a", "attr_b", "attr_c"],
            [{"attr_a": 1}, {"attr_b": 2.1, "attr_c": "bb"}],
        )
    ],
)
test_data_single_03 = Data(
    dedent(
        """\
        {"attr_a": "1", "attr_b": "4", "attr_c": "a"}
        {"attr_b": "2.1", "attr_c": "bb", "attr_a": "2"}
        {"attr_b": "120.9", "attr_c": "ccc", "attr_a": "3"}
        """
    ),
    [
        TableData(
            "json_lines1",
            ["attr_a", "attr_b", "attr_c"],
            [
                {"attr_a": 1, "attr_b": 4, "attr_c": "a"},
                {"attr_a": 2, "attr_b": "2.1", "attr_c": "bb"},
                {"attr_a": 3, "attr_b": "120.9", "attr_c": "ccc"},
            ],
        )
    ],
)
test_data_single_04 = Data(
    dedent(
        """\
        {"attr_b": true, "attr_c": false}
        """
    ),
    [TableData("json_lines1", ["attr_b", "attr_c"], [{"attr_b": True, "attr_c": False}])],
)
test_data_single_20 = Data(
    dedent(
        '{"num_ratings": 27, "support_threads": 1, "downloaded": 925716, '
        '"last_updated":"2017-12-01 6:22am GMT", "added":"2010-01-20", "num": 1.1, "hoge": null}'
    ),
    [
        TableData(
            "json_lines1",
            [
                "num_ratings",
                "support_threads",
                "downloaded",
                "last_updated",
                "added",
                "num",
                "hoge",
            ],
            [
                {
                    "num_ratings": 27,
                    "support_threads": 1,
                    "downloaded": 925716,
                    "last_updated": "2017-12-01 6:22am GMT",
                    "added": "2010-01-20",
                    "num": 1.1,
                    "hoge": None,
                }
            ],
        )
    ],
)


class Test_JsonLinesTableFileLoader_make_table_name:
    LOADER_CLASS = ptr.JsonLinesTableFileLoader

    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            ["%(filename)s", "/path/to/data.json", "data"],
            ["prefix_%(filename)s", "/path/to/data.json", "prefix_data"],
            ["%(filename)s_suffix", "/path/to/data.json", "data_suffix"],
            ["prefix_%(filename)s_suffix", "/path/to/data.json", "prefix_data_suffix"],
            ["%(filename)s%(filename)s", "/path/to/data.json", "datadata"],
            ["%(format_name)s%(format_id)s_%(filename)s", "/path/to/data.json", "json_lines0_data"],
            ["hoge_%(filename)s", None, "hoge"],
            ["hoge_%(filename)s", "", "hoge"],
            ["%(%(filename)s)", "/path/to/data.json", "%(data)"],
        ],
    )
    def test_normal(self, value, source, expected):
        loader = self.LOADER_CLASS(source)
        loader.table_name = value

        assert loader.make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            [None, "/path/to/data.ldjson", ValueError],
            ["", "/path/to/data.ldjson", ValueError],
            [None, "/path/to/data.jsonl", ValueError],
            ["", "/path/to/data.jsonl", ValueError],
            ["%(filename)s", None, InvalidTableNameError],
            ["%(filename)s", "", InvalidTableNameError],
        ],
    )
    def test_exception(self, value, source, expected):
        loader = self.LOADER_CLASS(source)
        loader.table_name = value

        with pytest.raises(expected):
            loader.make_table_name()


class Test_JsonLinesTableFileLoader_load:
    LOADER_CLASS = ptr.JsonLinesTableFileLoader

    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @pytest.mark.parametrize(
        ["table_text", "filename", "table_name", "expected_tabletuple_list"],
        [
            [
                test_data_single_01.value,
                "json_lines1.jsonl",
                "%(key)s",
                test_data_single_01.expected,
            ],
            [
                test_data_single_02.value,
                "json_lines1.jsonl",
                "%(key)s",
                test_data_single_02.expected,
            ],
            [
                test_data_single_20.value,
                "json_lines1.jsonl",
                "%(key)s",
                test_data_single_20.expected,
            ],
        ],
    )
    def test_normal(self, tmpdir, table_text, filename, table_name, expected_tabletuple_list):
        file_path = Path(str(tmpdir.join(filename)))
        file_path.parent.makedirs_p()

        with open(file_path, "w") as f:
            f.write(table_text)

        loader = self.LOADER_CLASS(file_path)
        load = False
        for tabledata in loader.load():
            print("[actual]\n{}".format(dumps_tabledata(tabledata)))

            assert tabledata.in_tabledata_list(expected_tabletuple_list)
            load = True

        assert load

    @pytest.mark.skipif(platform.system() == "Windows", reason="platform dependent tests")
    @pytest.mark.parametrize(
        ["table_text", "fifo_name", "expected"],
        [[test_data_single_01.value, "json_lines1", test_data_single_01.expected]],
    )
    def test_normal_fifo(self, tmpdir, table_text, fifo_name, expected):
        namedpipe = str(tmpdir.join(fifo_name))

        os.mkfifo(namedpipe)

        loader = self.LOADER_CLASS(namedpipe)

        with ProcessPoolExecutor() as executor:
            executor.submit(fifo_writer, namedpipe, table_text)

            for tabledata in loader.load():
                print("[actual]\n{}".format(dumps_tabledata(tabledata)))

                assert tabledata.in_tabledata_list(expected)

    @pytest.mark.parametrize(
        ["table_text", "filename", "expected"],
        [
            ["[]", "tmp.jsonl", ptr.ValidationError],
            [
                """[
                    {"attr_b": 4, "attr_c": "a", "attr_a": {"aaa": 1}}
                ]""",
                "tmp.jsonl",
                ptr.ValidationError,
            ],
        ],
    )
    def test_exception(self, tmpdir, table_text, filename, expected):
        p_file_path = tmpdir.join(filename)

        with open(str(p_file_path), "w") as f:
            f.write(table_text)

        loader = self.LOADER_CLASS(str(p_file_path))

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(
        ["filename", "expected"], [["", ptr.InvalidFilePathError], [None, ptr.InvalidFilePathError]]
    )
    def test_null(self, tmpdir, filename, expected):
        loader = self.LOADER_CLASS(filename)

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass


class Test_JsonLinesTableTextLoader_make_table_name:
    LOADER_CLASS = ptr.JsonLinesTableTextLoader

    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["%(format_name)s%(format_id)s", "json_lines0"],
            ["tablename", "tablename"],
            ["[table]", "[table]"],
        ],
    )
    def test_normal(self, value, expected):
        loader = self.LOADER_CLASS("dummy")
        loader.table_name = value

        assert loader.make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [[None, "tablename", ValueError], ["", "tablename", ValueError]],
    )
    def test_exception(self, value, source, expected):
        loader = self.LOADER_CLASS(source)
        loader.table_name = value

        with pytest.raises(expected):
            loader.make_table_name()


class Test_JsonLinesTableTextLoader_load:
    LOADER_CLASS = ptr.JsonLinesTableTextLoader

    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @pytest.mark.parametrize(
        ["table_text", "table_name", "expected_tabletuple_list"],
        [
            [test_data_single_01.value, "json_lines1", test_data_single_01.expected],
            [test_data_single_02.value, "json_lines1", test_data_single_02.expected],
            [test_data_single_03.value, "%(key)s", test_data_single_03.expected],
            [test_data_single_04.value, "%(key)s", test_data_single_04.expected],
            [test_data_single_20.value, "%(key)s", test_data_single_20.expected],
        ],
    )
    def test_normal(self, table_text, table_name, expected_tabletuple_list):
        self.LOADER_CLASS.clear_table_count()
        loader = self.LOADER_CLASS(table_text)
        loader.table_name = table_name

        load = False
        for tabledata in loader.load():
            print("[actual]\n{}".format(dumps_tabledata(tabledata)))
            print("[expected]")
            for expected in expected_tabletuple_list:
                print("{}".format(dumps_tabledata(tabledata)))

            assert tabledata.in_tabledata_list(expected_tabletuple_list)
            load = True

        assert load

    def test_normal_type_hint_rules(self):
        table_text = dedent(
            """\
            {"a_text": 1, "b_integer": "1", "c_real": "1.1"}
            {"a_text": 2, "b_integer": "2", "c_real": "1.2"}
            {"a_text": 3, "b_integer": "3", "c_real": "1.3"}
            """
        )

        loader = self.LOADER_CLASS(table_text)
        loader.table_name = "type hint rules"
        loader.type_hint_rules = TYPE_HINT_RULES

        for tbldata in loader.load():
            assert tbldata.headers == ["a_text", "b_integer", "c_real"]
            assert tbldata.value_matrix == [
                ["1", 1, Decimal("1.1")],
                ["2", 2, Decimal("1.2")],
                ["3", 3, Decimal("1.3")],
            ]

    @pytest.mark.parametrize(
        ["table_text", "expected"],
        [
            ["[]", ptr.ValidationError],
            [
                """[
                {"attr_b": 4, "attr_c": "a", "attr_a": {"aaa": 1}}
            ]""",
                ptr.ValidationError,
            ],
        ],
    )
    def test_exception(self, table_text, expected):
        loader = self.LOADER_CLASS(table_text)
        loader.table_name = "dummy"

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(
        ["table_text", "expected"], [["", ptr.DataError], [None, ptr.DataError]]
    )
    def test_null(self, table_text, expected):
        loader = self.LOADER_CLASS(table_text)
        loader.table_name = "dummy"

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
