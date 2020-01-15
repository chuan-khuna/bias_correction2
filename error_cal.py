import numpy as np


def mae(a, b):
    return np.mean(np.abs(np.array(a) - np.array(b)))


def mse(a, b):
    return np.mean((np.array(a) - np.array(b))**2)


def rmse(a, b):
    return np.sqrt(np.mean((np.array(a) - np.array(b))**2))
