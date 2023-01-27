from src.bus import Bus
from src.line import Line
from src.line_type import LineType
from src.grid import Grid

bus0 = Bus(100, None, 10)
bus1 = Bus(200, None, 20)
bus2 = Bus(300, None, 30)
bus3 = Bus(400, None, 40)
bus4 = Bus(500, None, 50)
bus5 = Bus(600, None, 60)
type_a = LineType("Cool", 1000)
type_b = LineType("Uncool", 2000)
line_a = Line(bus0, bus1, 30, type_a)
line_b = Line(bus1, bus2, 40, type_b)
line_c = Line(bus2, bus3, 50, type_b)
line_1 = Line(bus0, bus4, 60, type_a)
line_2 = Line(bus4, bus5, 70, type_b)

grid = Grid([bus0, bus1, bus2, bus3, bus4, bus5], [line_a, line_b, line_c, line_1, line_2])

def test_sanity_grid():
    assert set(grid.buses) == {bus0, bus1, bus2, bus3, bus4, bus5}
    assert set(grid.lines) == {line_a, line_b, line_c, line_1, line_2}

def test_rating_matrix():
    R = grid.create_line_rating_matrix()
    L = grid.create_length_matrix()
    a = grid.create_area_vector()

def test_bus_left_out():
    grid2 = Grid([bus0, bus1, bus2, bus4, bus5], [line_a, line_b, line_1, line_2])
    grid2.create_line_rating_matrix()
    grid2.create_length_matrix()
    grid2.create_area_vector()
