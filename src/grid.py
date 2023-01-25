import itertools
import pandas as pd

import src.bus


class Grid:
    """
    A complete low voltage power grid.

    Args:

        buses (list of Bus instances):
            All buses in the power grid, mostly buildings.

        lines (list of Line instances):
            All lines connecting buses part of the grid.

        snapshots (Snapshots):
            Points in time with an efficiency and a power draw for each bus, both for each time point.
    """

    id_counter = itertools.count()

    def __init__(self, buses, lines, snapshots):
        self._id = next(Grid.id_counter)

        self._buses = None
        self._lines = None
        self._snapshots = None
        self._panels = None
        self._paths = None

        self.buses = buses
        self.lines = lines
        self.snapshots = snapshots

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        raise PermissionError("No change in unique identifier id allowed for Grids.")

    @property
    def buses(self):
        return self._buses
    
    @buses.setter
    def buses(self, value):
        if self._buses is not None:
            raise PermissionError("No changing of buses after Grid creation, add them all at once to prevent errors.")

        assert isinstance(value, list)
        for item in value:
            assert isinstance(item, src.bus.Bus)

        # Checks for duplicates in the buses
        unique_buses = []
        for item in value:
            assert item not in unique_buses
            unique_buses.append(item)

        self._buses = value



            
        
    
    @property
    def lines(self):
        return 
    
    @lines.setter
    def lines(self, value):
        pass
    
    @property
    def panels(self):
        raise NotImplementedError("Get for each line and return.")
        pass
    
    @panels.setter
    def panels(self, value):
        raise NotImplementedError("Set for each bus individually for now.")
    
    @property
    def paths(self):
        return 
    
    @paths.setter
    def paths(self, value):
        pass
    
    @property
    def snapshots(self):
        return 
    
    @snapshots.setter
    def snapshots(self, value):
        pass


    def add_bus(self):
        """


        Args:


        Returns:

        """
        pass

    def add_multiple_buses(self):
        """


        Args:


        Returns:

        """
        pass


    def remove_bus(self):
        """


        Args:


        Returns:

        """
        pass

    def remove_multiple_buses(self):
        """


        Args:


        Returns:

        """
        pass


    def add_line(self):
        """


        Args:


        Returns:

        """
        pass

    def add_multiple_lines(self):
        """


        Args:


        Returns:

        """
        pass


    def remove_line(self):
        """


        Args:


        Returns:

        """
        pass

    def remove_multiple_lines(self):
        """


        Args:


        Returns:

        """
        pass


    def create_build_out(self):
        """


        Args:


        Returns:

        """
        pass


    def calculate_paths(self):
        """


        Args:


        Returns:

        """
        pass


