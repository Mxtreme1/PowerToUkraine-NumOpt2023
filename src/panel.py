import itertools
import pandas

import src.bus


class Panel:
    """
    Auto-created with each bus. We only need to set the size really.
    A group of solar panels built on a roof (referred to as Bus internally).

    Args:
        bus (Bus):
            The location of the solar panel.

        size (int, float):
            The size of the solar panel in square meters. Has to be smaller or equal to roof size (Bus.size).

    """

    id_counter = itertools.count()

    def __init__(self, bus, size):
        self._id = next(Panel.id_counter)
        self._bus = None
        self._size = 0

        self.bus = bus
        self.size = size

    def get_id(self):
        return self._id

    def set_id(self, identifier):
        raise PermissionError("id can  never be overwritten.")

    def get_bus(self):
        return self._bus

    def set_bus(self, bus):
        assert isinstance(bus, src.bus.Bus)

        self._bus = bus

    def get_size(self):
        return self._size

    def set_size(self, size):
        assert isinstance(size, (int, float))
        assert size >= 0
        assert size <= self.bus.roof_size  # The solar panels built on a roof can not exceed the space on it.

        self._size = size

    id = property(get_id, set_id)
    bus = property(get_bus, set_bus)
    size = property(get_size, set_size)
