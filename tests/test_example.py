from .context import examples

import unittest


class ExampleClassTestSuite(unittest.TestCase):
    """Example Class test suite."""

    def test_ExampleClassName(self):
        example = examples.ExampleClass()
        assert example.getClassName() == 'ExamplesClass'