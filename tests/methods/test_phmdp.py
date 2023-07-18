import unittest
from os import remove
from nose2.tools import params
from heuristics.methods.phmdp import ParallelMethodDynamicPriorities as PHMDP
from tests.methods.test_serial_method import SerialMethodTestSuite
from tests.methods.test_parallel_method import ParallelMethodTestSuite
from tests.resources.problems.problems import ProblemsPaths


class ParallelMethodDynamicPrioritiesTestSuite(unittest.TestCase):
    """Tests that assure ParallelMethodDynamicPriorities works correctly."""

    ## Test correct behavior
    @params((ProblemsPaths.problem_1_dir, 7, 21),
            (ProblemsPaths.problem_2_dir, 6, 13),
            (ProblemsPaths.problem_3_dir, 8, 41),
            (ProblemsPaths.problem_4_dir, 6, 17))
    def test_solve(self, problem_dir: str, r_max: int, pmdp_project_end: int):
        """Tests solving a set of problems using PHMDP."""

        self.maxDiff = None
        problem_file = f"{problem_dir}/input.csv"
        cpm_correct_acts_file = f"{problem_dir}/cpm_solution.csv"
        pmdp_correct_acts_file = f"{problem_dir}/phmdp_solution.csv"

        phmdp = PHMDP(problem_file, r_max)
        phmdp.solve()

        # Verify that activities have correct values
        correct_activities = ParallelMethodTestSuite.get_correct_activities(
            cpm_correct_acts_file, pmdp_correct_acts_file)
        self.assertListEqual(phmdp.cpm.project.activities, correct_activities)

        # Verify that the project end is correct
        self.assertEqual(phmdp.cpm.project.actual_end, pmdp_project_end)

        # Verify that the resources available in each time point were not overstepped
        num_time_points = pmdp_project_end + 1
        self.assertEqual(len(phmdp.available_resources), num_time_points)
        self.assertListEqual([a_res <= r_max for a_res in phmdp.available_resources],
                             [True] * len(phmdp.available_resources))

    @params((ProblemsPaths.problem_1_dir, 7),
            (ProblemsPaths.problem_2_dir, 6),
            (ProblemsPaths.problem_3_dir, 8),
            (ProblemsPaths.problem_4_dir, 6))
    def test_to_json(self, problem_dir: str, r_max: int):
        """Tests saving an activity schedule produced by PHMDP to a JSON file."""

        problem_file = f"{problem_dir}/input.csv"
        cpm_acts_file = f"{problem_dir}/cpm_solution.csv"
        pmdp_acts_file = f"{problem_dir}/phmdp_solution.csv"

        activities = ParallelMethodTestSuite.get_correct_activities(
            cpm_acts_file, pmdp_acts_file)

        phmdp = PHMDP(problem_file, r_max)
        phmdp.cpm.project.activities = activities

        cpm_json_file = phmdp.activities_schedule_to_json_file(
            "CPM", "cpm", "cpm_activities_schedule.json")
        pmdp_json_file = phmdp.activities_schedule_to_json_file(
            json_file_path = "pmdp_activities_schedule.json")

        correct_cpm_acts_schedule_file = f"{problem_dir}/cpm_activities_schedule_correct.json"
        correct_serial_acts_schedule_file = f"{problem_dir}/"+ \
                                            "phmdp_activities_schedule_correct.json"

        cpm_acts_schedule = SerialMethodTestSuite.get_json_from_file(cpm_json_file)
        pmdp_acts_schedule = SerialMethodTestSuite.get_json_from_file(pmdp_json_file)

        correct_cpm_acts_schedule = SerialMethodTestSuite.get_json_from_file(
            correct_cpm_acts_schedule_file)
        correct_pmdp_acts_schedule = SerialMethodTestSuite.get_json_from_file(
            correct_serial_acts_schedule_file)

        self.assertDictEqual(cpm_acts_schedule, correct_cpm_acts_schedule)
        self.assertDictEqual(pmdp_acts_schedule, correct_pmdp_acts_schedule)

        # Clean up generated files
        remove(cpm_json_file)
        remove(pmdp_json_file)
