import unittest
from calculations import plotfunc
import numpy as np


class CalculationsTest(unittest.TestCase):
    def test_something(self):
        self.assertRaises(AssertionError, plotfunc, "x**2", start=6, end=1)
        self.assertRaises(TypeError, plotfunc)

        returnvalue = plotfunc("x**2", plot=False, start=0, end=2, points=3)
        self.assertTrue((np.array([0, 1, 2]) == returnvalue[0]).all())
        self.assertTrue((np.array([0, 1, 4]) == returnvalue[1]).all())

        returnvalue = plotfunc(lambda x: x**2, plot=False, start=0, end=2, points=3)
        self.assertTrue((np.array([0, 1, 2]) == returnvalue[0]).all())
        self.assertTrue((np.array([0, 1, 4]) == returnvalue[1]).all())
