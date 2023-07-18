from heuristics.core.activities.activity import Activity
from heuristics.methods.method import HeuristicMethod


class SerialMethod(HeuristicMethod):
    """Serial heuristic method for activity-based project planning."""

    ## Public methods
    def solve(self):
        """Solves the activity dependency problem with resources."""

        self.cpm.solve()

        # Schedule activities
        for act in self.cpm.project.activities:
            self._schedule_activity(act)

        self.cpm.project.actual_end = self._get_project_actual_end()

    def activities_schedule_to_json_file(self,
                                         method_name: str = "Serial heuristic method",
                                         act_timeframe_type: str = "serial_method",
                                         json_file_path: str = \
                                            "serial_method_activities_schedule.json") -> str:
        """Save the activities schedule produced by the serial heuristic method to a JSON file."""

        return super()._activities_schedule_to_json_file(method_name,
                                                         act_timeframe_type,
                                                         json_file_path=json_file_path)

    ## Private methods
    def _schedule_activity(self, act: Activity):
        """
        Schedules an activity as soon as possible considering dependencies and available resources.
        """
        time = self._get_predecessors_finished_time(act)

        while not act.is_scheduled():
            tentative_act_end = time + act.duration
            self._init_missing_available_resources_until(tentative_act_end)

            time_resources_exceed = self._get_time_available_resources_exceeded(
                act, time, tentative_act_end)

            if time_resources_exceed is None:
                self._schedule_activity_from(act, time)
            else:
                time = time_resources_exceed + 1

    def _get_predecessors_finished_time(self, act: Activity) -> int:
        """
        Returns the time when all predecessors of an activity are finished.

        If the activity has no predecessors, then the project start time is returned.
        """

        return max((pred.actual_end for pred in act.predecessors),
                   default=self.cpm.project.start)

    def _get_time_available_resources_exceeded(self, act: Activity, start_time: int,
                                               end_time: int) -> int:
        """
        Returns the latest time point in which the activity would exceed available resources had
        it been scheduled in a given time frame.

        The time frame does not include the `end_time`.
        None is returned if the activity does not exceed the resources available in the time frame.
        """

        return max((time for time in range(start_time, end_time) if \
                    act.resources > self.available_resources[time]),
                    default = None)
