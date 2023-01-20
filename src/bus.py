from src.panel import Panel

import itertools
import pandas


class Bus:
    """
    Generic point where a power line can start and or end.
    Automatically creates a Panel at the bus that defaults to size 0.

    Args:
        roof_size (int, float):
            square meters of roof size. Greater or equal to zero.

        power draw (Snapshots):
            Points in time with the power draw at that time for the bus.

        panel_size (int, float):
            The size of the solar panel on a roof, can be zero. Also defaults to 0.
    """

    id_counter = itertools.count()

    def __init__(self, roof_size, power_draw, panel_size=0):
        self._id = next(Bus.id_counter)  # Unique identifier
        self._roof_size = 0
        self._power_draw = None
        self._panel = None

        self.roof_size = roof_size
        self.power_draw = power_draw
        self.panel = Panel(self, panel_size)     # creates Panel instance and sets it as panel of the bus.

    def get_id(self):
        return self._id

    def set_id(self, identifier):
        raise PermissionError("Setting of id is not allowed.")

    def get_roof_size(self):

        return self._roof_size

    def set_roof_size(self, roof_size):
        assert isinstance(roof_size, (int, float))
        assert roof_size >= 0

        self._roof_size = roof_size

    def get_power_draw(self):
        return self._power_draw
    
    def set_power_draw(self, power_draw):
        assert isinstance(power_draw, (type(None), pandas.DataFrame))

        if power_draw is not None:
            raise NotImplemented("Check if power draw is valid")

        self._power_draw = power_draw

    def get_panel(self):
        return self._panel

    def set_panel(self, panel):
        assert isinstance(panel, Panel)

        self._panel = panel

    id = property(get_id, set_id)
    panel = property(get_panel, set_panel)
    roof_size = property(get_roof_size, set_roof_size)
    power_draw = property(get_power_draw, set_power_draw)