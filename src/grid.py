import itertools
import pandas as pd
import networkx as nx

import src.bus
import src.line
import src.path

from src.path import Path


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

    def __init__(self, buses=None, lines=None, snapshots=None):
        self._id = next(Grid.id_counter)

        self._buses = None
        self._lines = None
        self._snapshots = None
        self._panels = None
        self._paths = None

        self.buses = buses
        self.lines = lines
        self.snapshots = snapshots

        self._calculate_paths()

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
    def paths(self):
        return self._paths
    
    @paths.setter
    def paths(self, value):
        if self._paths is not None:
            raise PermissionError("Paths are calculated automatically when buses and lines are added.")

        assert isinstance(value, list)

        unique_paths = []
        for path in value:
            assert isinstance(path, src.path.Path)
            assert path not in unique_paths
            unique_paths.append(path)

        self._paths = value

    @property
    def snapshots(self):
        return self._snapshots
    
    @snapshots.setter
    def snapshots(self, value):
        pass

    def _add_bus(self, bus):
        """
        Adds single bus to the network.


        Args:
            bus (Bus):
                A bus instance not already part of the network.

        """

    def _add_multiple_buses(self):
        """


        Args:


        Returns:

        """
        pass


    def _remove_bus(self):
        """


        Args:


        Returns:

        """
        pass

    def _remove_multiple_buses(self):
        """


        Args:


        Returns:

        """
        pass


    def _add_line(self):
        """


        Args:


        Returns:

        """
        pass

    def _add_multiple_lines(self):
        """


        Args:


        Returns:

        """
        pass


    def _remove_line(self):
        """


        Args:


        Returns:

        """
        pass

    def _remove_multiple_lines(self):
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
    
    def _create_networkx_graph(self):
        """
        Creates a networkx graph object using the buses and lines.
        """

        graph = nx.MultiGraph()
        graph.add_nodes_from([bus for bus in self.buses])

        for line in self.lines:
            graph.add_edge(line.bus0, line.bus1, key=line)

        return graph

    def _calculate_paths(self):
        """
        Calculate all possible paths. Paths are directed in our model.

        """

        graph = self._create_networkx_graph()

        # Find all paths starting at each node (finds the paths as )
        paths = {}
        for start_node in self.buses:
            paths[start_node] = []
            for end_node in self.buses:
                start_to_end_paths = nx.all_simple_edge_paths(graph, start_node, end_node)
                start_to_end_paths = list(start_to_end_paths)
                if start_to_end_paths is not []:
                    paths[start_node] += start_to_end_paths

        # Convert to path objects
        all_path_instances = []
        for bus in self.buses:
            bus_paths = paths[bus]
            for bus_path in bus_paths:
                lines_on_bus_path = []
                for connection in bus_path:
                    lines_on_bus_path.append(connection[2])
                path = Path(lines_on_bus_path)
                all_path_instances.append(path)

        self.paths = all_path_instances