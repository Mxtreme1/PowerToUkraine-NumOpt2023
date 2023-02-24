from src.bus import Bus

import pytest


def test_bus_sanity():
    bus = Bus(70.0, [100], 1)
    assert bus.roof_size == 70
    assert bus.power_draw == [100]
    assert bus.panel.size == 1


def test_bus_negative_power_draw():
    with pytest.raises(AssertionError):
        Bus(70.0, [-100], 1)
    with pytest.raises(AssertionError):
        Bus(70.0, [100, -100], 1)


def test_bus_change_roof_size():
    bus = Bus(70.0, [100], 1)
    bus.roof_size = 50

    assert bus.roof_size == 50
    assert bus.power_draw == [100]
    assert bus.panel.size == 1


def test_bus_change_id():
    bus = Bus(70.0, [100], 1)
    with pytest.raises(PermissionError):
        bus.id = 100


def test_bus_change_power_draw():
    bus = Bus(70.0, [100], 1)

    with pytest.raises(AssertionError):
        bus.power_draw = 100

    with pytest.raises(PermissionError):
        bus.power_draw = [10]

    with pytest.raises(PermissionError):
        bus.power_draw = [-10]


def test_bus_change_panel():
    bus0 = Bus(70.0, None, 1)
    bus1 = Bus(80.0, None, 2)

    with pytest.raises(PermissionError):
        bus0.panel = bus1.panel
