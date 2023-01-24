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

    def __init__(self, bus0, bus1, length, line_type):
        assert bus0 != bus1
        assert length >= 0

        self._bus0 = None
        self._bus1 = None
        self._length = None
        self._line_type = None

        self.bus0 = bus0
        self.bus1 = bus1
        self.length = length
        self.line_type = line_type

    @property
    def bus0(self):
        return self._bus0

    @bus0.setter
    def bus0(self, value):
        assert isinstance(value, src.bus.Bus)

        self._bus0 = value

    @property
    def bus1(self):
        return self._bus1

    @bus1.setter
    def bus1(self, value):
        assert isinstance(value, src.bus.Bus)

        self._bus1 = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        assert isinstance(value, (int, float))

        self._length = value

    @property
    def line_type(self):
        return self._line_type

    @line_type.setter
    def line_type(self, value):
        assert isinstance(value, src.line_type.LineType)

        self._line_type = value

