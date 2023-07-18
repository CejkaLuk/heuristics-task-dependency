from typing import List, Dict
from heuristics.core.activities.activity_id import ActivityID as ID


class Activity:
    """Activity of the Critical Path Method (CPM)."""

    id: ID
    """ID of the activity."""

    duration: int
    """Duration of the activity."""
    resources: int
    """Resources required for the activity in a single time unit."""
    total_resources: int
    """Total resources required by this activity."""

    predecessors: List['Activity']
    """Activities that must be completed before this activity can begin."""
    successors: List['Activity']
    """Activities waiting for this activity for be completed."""

    earliest_start: int
    """Earliest possible time the activity can start."""
    earliest_end: int
    """Earliest possible time the activity can end."""
    latest_start: int
    """Latest permissible time the activity can start."""
    latest_end: int
    """Latest permissible time the activity can end."""

    time_reserve: int
    """
    How much the activity can be delayed before the end of the project
    it is a part of must be delayed.

    The value is in time units.
    """

    # Properties related to heuristic methods
    actual_start: int
    """The time that the activity is actually scheduled to begin by a heuristic method."""

    actual_end: int
    """The time that the activity is actually scheduled to end by a heuristic method."""

    ## Public methods
    def __init__(self, id, duration: int, resources: int,
                 predecessors: List['Activity'] = None, successors: List['Activity'] = None,
                 earliest_start: int = None, earliest_end: int = None, latest_start: int = None,
                 latest_end: int = None, time_reserve: int = None):
        self.id = id if isinstance(id, ID) else ID.from_str(id)

        self._validate_duration_resources(duration, resources)

        self.duration = duration
        self.resources = resources
        self.total_resources = resources * duration

        self.predecessors = predecessors
        self.successors = successors

        self.earliest_start = earliest_start
        self.earliest_end = earliest_end
        self.latest_start = latest_start
        self.latest_end = latest_end

        self.time_reserve = time_reserve

        self.actual_start = None
        self.actual_end = None

    def as_dict(self) -> Dict:
        """
        Returns a selection of properties of an Activity instance as a dict.

        The predecessors and successors are not returned as they contain other Activity
        instances, which would create a dict with a lot recursion.
        """

        props = vars(self).copy()
        del props['predecessors']
        del props['successors']

        return props

    def determine_predecessors(self, activities: List['Activity']):
        """
        Sets this activity's list of predecessors to the activities that are its predecessors
        within the given list.
        """

        predecessors = []

        predecessors.extend(filter(lambda act: act.id.end_node == self.id.start_node,
                                   activities))

        self.predecessors = predecessors

    def determine_successors(self, activities: List['Activity']):
        """
        Sets this activity's list of successors to the activities that are its successors
        within the given list.
        """

        successors = []

        successors.extend(filter(lambda act: self.id.end_node == act.id.start_node,
                                 activities))

        self.successors = successors

    def get_timeframe(self, type: str) -> Dict:
        """
        Returns the timeframe of the activity, along with its id (label) and resources
        depending on the type.
        """

        if type == "cpm":
            return {'label': str(self.id),
                    'start': self.earliest_start,
                    'end': self.earliest_end,
                    'resource': self.resources}

        if type == "serial_method":
            return {'label': str(self.id),
                    'start': self.actual_start,
                    'end': self.actual_end,
                    'resource': self.resources}

        raise ValueError(f"Cannot get timeframe of type '{type}!'" +
                         "\n Currently, only 'cpm, serial_method' are supported.")

    def is_scheduled(self) -> bool:
        """Returns True if the activity is scheduled."""
        return self.actual_start is not None

    def is_finished(self, time: int):
        """Returns True if the activity is finished."""
        return self.actual_end <= time

    ## Private methods
    @staticmethod
    def _validate_duration_resources(duration: int, resources: int):
        """Validates that the duration and resources values are correct."""

        main_failure_msg = "Creating Activity failed!"
        if duration is None or resources is None:
            raise TypeError(main_failure_msg +
                            "\n Parameters must not be NoneType!")

        if duration < 0 or resources < 0:
            raise ValueError(main_failure_msg + "\n Parameters 'duration' and " +
                             "'resources' must be nonnegative!")

    ## Magic methods
    def __repr__(self) -> str:
        return f"Activity({self.as_dict()})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Activity):
            raise NotImplementedError("Determining equality of Activity instances failed!" +
                                      f"\n Cannot compare instances of '{type(self)}' and" +
                                      f" '{type(other)}'")

        return self.as_dict() == other.as_dict()
