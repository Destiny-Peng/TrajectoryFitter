import numpy as np
import pandas as pd
import os  # Import os for path manipulation

# Adjust imports to be relative if main.py is inside src and run as a module
# If main.py is run as a script from the project root, these imports are fine.
# For simplicity, assuming main.py might be run from project root or src.
from simulation import predict_trajectory
from optimization import optimize_drag_coefficient
from plotting import plot_results
# -16.9, 1.0, -0.35
# -10.0, 2.0, -0.35
# -5.8, 3.0, -0.35
# -2.83, 4.0, -0.35


def load_data(filepath):
    """Loads data from a CSV file."""
    # Construct an absolute path to the data file
    # This assumes 'main.py' is in 'src' and 'data' is a sibling of 'src'
    base_dir = os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))  # This gets to project root
    absolute_filepath = os.path.join(base_dir, filepath)

    if not os.path.exists(absolute_filepath):
        print(f"Error: Data file not found at {absolute_filepath}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Base directory calculated: {base_dir}")
        return []
    try:
        data = pd.read_csv(absolute_filepath)
        # Convert angle to radians and ensure target_x, target_y are floats
        return [(np.radians(float(row['angle'])), float(row['target_x']), float(row['target_y']-0.375), float(row['bullet_speed']))
                for index, row in data.iterrows()]
    except Exception as e:
        print(f"Error loading data from {absolute_filepath}: {e}")
        return []


def main():
    # Relative path from the project root directory to the data file
    data_file_relative_path = 'data/measured_data.csv'
    data_points = load_data(data_file_relative_path)

    if not data_points:
        print("No data points loaded. Exiting.")
        return

    print("实测数据点 (角度已转为弧度):")
    for i, dp in enumerate(data_points):
        print(
            f"  {i+1}. Angle (rad): {dp[0]:.4f}, Target X: {dp[1]:.2f}, Target Y: {dp[2]:.2f}, Bullet Speed: {dp[3]}")

    initial_Cd_guess = 0.005  # Initial guess for drag coefficient
    # Define bounds for Cd to prevent unrealistic values
    # Cd should be positive and typically not excessively large
    cd_bounds = [(0.00000, 300.0)]

    print(f"\nStarting optimization with initial Cd guess: {initial_Cd_guess}")
    optimized_Cd = optimize_drag_coefficient(
        initial_Cd_guess, data_points, bounds=cd_bounds)

    if optimized_Cd is not None:
        print(f"\nOptimized drag coefficient (Cd): {optimized_Cd:.8f}")
        plot_results(optimized_Cd, data_points)
    else:
        print("Could not determine an optimized Cd value.")


if __name__ == "__main__":
    # This allows running main.py directly.
    # Ensure your PYTHONPATH includes the project root or run from the project root:
    # Example: From /home/jacy/project/python_test/python-trajectory-project/, run:
    # python src/main.py
    main()
