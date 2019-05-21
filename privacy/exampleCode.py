import numpy as np
import dp_techniques as dps


#Privacy parameters
epsilon = 0.1
delta = 0

# Example for privatizing counting
orig_count = 20
privatized_count = dps.dp_count(orig_count, epsilon, delta)
print("Original count: %d, Privatized count: %d, Epsilon: %f" % (orig_count, privatized_count, epsilon))