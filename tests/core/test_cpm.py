import unittest
from io import StringIO
from contextlib import redirect_stdout
from csv import reader as csv_reader
from nose2.tools import params
from heuristics.core.activities.activity import Activity
from heuristics.core.cpm import CriticalPathMethod as CPM
from heuristics.core.project import Project
from tests.resources.problems.problems import ProblemsPaths


class CPMTestSuite(unittest.TestCase):
    """Tests for CriticalPathMethod (CPM)."""

    ## Test correct behavior
    @params(# Problem 1
            (ProblemsPaths.problem_1_dir, "cpm_solution.csv", 7, 0, 13, None, 112),
            # Problem 2
            (ProblemsPaths.problem_2_dir, "cpm_solution.csv", 6, 0, 10, None, 71),
            # Problem 2 - with project start set to time unit 5
            (ProblemsPaths.problem_2_dir,
             "cpm_solution_delayed_proj_start.csv", 6, 5, 20, 20, 71),
            # Problem 3
            (ProblemsPaths.problem_3_dir, "cpm_solution.csv", 8, 0, 39, None, 255),
            # Problem 4
            (ProblemsPaths.problem_4_dir, "cpm_solution.csv", 6, 0, 11, None, 83))
    def test_cpm(self, problem_dir: str, solution_file: str, r_max: int, proj_start: int,
                 proj_end: int, proj_planned_end: int, proj_resources: int):
        """Tests CPM on a set of problems."""
        problem_file = f"{problem_dir}/input.csv"
        correct_acts_file = f"{problem_dir}/{solution_file}"

        cpm = CPM(problem_file, r_max, proj_start, proj_planned_end)

        # Assert that the method has no output
        self.assertEqual(self._get_method_output(cpm.solve), '')

        # Verify that activities have correct values
        cpm_proj_correct = self.get_correct_activities(correct_acts_file)
        self.assertListEqual(cpm.project.activities, cpm_proj_correct.activities)

        # Verify that the project has correct values
        self.assertEqual(cpm.project.start, proj_start)
        self.assertEqual(cpm.project.earliest_end, proj_end)
        self.assertEqual(cpm.project.total_resources_required, proj_resources)

    @params(# Problem 1 - with unrealistic project end
            (f"{ProblemsPaths.problem_1_dir}/input.csv",
             f"{ProblemsPaths.problem_1_dir}/cpm_solution.csv", 7, 0, 13, 10, 112))
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
        cpm_proj_correct = self.get_correct_activities(correct_acts_file)
        self.assertListEqual(cpm.project.activities, cpm_proj_correct.activities)

        # Verify that the project has correct values
        self.assertEqual(cpm.project.start, proj_start)
        self.assertEqual(cpm.project.earliest_end, proj_end)
        self.assertEqual(cpm.project.total_resources_required, proj_resources)

    @staticmethod
    def get_correct_activities(correct_acts_file: str) -> Project:
        """Returns the activities with correct values of a particular problem from a given file."""
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

        return Project(correct_acts, None)

    @staticmethod
    def _get_method_output(method) -> str:
        """Returns the stdout of a method."""
        str_io = StringIO()
        with redirect_stdout(str_io):
            method()
        return str_io.getvalue()
