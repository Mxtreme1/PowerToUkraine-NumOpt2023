import casadi as ca
import numpy as np
import math


# define function for energy consumption of every house, where c_max is the maximal energy house i consumes and
# cmin is the minimal energy it consumes(at night or at day)
def create_energy_consumption(c_max_arg, c_min_arg, t_arg):
    if 16 > t_arg >= 0:
        c_func = c_max_arg * (math.sin(2 * math.pi * (1 / 16) * t_arg)) ** 2 + c_min_arg
    elif 16 <= t_arg <= 24:
        c_func = c_min_arg
    else:
        raise ValueError("t is value between 0 and 24")

    return c_func

# define function that returns array of energy consumption of each individual house given time t1
# where the input arguments are a fixed time and the lists of cmax and cmin
def create_array_of_consumption(t1, argcmax, argcmin):
    consumption_at_time_t1_all_houses = []
    for argc_max, argc_min_ in zip(argcmax, argcmin):
        consumption_at_time_t1_all_houses.append(create_energy_consumption(argc_max, argc_min_, t1))
    return consumption_at_time_t1_all_houses

# define function for amount of sunlight we get at given time t
def sun(t_arg):
    s = 0
    if 16 > t_arg >= 0:
        s = 80 * (math.sin((2 * np.pi * (1 / 48) * t_arg - 4 / 5 * math.pi))) ** 4
    elif 16 <= t_arg:
        s = 0
    if s <= 0:
        s = 0

    return s





N = 4
snapshots = np.linspace(0, 24, 1)
num_snaps = range(len(snapshots))     # easy for loops

# create empty optimization problem
opti = ca.Opti()

# define variable(nxn matrix)

xt = []
for t in num_snaps:
    xt.append(opti.variable(N+1, N+1, 'symmetric'))

a = opti.variable(N, 1)

K = 1  # kw/(h*(m^2)) per day realistic
# L = [[0, 5, 5],
#      [5, 0, 99],
#      [5, 99, 0]]
z = 9999999999999
# L = [[0, 5, z, 5, 10],
#      [5, 0, 5, z, z],
#      [z, 5, 0, z, z],
#      [5, z, z, 0, 20],
#      [10, z, z, 20, 0]]
L = [[0, 40, 30, z, 100],
     [40, 0, z, 30, 100],
     [30, z, 0, z, z],
     [z, 30, z, 0, 100],
     [100, 100, z, 100, 0]]
# L = [[0, 5, 5, z, 40],
#      [5, 0, z, 5, 40],
#      [5, z, 0, z, z],
#      [z, 5, z, 0, 5],
#      [40, 40, z, 5, 0]]

# define objective, only sum over elements below and in main diagonal
f = 0
for t in num_snaps:
    for i in range(N):
        for j in range(N):
            if i == j:
                f += a[i] * 0.0001
            else:
                f += 1 / 2 * ((L[j][i] * xt[t][j, i])**2)

# TODO: Fix generator only punished for produced energy not flowing through
for t in num_snaps:
    for i in range(N):
        f += (L[i][N] * xt[t][i, N]) ** 2
    f += 999999999999999 * (xt[t][N, N])

opti.minimize(f)

available_panel_size = 9999

R = [[9999, 9999, 9999],
     [9999, 9999, 9999],
     [9999, 9999, 9999]]
R = [[z, z, z, z, z],
     [z, z, z, z, z],
     [z, z, z, z, z],
     [z, z, z, z, z],
     [z, z, z, z, z]]

c_max = [100, 80]
c_min = [10, 20]
# c_max = [100, 80, 90, 110]
# c_min = [10, 20, 30, 40]

# roof_sizes = [50, 70]
# roof_sizes = [50, 70, 90, 110]
# roof_sizes = [z, z, z, z]
# roof_sizes = [100, 150, 60, 150]
roof_sizes = [500, 750, 300, 750]
# constraint for maximal panel-area we have
area_sum = 0
for i in range(N):
    area_sum += a[i]

# constraint how much area of solar panels, we can distribute in total
opti.subject_to(area_sum <= available_panel_size)

# constraint how energy production of house i is connected to area of solar panels
for t in num_snaps:
    for i in range(N):
        opti.subject_to(xt[t][i, i] == K * a[i])

# constraint how much area of solar panels, we can distribute in total

# constraint that roof area is limited for each house i
for bus_num in range(N):
    opti.subject_to(a[bus_num] <= roof_sizes[bus_num])
    opti.subject_to(0 <= a[bus_num])

# constraint that each individual power line can only transport in one direction(positivity)
for t in num_snaps:
    for i in range(N + 1):
        for j in range(N + 1):
            if i == j:
                continue
            else:
                opti.subject_to(xt[t][i, j] <= R[i][j])
                opti.subject_to(xt[t][i, j] >= -R[i][j])

# constraint for the amount of energy each individual house consumes for N discrete times between
# 0 and 24 hours
ct = []
for t in num_snaps:
    ct.append(create_array_of_consumption(snapshots[t], c_max, c_min))

# ct = [[70, 50, 90, 110]]
ct = [[414, 360, 246, 2542.5], [276, 240, 164, 3559.5], [483, 420, 287, 10678.5], [966, 840, 574, 10768.5],
      [1035, 900, 615, 8136], [828, 720, 492, 6102], [828, 720, 492, 5058], [1104, 960, 656, 3051]]
ct = [[400, 350, 250, 2500]]

Pendt = []
for t in num_snaps:
    Pendt.append([])
    for i in range(N):
        Pendt[t].append([0])
for t in num_snaps:
    for i in range(N):
        for j in range(N+1):
            if i <= j:
                Pendt[t][i] += xt[t][i, j]
            else:
                Pendt[t][i] += -xt[t][i, j]
        opti.subject_to(ct[t][i] == Pendt[t][i])

# constraint for the generator
# constraint for generator
Pendgent = [0] * len(snapshots)
for t in num_snaps:
    for j in range(N):
        Pendgent[t] += xt[t][N, j]
    opti.subject_to(xt[t][N, N] == Pendgent[t])
    # opti.subject_to(xt[t][N, N] == 0)

# define solver
opti.solver('ipopt')  # Use IPOPT as solver

# solve optimization problem
sol = opti.solve()

# read and print solution
xopt = []
for t in num_snaps:
    xopt.append(sol.value(xt[t]))
aopt = sol.value(a)

print("#########################################")
for t in num_snaps:
    print(xopt[t])
    print("#########################################")
print(aopt)

# display(yopt)
# to see some more info
# print(yopt)
print(sol.stats)