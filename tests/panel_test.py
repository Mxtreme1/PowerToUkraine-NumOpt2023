from src.bus import Bus

import pytest


def test_panel_sanity():
    bus = Bus(70, None, 1)
    panel = bus.panel

    # assert panel.id == 0
    assert panel.bus == bus
    assert panel.size == 1


def test_panel_change_id():
    bus = Bus(70, None, 1)
    panel = bus.panel

    with pytest.raises(PermissionError):
        panel.id = 100


def test_panel_change_size():
    bus = Bus(70, None, 1)
    panel = bus.panel

    panel.size = 20.1

    # assert panel.id == 
    assert panel.bus == bus
    assert panel.size == 20.1

    panel.size = 20

    # assert panel.id == 0
    assert panel.bus == bus
    assert panel.size == 20
    assert panel.size == 20.0


def test_panel_change_bus():
    bus0 = Bus(70, None, 1)
    panel0 = bus0.panel

    bus1 = Bus(50, None, 2)

    with pytest.raises(PermissionError):
        panel0.bus = bus1
