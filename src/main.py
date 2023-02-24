from src.bus import Bus
from src.line import Line
from src.line_type import LineType
from src.grid import Grid

if __name__ == '__main__':
    """
    
    This is the large neighbourhood example, other examples can be found in the test files:
    - optimisation_task_test.py
    - complex_example_test.py
    They can be run as unittests, their results should be printed to console.
    
    """
    
    # Create buses, each one represents a building or part of one
    bus1 = Bus(105, [470, 1510, 1250, 1660], 0)
    bus2 = Bus(100, [1950, 5460, 4800, 3000], 0)
    bus3 = Bus(50, [1200, 3360, 2960, 1850], 0)
    bus4 = Bus(40, [200, 650, 550, 700], 0)
    bus5 = Bus(75, [200, 700, 600, 750], 0)
    bus6 = Bus(100, [4150, 9200, 5500, 2500], 0)
    bus7 = Bus(500, [7650, 29100, 26000, 13800], 0)
    bus8 = Bus(150, [130, 450, 360, 480], 0)
    bus9 = Bus(400, [200, 650, 540, 720], 0)
    bus10 = Bus(200, [2260, 11050, 4270, 6530], 0)
    bus11 = Bus(90, [160, 510, 420, 560], 0)
    bus12 = Bus(115, [170, 550, 460, 610], 0)
    bus13 = Bus(80, [130, 420, 350, 460], 0)
    bus14 = Bus(135, [180, 600, 490, 660], 0)
    bus15 = Bus(180, [220, 710, 590, 780], 0)
    bus16 = Bus(90, [140, 460, 380, 510], 0)
    bus17 = Bus(100, [140, 450, 370, 500], 0)
    bus18 = Bus(110, [190, 610, 500, 670], 0)
    bus19 = Bus(100, [170, 540, 440, 590], 0)
    bus20 = Bus(140, [150, 480, 400, 530], 0)
    generator = Bus(0, None, 0)

    buses = [bus1, bus2, bus3, bus4, bus5, bus6, bus7, bus8, bus9, bus10, bus11, bus12, bus13, bus14, bus15, bus16,
             bus17, bus18, bus19, bus20, generator]

    type_a = LineType("TypeA", 20000)
    type_b = LineType("TypeB", 10000)

    line1_2 = Line(bus1, bus2, 30, type_a)
    line1_5 = Line(bus1, bus5, 30, type_a)
    line1_8 = Line(bus1, bus8, 30, type_a)
    line1_g = Line(bus1, generator, 10, type_a)
    line2_3 = Line(bus2, bus3, 15, type_a)
    line2_g = Line(bus2, generator, 15, type_a)
    line3_4 = Line(bus3, bus4, 10, type_a)
    line3_g = Line(bus3, generator, 20, type_a)
    line4_6 = Line(bus4, bus6, 10, type_a)
    line4_g = Line(bus4, generator, 20, type_a)
    line5_6 = Line(bus5, bus6, 20, type_a)
    line5_7 = Line(bus5, bus7, 10, type_a)
    line5_g = Line(bus5, generator, 10, type_a)
    line6_11 = Line(bus6, bus11, 50, type_a)
    line7_8 = Line(bus7, bus8, 10, type_a)
    line8_9 = Line(bus8, bus9, 40, type_a)
    line9_10 = Line(bus9, bus10, 300, type_b)
    line11_12 = Line(bus11, bus12, 20, type_a)
    line11_13 = Line(bus11, bus13, 10, type_a)
    line12_14 = Line(bus12, bus14, 20, type_a)
    line13_15 = Line(bus13, bus15, 30, type_a)
    line14_17 = Line(bus14, bus17, 30, type_a)
    line15_18 = Line(bus15, bus18, 50, type_b)
    line16_17 = Line(bus16, bus17, 20, type_b)
    line17_19 = Line(bus17, bus19, 20, type_b)
    line18_20 = Line(bus18, bus20, 20, type_b)
    line19_20 = Line(bus19, bus20, 30, type_b)

    lines = [line1_2, line1_5, line1_8, line1_g, line2_3, line2_g, line3_4, line3_g, line4_6, line4_g, line5_6,
             line5_7, line5_g, line6_11, line7_8, line8_9, line9_10, line11_12, line11_13, line12_14, line13_15,
             line14_17, line15_18, line16_17, line17_19, line18_20, line19_20]

    snapshots = [3.5, 9.5, 15.5, 21]  # 3:30 am, 9:30 am 3:30 pm, 9 pm
    total_panel_size = 210  # Available square meters of panels

    grid = Grid(buses, lines, generator, snapshots, total_panel_size)

    grid.create_optimisation_task()
    grid.optimise()
