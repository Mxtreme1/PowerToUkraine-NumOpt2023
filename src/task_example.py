import casadi as ca
import numpy as np

N = 2
# create empty optimization problem
opti = ca.Opti()

# define variable(nxn matrix)
x = opti.variable(N, N)

ph = 1
# Length of House i to House j
L = [[0, 5],
     [5, 0]]
A = [100, 70]
c = [50, 100]
Amax = 200  # maximum area of sonal panels we can distribute
# maximal energy House i can make with all of the roof area having solar panels
Pmax = []
for i in range(N):
    Pmax.append(A[i] * ph)

R = [[Pmax[0], 100],
     [100, Pmax[1]]]

# ph=0,3653 #kw/(h*(m^2)) per day realistic


# define objective
f = 0
for i in range(N):
    for j in range(N):
        f += L[i][j] * x[i, j]

# hand objective to casadi, no minimization done yet
opti.minimize(f)
print(x)

# define constraints. To include several constraints, just call this
# function several times


# the energy house i has available (after subtracting the losses to other houses)

Pend = []
for i in range(N):
    Pend_m = 0
    for j in range(N):
        Pend_m += x[i, j] - x[j, i]
    Pend.append(Pend_m + x[i, i])

print(Pend)

# energy consumption of house i per day in Kw/h,
# note: House 5 is generator
# 14 kw/h is average energy consumption of a >3 person household


# constraint house i needs a minimum of c_i energy
for i in range(N):
    opti.subject_to(c[i] <= Pend[i])

# constraint house i can produce wiht maximal solar panels built
# and constraint on how much one cable can transport
# therefore we have a NxN matrix, where on the main diagonal, we have what one house can maximaly produce based in the area
# of the house roof which is P_max=A*ph


# roof area House i, average: 100m^2


for i in range(N):
    for j in range(N):
        opti.subject_to(x[i, j] <= R[i][j])

print(Pmax)
# constraint that sum of energy production is limited by the total amount of solar panels we can built
# were P_p stands for produced energy


P = ph * Amax  # maximum power we can produce based on the amount of solar panels we have
P_p = 0
for i in range(N):
    P_p += x[i, i]

opti.subject_to(P_p <= P)

for i in range(N):
    for j in range(N):
        opti.subject_to(x[i, j] >= 0)

# define solver
opti.solver('ipopt')  # Use IPOPT as solver

# solve optimization problem
sol = opti.solve()

# read and print solution
xopt = sol.value(x)
# yopt=opti.debug.value(x)
# display(yopt)
# to see some more info
print(xopt)
print(sol.stats)