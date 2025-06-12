# Python Trajectory Optimization Project

This project implements a trajectory optimization and visualization system for projectile motion. It includes functionalities for simulating projectile trajectories, optimizing parameters based on measured data, and visualizing the results.

## Project Structure

```
TrajectoryFitter
├── src
│   ├── __init__.py          # Marks the src directory as a Python package
│   ├── simulation.py        # Contains functions for simulating projectile motion
│   ├── optimization.py       # Implements optimization algorithms for trajectory parameters
│   ├── plotting.py          # Responsible for visualization of trajectories and error statistics
│   └── main.py              # Entry point of the program, orchestrates data loading, optimization, and visualization
├── data
│   └── measured_data.csv    # Contains measured data for optimization (angle, target distance, target height)
├── tests
│   ├── __init__.py          # Marks the tests directory as a Python package
│   ├── test_simulation.py    # Unit tests for functions in simulation.py
│   └── test_optimization.py   # Unit tests for functions in optimization.py
├── requirements.txt         # Lists required Python libraries and their versions
└── README.md                # Documentation for the project
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd TrajectoryFitter
pip install -r requirements.txt
```

## Usage

1. Place your measured data in the `data/measured_data.csv` file. The data should include the launch angle, target horizontal distance, and target height.
2. Run the main program:

```bash
python src/main.py
```

3. The program will optimize the drag coefficient based on the measured data, simulate the projectile motion, and generate visualizations of the results.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.