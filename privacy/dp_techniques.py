import numpy as np

def dp_count(count, epsilon=1.0, delta=0.1):

    """
    This function provides a differentially-private estimate of a count.

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