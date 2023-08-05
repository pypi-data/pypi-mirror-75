from parallelsdk.client import ParallelClient
from parallelsdk.mp_toolbox.mp_toolbox import *

mip = MPModel('mip_example')

### Variables ###
inf = Infinity()
x = mip.IntVar(0.0, inf, 'x')
y = mip.IntVar(0.0, inf, 'y')

### Constraints ###
c1 = mip.Constraint(x + 7*y <= 17.5)
print(c1)

# x <= 3.5
c2 = mip.Constraint(x <= 3.5)

### Objective ###
mip.Maximize(x + 10*y)

optimizer = ParallelClient('3.19.30.245')
optimizer.connect()

optimizer.run_optimizer(mip)

# Get solution and print the value of the variable
# after the model is solved.
# @note status of the model can be explored with "get_model_status":
# mip.get_model_status()
print(x)
print(y)

# The solution can be locked-down on each variable
x.lock_solution_value()
print(x)

# Print the objective value
mip.get_objective_value()

# Close the connection with the server
optimizer.disconnect()
