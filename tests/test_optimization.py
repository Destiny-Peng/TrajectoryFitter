import unittest
import numpy as np
from src.optimization import objective_function

class TestOptimization(unittest.TestCase):

    def setUp(self):
        self.data_points = [
            (np.radians(-16.9), 1.0, -0.35),
            (np.radians(-10.0), 2.0, -0.35),
            (np.radians(-5.8), 3.0, -0.35),
            (np.radians(-2.83), 4.0, -0.35),
            (np.radians(-0.38), 5.0, -0.35),
        ]
        self.initial_Cd = 2.0

    def test_objective_function(self):
        error = objective_function(self.initial_Cd, self.data_points)
        self.assertIsInstance(error, float)
        self.assertGreaterEqual(error, 0)

    def test_optimization_with_different_Cd(self):
        Cd_values = [1.0, 2.0, 3.0, 4.0, 5.0]
        for Cd in Cd_values:
            error = objective_function(Cd, self.data_points)
            self.assertIsInstance(error, float)

if __name__ == '__main__':
    unittest.main()