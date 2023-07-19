import json
from typing import  List
from heuristics.core.activities.activity import Activity
from heuristics.core.cpm import CriticalPathMethod as CPM


class HeuristicMethod():
    """
    Base class for heuristic methods that provides common functionalities.
    """

    cpm: CPM
    """
    CriticalPathMethod instance used in the initialization of the method.
    """

    available_resources: List[int]
    """
    Resources available in each point in time.

    The resources are dynamically added during computation as the final
    end time of the project is not known until the heuristic method has
    completed.
    """

    ## Public methods
    def __init__(self, acts_file_path, r_max: int):
        self.cpm = CPM(acts_file_path, r_max)

        self.available_resources = []

    ## Private methods
    def _init_missing_available_resources_until(self, time_end: int):
        """Initialize missing available resources until a given time point."""

        desired_num_time_points = time_end + 1
        actual_num_time_points = len(self.available_resources)
        missing_time_points = desired_num_time_points - actual_num_time_points
        if missing_time_points > 0:
            self.available_resources.extend([self.cpm.project.r_max] * missing_time_points)

    def _schedule_activity_from(self, act: Activity, start_time: int):
        """
        Schedules an activity from a given time point.

        If an activity is scheduled from 0 to 4, then it is finished at 4.
        """

        act.actual_start = start_time
        act.actual_end = act.actual_start + act.duration

        for time in range(act.actual_start, act.actual_end):
            self.available_resources[time] -= act.resources

    def _get_project_actual_end(self) -> int:
        """Returns the actual project end according to the heuristic method."""

        return max(act.actual_end for act in self.cpm.project.activities)

    def _activities_schedule_to_json_file(self, method_name: str,
                                          act_timeframe_type: str = "cpm",
                                          json_file_path: str = \
                                            "cpm_activities_schedule.json") -> str:
        """Save the activities schedule produced by the heuristic method to a JSON file."""

        data = {'packages': [], "title" : f"{method_name} - Gantt chart", "xlabel" : "Time",
                "ylabel" : "Activity"}
        for activity in self.cpm.project.activities:
            data['packages'].append(activity.get_time_frame(act_timeframe_type))

        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

        return json_file_path
