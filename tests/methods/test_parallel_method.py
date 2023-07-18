import unittest
from os import remove
from typing import List
from csv import reader as csv_reader
from nose2.tools import params
from heuristics.core.activities.activity import Activity
from heuristics.core.activities.activity_id import ActivityID as ID
from heuristics.methods.parallel_method import ParallelMethod
from tests.core.test_cpm import CPMTestSuite
from tests.methods.test_serial_method import SerialMethodTestSuite
from tests.resources.problems.problems import ProblemsPaths


class ParallelMethodTestSuite(unittest.TestCase):
    """Tests that assure ParallelMethod works correctly."""

    ## Test correct behavior
    @params((ProblemsPaths.problem_1_dir, 7, 20),
            (ProblemsPaths.problem_2_dir, 6, 15),
            (ProblemsPaths.problem_3_dir, 8, 43),
            (ProblemsPaths.problem_4_dir, 6, 17))
    def test_solve(self, problem_dir: str, r_max: int, parallel_method_project_end: int):
        """Tests solving a set of problems using ParallelMethod."""

        problem_file = f"{problem_dir}/input.csv"
        cpm_correct_acts_file = f"{problem_dir}/cpm_solution.csv"
        parallel_method_correct_acts_file = f"{problem_dir}/parallel_method_solution.csv"

        parallel_method = ParallelMethod(problem_file, r_max)
        parallel_method.solve()

        # Verify that activities have correct values
        correct_activities = self.get_correct_activities(cpm_correct_acts_file,
                                                         parallel_method_correct_acts_file)
        self.assertListEqual(parallel_method.cpm.project.activities, correct_activities)

        # Verify that the project end is correct
        self.assertEqual(parallel_method.cpm.project.actual_end, parallel_method_project_end)

        # Verify that the resources available in each time point were not overstepped
        num_time_points = parallel_method_project_end + 1
        self.assertEqual(len(parallel_method.available_resources), num_time_points)
        self.assertListEqual([a_res <= r_max for a_res in parallel_method.available_resources],
                             [True] * len(parallel_method.available_resources))

    @params((ProblemsPaths.problem_1_dir, 7),
            (ProblemsPaths.problem_2_dir, 6),
            (ProblemsPaths.problem_3_dir, 8),
            (ProblemsPaths.problem_4_dir, 6))
    def test_to_json(self, problem_dir: str, r_max: int):
        """Tests saving an activity schedule produced by ParallelMethod to a JSON file."""

        problem_file = f"{problem_dir}/input.csv"
        cpm_acts_file = f"{problem_dir}/cpm_solution.csv"
        parallel_method_acts_file = f"{problem_dir}/parallel_method_solution.csv"

        activities = self.get_correct_activities(cpm_acts_file,
                                                 parallel_method_acts_file)

        parallel_method = ParallelMethod(problem_file, r_max)
        parallel_method.cpm.project.activities = activities

        cpm_json_file = parallel_method.activities_schedule_to_json_file(
            "CPM", "cpm", "cpm_activities_schedule.json")
        parallel_json_file = parallel_method.activities_schedule_to_json_file(
            json_file_path = "parallel_method_output.json")

        correct_cpm_acts_schedule_file = f"{problem_dir}/cpm_activities_schedule_correct.json"
        correct_serial_acts_schedule_file = f"{problem_dir}/"+ \
                                            "parallel_method_activities_schedule_correct.json"

        cpm_acts_schedule = SerialMethodTestSuite.get_json_from_file(cpm_json_file)
        parallel_method_acts_schedule = SerialMethodTestSuite.get_json_from_file(parallel_json_file)

        correct_cpm_acts_schedule = SerialMethodTestSuite.get_json_from_file(
            correct_cpm_acts_schedule_file)
        correct_parallel_method_acts_schedule = SerialMethodTestSuite.get_json_from_file(
            correct_serial_acts_schedule_file)

        self.assertDictEqual(cpm_acts_schedule, correct_cpm_acts_schedule)
        self.assertDictEqual(parallel_method_acts_schedule, correct_parallel_method_acts_schedule)

        # Clean up generated files
        remove(cpm_json_file)
        remove(parallel_json_file)

    ## Helpful functions
    @staticmethod
    def get_correct_activities(cpm_correct_acts_file: str,
                               parallel_method_correct_acts_file: str) -> List[Activity]:
        """Returns the activities with correct values of a particular problem from a given file."""
        activities = CPMTestSuite.get_correct_activities(cpm_correct_acts_file).activities

        with open(parallel_method_correct_acts_file, encoding='utf-8') as sol:
            lines = csv_reader(sol, delimiter=' ')
            next(lines) # Skip CSV headers
            for line in lines:
                id = ID.from_str(str(line[0]))
                act = SerialMethodTestSuite.get_act_by_id(id, activities)
                act.actual_start = int(line[1])
                act.actual_end = int(line[2])
                act.priority = int(line[3])

        return activities
