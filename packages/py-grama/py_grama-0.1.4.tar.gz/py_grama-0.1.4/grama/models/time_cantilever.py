## Function timing machinery
import timeit
import numpy as np
from numpy import sqrt, array, Inf

LENGTH = 100
D_MAX  = 2.2535

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def function_area(x):
    w, t = x
    return w * t

def function_stress(x):
    w, t, H, V, E, Y = x
    return Y - 600 * V / w / t**2 - 600 * H / w**2 / t

def function_displacement(x):
    w, t, H, V, E, Y = x
    return D_MAX - np.float64(4) * LENGTH**3 / E / w / t * sqrt(
        V**2 / t**4 + H**2 / w**4
    )

wr_area         = wrapper(function_area, [1] * 2)
wr_stress       = wrapper(function_stress, [1] * 6)
wr_displacement = wrapper(function_displacement, [1] * 6)

num = int(1e6)
total_area         = timeit.timeit(wr_area, number=num)
total_stress       = timeit.timeit(wr_stress, number=num)
total_displacement = timeit.timeit(wr_displacement, number=num)

print("time_area         = {}".format(total_area / num))
print("time_stress       = {}".format(total_stress / num))
print("time_displacement = {}".format(total_displacement / num))
