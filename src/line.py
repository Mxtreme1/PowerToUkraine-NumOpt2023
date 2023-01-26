import src.bus

import itertools


class Line:
    """
    A power line connecting two buses.

    Args:
        bus0 (Bus):
            "Start"-point of the line.

        bus1 (Bus):
            "End"-point of the line.

        length (int, float):
            Length of the line in meters.

        line_type (Line_Type):
            Type of the line. Determines the rating of the line aka how much current can be carried.
    """

    id_counter = itertools.count()

    def __init__(self, bus0, bus1, length, line_type):

        self._id = next(Line.id_counter)

        self._bus0 = None
        self._bus1 = None
        self._length = None
        self._line_type = None

        self.bus0 = bus0
        self.bus1 = bus1
        self.length = length
        self.line_type = line_type

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        raise PermissionError("No changes in ID of Line possible.")

    @property
    def bus0(self):
        return self._bus0

    @bus0.setter
    def bus0(self, value):
        if self._bus0 is not None:
            raise PermissionError("Network topology is fixed. Change it in the network definition.")
        assert isinstance(value, src.bus.Bus)
        assert self.bus1 != value

        self._bus0 = value

    @property
    def bus1(self):
        return self._bus1

    @bus1.setter
    def bus1(self, value):
        if self._bus1 is not None:
            raise PermissionError("Network topology is fixed. Change it in the network definition.")

        assert isinstance(value, src.bus.Bus)
        assert self.bus0 != value

        # bus1 is always set second therefore we can already access self.bus0, not true the other way around.
        # That is why we add the buses to the others connected buses here and not in bus0 setter.
        self.bus0.connected_buses = value
        value.connected_buses = self.bus0

        self._bus1 = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        assert isinstance(value, (int, float))
        assert value >= 0

        self._length = value

    @property
    def line_type(self):
        return self._line_type

    @line_type.setter
    def line_type(self, value):
        assert isinstance(value, src.line_type.LineType)

        self._line_type = value
