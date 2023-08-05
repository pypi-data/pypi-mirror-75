========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/monopolion-evaluator/badge/?style=flat
    :target: https://readthedocs.org/projects/monopolion-evaluator
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/miermans/monopolion-evaluator.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/miermans/monopolion-evaluator

.. |coveralls| image:: https://coveralls.io/repos/miermans/monopolion-evaluator/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/miermans/monopolion-evaluator

.. |version| image:: https://img.shields.io/pypi/v/monopolion-evaluator.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/monopolion-evaluator

.. |wheel| image:: https://img.shields.io/pypi/wheel/monopolion-evaluator.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/monopolion-evaluator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/monopolion-evaluator.svg
    :alt: Supported versions
    :target: https://pypi.org/project/monopolion-evaluator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/monopolion-evaluator.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/monopolion-evaluator

.. |commits-since| image:: https://img.shields.io/github/commits-since/miermans/monopolion-evaluator/v0.0.2.svg
    :alt: Commits since latest release
    :target: https://github.com/miermans/monopolion-evaluator/compare/v0.0.2...master



.. end-badges

Neural net to predict winning probability in Monopoly

* Free software: MIT license

Installation
============

::

    pip install monopolion-evaluator

You can also install the in-development version with::

    pip install https://github.com/miermans/monopolion-evaluator/archive/master.zip


Documentation
=============


https://monopolion-evaluator.readthedocs.io/


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
