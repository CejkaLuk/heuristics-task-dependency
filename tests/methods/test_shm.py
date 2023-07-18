import unittest
from os import remove
from json import load
from typing import Dict, List
from csv import reader as csv_reader
from nose2.tools import params
from heuristics.core.activities.activity import Activity
from heuristics.core.activities.activity_id import ActivityID as ID
from heuristics.methods.shm import SerialHeuristicMethod as SHM
from tests.core.test_cpm import CPMTestSuite
from tests.resources.problems.problems import ProblemsPaths


class SHMTestSuite(unittest.TestCase):
    """Tests that assure SHM works correctly."""

    ## Test correct behavior
    @params((ProblemsPaths.problem_1_dir, 7, 24),
            (ProblemsPaths.problem_2_dir, 6, 16),
            (ProblemsPaths.problem_3_dir, 8, 44),
            (ProblemsPaths.problem_4_dir, 6, 19))
    def test_solve(self, problem_dir: str, r_max: int, shm_project_end: int):
        """Tests solving a set of problems using SHM."""

        problem_file = f"{problem_dir}/input.csv"
        cpm_correct_acts_file = f"{problem_dir}/cpm_solution.csv"
        shm_correct_acts_file = f"{problem_dir}/shm_solution.csv"

        shm = SHM(problem_file, r_max)
        shm.solve()

        # Verify that activities have correct values
        correct_activities = self.get_correct_activities(cpm_correct_acts_file,
                                                         shm_correct_acts_file)
        self.assertListEqual(shm.cpm.project.activities, correct_activities)

        # Verify that the project end is correct
        self.assertEqual(shm.cpm.project.actual_end, shm_project_end)

        # Verify that the resources available in each time point were not overstepped
        num_time_points = shm_project_end + 1
        self.assertEqual(len(shm.available_resources), num_time_points)
        self.assertListEqual([a_res <= r_max for a_res in shm.available_resources],
                             [True] * len(shm.available_resources))

    @params((ProblemsPaths.problem_1_dir, 7),
            (ProblemsPaths.problem_2_dir, 6),
            (ProblemsPaths.problem_3_dir, 8),
            (ProblemsPaths.problem_4_dir, 6))
    def test_to_json(self, problem_dir: str, r_max: int):
        """Tests saving an activity schedule produced by SHM to a JSON file."""

        problem_file = f"{problem_dir}/input.csv"
        cpm_acts_file = f"{problem_dir}/cpm_solution.csv"
        shm_acts_file = f"{problem_dir}/shm_solution.csv"

        activities = self.get_correct_activities(cpm_acts_file,
                                                 shm_acts_file)

        shm = SHM(problem_file, r_max)
        shm.cpm.project.activities = activities

        cpm_json_file = shm.activities_schedule_to_json_file(
            "CPM", "cpm", "cpm_activities_schedule.json")
        shm_json_file = shm.activities_schedule_to_json_file(
            json_file_path = "shm_activities_schedule.json")

        correct_cpm_acts_schedule_file = f"{problem_dir}/cpm_activities_schedule_correct.json"
        correct_shm_acts_schedule_file = f"{problem_dir}/"+ \
                                            "shm_activities_schedule_correct.json"

        cpm_acts_schedule = self.get_json_from_file(cpm_json_file)
        shm_acts_schedule = self.get_json_from_file(shm_json_file)

        correct_cpm_acts_schedule = self.get_json_from_file(correct_cpm_acts_schedule_file)
        correct_shm_acts_schedule = self.get_json_from_file(
            correct_shm_acts_schedule_file)

        self.assertDictEqual(cpm_acts_schedule, correct_cpm_acts_schedule)
        self.assertDictEqual(shm_acts_schedule, correct_shm_acts_schedule)

        # Clean up generated files
        remove(cpm_json_file)
        remove(shm_json_file)

    ## Helpful functions
    @staticmethod
    def get_correct_activities(cpm_correct_acts_file: str,
                               shm_correct_acts_file: str) -> List[Activity]:
        """Returns the activities with correct values of a particular problem from a given file."""
        activities = CPMTestSuite.get_correct_activities(cpm_correct_acts_file).activities

        with open(shm_correct_acts_file, encoding='utf-8') as sol:
            lines = csv_reader(sol, delimiter=' ')
            next(lines) # Skip CSV headers
            for line in lines:
                id = ID.from_str(str(line[0]))
                act = SHMTestSuite.get_act_by_id(id, activities)
                act.actual_start = int(line[1])
                act.actual_end = int(line[2])

        return activities

    @staticmethod
    def get_act_by_id(id: ID, activities: List[Activity]) -> Activity:
        """Returns the activity with the given id from the given list."""
        return next(filter(lambda act: act.id == id, activities))

    @staticmethod
    def get_json_from_file(file_path: str) -> Dict:
        """Returns the contents of the given JSON file as a dict."""
        with open(file_path, encoding = 'utf-8') as file:
            return load(file)
