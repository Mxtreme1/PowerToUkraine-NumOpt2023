import pytest

from src.bus import Bus
from src.line import Line
from src.line_type import LineType
from src.path import Path


def test_path_sanity():
    bus0 = Bus(100, None, 10)
    bus1 = Bus(200, None, 20)
    bus2 = Bus(300, None, 30)
    bus3 = Bus(400, None, 40)
    type_a = LineType("Cool", None)
    type_b = LineType("Uncool", None)
    line_a = Line(bus0, bus1, 30, type_a)
    line_b = Line(bus1, bus2, 40, type_b)
    line_c = Line(bus2, bus3, 50, type_b)

    path = Path([line_a, line_b, line_c])

    assert path.bus_amount == 4
    assert path.line_amount == 3
    assert path.buses == [bus0, bus1, bus2, bus3]
    assert path.lines == [line_a, line_b, line_c]


def test_path_circle():

    bus0 = Bus(100, None, 10)
    bus1 = Bus(200, None, 20)
    bus2 = Bus(300, None, 30)
    type_a = LineType("Cool", None)
    type_b = LineType("Uncool", None)
    line_a = Line(bus0, bus1, 30, type_a)
    line_b = Line(bus1, bus2, 40, type_b)
    line_c = Line(bus2, bus0, 50, type_b)

    with pytest.raises(AssertionError):
        path = Path([line_a, line_b, line_c])


def test_path_change():

    bus0 = Bus(100, None, 10)
    bus1 = Bus(200, None, 20)
    bus2 = Bus(300, None, 30)
    bus3 = Bus(400, None, 40)
    type_a = LineType("Cool", None)
    type_b = LineType("Uncool", None)
    line_a = Line(bus0, bus1, 30, type_a)
    line_b = Line(bus1, bus2, 40, type_b)
    line_c = Line(bus2, bus3, 50, type_b)

    path = Path([line_a, line_b, line_c])

    assert path.bus_amount == 4
    assert path.line_amount == 3
    assert path.buses == [bus0, bus1, bus2, bus3]
    assert path.lines == [line_a, line_b, line_c]

    with pytest.raises(PermissionError):
        path.id = 100

    with pytest.raises(PermissionError):
        path.buses = [bus0, bus1]

    with pytest.raises(PermissionError):
        path.lines = [line_a, line_b]

    with pytest.raises(AttributeError):
        path.line_amount = 100

    with pytest.raises(AttributeError):
        path.bus_amount = 100
