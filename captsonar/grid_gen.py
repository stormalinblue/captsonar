import numpy as np


def get_grid(generator, size=15):
    return generator.binomial(1, 0.05, size=(size, size))


def get_generator(seed=0):
    return np.random.default_rng(seed)
