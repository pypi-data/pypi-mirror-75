import numpy as np


class Benchmark:

    def __init__(self):
        """
        implements the definition of benchmark functions to optimize in 2D space
        """
        pass

    def salustowicz(x):  # [0, 10]
        return np.exp(-x[0]) * x[0] ** 3 * np.cos(x[0]) * np.sin(x[0]) \
               * (np.cos(x[0]) * np.sin(x[0]) ** 2 - 1) * (x[1] - 5)

    def x2(x):  # no range
        return x[0] ** 2 + x[1] ** 2

    def ackley(x):  # [-15, 30]
        part_1 = -0.2 * np.sqrt(0.5 * (x[0] * x[0] + x[1] * x[1]))
        part_2 = 0.5 * (np.cos(2 * np.pi * x[0]) + np.cos(2 * np.pi * x[1]))
        return np.exp(1) + 20 - 20 * np.exp(part_1) - np.exp(part_2)
