import itertools
import pandas as pd
import numpy as np

import src.bus
import src.line
import src.optimisation_task

class Grid:
    """
    A complete low voltage power grid.

    Args:

        buses (list of Bus instances):
            All buses in the power grid, mostly buildings. Default: None

        lines (list of Line instances):
            All lines connecting buses part of the grid. Default: None

        snapshots (Snapshots):
            Points in time with an efficiency and a power draw for each bus, both for each time point. Default: None
    """

    id_counter = itertools.count()

    def __init__(self, buses=None, lines=None, slack_bus=None, snapshots=None):
        self._id = next(Grid.id_counter)

        self._buses = None
        self._lines = None
        self._snapshots = None
        self._slack_bus = None
        self._panels = None
        self._paths = None
        self._optimisation_task = None

        self.buses = buses
        self.lines = lines
        self.snapshots = snapshots
        self.slack_bus = slack_bus

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
        return self._lines
    
    @lines.setter
    def lines(self, value):
        assert isinstance(value, list)
        for line in value:
            assert isinstance(line, src.line.Line)

        unique_lines = []
        for line in value:
            assert line not in unique_lines
            unique_lines.append(line)

        self._lines = value

    @property
    def panels(self):
        panels = []
        for bus in self.buses:
            assert bus.panel not in panels      # Test uniqueness, just in case
            panels.append(bus.panel)

        return panels
    
    @panels.setter
    def panels(self, value):
        raise NotImplementedError("Set for each bus individually for now.")
    
    @property
    def snapshots(self):
        return self._snapshots
    
    @snapshots.setter
    def snapshots(self, value):
        if self.snapshots is not None:
            raise PermissionError("Snapshots can only be set once.")
        else:
            assert isinstance(value, np.ndarray)
            self._snapshots = value

    @property
    def slack_bus(self):
        return self._slack_bus

    @slack_bus.setter
    def slack_bus(self, value):
        if self.slack_bus is not None:
            raise PermissionError("Slack bus can be set only once!")
        else:
            assert isinstance(value, src.bus.Bus)
            self._slack_bus = value


    @property
    def optimisation_task(self):
        return self._optimisation_task

    @optimisation_task.setter
    def optimisation_task(self, value):
        if self.optimisation_task is None:
            assert isinstance(value, src.optimisation_task.OptimisationTask)
            self._optimisation_task = value
        else:
            raise PermissionError("Optimisation task is only settable once to prevent errors.")



    # TODO: Next two methods can be simplified.
    def create_line_rating_matrix(self):
        """
        Creates the matrix R where R_i,j is the rating of the line going from Bus_i to Bus_j if i != j.
        If i == j then it is the maximum possible electricity created on the panel of Bus_i:
        Bus_i.panel.size * output/m^2

        Returns:
            pandas.DataFrame:
                The matrix R with row and column names being the id's of the corresponding buses.

        """

        R = pd.DataFrame(index=[bus.id for bus in self.buses], columns=[bus.id for bus in self.buses])
        R = R.fillna(0)

        for line in self.lines:
            bus0 = line.bus0.id
            bus1 = line.bus1.id
            rating = line.line_type.rating
            
            assert isinstance(rating, (int, float))
            
            
            R.loc[bus0, bus1] = rating
            R.loc[bus1, bus0] = rating

        for bus in self.buses:
            i = bus.id
            R.loc[i, i] = bus.roof_size * bus.panel.output_per_sqm

        return R

    def create_length_matrix(self):
        """
        Creates a matrix with the length of the line going from Bus_i to Bus_j in its entry ij. It is symmetrical.
        If there is no line between them, the value is infinity, if the line is going from the bus to itself it is 0.
        
        Returns:
            pandas.DataFrame:
                The matrix L, where its rows and column names are the id's of buses.

        """

        L = pd.DataFrame(index=[bus.id for bus in self.buses], columns=[bus.id for bus in self.buses])
        L = L.fillna(99999999999)

        for line in self.lines:
            bus0 = line.bus0.id
            bus1 = line.bus1.id
            length = line.length

            assert isinstance(length, (int, float))

            L.loc[bus0, bus1] = length
            L.loc[bus1, bus0] = length

        for bus in self.buses:
            i = bus.id
            L.loc[i, i] = 0

        return L

    def create_area_vector(self):
        """
        Creates a Vector A that has the roof area of Bus_i in its i-th entry.
        
        Returns:
            pandas.Series:
                Vector as described above, the entries are denoted by the id of the bus it describes.
        """

        a = pd.Series(index=[bus.id for bus in self.buses])

        for bus in self.buses:
            a.loc[bus.id] = bus.roof_size

        return a

    def calculate_total_panel_size(self):
        """
        Sum over all roof sizes.

        Returns:
            (int, float):
                Sum over all roof sizes.

        """

        total_size = 0

        for bus in self.buses:
            total_size += bus.roof_size

        return total_size

    def get_panel_output_per_sqm(self):
        """
        Output of any solar panel per square meter.

        Returns:
            (int, float):
                Output of any solar panel per square meter.

        """

        return self.buses[0].panel.output_per_sqm       # All panels currently have the same output per sqm.

    def create_optimisation_task(self):
        """
        Creates the problem to be optimised .
        """

        L = self.create_length_matrix()
        R = self.create_line_rating_matrix()
        a = self.create_area_vector()
        total_panel_size = self.calculate_total_panel_size()
        panel_output_per_sqm = self.get_panel_output_per_sqm()

        self.optimisation_task = src.optimisation_task.OptimisationTask(L, R, a, total_panel_size, panel_output_per_sqm,
                                                                        self.snapshots)
        self.optimisation_task.create_optimisation_task()

    def optimise(self):
        """
        Executes the optimisation task.

        Returns:

        """

        # TODO calc buildout
        self.optimisation_task.optimise()



    def create_build_out(self):
        """


        Args:


        Returns:

        """
        pass
