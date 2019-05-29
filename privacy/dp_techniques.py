import numpy as np


def dp_count(count, epsilon=1.0, delta=0.1):

		"""
		This function provides a differentially-private estimate of a count. Here each user's record affects by 1

		Input:

			count = The value of count that needs to be privatized based on an epsilon.
			epsilon = privacy parameter, default 1.0
			delta = privacy parameter, default 0.1

		Output:

			Privatized count

		"""
		COUNT_SENSITIVITY = 1  # Global sensitivity of a simple count query
		
		if delta == 0:
			noise = np.random.laplace(loc = 0, scale = COUNT_SENSITIVITY/float(epsilon), size = (1,1))
		else:    
			sigma = (COUNT_SENSITIVITY/(epsilon))*np.sqrt(2*np.log(1.25/delta))
			noise = np.random.normal(0.0, sigma, 1)

		count += noise

		return int(count)

def dp_sensitive_count(sensitivity, count, epsilon=1.0, delta=0.1):

		"""
		This function provides a differentially-private estimate of a count where the effect of one user's data is greater than one on the count.

		Input:

			sensitivity = The max amount by which one user's data can change the count. 
			count = The value of count that needs to be privatized based on an epsilon.
			epsilon = privacy parameter, default 1.0
			delta = privacy parameter, default 0.1

		Output:
			Privatized count
		"""
		COUNT_SENSITIVITY = sensitivity
		if delta == 0:
			noise = np.random.laplace(loc = 0, scale = COUNT_SENSITIVITY/float(epsilon), size = (1,1))
		else:    
			sigma = (COUNT_SENSITIVITY/(epsilon))*np.sqrt(2*np.log(1.25/delta))
			noise = np.random.normal(0.0, sigma, 1)

		count += noise

		return int(count)

def dp_mean(mean_min, mean_max,num_samples, mean, epsilon=1.0, delta=0.1):

	"""
		This function provides a differentially-private estimate of the mean of a vector.

		Input:

			mean = Mean to be privatized
			sensitivity = Max of the range of values used to compute the mean 
			num_samples = number if samples used to calculate the mean
			epsilon = privacy parameter, default 1.0
			delta = privacy parameter, default 0.1

		Output:

			a scalar.

	 """
	n = num_samples
	f = mean
	MEAN_SENSITIVITY = (mean_max - mean_min)/n

	if delta == 0:
			noise = np.random.laplace(loc = 0, scale = MEAN_SENSITIVITY/float(epsilon), size = (1,1))
	else:      
			sigma = (MEAN_SENSITIVITY/(epsilon))*np.sqrt(2*np.log(1.25/delta))
			noise = np.random.normal(0.0, sigma, 1)

	f += noise
	return f

def dp_variance(var_min, var_max,  num_samples, variance, epsilon=1.0, delta=0.1):

	"""
		This function provides a differentially-private estimate of the mean of a vector.

		Input:

			var = Variance to be privatized
			var_max = Max of the range of values used to compute variance 
			var_min = Min of the range of values used to compute the variance

			num_samples = number if samples used to calculate the mean
			epsilon = privacy parameter, default 1.0
			delta = privacy parameter, default 0.1

		Output:

			a scalar.

	 """
	f = variance
	n = num_samples   

	VAR_SENSITIVITY = ((var_max - var_min)**2)/n

	if delta == 0:
			noise = np.random.laplace(loc = 0, scale = VAR_SENSITIVITY/float(epsilon), size = (1,1))
	else:      
			sigma = (VAR_SENSITIVITY/(epsilon))*np.sqrt(2*np.log(1.25/delta))
			noise = np.random.normal(0.0, sigma, 1)

	f += noise

	return f










