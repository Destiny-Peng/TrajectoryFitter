import numpy as np
from scipy.integrate import solve_ivp


def f(t, y, Cd):
    """
    Differential equations for the trajectory.
    y[0] = x (horizontal position)
    y[1] = vx (horizontal velocity)
    y[2] = y (vertical position)
    y[3] = vy (vertical velocity)
    Cd = drag coefficient
    """
    v = np.sqrt(y[1]**2 + y[3]**2)
    # Avoid division by zero if velocity is zero

    # Drag force components
    # Simplified drag model, proportional to v
    drag_force_x = -Cd * v * y[1]
    # Simplified drag model, proportional to v
    drag_force_y = -Cd * v * v * y[3]
    ax = drag_force_x
    ay = drag_force_y - 9.8  # Gravity

    dydt = [y[1], ax, y[3], ay]
    # print(
    # f"t={t:.4f}, x={y[0]:.4f}, y={y[2]:.4f}, vx={y[1]:.4f}, vy={y[3]:.4f}, ax={ax:.4f}, ay={ay:.4f}")
    return dydt


def event_cross_x_level(t, y, Cd_param, x_level):
    """
    Event function to stop when projectile's height y[2] crosses a specified x_level.
    Cd_param is passed by solve_ivp from 'args' but not used in this event's logic.
    """
    # print(y[0] - x_level)
    return y[0] - x_level


def predict_trajectory(initial_velocity, theta, Cd, target_x=None, target_y=None, t_span_end=5.0):
    """
    Predicts the trajectory of a projectile.
    The event will trigger when y[2] (height) crosses the provided target_y.
    """
    yinit = [0., initial_velocity * np.cos(theta),    # x0, vx0
             0, initial_velocity * np.sin(theta)]    # y0, vy0

    current_event_handler = None
    if target_x is not None:
        # Event: stop when y[2] reaches target_y
        # The lambda captures target_y from the outer scope.
        # Cd (as cd_val_from_args) is passed by solve_ivp due to 'args=(Cd,)'
        def current_event_handler(t_sol, y_sol, cd_val_from_args): return \
            event_cross_x_level(t_sol, y_sol, cd_val_from_args, target_x)
        # print(target_y)
        current_event_handler.terminal = True
        # Trigger when y[2] - target_y becomes non-positive (i.e., y[2] crosses target_y from above)
        current_event_handler.direction = 0
    # If target_y is None, no height-based event is set, simulation runs until t_span_end.

    sol = solve_ivp(
        f,
        [0, t_span_end],
        yinit,
        # This Cd will be passed as an argument to f and to current_event_handler
        args=(Cd,),
        events=current_event_handler,  # Can be None if target_y is not provided
        method='DOP853',  # Run
        dense_output=True,
        rtol=1e-9, atol=1e-9, max_step=0.001
    )
    return sol


def calculate_final_position(sol):
    if sol.t_events[0].size > 0:
        t_event = sol.t_events[0][0]
        final_x, final_y = sol.sol(t_event)[0], sol.sol(t_event)[2]
    else:
        final_x, final_y = sol.y[0][-1], sol.y[2][-1]
    return final_x, final_y


def calculate_error(pred_x, pred_y, target_x, target_y):
    return np.sqrt((pred_x - target_x)**2 + (pred_y - target_y)**2)
