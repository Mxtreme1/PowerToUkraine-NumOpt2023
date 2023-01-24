from src.bus import *

import pytest


def test_bus_sanity():
    bus = Bus(70.0, None, 1)
    assert bus.roof_size == 70
    assert bus.power_draw is None
    assert bus.panel.size == 1
    # assert bus.id == 0


def test_bus_change_roof_size():
    bus = Bus(70.0, None, 1)
    bus.roof_size = 50

    assert bus.roof_size == 50
    assert bus.power_draw is None
    assert bus.panel.size == 1
    # assert bus.id == 1


def test_bus_change_id():
    bus = Bus(70.0, None, 1)
    with pytest.raises(PermissionError):
        bus.id = 1


def test_bus_change_panel():
    bus0 = Bus(70.0, None, 1)
    bus1 = Bus(80.0, None, 2)

    with pytest.raises(PermissionError):
        bus0.panel = bus1.panel
