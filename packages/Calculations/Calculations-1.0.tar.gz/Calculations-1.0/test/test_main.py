import unittest
from calculations import plottaren
import numpy as np


class CalculationsTest(unittest.TestCase):
    def test_something(self):
        self.assertRaises(AssertionError, plottaren, "x**2", start=6, slut=1)
        self.assertRaises(TypeError, plottaren)

        returnvalue = plottaren("x**2", plot=False, start=0, slut=2, noggrannhet=3)
        self.assertTrue((np.array([0, 1, 2]) == returnvalue[0]).all())
        self.assertTrue((np.array([0, 1, 4]) == returnvalue[1]).all())

        returnvalue = plottaren(lambda x: x**2, plot=False, start=0, slut=2, noggrannhet=3)
        self.assertTrue((np.array([0, 1, 2]) == returnvalue[0]).all())
        self.assertTrue((np.array([0, 1, 4]) == returnvalue[1]).all())
