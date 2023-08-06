.. contents:: **pytablereader**
   :backlinks: top
   :depth: 2

Summary
=========
`pytablereader <https://github.com/thombashi/pytablereader>`__ is a Python library to load structured table data from files/strings/URL with various data format: CSV / Excel / Google-Sheets / HTML / JSON / LDJSON / LTSV / Markdown / SQLite / TSV.

.. image:: https://badge.fury.io/py/pytablereader.svg
    :target: https://badge.fury.io/py/pytablereader
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/pytablereader.svg
    :target: https://pypi.org/project/pytablereader
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/pytablereader.svg
    :target: https://pypi.org/project/pytablereader
    :alt: Supported Python implementations

.. image:: https://img.shields.io/travis/thombashi/pytablereader/master.svg?label=Linux/macOS%20CI
    :target: https://travis-ci.org/thombashi/pytablereader
    :alt: Linux/macOS CI status

.. image:: https://img.shields.io/appveyor/ci/thombashi/pytablereader/master.svg?label=Windows%20CI
    :target: https://ci.appveyor.com/project/thombashi/pytablereader/branch/master
    :alt: Windows CI status

.. image:: https://coveralls.io/repos/github/thombashi/pytablereader/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/pytablereader?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/github/stars/thombashi/pytablereader.svg?style=social&label=Star
    :target: https://github.com/thombashi/pytablereader
    :alt: GitHub stars

Features
--------
- Extract structured tabular data from various data format:
    - CSV / Tab separated values (TSV) / Space separated values (SSV)
    - Microsoft Excel :superscript:`TM` file
    - `Google Sheets <https://www.google.com/intl/en_us/sheets/about/>`_
    - HTML (``table`` tags)
    - JSON
    - `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
    - `Line-delimited JSON(LDJSON) <https://en.wikipedia.org/wiki/JSON_streaming#Line-delimited_JSON>`__ / NDJSON / JSON Lines
    - Markdown
    - MediaWiki
    - SQLite database file
- Supported data sources are:
    - Files on a local file system
    - Accessible URLs
    - ``str`` instances
- Loaded table data can be used as:
    - `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html>`__ instance
    - ``dict`` instance

Examples
==========
Load a CSV table
------------------
:Sample Code:
    .. code-block:: python

        import pytablereader as ptr
        import pytablewriter as ptw


        # prepare data ---
        file_path = "sample_data.csv"
        csv_text = "\n".join([
            '"attr_a","attr_b","attr_c"',
            '1,4,"a"',
            '2,2.1,"bb"',
            '3,120.9,"ccc"',
        ])

        with open(file_path, "w") as f:
            f.write(csv_text)

        # load from a csv file ---
        loader = ptr.CsvTableFileLoader(file_path)
        for table_data in loader.load():
            print("\n".join([
                "load from file",
                "==============",
                "{:s}".format(ptw.dumps_tabledata(table_data)),
            ]))

        # load from a csv text ---
        loader = ptr.CsvTableTextLoader(csv_text)
        for table_data in loader.load():
            print("\n".join([
                "load from text",
                "==============",
                "{:s}".format(ptw.dumps_tabledata(table_data)),
            ]))


:Output:
    .. code-block::

        load from file
        ==============
        .. table:: sample_data

            ======  ======  ======
            attr_a  attr_b  attr_c
            ======  ======  ======
                 1     4.0  a
                 2     2.1  bb
                 3   120.9  ccc
            ======  ======  ======

        load from text
        ==============
        .. table:: csv2

            ======  ======  ======
            attr_a  attr_b  attr_c
            ======  ======  ======
                 1     4.0  a
                 2     2.1  bb
                 3   120.9  ccc
            ======  ======  ======

Get loaded table data as pandas.DataFrame instance
----------------------------------------------------

:Sample Code:
    .. code-block:: python

        import pytablereader as ptr

        loader = ptr.CsvTableTextLoader(
            "\n".join([
                "a,b",
                "1,2",
                "3.3,4.4",
            ]))
        for table_data in loader.load():
            print(table_data.as_dataframe())

:Output:
    .. code-block::

             a    b
        0    1    2
        1  3.3  4.4

For more information
----------------------
More examples are available at 
https://pytablereader.rtfd.io/en/latest/pages/examples/index.html

Installation
============

Install from PyPI
------------------------------
::

    pip install pytablereader

Some of the formats require additional dependency packages, you can install the dependency packages as follows:

- Excel
    - ``pip install pytablereader[excel]``
- Google Sheets
    - ``pip install pytablereader[gs]``
- Markdown
    - ``pip install pytablereader[md]``
- Mediawiki
    - ``pip install pytablereader[mediawiki]``
- SQLite
    - ``pip install pytablereader[sqlite]``
- Load from URLs
    - ``pip install pytablereader[url]``
- All of the extra dependencies
    - ``pip install pytablereader[all]``

Install from PPA (for Ubuntu)
------------------------------
::

    sudo add-apt-repository ppa:thombashi/ppa
    sudo apt update
    sudo apt install python3-pytablereader


Dependencies
============
- Python 3.5+
- `Python package dependencies (automatically installed) <https://github.com/thombashi/pytablereader/network/dependencies>`__


Optional Python packages
------------------------------------------------
- `logging` extras
    - `loguru <https://github.com/Delgan/loguru>`__: Used for logging if the package installed
- `excel` extras
    - `excelrd <https://github.com/thombashi/excelrd>`__
- `md` extras
    - `Markdown <https://github.com/Python-Markdown/markdown>`__
- `mediawiki` extras
    - `pypandoc <https://github.com/bebraw/pypandoc>`__
- `sqlite` extras
    - `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- `url` extras
    - `requests <http://python-requests.org/>`__
    - `retryrequests <https://github.com/thombashi/retryrequests>`__
- `pandas <https://pandas.pydata.org/>`__
    - required to get table data as a pandas data frame
- `lxml <https://lxml.de/installation.html>`__

Optional packages (other than Python packages)
------------------------------------------------
- ``libxml2`` (faster HTML conversion)
- `pandoc <https://pandoc.org/>`__ (required when loading MediaWiki file)

Documentation
===============
https://pytablereader.rtfd.io/

Related Project
=================
- `pytablewriter <https://github.com/thombashi/pytablewriter>`__
    - Tabular data loaded by ``pytablereader`` can be written another tabular data format with ``pytablewriter``.

Sponsors
====================================
.. image:: https://avatars0.githubusercontent.com/u/44389260?s=48&u=6da7176e51ae2654bcfd22564772ef8a3bb22318&v=4
   :target: https://github.com/chasbecker
   :alt: Charles Becker (chasbecker)

`Become a sponsor <https://github.com/sponsors/thombashi>`__

