Usage
=====

Core Dependencies
-----------------

The core dependencies for the HMADP project are:

* `Python <https://www.python.org/>`_ - version 3.9.6 or newer

Python Package Dependencies
---------------------------

The dependencies for HMADP are the following Python packages:

* `nose2 <https://docs.nose2.io/en/latest/>`_ - for unit tests
* `nose2-cov <https://pypi.org/project/nose2-cov/>`_ - for test coverage (with reports etc.)
* `sphinx <https://www.sphinx-doc.org/en/master/>`_ - for generating the documentation

They can be installed using the :code:`init` task predefined in :code:`Makefile`:

.. code-block:: console

   $ make init


Unit Tests
----------

Unit tests are written using the `nose2 <https://docs.nose2.io/en/latest/>`_ testing framework.
They can be run using the following tasks predefined in :code:`Makefile`:

.. code-block:: bash

   # Run tests only
   $ make tests

   # Run tests with coverage
   $ make tests_coverage

   # Run tests with coverage and output the results into a html report
   $ make tests_coverage_report

To remove the generated coverage report run:

.. code-block:: bash

   $ make clean


Build Documentation
___________________

Documentation is generated using `sphinx <https://www.sphinx-doc.org/en/master/>`_.
To build the documentation go to :code:`docs/` and run the following predefined task:

.. code-block:: bash

   $ make html

To remove the generated documentation run in :code:`docs/`:

.. code-block:: bash

   $ make clean