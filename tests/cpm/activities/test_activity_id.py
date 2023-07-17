import unittest
from nose2.tools import params

from heuristics.core.cpm.activities.activity_id import ActivityID as ID
from heuristics.core.cpm.activities.activity import Activity


class ActivityIDTest(unittest.TestCase):
    """Tests For ActivityID."""

    ## Test correct behavior
    @params((1, 2), (1, 3), (2, 3), (4, 5), (4, 12), (11, 13))
    def test_default_constructor(self, start_node, end_node):
        """Tests that the constructor of ActivityID works correctly."""

        act_id = ID(start_node, end_node)

        self.assertEqual(act_id.start_node, start_node)
        self.assertEqual(act_id.end_node, end_node)

    @params((1, 2), (1, 3), (2, 3), (4, 5), (4, 12), (11, 13))
    def test_from_str_constructor(self, start_node, end_node):
        """Tests that the 'from_str' constructor of ActivityID works correctly."""

        act_id = ID.from_str(f"{start_node}-{end_node}")

        self.assertEqual(act_id.start_node, start_node)
        self.assertEqual(act_id.end_node, end_node)

    @params((1, 2), (1, 3), (2, 3), (4, 5), (4, 12), (11, 13))
    def test_as_dict(self, start_node, end_node):
        """Tests that the 'as_dict' function of ActivityID returns a dict of its properties."""

        act_id = ID(start_node, end_node)
        self.assertDictEqual(act_id.as_dict(), {'start_node': start_node, 'end_node': end_node})

    @params((ID.from_str("1-2"), ID.from_str("1-2"), True),
            (ID.from_str("1-2"), ID.from_str("2-3"), False))
    def test_equality_comparison(self, act_id_left: ID, act_id_right: ID,
                                 acts_equal: bool):
        """Tests that the __eq__ function of ActivityID works correctly."""

        self.assertEqual(act_id_left == act_id_right, acts_equal)

    @params((ID.from_str("1-2"), ID.from_str("1-3"), True),
            (ID.from_str("1-2"), ID.from_str("2-2"), True),
            (ID.from_str("1-2"), ID.from_str("2-3"), True),
            (ID.from_str("1-2"), ID.from_str("1-2"), False),
            (ID.from_str("1-3"), ID.from_str("1-2"), False),
            (ID.from_str("2-2"), ID.from_str("1-2"), False),
            (ID.from_str("2-3"), ID.from_str("1-2"), False))
    def test_less_than_comparison(self, act_id_left: ID, act_id_right: ID,
                                  expected_result: bool):
        """Tests that the __lt__ function of ActivityID works correctly."""

        self.assertEqual(act_id_left < act_id_right, expected_result)

    @params((1, 2), (1, 3), (2, 3), (4, 5), (4, 12), (11, 13))
    def test_hash(self, start_node, end_node):
        """Tests that the __hash__ function of ActivityID works correctly."""

        act_id = ID(start_node, end_node)
        self.assertIsInstance(hash(act_id), int)

    ## Test failures
    @params((1, None), (None, 2))
    def test_creating_id_for_nonetype_should_fail(self, start_node, end_node):
        """Tests that ActivityID is not created from NoneType nodes."""

        with self.assertRaises(TypeError, msg="Creating the ID instance as the nodes" +
                               f" '{(start_node, end_node)}' contain a NoneType!"):
            ID(start_node, end_node)

    @params((0, 3), (4, 0), (-2, 12), (-4, -3), (4, 3))
    def test_creating_id_for_nodes_smaller_than_1_should_fail(self, start_node, end_node):
        """Tests that ActivityID is not created for nodes smaller than 1."""

        with self.assertRaises(ValueError, msg=f"Parsing of ActivityID '{(start_node, end_node)}'" +
                               "which contains a value smaller than 1!"):
            ID(start_node, end_node)

    @params((4, 3), (7, 1), (6, 2))
    def test_creating_id_for_activity_in_opposite_direction_should_fail(self, start_node, end_node):
        """
        Tests that ActivityID is not created if the activity is going in the opposite direction.

        Opposite direction means from start_node with a larger number than the end_node.
        """

        with self.assertRaises(ValueError, msg=f"Parsing of ActivityID '{(start_node, end_node)}'" +
                               " should have failed as the activity is in the opposite direction!"):
            ID(start_node, end_node)

    def test_comparing_equality_with_different_type_should_fail(self):
        """Tests that equality comparison fails when a different type is supplied."""

        act_id = ID.from_str("1-2")
        act = Activity("1-2", 4, 3)

        with self.assertRaises(NotImplementedError, msg="Validating the equality comparison of" +
                               " type 'ID' and type 'Activity' should have failed as the" +
                               " equality comparison is implemented only between the same types!"):
            act_id == act
