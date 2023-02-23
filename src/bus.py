from src.panel import Panel

import itertools
import numpy as np


class Bus:
    """
    Generic point where a power line can start and or end.
    Automatically creates a Panel at the bus that defaults to size 0.

    Args:
        roof_size (int, float):
            square meters of roof size. Greater or equal to zero.

        power draw (pandas.DataFrame):
            Points in time with the power draw at that time for the bus.
            Need to be same time frames aka snapshots as in Line efficiency DataFrame.

        panel_size (int, float):
            The size of the solar panel on a roof, can be zero. Also defaults to 0.
    """

    id_counter = itertools.count()

    def __init__(self, roof_size, power_draw, panel_size=0):

        self._id = next(Bus.id_counter)  # Unique identifier

        self._roof_size = None
        self._power_draw = None
        self._panel = None
        self._connected_buses = []

        self.roof_size = roof_size
        self.power_draw = power_draw
        self.panel = Panel(self, panel_size)     # creates Panel instance and sets it as panel of the bus.

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, identifier):
        raise PermissionError("Setting of id is not allowed.")

    @property
    def roof_size(self):

        return self._roof_size

    @roof_size.setter
    def roof_size(self, value):
        assert isinstance(value, (int, float))
        assert value >= 0

        self._roof_size = value

    @property
    def power_draw(self):
        return self._power_draw

    @power_draw.setter
    def power_draw(self, value):
        assert isinstance(value, (type(None), list))

        if value is not None and self.power_draw is not None:
            raise PermissionError("Power draw can be set only once!")
        else:
            assert isinstance(value, (list, type(None)))

            if isinstance(value, list):
                for item in value:
                    assert isinstance(item, (int, float, np.int64, np.float64))
                    assert item >= 0        # Power draw is non-negative

        self._power_draw = value

    @property
    def panel(self):
        return self._panel

    @panel.setter
    def panel(self, value):
        if self._panel is not None:
            raise PermissionError("A panel is fixed on a bus. Each bus has a unique panel. Get off my roof!")

        assert isinstance(value, Panel)

        self._panel = value

    @property
    def connected_buses(self):
        return self._connected_buses

    @connected_buses.setter
    def connected_buses(self, value):   # Only adds a new bus.
        assert isinstance(value, Bus)

        # It is okay if it already connected, there might be two lines connecting the buses.
        if value not in self.connected_buses:
            self._connected_buses.append(value)
        