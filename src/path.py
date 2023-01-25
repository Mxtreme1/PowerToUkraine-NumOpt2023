import src.bus
import src.line

import itertools


class Path:
    """
    A collection of lines connecting two DIFFERENT buses. There may be multiple paths connecting two buses.

    Args:

        lines (list if Lines):
            All lines the path comprises of.

    """

    id_counter = itertools.count()

    def __init__(self, lines):

        self._id = next(Path.id_counter)

        self._lines = None
        self._line_amount = None
        self._buses = None      # Will be a list of buses later.
        self._bus_amount = None

        self.lines = lines

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        raise PermissionError("No change of unique identifier id allowed for paths.")

    @property
    def lines(self):
        return self._lines
    
    @lines.setter
    def lines(self, value):
        if self._lines is not None:
            raise PermissionError("A path is a fixed entity, it can not be changed. That means no changing of lines.")

        assert isinstance(value, list)
        for item in value:
            assert isinstance(item, src.line.Line)

        # The next two code blocks (checking connection and the buses on a path) are separated for readability.
        # Checks that the lines are actually connected via a bus.
        last_bus = value[0].bus1
        for item in value[1:]:
            assert item.bus0 == last_bus
            last_bus = item.bus1

        # List all buses on the path
        buses_on_lines = []

        for item in value:
            buses_on_lines.append(item.bus0)
        buses_on_lines.append(value[-1].bus1)

        self.buses = buses_on_lines
        self._bus_amount = len(buses_on_lines)
        self._lines = value
        self._line_amount = len(value)

    @property
    def line_amount(self):
        return self._line_amount

    @property
    def buses(self):
        return self._buses

    @buses.setter
    def buses(self, value):
        if self._buses is not None:
            raise PermissionError("Paths are fixed, a change of its buses is a change of the path. It shall not pass!")

        assert isinstance(value, list)
        
        for item in value:
            assert isinstance(item, src.bus.Bus)

        # Check for uniqueness of buses aka no circles.
        unique_buses = []
        for item in value:
            assert item not in unique_buses
            unique_buses.append(item)

        self._buses = value

    @property
    def bus_amount(self):
        return self._bus_amount

    @property
    def length(self):
        """
        Calculates the cumulated length of all lines on the path.

        Returns:
            float:
                Total length of the lines.

        """

        length = 0
        for line in self.lines:
            length += line.length

        return length
