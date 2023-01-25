import pytest

from src.bus import Bus
from src.line import Line
from src.line_type import LineType
from src.grid import Grid


def sanity_check_grid():

    bus0 = Bus(100, None, 10)
    bus1 = Bus(200, None, 20)
    bus2 = Bus(300, None, 30)
    bus3 = Bus(400, None, 40)
    bus4 = Bus(500, None, 50)
    bus5 = Bus(600, None, 60)
    type_a = LineType("Cool", None)
    type_b = LineType("Uncool", None)
    line_a = Line(bus0, bus1, 30, type_a)
    line_b = Line(bus1, bus2, 40, type_b)
    line_c = Line(bus2, bus3, 50, type_b)
    line_A = Line(bus0, bus4, 60, type_a)
    line_B = Line(bus4, bus5, 70, type_b)

    grid = Grid([bus0, bus1, bus2, bus3, bus4, bus5], [line_a, line_b, line_c, line_A, line_B])