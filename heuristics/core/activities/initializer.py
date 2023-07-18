from typing import List
from heuristics.core.activities.activity import Activity


class ActivitiesInitializer():
    """Initializer for the activities."""

    ## Public methods
    @staticmethod
    def init_activities(activities: List[Activity]):
        """Initializes the predecessors and successors of provided activities."""

        if (not isinstance(activities, List) or
            (len(activities) > 0 and
             not all(isinstance(act, Activity) for act in activities))):
            raise TypeError("Initializing Activities from 'activities' failed!" +
                            "\n Input variable must a 'List' with 'Activity' instances.")

        for act in activities:
            act.determine_predecessors(activities)
            act.determine_successors(activities)
