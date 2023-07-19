from typing import List
from heuristics.core.activities.activity import Activity
from heuristics.methods.method import HeuristicMethod

class ParallelHeuristicMethod(HeuristicMethod):
    """
    Parallel Heuristic Method (PHM) for activity-based project planning.

    In every time unit, the method generates a list of activities whose predecessors have
    been completed.
    Then, it arranges the activities according to their Time Reserves (TR) determined
    by CPM.
    Note that the TR of an activity is used as its priority value.
    Therefore, the lower the priority value, the higher the priority of the activity.
    If two activities have the same TR value (priority), then they are sorted in ascending order
    according to their IDs
    Starting with the lowest TR value, the method schedules as many activities in the time
    unit as possible before moving to the next time unit.
    """

    __method_name: str = "Parallel Heuristic Method (PHM)"

    ## Public methods
    def solve(self):
        """
        Solves the activity dependency problem with resources and time reserves as priorities.
        """

        self.cpm.solve()

        self._init_activity_priorities()

        time = 0
        while self._unfinished_activities_exist(time):
            self._update_priorities(time)

            viable_activities = self._get_viable_activities(time)

            if len(viable_activities) > 0:
                self._sort_by_priority_and_id(viable_activities)

                for act in viable_activities:
                    if not self._resources_exceeded(act, time, time + act.duration):
                        self._schedule_activity_from(act, time)

            time = self._get_time_next_act_finish(time)

        self.cpm.project.actual_end = self._get_project_actual_end()

    def activities_schedule_to_json_file(self,
                                         method_name: str = __method_name,
                                         act_timeframe_type: str = "phm",
                                         json_file_path: str = \
                                            "phm_activities_schedule.json") -> str:
        """Save the activities schedule produced by PHM to a JSON file."""

        return super()._activities_schedule_to_json_file(method_name,
                                                         act_timeframe_type,
                                                         json_file_path=json_file_path)

    ## Private methods
    def _init_activity_priorities(self):
        """
        Initializes the priority of each activity.

        In the context of the PHM, the priority of an activity is equal to its time reserve.
        """

        for act in self.cpm.project.activities:
            act.priority = act.time_reserve

    def _update_priorities(self, time: int):
        """
        Does nothing for PHM as it doesn't support dynamic priorities.

        It servers as a placeholder for the implementation of PHMDP, which overrides
        this method with its dynamic updating of priorities.
        """

    def _unfinished_activities_exist(self, time: int) -> bool:
        """Returns True if there are unfinished activities at a given time."""

        return any(not act.is_finished(time) for act in self.cpm.project.activities)

    def _get_viable_activities(self, start_time: int) -> List[Activity]:
        """
        Returns activities that can be scheduled from a given `start_time` while adhering
        to dependencies and resources available.
        """

        unscheduled_activities = [act for act in self.cpm.project.activities \
                                  if not act.is_scheduled()]
        viable_activities = []
        for act in unscheduled_activities:
            if self._activity_is_viable(act, start_time):
                viable_activities.append(act)

        return viable_activities

    def _activity_is_viable(self, act: Activity, start_time: int) -> bool:
        """
        Returns True if the given activity is viable for scheduling.

        An activity is considered viable for scheduling if all its predecessors have
        completed, and scheduling it from the specified `start_time` would not exceed
        the available resources during its executing time.
        """

        if not self._predecessors_finished(act, start_time):
            return False

        tentative_act_end = start_time + act.duration
        self._init_missing_available_resources_until(tentative_act_end)

        if self._resources_exceeded(act, start_time, tentative_act_end):
            return False

        return True

    def _predecessors_finished(self, act:Activity, time: int):
        """Returns True if all predecessors of the given activity have finished."""

        return all(pred.is_finished(time) for pred in act.predecessors)

    @staticmethod
    def _sort_by_priority_and_id(activities: List[Activity]):
        """
        Sorts the given list of activities in ascending order by their priority and id.

        Lower priority is better.

        Specifically, if two activities have the same priority, then they are sorted
        according to their ids.
        """

        activities.sort(key=lambda act: (act.priority, act.id))

    def _resources_exceeded(self, act: Activity, start_time: int, end_time: int) -> bool:
        """
        Returns True if the available resources would be exceeded between `start_time`
        and `end_time` (excluding the `end_time`).
        """

        return any(act.resources > self.available_resources[time] \
                   for time in range(start_time, end_time))

    def _get_time_next_act_finish(self, time: int) -> int:
        """Returns the time when the next activity finishes."""

        return min((act.actual_end for act in self.cpm.project.activities \
                   if act.is_scheduled() and not act.is_finished(time)),
                   default=self.cpm.project.start)
