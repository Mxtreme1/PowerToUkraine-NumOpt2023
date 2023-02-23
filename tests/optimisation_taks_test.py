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
snapshots = np.linspace(0, 24, 1)

grid = Grid([bus0, bus1, bus2, bus3, bus4, bus5, slack_bus], [line_a, line_b, line_c, line_1, line_2, line_slack],
            slack_bus, snapshots)


def test_original_task():
    house1 = Bus(100, None, 0)
    house2 = Bus(150, None, 0)
    house3 = Bus(60, None, 0)
    bakery = Bus(150, None, 0)
    generator = Bus(0, None, 0)

    type_inf = LineType("inf", 9999999999999)

    line1_2 = Line(house1, house2, 40, type_inf)
    line1_3 = Line(house1, house3, 30, type_inf)
    line1_g = Line(house1, generator, 10, type_inf)
    line2_4 = Line(house2, bakery, 30, type_inf)
    line2_g = Line(house2, generator, 30, type_inf)
    line4_g = Line(bakery, generator, 5, type_inf)

    snaps = np.linspace(0, 24, 1)

    original_grid = Grid([house1, house2, house3, bakery, generator],
                         [line1_2, line1_3, line1_g, line2_4, line2_g, line4_g],
                         generator, snaps)
    original_grid.create_optimisation_task()
    original_grid.optimise()


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


def test_presentation_grid():
    house_1 = Bus(100, None, 0)
    house_2 = Bus(150, None, 0)
    house_3 = Bus(60, None, 0)
    bakery = Bus(150, None, 0)
    slack_node = Bus(0, None, 0)
    line_slack_1 = Line(slack_node, house_1, 10, type_b)
    line_slack_2 = Line(slack_node, house_2, 20, type_a)
    line_slack_bakery = Line(slack_node, bakery, 5, type_b)
    line_1_3 = Line(house_1, house_3, 30, type_a)
    line_1_2 = Line(house_1, house_2, 30, type_a)
    line_2_bakery = Line(house_2, bakery, 30, type_a)
    presentation_grid = Grid([house_1, house_2, house_3, bakery, slack_node], [line_slack_1, line_slack_2,
                             line_slack_bakery, line_1_2, line_1_3, line_2_bakery], slack_node, snapshots)

    presentation_grid.create_optimisation_task()
    presentation_grid.optimise()


def test_optimisation_task_sanity():
    L = grid.create_length_matrix()
    R = grid.create_line_rating_matrix()
    a = grid.create_area_vector()
    # TODO replace with power flow
    c = None
    total_panel_size = grid.calculate_total_panel_size()
    panel_output_per_sqm = grid.get_panel_output_per_sqm()

    OptimisationTask(L, R, a, total_panel_size, panel_output_per_sqm, snapshots)
