import unittest
from nose2.tools import params
from heuristics.core.activities.activity import Activity
from heuristics.core.activities.activity_id import ActivityID as ID
from heuristics.core.activities.initializer import ActivitiesInitializer


class ActivitiesInitializerTestSuite(unittest.TestCase):
    """Test that ActivitiesInitializer works correctly."""

    activities = [Activity("1-2", 4, 3), Activity("1-3", 6, 5), Activity("2-3", 3, 3),
                  Activity("2-5", 3, 3), Activity("2-6", 3, 3), Activity("3-5", 4, 3),
                  Activity("4-5", 4, 5), Activity("4-6", 4, 5), Activity("5-6", 3, 3)]
    correct_predecessors_ids = {ID.from_str("1-2"): [],
                                ID.from_str("1-3"): [],
                                ID.from_str("2-3"): [ID.from_str("1-2")],
                                ID.from_str("2-5"): [ID.from_str("1-2")],
                                ID.from_str("2-6"): [ID.from_str("1-2")],
                                ID.from_str("3-5"): [ID.from_str("1-3"), ID.from_str("2-3")],
                                ID.from_str("4-5"): [],
                                ID.from_str("4-6"): [],
                                ID.from_str("5-6"): [ID.from_str("2-5"), ID.from_str("3-5"),
                                                     ID.from_str("4-5")]}
    correct_successors_ids = {ID.from_str("1-2"): [ID.from_str("2-3"), ID.from_str("2-5"),
                                                   ID.from_str("2-6")],
                              ID.from_str("1-3"): [ID.from_str("3-5")],
                              ID.from_str("2-3"): [ID.from_str("3-5")],
                              ID.from_str("2-5"): [ID.from_str("5-6")],
                              ID.from_str("2-6"): [],
                              ID.from_str("3-5"): [ID.from_str("5-6")],
                              ID.from_str("4-5"): [ID.from_str("5-6")],
                              ID.from_str("4-6"): [],
                              ID.from_str("5-6"): []}

    activities_2 = [Activity("1-2", 4, 3), Activity("1-3", 6, 5), Activity("1-4", 5, 4),
                    Activity("2-3", 3, 3), Activity("2-4", 3, 3), Activity("2-5", 3, 3),
                    Activity("2-6", 3, 3), Activity("3-5", 4, 3)]

    correct_predecessors_ids_2 = {ID.from_str("1-2"): [],
                                  ID.from_str("1-3"): [],
                                  ID.from_str("1-4"): [],
                                  ID.from_str("2-3"): [ID.from_str("1-2")],
                                  ID.from_str("2-4"): [ID.from_str("1-2")],
                                  ID.from_str("2-5"): [ID.from_str("1-2")],
                                  ID.from_str("2-6"): [ID.from_str("1-2")],
                                  ID.from_str("3-5"): [ID.from_str("1-3"),
                                                       ID.from_str("2-3")]}
    correct_successors_ids_2 = {ID.from_str("1-2"): [ID.from_str("2-3"), ID.from_str("2-4"),
                                                     ID.from_str("2-5"), ID.from_str("2-6")],
                                ID.from_str("1-3"): [ID.from_str("3-5")],
                                ID.from_str("1-4"): [],
                                ID.from_str("2-3"): [ID.from_str("3-5")],
                                ID.from_str("2-4"): [],
                                ID.from_str("2-5"): [],
                                ID.from_str("2-6"): [],
                                ID.from_str("3-5"): []}

    ## Test correct behavior
    @params((activities, correct_predecessors_ids, correct_successors_ids),
            (activities_2, correct_predecessors_ids_2, correct_successors_ids_2),
            ([], {}, {}))
    def test_init_activities(self, activities, correct_pred_ids, correct_succs_ids):
        """Tests that 'init_activities' initializes Activity instances correctly."""

        ActivitiesInitializer.init_activities(activities)

        for act in activities:
            preds_ids = [pred.id for pred in act.predecessors]
            self.assertListEqual(preds_ids, correct_pred_ids[act.id])

            succs_ids = [succ.id for succ in act.successors]
            self.assertListEqual(succs_ids, correct_succs_ids[act.id])

    ## Test failures
    def test_init_activities_provided_in_nonlist_should_fail(self):
        """
        Tests that 'init_activities' fails to initialize Activity instances if
        they are provided in something else than a list.
        """

        with self.assertRaises(TypeError, msg="Initializing activities should have failed as" +
                               " they were provided in a dict, rather than a list!"):
            ActivitiesInitializer.init_activities({ID.from_str("1-2"): Activity("1-2", 4, 3),
                                                   ID.from_str("1-3"): Activity("1-3", 6, 5),
                                                   ID.from_str("2-3"): Activity("2-3", 3, 3)})
