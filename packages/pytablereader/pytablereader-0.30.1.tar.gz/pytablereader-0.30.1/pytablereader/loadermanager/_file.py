"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import warnings

import typepy

from ..factory import TableFileLoaderFactory
from ._base import TableLoaderManager


class TableFileLoader(TableLoaderManager):
    """
    Loader class to loading tables from a file.

    :param str file_path: Path to the file to load.
    :param str format_name: Data format name to load.
        Supported formats are as follows:
        ``"csv"``, ``"excel"``, ``"html"``, ``"json"``, ``"ltsv"``,
        ``"markdown"``, ``"mediawiki"``, ``"sqlite"``, ``"ssv"``, ``"tsv"``.
        If the value is |None|, automatically detect file format from
        the ``file_path``.
    :raise pytablereader.InvalidFilePathError:
        If ``file_path`` is an invalid file path.
    :raises pytablereader.LoaderNotFoundError:
        |LoaderNotFoundError_desc| loading the file.

    .. py:method:: load

        Loading table data from a file as ``format_name`` format.
        Automatically detect file format if ``format_name`` is |None|.

        :return: Loaded table data iterator.
        :rtype: |TableData| iterator

        .. seealso::
            * :py:meth:`pytablereader.factory.TableFileLoaderFactory.create_from_format_name`
            * :py:meth:`pytablereader.factory.TableFileLoaderFactory.create_from_path`
    """

    def __init__(self, file_path, format_name=None, encoding=None, type_hint_rules=None):
        loader_factory = TableFileLoaderFactory(file_path, encoding=encoding)

        if typepy.is_not_null_string(format_name):
            loader = loader_factory.create_from_format_name(format_name)
        else:
            loader = loader_factory.create_from_path()

        loader.type_hint_rules = type_hint_rules

        super().__init__(loader)

    @classmethod
    def get_format_names(cls):
        """
        :return:
            Available format names. These names can use by
            :py:class:`.TableFileLoader` class constructor.
        :rtype: list

        :Example:
            .. code:: python

                >>> from pytablereader import TableFileLoader
                >>> for format_name in TableFileLoader.get_format_names():
                ...     print(format_name)
                ...
                csv
                excel
                html
                json
                json_lines
                jsonl
                ldjson
                ltsv
                markdown
                mediawiki
                ndjson
                sqlite
                ssv
                tsv
        """

        return TableFileLoaderFactory("dummy").get_format_names()

    @classmethod
    def get_format_name_list(cls):
        warnings.warn("'get_format_name_list' has moved to 'get_format_names'", DeprecationWarning)
        return cls.get_format_names()
