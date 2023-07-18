from typing import Tuple


class ActivityID:
    """
    ActivityID of an activity in the Critical Path Method (CPM).

    The ActivityID is made up of the node the activity starts from and the node the
    activity ends in.
    """

    start_node: int
    """The node that the activity starts from."""
    end_node: int
    """The node that the activity ends in."""

    ## Public methods
    def __init__(self, start_node: int, end_node: int):
        self._validate_id(start_node, end_node)

        self.start_node = start_node
        self.end_node = end_node

    @classmethod
    def from_str(cls, id: str):
        """Overloaded constructor for initializing ActivityID from a string."""
        start_node, end_node = cls._parse_id(id)

        return cls(start_node, end_node)

    def as_dict(self) -> dict:
        """Returns the ActivityID as a tuple comprising: start node, end node."""

        return vars(self)

    ## Private methods
    @staticmethod
    def _parse_id( id: str) -> Tuple[int, int]:
        """Parses the start and end node from the id in string form '<start_node>-<end_node>'."""

        return [int(num) for num in id.split('-')]

    @staticmethod
    def _validate_id(start_node: int, end_node: int):
        """Validates that the nodes of the id are correct."""

        main_failure_msg = f"Creating ActivityID of activity ({start_node}, {end_node}) failed!"
        if start_node is None or end_node is None:
            raise TypeError(main_failure_msg + "\n Both nodes must exist!")

        # Only nodes with ID >= 1 are supported.
        if start_node < 1 or end_node < 1:
            raise ValueError(main_failure_msg +
                             "\n Both nodes must have an ActivityID greater than zero!")

        # Only activities going from left to right are supported.
        if start_node > end_node:
            raise ValueError(main_failure_msg + "\n The ActivityID of the start node must be" +
                             "smaller than the ActivityID of the end node!")

    ## Magic methods
    def __repr__(self) -> str:
        return f"ActivityID({self.as_dict()})"

    def __str__(self) -> str:
        return f"{self.start_node}-{self.end_node}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ActivityID):
            raise NotImplementedError("Determining equality of ActivityID instances failed!" +
                                      f"\n Cannot compare instances of '{type(self)}' and" +
                                      f" '{type(other)}'")

        return self.as_dict() == other.as_dict()

    def __lt__(self, other):
        return (self.start_node, self.end_node) < (other.start_node, other.end_node)

    def __hash__(self):
        return hash(frozenset(self.as_dict()))
