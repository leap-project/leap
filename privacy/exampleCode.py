import numpy as np
import dp_techniques as dps


#Privacy parameters
epsilon = 0.5
delta = 0

# Example for privatizing simple counts 
orig_count = 20
privatized_count = dps.dp_count(orig_count, epsilon, delta)
print("Original count: %d, Privatized count: %d, Epsilon: %f" % (orig_count, privatized_count, epsilon))

# Example for privatizing more sensitive counts
orig_count = 20
count_sensitivity=5 # how much can a record change the record
privatized_count = dps.dp_sensitive_count(count_sensitivity, orig_count, epsilon, delta)
print("Original count: %d with sensitivity: %d, Privatized count: %d, Epsilon: %f" % (orig_count,count_sensitivity, privatized_count, epsilon))

# # Example for privatizing means
data_vec = np.random.rand(10) # values in the range 0,1
data_max = 1
data_min = 0
n = len(data_vec)
avg = np.mean(data_vec)
privatized_mean = dps.dp_mean(data_min, data_max, n, avg, epsilon, delta)
print("Original data: %s, Privatized mean: %f, Epsilon: %f" % (str(data_vec), privatized_mean, epsilon))

#Example for privatizing variance

data_vec = np.random.rand(10) # values in the range 0,1
data_max = 1.0
data_min = 0.0
n = len(data_vec)
avg = np.mean(data_vec)
var = (1.0/n) * sum((value - avg) ** 2 for value in data_vec)

privatized_var = dps.dp_variance(data_min,data_max,n, var,epsilon, delta)
print("Original data: %s , Privatized variance: %f, Epsilon: %f" % (str(data_vec), privatized_var, epsilon))

# Example for privatizing median
data_vec = np.random.rand(10) # values in the range 0,1
data_max = 1.0
data_min = 0.0




# Example for privatizing median


#Example for privatizing linear regression







