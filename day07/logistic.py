import numpy as np
import math

K = 10000
P0 = 1000
r = 0.2

def logistic_function(t):
    exp_r = np.exp(r *t)
    return K * P0 *exp_r / (K + P0 * (exp_r-1))

t1 = np.array([1,2,3])
p1 = logistic_function(t1)
print(p1)