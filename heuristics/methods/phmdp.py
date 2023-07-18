from heuristics.methods.parallel_method import ParallelMethod

class ParallelMethodDynamicPriorities(ParallelMethod):
    """
    Parallel Heuristic Method with Dynamic Priorities (PHMDP) for activity-based
    project planning.
    """

    _method_name: str = "Parallel Heuristic Method with Dynamic Priorities (PHMDP)"

    ## Public methods
    def activities_schedule_to_json_file(self,
                                         method_name: str = _method_name,
                                         act_timeframe_type: str = "phmdp",
                                         json_file_path: str = \
                                            "pmdp_activities_schedule.json") -> str:
        """Save the activities schedule produced by PHMDP to a JSON file."""

        return super()._activities_schedule_to_json_file(method_name,
                                                         act_timeframe_type,
                                                         json_file_path=json_file_path)

    ## Private methods
    def _init_activity_priorities(self):
        """Override the method in ParallelMethod to avoid initializing activities without time."""

    def _update_priorities(self, time: int):
        """Override the method in ParallelMethod to update the priorities dynamically."""
        for act in self.cpm.project.activities:
            act.priority = act.latest_start - time
