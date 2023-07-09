Usage
==========================================================================

Core dependencies
-----------------

The core dependecies for EP are:

* `Python <https://www.python.org/>`_ - version 3.9.6 or newer

Python package dependencies
---------------------------

The dependencies for EP are the following Python packages:

* `nose2 <https://docs.nose2.io/en/latest/>`_ - for unit tests
* `nose2-cov <https://pypi.org/project/nose2-cov/>`_ - for test coverage (with reports etc.)
* `sphinx <https://www.sphinx-doc.org/en/master/>`_ - for generating the documentation

They can be installed using the :code:`init` task predefined in :code:`Makefile`:

.. code-block:: console

   $ make init


Run unit tests
--------------

Unit tests are written using the `nose2 <https://docs.nose2.io/en/latest/>`_ testing framework.
They can be run using the following tasks predefined in :code:`Makefile`:

.. code-block:: bash

   # Run tests only
   $ make test

   # Run tests with coverage
   $ make test_coverage

   # Run tests with coverage and output the results into a html report
   $ make test_coverage_report

To remove the generated coverage report run:

.. code-block:: bash

   $ make clean


Build documentation
___________________

Documentation is generated using `sphinx <https://www.sphinx-doc.org/en/master/>`_.
To build the documentation go to :code:`docs/` and run the following predefined task:

.. code-block:: bash

   $ make html

To remove the generated documentation run in :code:`docs/`:

.. code-block:: bash

   $ make clean