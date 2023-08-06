========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - |
        |
    * - package
      - | |commits-since|

.. |commits-since| image:: https://img.shields.io/github/commits-since/claudioperez/Beam2D/v1.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/claudioperez/Beam2D/compare/v1.0.0...master



.. end-badges

2D beam model.

* Free software: BSD 3-Clause License

Installation
============

::

    pip install beam2d

You can also install the in-development version with::

    pip install https://github.com/claudioperez/Beam2D/archive/master.zip


Documentation
=============


To use the project:

.. code-block:: python

    import beam2d
    beam2d.longest()


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
