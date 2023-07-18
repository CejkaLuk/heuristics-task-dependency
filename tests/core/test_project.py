from random import shuffle
import unittest
from typing import List
from nose2.tools import params
from heuristics.core.project import Project
from heuristics.core.activities.activity import Activity
from tests.resources.problems.problems import ProblemsPaths


class ProjectTestSuite(unittest.TestCase):
    """Tests that assure Project works correctly."""

    activities = [Activity("1-2", 4, 3), Activity("1-3", 6, 5), Activity("2-3", 3, 3),
                  Activity("2-5", 3, 3), Activity("2-6", 3, 3), Activity("3-5", 4, 3),
                  Activity("4-5", 4, 5), Activity("4-6", 4, 5), Activity("5-6", 3, 3)]
    r_max_1 = 6

    activities_2 = [Activity("1-2", 4, 3), Activity("1-3", 6, 5), Activity("1-4", 5, 4),
                    Activity("2-3", 3, 3), Activity("2-4", 3, 3), Activity("2-5", 3, 3),
                    Activity("2-6", 3, 3), Activity("3-5", 4, 3)]
    r_max_2 = 7

    ## Test correct behavior
    @params((activities, r_max_1, 130),
            (activities_2, r_max_2, 110))
    def test_default_constructor(self, activities, r_max, total_resources_required):
        """Tests that the default constructor works correctly."""

        cpm_proj = Project(activities, r_max)

        self.assertIsInstance(cpm_proj.activities, list)
        for act in cpm_proj.activities:
            self.assertIsInstance(act, Activity)

            self.assertRegex(str(act.id), "^[1-9][0-9]*-[1-9][0-9]*$")
            self.assertGreaterEqual(act.duration, 0)
            self.assertGreaterEqual(act.resources, 0)
            self.assertGreaterEqual(len(act.predecessors), 0)
            self.assertGreaterEqual(len(act.successors), 0)

        self.assertIsInstance(cpm_proj.r_max, int)
        self.assertEqual(cpm_proj.r_max, r_max)

        self.assertEqual(cpm_proj.total_resources_required, total_resources_required)

    @params((f"{ProblemsPaths.problem_1_dir}/input.csv", 7, 112),
            (f"{ProblemsPaths.problem_2_dir}/input.csv", 6, 71))
    def test_from_file_and_args_constructor(self, acts_file_path, r_max, total_resources_required):
        """Tests that the 'from_file_and_args' constructor works correctly."""

        cpm_proj = Project.from_file_and_args(acts_file_path, r_max)

        self.assertIsInstance(cpm_proj.activities, list)
        for act in cpm_proj.activities:
            self.assertIsInstance(act, Activity)

            self.assertRegex(str(act.id), "^[1-9][0-9]*-[1-9][0-9]*$")
            self.assertGreaterEqual(act.duration, 0)
            self.assertGreaterEqual(act.resources, 0)
            self.assertGreaterEqual(len(act.predecessors), 0)
            self.assertGreaterEqual(len(act.successors), 0)

        self.assertIsInstance(cpm_proj.r_max, int)
        self.assertGreater(cpm_proj.r_max, 0)

        self.assertEqual(cpm_proj.total_resources_required, total_resources_required)

    @params(activities, activities_2)
    def test_sorting_activities_by_id(self, activities: List[Activity]):
        """Tests that the activities are sorted in ascending order according to their ID."""

        r_max = 6
        activities_copy = activities.copy()

        cpm_proj = Project(activities_copy, r_max)

        self.assertListEqual(activities, cpm_proj.activities)

        shuffled_activities = activities.copy()
        shuffle(shuffled_activities)

        self.assertNotEqual(activities, shuffled_activities)

        cpm_proj_2 = Project(shuffled_activities, r_max)

        self.assertListEqual(activities, cpm_proj_2.activities)
