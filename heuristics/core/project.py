from typing import List
from heuristics.core.activities.activity import Activity
from heuristics.core.activities.loader import ActivitiesLoader
from heuristics.core.activities.initializer import ActivitiesInitializer

class Project():
    """
    Project that is analyzed/planned using heuristics.

    The project consists of:
    - Activities that need to be completed.

    - Limiting aspects:
      - The max. resources available in a single time unit
      - The set start of the project.
      - The desired end of the project.

    - Results:
      - The actual time when the project can be completed earliest.
      - Total resources required to complete the entire project.
    """

    activities: List[Activity]
    """List of activities."""

    r_max: int
    """Max. resources available for all activities in a single time unit."""

    start: int
    """The point in time when the project starts."""

    earliest_end: int
    """The earliest possible end of the project according to the activity dependencies."""

    planned_end: int
    """The point in time when the project is desired to end."""

    total_resources_required: int
    """
    The total number of resources used to complete the project.

    It is equal to the sum of total resources of all activities.
    """

    actual_end: int
    """
    The time that the project can actually end according to a heuristic method which takes
    into account the max. resources available at one point in time.
    """

    ## Public methods
    def __init__(self, activities: List[Activity], r_max: int,
                 start: int = 0, end: int = None, planned_end: int = None):
        ActivitiesInitializer.init_activities(activities)
        self._sort_activities_by_id(activities)

        self.activities = activities
        self.r_max = r_max

        self.start = start
        self.earliest_end = end
        self.planned_end = planned_end
        self.total_resources_required = self._get_total_resources_required(self.activities)

        self.actual_end = None

    @classmethod
    def from_file_and_args(cls, data_file_path: str, r_max: int,
                           start: int = 0, end: int = None, planned_end: int = None):
        """
        Overloaded constructor for loading the activities of a Project from a data file and
        supplying the remaining properties as arguments.
        """

        activities = ActivitiesLoader.get_activities(data_file_path)

        return cls(activities, r_max, start, end, planned_end)

    ## Private methods
    @staticmethod
    def _get_total_resources_required(activities: List[Activity]) -> int:
        """Returns the total resources required to complete the project."""

        return sum(act.total_resources for act in activities)

    @staticmethod
    def _sort_activities_by_id(activities: List[Activity]):
        """Sorts the activities in a list in ascending order according to their ID."""

        activities.sort(key=lambda act_id: act_id.id)
