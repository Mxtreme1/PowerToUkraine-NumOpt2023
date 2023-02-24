import casadi
import pandas as pd
import numpy as np
import casadi as ca
import math

import src.bus


class OptimisationTask:
    """
    Handles the creation and solving of the optimisation problem.

    Args:
        line_length (pandas.DataFrame):
            A matrix with the length of the line going from Bus_i to Bus_j in its entry ij. It is symmetrical.
            If there is no line between them, the value is infinity,
            if the line is going from the bus to itself it is 0.

        line_rating (pandas.DataFrame):
            The matrix R where R_i,j is the rating of the line going from Bus_i to Bus_j if i != j.
            If i == j then it is the maximum possible electricity created on the panel of Bus_i:
            Bus_i.panel.size * output/m^2

        a (pandas.Series):
            Vector A that has the roof area of Bus_i in its i-th entry.
    """

    def __init__(self, line_length, line_rating, a, total_panel_size, panel_output_per_sqm, snapshots, buses):

        self._L = None
        self._R = None
        self._a = None
        self._total_panel_size = None
        self._panel_output_per_sqm = None
        self._task = None
        self._solution = None
        self._x_task = None
        self._a_task = None
        self._snapshots = None
        self._num_snapshots = None
        # Write getters and setters
        self._xt = None
        self._a = None
        self._buses = None

        self.line_length = line_length
        self.line_rating = line_rating
        self.a = a
        self.total_panel_size = total_panel_size
        self.panel_output_per_sqm = panel_output_per_sqm
        self.snapshots = snapshots
        self.buses = buses

    @property
    def line_length(self):
        return self._L

    @line_length.setter
    def line_length(self, value):
        assert isinstance(value, pd.DataFrame)
        for row in value.index.values:
            for column in value.columns.values:
                assert isinstance(value.loc[row, column], (np.int64, np.float64))
                assert value.loc[row, column] == value.loc[column, row]     # Symmetry test
            assert value.loc[row, row] == 0

        self._L = value

    @property
    def line_rating(self):
        return self._R

    @line_rating.setter
    def line_rating(self, value):
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
            assert isinstance(value, casadi.Opti)

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
            self._x = value

    @property
    def snapshots(self):
        return self._snapshots

    @snapshots.setter
    def snapshots(self, value):
        if self.snapshots is not None:
            raise PermissionError("Snapshots can only be set once.")
        else:
            assert isinstance(value, (np.ndarray, list))
            self._snapshots = value

    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, value):
        if self.solution is not None:
            raise PermissionError("Solution settable only once.")
        else:
            self._solution = value

    @property
    def num_snapshots(self):
        if self.snapshots is None:
            raise ValueError("Snapshots not set.")
        else:
            return range(len(self.snapshots))  # easy for loops

    @property
    def buses(self):
        return self._buses

    @buses.setter
    def buses(self, value):
        assert isinstance(value, list)
        for item in value:
            assert isinstance(item, src.bus.Bus)

        self._buses = value

    @staticmethod
    def create_energy_consumption(c_max_arg, c_min_arg, t_arg):
        """
        Define function for energy consumption of every house, where c_max is the maximal energy house i consumes and
        cmin is the minimal energy it consumes(at night or at day)

        Args:
            c_max_arg:
            c_min_arg:
            t_arg:

        Returns:

        """
        if 16 > t_arg >= 0:
            c_func = c_max_arg * (math.sin(2 * math.pi * (1 / 16) * t_arg)) ** 2 + c_min_arg
        elif 16 <= t_arg <= 24:
            c_func = c_min_arg
        else:
            raise ValueError("t is value between 0 and 24")

        return c_func

    @staticmethod
    def create_array_of_consumption(t1, argcmax, argcmin):
        """
        Define function that returns array of energy consumption of each individual house given time t1
        where the input arguments are a fixed time and the lists of cmax and cmin

        Args:
            t1:
            argcmax:
            argcmin:

        Returns:

        """
        consumption_at_time_t1_all_houses = []
        for argc_max, argc_min_ in zip(argcmax, argcmin):
            consumption_at_time_t1_all_houses.append(OptimisationTask.create_energy_consumption(argc_max, argc_min_, t1))
        return consumption_at_time_t1_all_houses

    @staticmethod
    def sun(t_arg):
        """
        Define function for amount of sunlight we get at given time t

        Args:
            t_arg:

        Returns:

        """
        s = 0
        if 16 > t_arg >= 0:
            s = (math.sin((2 * np.pi * (1 / 48) * (t_arg - 8.5) - 4 / 5 * math.pi))) ** 4
        elif 16 <= t_arg:
            s = 0
        if s <= 0:
            s = 0

        return s

    def create_problem_and_variables(self, N, num_snaps):
        """
        Initialises the optimisation problem and its variables.
        Args:
            N (int):
                The number of buildings/buses, excluding the generator/slack node.

            num_snaps (int):
                Number of snapshots.

        """

        # create empty optimization problem
        opti = ca.Opti()

        # define variable(nxn matrix)

        xt = []
        for _ in num_snaps:
            xt.append(opti.variable(N + 1, N + 1))

        a = opti.variable(N, 1)

        self.task = opti
        self._x_task = xt
        self._a_task = a

    def create_cost_function(self, N, num_snaps, L=None):
        """
        Adds the cost function to the optimisation problem.

        Args:
            N (int):
                The number of buildings/buses, excluding the generator/slack node.

            num_snaps (int):
                Number of snapshots.

            L (pandas.DataFrame):
                The length of power lines from each house to another, 0 for house to itself and very high value for
                nonexistent lines.

        """
        # define objective, only sum over elements below and in main diagonal
        opti = self.task
        xt = self._x_task
        a = self._a_task
        if L is None:
            L = self.line_length

        f = 0
        for t in num_snaps:
            for i in range(N + 1):
                for j in range(N + 1):
                    if i == j and i < N:
                        f += a[i] * 0.0001  # Generator does not have a roof
                    elif i == j and i == N:
                        f += 999999999 * (xt[t][N, N])  # Punish generator current hard
                    else:
                        # Only x[t][i, j] or x[t][j, i] should ever be nonzero due to >= 0 and cost function punishing
                        # f += L.iloc[i, j] * xt[t][i, j]  # Punish including generator lines
                        length = L.iloc[i, j]
                        power_flow = xt[t][i, j]
                        f += length * power_flow      # Punish including generator lines

        opti.minimize(f)

    def create_constraint_total_panel_size(self, N, available_panel_size=None):
        opti = self.task
        a = self._a_task
        if available_panel_size is None:
            available_panel_size = self.total_panel_size
        # constraint for maximal panel-area we have
        area_sum = 0
        for i in range(N):
            area_sum += a[i]

        # constraint how much area of solar panels, we can distribute in total
        opti.subject_to(area_sum <= available_panel_size)

    def create_constraint_panel_output(self, N, num_snaps, snapshots, K=None):
        opti = self.task
        xt = self._x_task
        a = self._a_task
        if K is None:
            K = self.panel_output_per_sqm
        # constraint how energy production of house i is connected to area of solar panels
        for t in num_snaps:
            for i in range(N):
                opti.subject_to(xt[t][i, i] == K * max(0.01, self.sun(snapshots[t])) * a[i])

    def create_constraint_house_panel_size(self, N, roof_sizes=None):
        opti = self.task
        a = self._a_task
        if roof_sizes is None:
            roof_sizes = self.a     # Different from a_task, a_task is variable, a is actual roof size
        # constraint that roof area is limited for each house i
        for bus_num in range(N):
            opti.subject_to(a[bus_num] <= roof_sizes.iloc[bus_num])
            opti.subject_to(0 <= a[bus_num])

    def create_constraint_line_rating(self, N, num_snaps, R=None):
        opti = self.task
        xt = self._x_task
        if R is None:
            R = self.line_rating
        # constraint that each individual power line can only transport in one direction(positivity)
        for t in num_snaps:
            for i in range(N + 1):
                for j in range(N + 1):
                    if [i, j] == [N, N]:
                        continue        # The generator can take current out of the system.
                    elif i == j:
                        opti.subject_to(xt[t][i, j] >= 0)
                    else:
                        opti.subject_to(xt[t][i, j] <= R.iloc[i, j])
                        opti.subject_to(xt[t][i, j] >= 0)

    def create_constraint_house_consumption(self, N, num_snaps):
        opti = self.task
        xt = self._x_task
        # constraint for the amount of energy each individual house consumes for N discrete times between
        # 0 and 24 hours

        Pendt = []
        for t in num_snaps:
            Pendt.append([])
            for i in range(N):
                Pendt[t].append([0])
        for t in num_snaps:
            for i in range(N):
                for j in range(N + 1):
                    Pendt[t][i] += xt[t][i, j]
                    Pendt[t][i] += -xt[t][j, i]
                Pendt[t][i] += xt[t][i, i]
                opti.subject_to(self.buses[i].power_draw[t] == Pendt[t][i])

    def create_constraint_generator_production(self, N, num_snaps):
        opti = self.task
        xt = self._x_task
        # constraint for the generator
        Pendgent = [0] * len(num_snaps)
        for t in num_snaps:
            for j in range(N):
                # What is coming out minus what is coming in, aka production of gen should be xt[t][N, N]
                Pendgent[t] += xt[t][j, N]
                Pendgent[t] += -xt[t][N, j]
            opti.subject_to(xt[t][N, N] == Pendgent[t])

    def solve(self):
        opti = self.task
        # define solver
        opti.solver('ipopt')  # Use IPOPT as solver

        # solve optimization problem
        self.solution = opti.solve()

    def print_solution(self):
        xt = self._x_task
        a = self._a_task
        sol = self.solution
        num_snaps = self.num_snapshots

        # read and print solution
        xopt = []
        for t in num_snaps:
            xopt.append(sol.value(xt[t]))
        aopt = sol.value(a)
        print("#########################################")
        for t in num_snaps:
            print(xopt[t].round())
            print("#########################################")
        print(aopt.round())

        # display(yopt)
        # to see some more info
        # print(yopt)
        print(sol.stats)

    def create_optimisation_task(self):
        """
        Creates the pulp variables P_ij for the lines.
        """

        N_const = self.a.size - 1       # Slack bus is a regular bus, but is not counted in N
        num_snaps = self.num_snapshots
        snapshots = self.snapshots

        self.create_problem_and_variables(N_const, num_snaps)

        # self.create_cost_function(N_const, num_snaps, L_const)
        self.create_cost_function(N_const, num_snaps)

        # self.create_constraint_total_panel_size(N_const, available_panel_size_const)
        self.create_constraint_total_panel_size(N_const)

        # self.create_constraint_panel_output(N_const, num_snaps, K_const)
        self.create_constraint_panel_output(N_const, num_snaps, snapshots)

        # self.create_constraint_house_panel_size(N_const, roof_sizes_const)
        self.create_constraint_house_panel_size(N_const)

        # self.create_constraint_line_rating(N_const, num_snaps, R_const)
        self.create_constraint_line_rating(N_const, num_snaps)

        # self.create_constraint_house_consumption(N_const, num_snaps, ct_const)
        self.create_constraint_house_consumption(N_const, num_snaps)

        self.create_constraint_generator_production(N_const, num_snaps)

    def optimise(self):
        """
        Runs the optimiser (ipopt).

        Args:


        Returns:
            The current on each line as a matrix with directed line entries.
        """

        self.solve()

        self.print_solution()

        return self.solution, self._x_task, self._a_task
