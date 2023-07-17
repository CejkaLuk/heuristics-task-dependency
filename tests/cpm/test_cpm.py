import unittest
from io import StringIO
from contextlib import redirect_stdout
from csv import reader as csv_reader  # For CSV file operations
from nose2.tools import params
from heuristics.core.cpm.activities.activity import Activity
from heuristics.core.cpm.cpm import CriticalPathMethod as CPM
from heuristics.core.cpm.project.project import CPMProject


class CPMTestSuite(unittest.TestCase):
    """Tests for CriticalPathMethod (CPM)."""

    problems_path = 'tests/resources/problems'
    solutions_path = 'tests/resources/problems/cpm_solutions'

    ## Test correct behavior
    @params(# Problem 1
            (f"{problems_path}/problem1.csv",
             f"{solutions_path}/problem1.csv", 7, 0, 13, None, 112),
            # Problem 2
            (f"{problems_path}/problem2.csv",
             f"{solutions_path}/problem2.csv", 6, 0, 10, None, 71),
            # Problem 2 - with project start set to time unit 5
            (f"{problems_path}/problem2.csv",
             f"{solutions_path}/problem2_delayed_proj_start.csv", 6, 5, 20, 20, 71),
            # Problem 3
            (f"{problems_path}/problem3.csv",
             f"{solutions_path}/problem3.csv", 8, 0, 39, None, 252),
            # Problem 4
            (f"{problems_path}/problem4.csv",
             f"{solutions_path}/problem4.csv", 6, 0, 11, None, 83))
    def test_cpm(self, problem_file: str, correct_acts_file: str, r_max: int, proj_start: int,
                 proj_end: int, proj_planned_end: int, proj_resources: int):
        """Tests CPM on a set of problems."""

        cpm = CPM(problem_file, r_max, proj_start, proj_planned_end)

        # Assert that the method has no output
        self.assertEqual(self._get_method_output(cpm.solve), '')

        # Verify that activities have correct values
        cpm_proj_correct = self._get_correct_activities(correct_acts_file)
        self.assertListEqual(cpm.project.activities, cpm_proj_correct.activities)

        # Verify that the project has correct values
        self.assertEqual(cpm.project.start, proj_start)
        self.assertEqual(cpm.project.end, proj_end)
        self.assertEqual(cpm.project.total_resources_required, proj_resources)

    @params(# Problem 1 - with unrealistic project end
            (f"{problems_path}/problem1.csv",
             f"{solutions_path}/problem1.csv", 7, 0, 13, 10, 112))
    def test_cpm_solve_warning_for_unrealistic_project_end(self, problem_file: str,
                                                           correct_acts_file: str, r_max: int,
                                                           proj_start: int, proj_end: int,
                                                           proj_planned_end : int,
                                                           proj_resources: int):
        """
        Tests CPM on a problem with an unrealistic planned project end (planned to end earlier
        than possible).
        """

        cpm = CPM(problem_file, r_max, proj_start, proj_planned_end)

        self.assertGreater(len(self._get_method_output(cpm.solve)), 0)

        # Verify that activities have correct values
        cpm_proj_correct = self._get_correct_activities(correct_acts_file)
        self.assertListEqual(cpm.project.activities, cpm_proj_correct.activities)

        # Verify that the project has correct values
        self.assertEqual(cpm.project.start, proj_start)
        self.assertEqual(cpm.project.end, proj_end)
        self.assertEqual(cpm.project.total_resources_required, proj_resources)

    @staticmethod
    def _get_correct_activities(correct_acts_file: str) -> CPMProject:
        """Returns the solution to a problem from a given file."""
        correct_acts = []

        with open(correct_acts_file, encoding='utf-8') as sol:
            lines = csv_reader(sol, delimiter=' ')
            next(lines) # Skip CSV headers
            for line in lines:
                act = Activity(id = str(line[0]), duration = int(line[1]), resources = int(line[2]),
                               earliest_start = int(line[3]), earliest_end = int(line[4]),
                               latest_start = int(line[5]), latest_end = int(line[6]),
                               time_reserve = int(line[7]))
                correct_acts.append(act)

        return CPMProject(correct_acts, None)

    @staticmethod
    def _get_method_output(method) -> str:
        """Returns the stdout of a method."""
        str_io = StringIO()
        with redirect_stdout(str_io):
            method()
        return str_io.getvalue()
