from src.bus import Bus
from src.line_type import LineType
from src.line import Line

import pytest


def test_sanity_line():
    bus0 = Bus(100, None, 10)
    bus1 = Bus(200, None, 20)
    type_a = LineType("Cool", None)
    line = Line(bus0, bus1, 30, type_a)

    assert line.bus0 == bus0
    assert line.bus1 == bus1
    assert line.length == 30
    assert line.line_type == type_a


def test_multiple_types():
    bus0 = Bus(100, None, 10)
    bus1 = Bus(200, None, 20)
    bus2 = Bus(300, None, 30)
    bus3 = Bus(400, None, 40)
    type_a = LineType("Cool", None)
    type_b = LineType("Uncool", None)
    line_a = Line(bus0, bus1, 30, type_a)
    line_b = Line(bus0, bus1, 40, type_b)
    line_c = Line(bus2, bus3, 50, type_b)

    assert line_a.bus0 == bus0
    assert line_a.bus1 == bus1
    assert line_a.length == 30
    assert line_a.line_type == type_a

    assert line_b.bus0 == bus0
    assert line_b.bus1 == bus1
    assert line_b.length == 40
    assert line_b.line_type == type_b

    assert line_c.bus0 == bus2
    assert line_c.bus1 == bus3
    assert line_c.length == 50
    assert line_c.line_type == type_b


def test_line_same_buses():
    bus = Bus(100, None, 10)
    type_a = LineType("Macho", None)

    with pytest.raises(AssertionError):
        Line(bus, bus, 30, type_a)


def test_connected_buses():
    bus0 = Bus(100, None, 10)
    bus1 = Bus(200, None, 20)
    bus2 = Bus(300, None, 30)
    bus3 = Bus(400, None, 40)
    type_a = LineType("Cool", None)
    type_b = LineType("Uncool", None)
    Line(bus0, bus1, 30, type_a)
    Line(bus0, bus1, 40, type_b)
    Line(bus1, bus2, 50, type_b)
    Line(bus2, bus3, 60, type_a)
    Line(bus0, bus3, 70, type_a)

    # A list is ordered, this should be thought of in different places, but here it is okay, as we only test.
    assert bus0.connected_buses == [bus1, bus3]
    assert bus1.connected_buses == [bus0, bus2]
    assert bus2.connected_buses == [bus1, bus3]
    assert bus3.connected_buses == [bus2, bus0]


def test_line_change_bus0():

    bus0 = Bus(100, None, 10)
    bus1 = Bus(200, None, 20)
    bus2 = Bus(300, None, 30)
    type_a = LineType("Lazy", None)
    line = Line(bus0, bus1, 30, type_a)

    with pytest.raises(PermissionError):
        line.id = 100

    with pytest.raises(PermissionError):
        line.bus0 = bus1

    with pytest.raises(PermissionError):
        line.bus0 = bus2

    assert line.bus0 == bus0
    assert line.bus1 == bus1
    assert line.length == 30
    assert line.line_type == type_a


def test_line_change_length():

    bus0 = Bus(100, None, 10)
    bus1 = Bus(200, None, 20)
    type_a = LineType("Surfer", None)
    line = Line(bus0, bus1, 30, type_a)

    assert line.bus0 == bus0
    assert line.bus1 == bus1
    assert line.length == 30
    assert line.line_type == type_a

    line.length = 0

    assert line.length == 0

    with pytest.raises(AssertionError):
        line.length = "a"

    assert line.length == 0

    line.length = 30.0

    assert line.length == 30

    line.length = 40

    assert line.length == 40.0

    assert line.bus0 == bus0
    assert line.bus1 == bus1
    assert line.line_type == type_a
