from src.bus import Bus
from src.line import Line
from src.line_type import LineType
from src.grid import Grid
from src.optimisation_task import OptimisationTask

import numpy as np

bus0 = Bus(100.0001, None, 10)
bus1 = Bus(200, None, 20)
bus2 = Bus(300, None, 30)
bus3 = Bus(400, None, 40)
bus4 = Bus(500, None, 50)
bus5 = Bus(600, None, 60)
slack_bus = Bus(0, None, 0)
type_a = LineType("Cool", 1000)
type_b = LineType("Uncool", 2000)
line_a = Line(bus0, bus1, 30, type_a)
line_b = Line(bus1, bus2, 40, type_b)
line_c = Line(bus2, bus3, 50, type_b)
line_1 = Line(bus0, bus4, 60, type_a)
line_2 = Line(bus4, bus5, 70, type_b)
line_slack = Line(slack_bus, bus0, 100, type_b)
snapshots = np.linspace(0, 24, 2)

grid = Grid([bus0, bus1, bus2, bus3, bus4, bus5, slack_bus], [line_a, line_b, line_c, line_1, line_2, line_slack],
            slack_bus, snapshots)

def test_simple_task():
    b0 = Bus(100, None, 0)
    b1 = Bus(70, None, 0)
    bs = Bus(0, None, 0)
    t_a = LineType("Cool", 100)
    l = Line(b0, b1, 5, t_a)
    ls = Line(bs, b0, 100, t_a)

    simple_grid = Grid([b0, b1, bs], [l, ls], bs, snapshots)
    simple_grid.create_optimisation_task()
    simple_grid.optimise()
    pass


def test_optimisation_task_sanity():
    L = grid.create_length_matrix()
    R = grid.create_line_rating_matrix()
    a = grid.create_area_vector()
    # TODO replace with power flow
    c = None
    total_panel_size = grid.calculate_total_panel_size()
    panel_output_per_sqm = grid.get_panel_output_per_sqm()

    OptimisationTask(L, R, a, total_panel_size, panel_output_per_sqm, snapshots)
