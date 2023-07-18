import unittest
from os import remove
from typing import List
from csv import reader as csv_reader
from nose2.tools import params
from heuristics.core.activities.activity import Activity
from heuristics.core.activities.activity_id import ActivityID as ID
from heuristics.methods.phm import ParallelHeuristicMethod as PHM
from tests.core.test_cpm import CPMTestSuite
from tests.methods.test_shm import SHMTestSuite
from tests.resources.problems.problems import ProblemsPaths


class PHMTestSuite(unittest.TestCase):
    """Tests that assure PHM works correctly."""

    ## Test correct behavior
    @params((ProblemsPaths.problem_1_dir, 7, 20),
            (ProblemsPaths.problem_2_dir, 6, 15),
            (ProblemsPaths.problem_3_dir, 8, 43),
            (ProblemsPaths.problem_4_dir, 6, 17))
    def test_solve(self, problem_dir: str, r_max: int, phm_project_end: int):
        """Tests solving a set of problems using PHM."""

        problem_file = f"{problem_dir}/input.csv"
        cpm_correct_acts_file = f"{problem_dir}/cpm_solution.csv"
        phm_correct_acts_file = f"{problem_dir}/phm_solution.csv"

        phm = PHM(problem_file, r_max)
        phm.solve()

        # Verify that activities have correct values
        correct_activities = self.get_correct_activities(cpm_correct_acts_file,
                                                         phm_correct_acts_file)
        self.assertListEqual(phm.cpm.project.activities, correct_activities)

        # Verify that the project end is correct
        self.assertEqual(phm.cpm.project.actual_end, phm_project_end)

        # Verify that the resources available in each time point were not overstepped
        num_time_points = phm_project_end + 1
        self.assertEqual(len(phm.available_resources), num_time_points)
        self.assertListEqual([a_res <= r_max for a_res in phm.available_resources],
                             [True] * len(phm.available_resources))

    @params((ProblemsPaths.problem_1_dir, 7),
            (ProblemsPaths.problem_2_dir, 6),
            (ProblemsPaths.problem_3_dir, 8),
            (ProblemsPaths.problem_4_dir, 6))
    def test_to_json(self, problem_dir: str, r_max: int):
        """Tests saving an activity schedule produced by PHM to a JSON file."""

        problem_file = f"{problem_dir}/input.csv"
        cpm_acts_file = f"{problem_dir}/cpm_solution.csv"
        phm_acts_file = f"{problem_dir}/phm_solution.csv"

        activities = self.get_correct_activities(cpm_acts_file,
                                                 phm_acts_file)

        phm = PHM(problem_file, r_max)
        phm.cpm.project.activities = activities

        cpm_json_file = phm.activities_schedule_to_json_file(
            "CPM", "cpm", "cpm_activities_schedule.json")
        phm_json_file = phm.activities_schedule_to_json_file(
            json_file_path = "phm_activities_schedule.json")

        correct_cpm_acts_schedule_file = f"{problem_dir}/cpm_activities_schedule_correct.json"
        correct_phm_acts_schedule_file = f"{problem_dir}/"+ \
                                            "phm_activities_schedule_correct.json"

        cpm_acts_schedule = SHMTestSuite.get_json_from_file(cpm_json_file)
        phm_acts_schedule = SHMTestSuite.get_json_from_file(phm_json_file)

        correct_cpm_acts_schedule = SHMTestSuite.get_json_from_file(
            correct_cpm_acts_schedule_file)
        correct_phm_acts_schedule = SHMTestSuite.get_json_from_file(
            correct_phm_acts_schedule_file)

        self.assertDictEqual(cpm_acts_schedule, correct_cpm_acts_schedule)
        self.assertDictEqual(phm_acts_schedule, correct_phm_acts_schedule)

        # Clean up generated files
        remove(cpm_json_file)
        remove(phm_json_file)

    ## Helpful functions
    @staticmethod
    def get_correct_activities(cpm_correct_acts_file: str,
                               phm_correct_acts_file: str) -> List[Activity]:
        """Returns the activities with correct values of a particular problem from a given file."""
        activities = CPMTestSuite.get_correct_activities(cpm_correct_acts_file).activities

        with open(phm_correct_acts_file, encoding='utf-8') as sol:
            lines = csv_reader(sol, delimiter=' ')
            next(lines) # Skip CSV headers
            for line in lines:
                id = ID.from_str(str(line[0]))
                act = SHMTestSuite.get_act_by_id(id, activities)
                act.actual_start = int(line[1])
                act.actual_end = int(line[2])
                act.priority = int(line[3])

        return activities
