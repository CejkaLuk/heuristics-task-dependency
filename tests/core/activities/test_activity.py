import unittest
from typing import List
from nose2.tools import params
from heuristics.core.activities.activity_id import ActivityID as ID
from heuristics.core.activities.activity import Activity


class ActivityTest(unittest.TestCase):
    """Test that Activity works correctly."""

    # Lists of activities to use for testing predecessors and successors
    activities = [Activity("1-2", 4, 3), Activity("1-3", 6, 5), Activity("2-3", 3, 3),
                  Activity("2-5", 3, 3), Activity("2-6", 3, 3), Activity("3-5", 4, 3),
                  Activity("4-5", 4, 5), Activity("4-6", 4, 5), Activity("5-6", 3, 3)]
    activities_2 = [Activity("1-2", 4, 3), Activity("1-3", 6, 5), Activity("1-4", 5, 4),
                    Activity("2-3", 3, 3), Activity("2-4", 3, 3), Activity("2-5", 3, 3),
                    Activity("2-6", 3, 3), Activity("3-5", 4, 3)]

    ## Test correct behavior
    @params("1-2", ID(1, 2))
    def test_constructor_id_various_types(self, act_id):
        """
        Tests that the Activity constructor works correctly when its id is supplied as
        a string or as an ActivityID instance.
        """

        duration = 3
        resources = 4
        act = Activity(act_id, duration, resources)

        self.assertEqual(act.id, ID(1, 2))
        self.assertEqual(act.duration, duration)
        self.assertEqual(act.resources, resources)
        self.assertEqual(act.total_resources, duration * resources)

        self.assertEqual(act.predecessors, None)
        self.assertEqual(act.successors, None)

        self.assertEqual(act.earliest_start, None)
        self.assertEqual(act.earliest_end, None)
        self.assertEqual(act.latest_start, None)
        self.assertEqual(act.latest_end, None)

        self.assertEqual(act.time_reserve, None)

    @params(("1-2", 1, 2, None, None, None, None, None, None, None),
            ("1-2", 1, 2, None, None, 3, 4, 5, 6, 7),
            ("1-2", 1, 2, [], [], 3, 4, 5, 6, 7),
            ("1-2", 1, 2, [], [], 3, 4, 5, 6, 7))
    def test_as_dict(self, act_id: ID, duration: int, resources: int,
                     predecessors: List[Activity], successors: List[Activity],
                     earliest_start: int, earliest_end: int, latest_start: int,
                     latest_end: int, time_reserve: int):
        """Tests that all variables of Activity can be fetched in a dict."""

        act = Activity(act_id, duration, resources, predecessors, successors,
                       earliest_start, earliest_end, latest_start, latest_end,
                       time_reserve)

        self.assertDictEqual(act.as_dict(),
                             {'id': ID.from_str(act_id), 'duration': duration,
                              'resources': resources, 'total_resources': duration * resources,
                              'earliest_start': earliest_start, 'earliest_end': earliest_end,
                              'latest_start': latest_start, 'latest_end': latest_end,
                              'time_reserve': time_reserve, 'actual_start': None,
                              'actual_end': None, 'priority': None })

    @params((Activity("2-3", 0, 0), activities, [ID.from_str("1-2")]),
            (Activity("3-5", 0, 0), activities, [ID.from_str("1-3"), ID.from_str("2-3")]),
            (Activity("4-5", 0, 0), activities, []),
            (Activity("1-2", 0, 0), activities_2, []), (Activity("1-3", 0, 0), activities_2, []),
            (Activity("2-3", 0, 0), activities_2, [ID.from_str("1-2")]),
            (Activity("3-5", 0, 0), activities_2, [ID.from_str("1-3"), ID.from_str("2-3")]),
            (Activity("3-5", 0, 0, []), activities_2, [ID.from_str("1-3"), ID.from_str("2-3")]),
            # Predefined (incorrect) predecessors
            (Activity("3-5", 0, 0, [Activity("4-5", 0, 0)]), activities_2, [ID.from_str("1-3"),
                                                                            ID.from_str("2-3")]))
    def test_determine_predecessors(self, act: Activity, activities: List[Activity],
                                    correct_predecessors_ids: List[ID]):
        """Tests that Activity determines its predecessors correctly from a list of activities."""

        act.determine_predecessors(activities)

        self.assertListEqual([pred.id for pred in act.predecessors], correct_predecessors_ids)

    @params((Activity("1-2", 0, 0), activities, [ID.from_str("2-3"), ID.from_str("2-5"),
                                                 ID.from_str("2-6")]),
            (Activity("2-3", 0, 0), activities, [ID.from_str("3-5")]),
            (Activity("3-5", 0, 0), activities, [ID.from_str("5-6")]),
            (Activity("1-2", 0, 0), activities_2, [ID.from_str("2-3"), ID.from_str("2-4"),
                                                   ID.from_str("2-5"), ID.from_str("2-6")]),
            (Activity("2-3", 0, 0), activities_2, [ID.from_str("3-5")]),
            (Activity("3-5", 0, 0), activities_2, []),
            (Activity("3-5", 0, 0, None, []), activities_2, []),
            # Predefined (incorrect) successors
            (Activity("3-5", 0, 0, None, [Activity("4-5", 0, 0)]), activities_2, []))
    def test_determine_successors(self, act: Activity, activities: List[Activity],
                                    correct_successors_ids: List[ID]):
        """Tests that Activity determines its successors correctly from a list of activities."""

        act.determine_successors(activities)

        self.assertListEqual([succ.id for succ in act.successors], correct_successors_ids)

    @params(# Activity ID equal and NOT equal
            (Activity("1-2", 0, 0), Activity("1-2", 0, 0), True),
            (Activity("1-2", 0, 0), Activity("2-3", 0, 0), False),
            # Duration/Resources NOT equal
            (Activity("1-2", 0, 0), Activity("1-2", 1, 0), False),
            (Activity("1-2", 0, 0), Activity("1-2", 0, 1), False),
            # Earliest start equal and NOT equal
            (Activity("1-2", 0, 0, None, None, 0),
             Activity("1-2", 0, 0, None, None, 0), True),
            (Activity("1-2", 0, 0, None, None, 1),
             Activity("1-2", 0, 0, None, None, 0), False),
            # Earliest end equal and NOT equal
            (Activity("1-2", 0, 0, None, None, 0, 0),
             Activity("1-2", 0, 0, None, None, 0, 0), True),
            (Activity("1-2", 0, 0, None, None, 0, 1),
             Activity("1-2", 0, 0, None, None, 0, 0), False),
            # Latest start equal and NOT equal
            (Activity("1-2", 0, 0, None, None, 0, 0, 0),
             Activity("1-2", 0, 0, None, None, 0, 0, 0), True),
            (Activity("1-2", 0, 0, None, None, 0, 0, 1),
             Activity("1-2", 0, 0, None, None, 0, 0, 0), False),
            # Latest end equal and NOT equal
            (Activity("1-2", 0, 0, None, None, 0, 0, 0, 0),
             Activity("1-2", 0, 0, None, None, 0, 0, 0, 0), True),
            (Activity("1-2", 0, 0, None, None, 0, 0, 0, 1),
             Activity("1-2", 0, 0, None, None, 0, 0, 0, 0), False),
            # Latest end equal and NOT equal
            (Activity("1-2", 0, 0, None, None, 0, 0, 0, 0, 0),
             Activity("1-2", 0, 0, None, None, 0, 0, 0, 0, 0), True),
            (Activity("1-2", 0, 0, None, None, 0, 0, 0, 0, 1),
             Activity("1-2", 0, 0, None, None, 0, 0, 0, 0, 0), False))
    def test_equality_comparison(self, act_left: Activity, act_right: Activity,
                                 acts_equal: bool):
        """Tests that the equality comparison of Activity works correctly."""

        # If this fails, then edit this test to validate the comparison of the equality
        # of Activity instances using all variables
        self.assertEqual(len(vars(act_left).items()), 14)

        self.assertEqual(act_left == act_right, acts_equal,
                         msg="Comparison of equality failed!" +
                         f"\n act_left = {act_left.as_dict()}" +
                         f"\n act_right = {act_right.as_dict()}")

    ## Test failures
    def test_creating_activity_with_invalid_duration_resources_should_fail(self):
        """Tests that Activity fails to be created for invalid duration and resources values."""

        with self.assertRaises(TypeError, msg="Creating the Activity instance should have failed" +
                               " as an input is NoneType!"):
            Activity(ID.from_str("1-2"), None, None)

        with self.assertRaises(ValueError, msg="Creating the Activity instance should have failed" +
                               " as an input is negative!"):
            Activity(ID.from_str("2-3"), -1, -2)

    def test_comparing_equality_with_different_type_should_fail(self):
        """Tests that the equality comparison fails when a different type is compared."""

        act = Activity("1-2", 4, 3)
        act_id = ID.from_str("1-2")

        with self.assertRaises(NotImplementedError, msg="Validating the equality comparison of" +
                               " type 'Activity' and type 'ID' should have failed as the" +
                               " equality comparison is implemented only between the same types!"):
            act == act_id

    def test_get_time_frame_with_unsupported_type_should_fail(self):
        """
        Tests that getting the time frame of an activity fails for an unsupported heuristic
        method.
        """

        act = Activity("1-2", 4, 3)

        with self.assertRaises(ValueError, msg="Getting the time frame for the 'fake_method'" +
                               " heuristic method should have failed as it is not supported."):
            act.get_time_frame("fake_method")
