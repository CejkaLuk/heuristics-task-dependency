import unittest
from pathlib import Path
from nose2.tools import params
from heuristics.core.cpm.activities.loader import CPMActivitiesLoader
from heuristics.core.cpm.activities.activity import Activity
from heuristics.exceptions.data_not_found import DataNotFoundError


class CPMActivitiesLoaderTestSuite(unittest.TestCase):
    """Tests For CPMActivitiesLoader."""

    activities_correct = [Activity("1-2", 4, 3), Activity("1-3", 6, 5), Activity("1-4", 5, 4),
                          Activity("2-5", 3, 3), Activity("3-5", 4, 3), Activity("4-6", 4, 5),
                          Activity("5-6", 3, 3)]

    activities_2_correct = [Activity("1-2", 4, 3), Activity("1-3", 3, 4), Activity("1-4", 5, 3),
                            Activity("2-5", 3, 2), Activity("3-5", 2, 3), Activity("4-6", 4, 2),
                            Activity("5-6", 3, 4)]

    problems_dir = "tests/resources/problems"
    invalid_problems_dir = problems_dir + "/invalid"

    ## Test correct behavior
    @params((f"{problems_dir}/problem1.csv", True, activities_correct),
            (f"{problems_dir}/problem2.csv", True, activities_2_correct,),
            (f"{problems_dir}/problem1.csv", False, activities_correct),
            (f"{problems_dir}/problem2.csv", False, activities_2_correct))
    def test_get_data(self, acts_file_path, provide_path_as_string, acts_correct):
        """Tests that the 'get_cpm_activities' method produces the correct output."""

        acts_file_path = acts_file_path if provide_path_as_string else Path(acts_file_path)
        acts = CPMActivitiesLoader.get_cpm_activities(acts_file_path)

        self.assertListEqual(acts, acts_correct)

    ## Test failures
    @params(f"{invalid_problems_dir}/problem_duplicate_activity_id.csv")
    def test_get_data_with_duplicate_activity_should_fail(self, acts_file_path):
        """
        Tests that the 'get_cpm_activities' method fails if the input file contains two
        activities with the same ID.
        """

        with self.assertRaises(ValueError, msg="Getting the data should have failed as" +
                               " there are two activities with the same ID in the" +
                               f"'{acts_file_path}' file!"):
            CPMActivitiesLoader.get_cpm_activities(acts_file_path)

    @params(f"{invalid_problems_dir}/problem_missing_activity_id.csv",
            f"{invalid_problems_dir}/problem_missing_duration.csv",
            f"{invalid_problems_dir}/problem_missing_resources.csv")
    def test_get_data_with_missing_values_should_fail(self, acts_file_path):
        """Tests that the 'get_cpm_activities' method fails for missing values."""

        with self.assertRaises(DataNotFoundError, msg="Getting the data should have failed as" +
                               f" a value is missing in the '{acts_file_path}' file!"):
            CPMActivitiesLoader.get_cpm_activities(acts_file_path)

    @params((f"{invalid_problems_dir}/problem_invalid_activity_id.csv", 'activity_id'),
            (f"{invalid_problems_dir}/problem_invalid_duration.csv", 'duration'),
            (f"{invalid_problems_dir}/problem_invalid_resources.csv", 'resources'))
    def test_get_data_for_invalid_values_should_fail(self, acts_file_path, value_type):
        """Tests that the 'get_cpm_activities' method fails for invalid values in the file."""

        with self.assertRaises(ValueError, msg="Getting the data should have failed as" +
                               f" the '{value_type}' value is invalid!" +
                               "\n The ID of an Activity should start with 1-9." +
                               "\n The values of duration and resources should be nonnegative."):
            CPMActivitiesLoader.get_cpm_activities(acts_file_path)
