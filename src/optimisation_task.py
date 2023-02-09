import pandas as pd
import numpy as np
import casadi as ca
import math


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

    def __init__(self, L, R, a, total_panel_size, panel_output_per_sqm, snapshots):

        self._L = None
        self._R = None
        self._a = None
        self._total_panel_size = None
        self._panel_output_per_sqm = None
        self._task = None
        self._x = None
        self._snapshots = None
        # Write getters and setters
        self._xt = None
        self._a = None

        self.L = L
        self.R = R
        self.a = a
        self.total_panel_size = total_panel_size
        self.panel_output_per_sqm = panel_output_per_sqm
        self.snapshots = snapshots

    @property
    def L(self):
        return self._L

    @L.setter
    def L(self, value):
        assert isinstance(value, pd.DataFrame)
        for row in value.index.values:
            for column in value.columns.values:
                assert isinstance(value.loc[row, column], (np.int64, np.float64))
                assert value.loc[row, column] == value.loc[column, row]     # Symmetry test
            assert value.loc[row, row] == 0

        self._L = value

    @property
    def R(self):
        return self._R

    @R.setter
    def R(self, value):
        assert isinstance(value, pd.DataFrame)
        for row in value.index.values:
            for column in value.columns.values:
                assert isinstance(value.loc[row, column], (np.int64, np.float64))
                assert value.loc[row, column] == value.loc[column, row]     # Tests symmetry

        self._R = value

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        assert isinstance(value, pd.Series)
        for bus_id in value.index.values:
            assert isinstance(bus_id, (np.int64, np.float64))

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

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, value):
        if self._task is None:
            # TODO: add type assertion
            self._task = value
        else:
            raise PermissionError("Task is only settable once to prevent errors.")

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self.x is not None:
            raise PermissionError("Not settable")
        else:
            # TODO: assert type
            self._x = value

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

    # define function for energy consumption of every house, where c_max is the maximal energy house i consumes and
    # cmin is the minimal energy it consumes(at night or at day)
    @staticmethod
    def create_energy_consumption(c_max_arg, c_min_arg, t_arg):
        if 16 > t_arg >= 0:
            c_func = c_max_arg * (math.sin(2 * math.pi * (1 / 16) * t_arg)) ** 2 + c_min_arg
        elif 16 <= t_arg <= 24:
            c_func = c_min_arg
        else:
            raise ValueError("t is value between 0 and 24")

        return c_func

    # define function that returns array of energy consumption of each individual house given time t1
    # where the input arguments are a fixed time and the lists of cmax and cmin
    @staticmethod
    def create_array_of_consumption(t1, argcmax, argcmin):
        consumption_at_time_t1_all_houses = []
        for argc_max, argc_min_ in zip(argcmax, argcmin):
            consumption_at_time_t1_all_houses.append(OptimisationTask.create_energy_consumption(argc_max, argc_min_, t1))
        return consumption_at_time_t1_all_houses

    # define function for amount of sunlight we get at given time t
    @staticmethod
    def sun(t_arg):
        s = 0
        if 16 > t_arg >= 0:
            s = 80 * (math.sin((2 * np.pi * (1 / 48) * t_arg - 4 / 5 * math.pi))) ** 4
        elif 16 <= t_arg:
            s = 0
        if s <= 0:
            s = 0

        return s

    def create_optimisation_task(self):
        """
        Creates the pulp variables P_ij for the lines.
        """

        L = self.L
        R = self.R
        roof_sizes = self.a
        snapshots = self.snapshots
        available_panel_size = self.total_panel_size
        N = roof_sizes.size - 1      # Ignore slack bus for solar panels on roof

        # TODO: Code this
        c_max = [100, 80]
        c_min = [10, 20]

        K = self.panel_output_per_sqm
        num_snaps = range(len(snapshots))  # easy for loops

        # create empty optimization problem
        opti = ca.Opti()


        xt = []
        for t in num_snaps:
            xt.append(opti.variable(N + 1, N + 1, 'symmetric'))

        a = opti.variable(N, 1)



        # define objective, only sum over elements below and in main diagonal
        f = 0
        for t in num_snaps:
            for i in range(N):
                for j in range(N):
                    if i == j:
                        f += a[i] * 0.1
                    else:
                        f += 1 / 2 * L.iloc[j, i] * ((xt[t][j, i]) ** 2)

        big_m = 999999
        for t in num_snaps:
            for i in range(N):
                f += big_m * (xt[t][i, N] * L.iloc[i, N]) ** 2

        opti.minimize(f)



        # constraint how much area of solar panels, we can distribute in total
        area_sum = 0
        for i in range(N):
            area_sum += a[i]

        opti.subject_to(area_sum <= available_panel_size)



        # constraint how energy production of house i is connected to area of solar panels
        for t in num_snaps:
            for i in range(N):
                opti.subject_to(xt[t][i, i] == K * a[i])



        # constraint that roof area is limited for each house i
        for bus_num in range(N):
            opti.subject_to(a[bus_num] <= roof_sizes.iloc[bus_num])
            opti.subject_to(0 <= a[bus_num])



        # constraint that each individual power line can only transport in one direction(positivity)
        for t in num_snaps:
            for i in range(N + 1):
                for j in range(N + 1):
                    if i == j:
                        continue
                    else:
                        opti.subject_to(xt[t][i, j] <= R.iloc[i, j])
                        opti.subject_to(xt[t][i, j] >= -R.iloc[i, j])



        # constraint for the amount of energy each individual house consumes for N discrete times between
        # 0 and 24 hours
        ct = []
        for t in num_snaps:
            ct.append(OptimisationTask.create_array_of_consumption(snapshots[t], c_max, c_min))

        Pendt = [0] * len(snapshots)
        for t in num_snaps:
            for i in range(N):
                for j in range(N + 1):
                    if i <= j:
                        Pendt[t] += xt[t][i, j]
                    else:
                        Pendt[t] += -xt[t][i, j]
                opti.subject_to(ct[t][i] == Pendt[t])

        # constraint for the generator
        # constraint for generator
        Pendgent = [0] * len(snapshots)
        for t in num_snaps:
            for j in range(N):
                Pendgent[t] += xt[t][N, j]
            opti.subject_to(xt[t][N, N] == Pendgent[t])


        self.task = opti
        self._xt = xt
        self._a = a


    def optimise(self):
        """
        Runs the optimiser (ipopt).

        Args:


        Returns:
            The current on each line as a matrix with directed line entries.
        """

        # define solver
        self.task.solver('ipopt')  # Use IPOPT as solver

        # solve optimization problem
        sol = self.task.solve()

        # read and print solution
        xopt = []
        for t in range(len(self.snapshots)):
            xopt.append(sol.value(self._xt[t]))
        aopt = sol.value(self._a)

        print("#########################################")
        for t in range(len(self.snapshots)):
            print(xopt[t])
            print("#########################################")
        print(aopt)

        # display(yopt)
        # to see some more info
        # print(yopt)
        print(sol.stats)
