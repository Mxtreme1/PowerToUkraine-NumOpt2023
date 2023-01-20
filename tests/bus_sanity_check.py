from src.bus import *


if __name__ == '__main__':
    b = Bus(70.0, None, 1)
    print(b.roof_size)
    print(b.panel.size)
    print(b.power_draw)
    b.roof_size = 60
    b.built_panel_size = 0
    b.power_draw = None
    print(b.roof_size)
    print(b.panel.size)
    print(b.power_draw)
