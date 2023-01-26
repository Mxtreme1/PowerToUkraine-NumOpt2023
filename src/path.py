import pandas as pd

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
        last_buses = [value[0].bus0, value[0].bus1]
        for item in value[1:]:
            assert item.bus0 in last_buses or item.bus1 in last_buses
            last_buses = [item.bus0, item.bus1]

        # List all buses on the path including duplicates
        buses_on_lines = []
        for item in value:
            buses_on_lines.append(item.bus0)
            buses_on_lines.append(item.bus1)

        if len(buses_on_lines) > 2:
            buses_on_lines = Path._check_for_circles(buses_on_lines)

        self.buses = buses_on_lines

        self._bus_amount = len(buses_on_lines)
        self._lines = value
        self._line_amount = len(value)

    @staticmethod
    def _check_for_circles(buses_on_lines):
        """
        Tests if the buses that are on the lines of a path contain one or multiple circles.
        Raises error if not the case, otherwise returns the unique buses on the path.
        
        Args:
            buses_on_lines (list of Bus instances)
            
        Returns:
            list of Bus instances:
                Unique buses on the path.
        """
        assert isinstance(buses_on_lines, list)
        for item in buses_on_lines:
            assert isinstance(item, src.bus.Bus)

        # Keep removing a bus and then its duplicate from the other line, if there are no loops
        # we will only remove each bus pair once and end up with two different buses, start and end of path.
        buses_set = set()
        non_duplicate_counter = 0
        while len(buses_on_lines) > 2 >= non_duplicate_counter:
            bus = buses_on_lines.pop()
            if bus in buses_set:
                raise ValueError("Circle detected in lines setter of Path class.")

            # If we found the start/end bus just add them to the front of the list again
            if bus not in buses_on_lines:
                buses_on_lines = [bus] + buses_on_lines
                non_duplicate_counter += 1
            else:
                buses_on_lines.remove(bus)  # Removes duplicate of bus (only one if multiple in list)
                buses_set.update([bus])

        if len(buses_on_lines) != 2 or buses_on_lines[0] == buses_on_lines[1]:
            raise ValueError("Something is wrong with the buses on your path. Check by hand.")

        return buses_on_lines + list(buses_set)

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
