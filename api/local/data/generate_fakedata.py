import numpy as np
import pdb

n = 500
d = 100
y = 1
data = np.random.rand(n,d+y)
np.save("randdata.npy", data)

