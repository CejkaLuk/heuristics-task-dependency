from csv import reader as csv_reader
from re import fullmatch
from pathlib import Path
from typing import List
from heuristics.core.activities.activity import Activity
from heuristics.exceptions.data_not_found import DataNotFoundError


class ActivitiesLoader():
    """Loader of activities from a file."""

    ## Public methods
    @staticmethod
    def get_activities(acts_file_path: str) -> List[Activity]:
        """Returns the activities parsed from the file."""

        acts_file_path = acts_file_path if isinstance(acts_file_path, Path) else \
                                           Path(acts_file_path)
        activities = []
        with open(acts_file_path, encoding="utf-8") as file:
            lines = csv_reader(file, delimiter=' ')
            next(lines) # Skip CSV headers
            for line in lines:
                act = ActivitiesLoader._get_activity_from_line(line)
                ActivitiesLoader._check_if_duplicate_activity(act, activities)
                activities.append(act)

        return activities

    ## Private methods
    @staticmethod
    def _get_activity_from_line(line: List[str]) -> Activity:
        """Formats an activity line into a dict."""

        ActivitiesLoader._validate_activity_line(line)

        activity_id = str(line[0])
        duration = int(line[1])
        resources = int(line[2])

        return Activity(activity_id, duration, resources)

    @staticmethod
    def _check_if_duplicate_activity(act: Activity, activities: List[Activity]):
        """Checks if the activity is already present in activities."""
        if act.id in [a.id for a in activities]:
            raise ValueError("Failed loading data from file!" +
                             f"\n Activity with ID '{act.id}' was already loaded.")

    @staticmethod
    def _validate_activity_line(line: List[str]) -> None:
        """Verifies that the activity line contains the required data."""

        if line.count(None) > 0 or line.count("") > 0 or len(line) != 3:
            raise DataNotFoundError(f"Error parsing data line '{' '.join(line)}'!" +
                                    "\n The line must contain 3 values that are not NoneType.")

        # Check activity ID
        activity_pattern = "[1-9][0-9]*-[1-9][0-9]*"
        if not fullmatch(activity_pattern, line[0]):
            raise ValueError(f"Error parsing data Activity ID '{line[0]}' from" +
                             f"line '{' '.join(line)}'" +
                             f"\n Activity ID should match the pattern '{activity_pattern}'")

        # Check duration/resources
        integer_pattern = "[0-9]+"
        if not fullmatch(integer_pattern, line[1]) or \
           not fullmatch(integer_pattern, line[2]):
            raise ValueError(f"Error parsing data line '{' '.join(line)}'" +
                             "\n Activity duration/resources should match" +
                             f" the pattern '{integer_pattern}'")
