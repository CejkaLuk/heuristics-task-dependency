import json
from typing import  List
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
    def _activities_schedule_to_json_file(self, method_name: str,
                                          act_timeframe_type: str = "cpm",
                                          json_file_path: str = \
                                            "cpm_activities_schedule.json") -> str:
        """Save the activities schedule produced by the method to a JSON file."""

        data = {'packages': [], "title" : f"{method_name} - Gantt diagram", "xlabel" : "Time",
                "ylabel" : "Activity"}
        for activity in self.cpm.project.activities:
            data['packages'].append(activity.get_timeframe(act_timeframe_type))

        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

        return json_file_path
