import numpy as np
from scipy.optimize import minimize
from simulation import predict_trajectory  # Use relative import


def calculate_error(theta, target_x, target_y, bullet_speed, Cd):
    """
    Calculates the squared error between the predicted and target landing points.
    """
    sol = predict_trajectory(bullet_speed, theta,
                             Cd, target_x, target_y, t_span_end=5.0)

    if sol.t_events and len(sol.t_events[0]) > 0:
        t_event = sol.t_events[0][0]
        # Ensure t_event is within the solution's time domain
        if t_event > sol.t[-1]:
            t_event = sol.t[-1]
        elif t_event < sol.t[0]:  # Should not happen with proper t_span
            t_event = sol.t[0]

        final_pos = sol.sol(t_event)
        final_x, final_y = final_pos[0], final_pos[2]

    else:  # No event triggered, use the last point of the trajectory
        final_x, final_y = sol.y[0, -1], sol.y[2, -1]
    # print(
    #     f"Final position for theta={np.degrees(theta):.2f}°: x={final_x:.2f}, y={final_y:.2f},vx={sol.y[1, -1]:.2f}, vy={sol.y[3, -1]:.2f}")
    error = (final_y - target_y)**2
    return error


def objective_function(Cd, data_points):
    """
    Objective function to minimize (total error).
    Cd is a single value, not an array, so access Cd directly.
    """
    total_error = 0.0
    current_Cd = Cd if isinstance(
        Cd, (int, float)) else Cd[0]  # Ensure Cd is a scalar

    for theta, target_x, target_y, bullet_speed in data_points:
        total_error += calculate_error(theta, target_x,
                                       target_y, bullet_speed, current_Cd)
    return total_error


def optimize_drag_coefficient(initial_Cd, data_points, bounds=[(0.01, 5.0)]):
    """
    Optimizes the drag coefficient using the provided data points.
    """
    result = minimize(
        objective_function,
        initial_Cd,
        args=(data_points,),
        method='L-BFGS-B',  # A common method for bound-constrained optimization
        bounds=bounds,
        # Add options for convergence
        options={'ftol': 1e-9, 'gtol': 1e-9, 'maxiter': 2000}
    )

    if result.success:
        optimized_Cd = result.x if isinstance(
            result.x, (int, float)) else result.x[0]
        print(f"Optimization successful. Final error: {result.fun:.6f}")
        return optimized_Cd
    else:
        print("Optimization failed:", result.message)
        # Return initial_Cd or handle failure appropriately
        return initial_Cd if isinstance(initial_Cd, (int, float)) else initial_Cd[0]
