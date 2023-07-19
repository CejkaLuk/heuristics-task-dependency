from heuristics.methods.phm import ParallelHeuristicMethod as PHM

class ParallelHeuristicMethodDynamicPriorities(PHM):
    """
    Parallel Heuristic Method with Dynamic Priorities (PHMDP) for activity-based
    project planning.

    In every time unit, the method generates a list of activities whose predecessors have
    been completed.
    Then, it updates their priority values as: Latest Start (LS) - time
    Next, it arranges the activities according to their priority values.
    Note that the lower the priority value, the higher the priority of the activity.
    If two activities have the same priority value, then they are sorted in ascending order
    according to their IDs.
    Starting with the lowest priority value, the method schedules as many activities in the time
    unit as possible before moving to the next time unit.
    """

    _method_name: str = "Parallel Heuristic Method with Dynamic Priorities (PHMDP)"

    ## Public methods
    def activities_schedule_to_json_file(self,
                                         method_name: str = _method_name,
                                         act_timeframe_type: str = "phmdp",
                                         json_file_path: str = \
                                            "phmdp_activities_schedule.json") -> str:
        """Save the activities schedule produced by PHMDP to a JSON file."""

        return super()._activities_schedule_to_json_file(method_name,
                                                         act_timeframe_type,
                                                         json_file_path=json_file_path)

    ## Private methods
    def _init_activity_priorities(self):
        """
        Override the method in PHM to avoid initializing activities without
        time.
        """

    def _update_priorities(self, time: int):
        """Override the method in PHM to update the priorities dynamically."""
        for act in self.cpm.project.activities:
            act.priority = act.latest_start - time
