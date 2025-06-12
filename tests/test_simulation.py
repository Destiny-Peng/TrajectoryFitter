import unittest
import numpy as np
from src.simulation import f, calculate_trajectory

class TestSimulation(unittest.TestCase):

    def test_trajectory_calculation(self):
        theta = np.radians(45)  # 45 degrees
        Cd = 0.5  # Example drag coefficient
        initial_velocity = 15.0
        t_end = 2.0  # Time duration for the simulation

        # Calculate trajectory
        trajectory = calculate_trajectory(theta, Cd, initial_velocity, t_end)

        # Check if the trajectory has the expected shape
        self.assertEqual(trajectory.shape, (4, 100))  # Expecting (x, vx, y, vy) over time

    def test_motion_equation(self):
        y = np.array([0, 10, 0, 10])  # Initial state: [x, vx, y, vy]
        Cd = 0.5
        t = 0.1  # Time step

        # Calculate the derivatives
        dydt = f(t, y, Cd)

        # Check if the output has the expected shape
        self.assertEqual(len(dydt), 4)  # Should return [dx, dvx, dy, dvy]

        # Check if the values are numeric
        for value in dydt:
            self.assertIsInstance(value, (int, float))

if __name__ == '__main__':
    unittest.main()