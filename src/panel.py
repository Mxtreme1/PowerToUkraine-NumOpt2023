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
        assert isinstance(bus, src.bus.Bus)
        assert isinstance(size, (int, float))


        self._id = next(Panel.id_counter)
        self._bus = None
        self._size = 0

        self.bus = bus
        self.size = size

    @property
    def id(self):
        return self._id

    @id.setter
    def set_id(self, identifier):
        raise PermissionError("id can  never be overwritten.")

    @property
    def bus(self):
        return self._bus

    @bus.setter
    def bus(self, value):
        assert isinstance(value, src.bus.Bus)

        self._bus = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        assert isinstance(value, (int, float))
        assert value >= 0
        assert value <= self.bus.roof_size  # The solar panels built on a roof can not exceed the space on it.

        self._size = value
    
    def change_panel_size(self, factor):
        """
        Adds or removes square meters of solar panel, depending on signum of factor. [New_Size] = [Old_Size] + factor
        
        Args:
            factor (int, float):
                Change of panel size, positive or negative.
            
        Returns:

        """
        assert isinstance(factor, (int, float))
        self.size = self.size + factor     # All tests are in setter