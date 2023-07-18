from typing import List
from heuristics.core.activities.activity import Activity
from heuristics.core.project import Project


class CriticalPathMethod():
    """
    Solver for a project timing problem using the Critical Path Method (CPM).

    To solve a problem a new instance of CriticalPathMethod must be created.
    This is because the project is initialized in the constructor.
    """

    ## Public properties
    project: Project
    """The project whose timeline CPM solves."""

    ## Private properties
    _final_activities: List[Activity]
    """
    List of activities whose completion marks the end of the project.
    These activities have no successors.

    This variable is used to avoid recomputing the list of final activities during the run
    of the algorithm.
    """

    ## Public methods
    def __init__(self, acts_file_path, r_max: int,
                 proj_start: int = 0, planned_proj_end: int = None):

        self.project = Project.from_file_and_args(acts_file_path, r_max,
                                                  proj_start, None, planned_proj_end)

        self._final_activities = self._get_final_activities()

    def solve(self):
        """Solves the timing problem using the CPM algorithm."""

        # Determine the earliest starts and ends of activities
        self._forward_walk()
        # Determine the latest starts and ends of activities
        self._backward_walk()

        # Determine how many time units each activity can be delayed before
        # the end of the project must be postponed
        self._calculate_time_reserves()
        # Determine when the project starts and ends
        self._calculate_project_start_end()

    ## Private methods
    def _forward_walk(self):
        """
        Performs the forward walk of the CPM algorithm.

        This involves computing the earliest starts and ends of activities.
        """

        for act in self.project.activities:
            act.earliest_start = self._get_earliest_start(act)
            act.earliest_end = act.earliest_start + act.duration

    def _backward_walk(self):
        """
        Performs the backward walk of the CPM algorithm.

        This involves computing the latest starts and ends of activities.
        """

        activities_rev = reversed(self.project.activities.copy())
        for act in activities_rev:
            act.latest_end = self._get_latest_end(act)
            act.latest_start = act.latest_end - act.duration

    def _calculate_time_reserves(self):
        """
        Calculates the time reserves of activities.

        In other words, determine how many time units each activity can be delayed
        before the end of the project must be postponed.
        """

        for act in self.project.activities:
            if (act.latest_start - act.earliest_start) == \
               (act.latest_end - act.earliest_end):
                act.time_reserve = act.latest_start - act.earliest_start
            else:
                raise RuntimeError("CPM failed!\n The time reserves of Activity with ID"
                                   f"'{act.id}' do not match!" +
                                   "\n The difference between earliest_start-latest_start and" +
                                   " earliest_end-latest_end should be the same"
                                   "\n The results are incorrect.")

    def _get_earliest_start(self, act: Activity) -> int:
        """
        Returns the earliest start for a given activity.

        The earliest start of an activity is equal to the latest (max) earliest end time
        of its predecessors.
        If the activity has no predecessors, then its earliest start is set to the project's
        start time (0 by default).
        """

        if self._is_first(act):
            return self.project.start

        if len(act.predecessors) == 1:
            return act.predecessors[0].earliest_end

        return max(pred.earliest_end for pred in act.predecessors)

    def _get_latest_end(self, act: Activity) -> int:
        """
        Returns the latest end for a given activity.

        The latest end of an activity is equal to the earliest (min) latest start time from
        of its successors.
        If the activity has no successors, then its latest end is set to its earliest end, or
        it is set to the the project's planned end if it is specified and valid.
        """

        if self._is_final(act):
            proj_earliest_end = max(act.earliest_end for act in self._final_activities)
            if self.project.planned_end is not None:
                if self.project.planned_end < proj_earliest_end:
                    print(f"Warning: Provided planned end of project '{self.project.planned_end}'" +
                          " not used as its value is smaller than the earliest possible end of" +
                          f" the project '{act.earliest_end}'.")
                else:
                    proj_earliest_end = self.project.planned_end
            return proj_earliest_end

        if len(act.successors) == 1:
            return act.successors[0].latest_start

        return min(succ.latest_start for succ in act.successors)

    def _calculate_project_start_end(self):
        self.project.start = min(act.earliest_start for act in self.project.activities)
        self.project.earliest_end = max(act.latest_end for act in self.project.activities)

    def _get_final_activities(self) -> List[Activity]:
        """Returns the list of final activities of the project."""
        return [act for act in self.project.activities if self._is_final(act)]

    @staticmethod
    def _is_first(act: Activity):
        """
        Determines if the activity is one of the first activities to be completed in the project.
        """

        return len(act.predecessors) == 0

    @staticmethod
    def _is_final(act: Activity):
        """
        Determines if the activity is one of the final activities to be completed in the project.
        """

        return len(act.successors) == 0
