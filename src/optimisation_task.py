import pandas
import pandas as pd
import pulp as pl


class OptimisationTask:
    """
    Handles the creation and solving of the optimisation problem.

    Args:
        L (pandas.DataFrame):
            A matrix with the length of the line going from Bus_i to Bus_j in its entry ij. It is symmetrical.
            If there is no line between them, the value is infinity,
            if the line is going from the bus to itself it is 0.

        R (pandas.DataFrame):
            The matrix R where R_i,j is the rating of the line going from Bus_i to Bus_j if i != j.
            If i == j then it is the maximum possible electricity created on the panel of Bus_i:
            Bus_i.panel.size * output/m^2

        a (pandas.Series):
            Vector A that has the roof area of Bus_i in its i-th entry.
    """

    def __init__(self, L, R, a, total_panel_size, panel_output_per_sqm):

        self._L = None
        self._R = None
        self._a = None
        self._total_panel_size = None
        self._panel_output_per_sqm = None

        self.L = L
        self.R = R
        self.a = a
        self.total_panel_size = total_panel_size
        self.panel_output_per_sqm = panel_output_per_sqm

    @property
    def L(self):
        return self._L

    @L.setter
    def L(self, value):
        assert isinstance(value, pandas.DataFrame)
        for row in value.index.values:
            for column in value.columns.values:
                assert isinstance(value.loc[row, column], (int, float))
                assert value.loc[row, column] == value.loc[column, row]     # Tests symmetry
            assert value.loc[row, row] == 0

        self._L = value

    @property
    def R(self):
        return self._R

    @R.setter
    def R(self, value):
        assert isinstance(value, pandas.DataFrame)
        for row in value.index.values:
            for column in value.columns.values:
                assert isinstance(value.loc[row, column], (int, float))
                assert value.loc[row, column] == value.loc[column, row]     # Tests symmetry

        self._R = value

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        assert isinstance(value, pandas.Series)
        for bus in value.index.values:
            assert isinstance(bus, (int, float))

        self._a = value

    @property
    def total_panel_size(self):
        return self._total_panel_size

    @total_panel_size.setter
    def total_panel_size(self, value):
        assert isinstance(value, (int, float))
        self._total_panel_size = value

    @property
    def panel_output_per_sqm(self):
        return self._panel_output_per_sqm

    @panel_output_per_sqm.setter
    def panel_output_per_sqm(self, value):
        assert isinstance(value, (int, float))

        self._panel_output_per_sqm = value
