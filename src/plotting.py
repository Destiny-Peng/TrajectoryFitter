import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from simulation import predict_trajectory  # Use relative import

# Set Matplotlib defaults for Chinese characters
plt.rcParams['font.family'] = 'SimHei'  # Or any other Chinese font you have
# Ensure minus sign displays correctly
plt.rcParams['axes.unicode_minus'] = False


def plot_trajectory(x, y, target_x, target_y, optimized_Cd):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label='Predicted Trajectory', color='blue', lw=2)
    plt.scatter(target_x, target_y, color='red',
                marker='x', s=100, label='Target Point')

    plt.title(f'Trajectory Prediction (Cd = {optimized_Cd:.6f})')
    plt.xlabel('Horizontal Distance (m)')
    plt.ylabel('Height (m)')
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.gca().set_axisbelow(True)
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_error_distribution(error_list):
    plt.figure(figsize=(8, 4))
    plt.hist(error_list, bins=10, color='steelblue', edgecolor='white')
    plt.title('Error Distribution')
    plt.xlabel('Error Distance (m)')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_results(optimized_Cd, data_points):
    plt.figure(figsize=(12, 7))
    colors = plt.cm.viridis(np.linspace(0, 1, len(data_points)))

    error_stats = {
        'max_error': 0,
        'total_squared_error': 0,  # Sum of squared errors for consistency with optimization
        'error_distances': []
    }

    print(f"\nPlotting results with Optimized Cd: {optimized_Cd:.6f}")

    for idx, (theta, target_x, target_y, bullet_speed) in enumerate(data_points):
        sol = predict_trajectory(
            bullet_speed, theta, optimized_Cd, target_x, target_y, t_span_end=1.5)

        # Determine landing time and position
        t_land = sol.t[-1]  # Default to last time point
        if sol.t_events and len(sol.t_events[0]) > 0:
            # Check if event time is reasonable (not too small, within bounds)
            event_time = sol.t_events[0][0]
            # Avoid t=0 or past t_max
            if event_time > 1e-3 and event_time <= sol.t[-1]:
                t_land = event_time

        t_plot = np.linspace(0, t_land, 200)
        trajectory = sol.sol(t_plot)
        pred_x_traj, pred_y_traj = trajectory[0], trajectory[2]

        # Predicted landing point (end of plotted trajectory)
        pred_x, pred_y = pred_x_traj[-1], pred_y_traj[-1]

        # Plot trajectory
        plt.plot(pred_x_traj, pred_y_traj, color=colors[idx], lw=1.5,
                 label=f'发射角 {np.degrees(theta):.1f}°')

        # Mark target point
        plt.scatter(target_x, target_y,
                    color=colors[idx], marker='x', s=100, linewidth=2, label=f'_nolegend_')

        # Mark predicted landing point
        plt.scatter(pred_x, pred_y, color=colors[idx], marker='o',
                    s=50, facecolors='none', label=f'_nolegend_')

        # Calculate error distance
        error_distance = np.sqrt((pred_x - target_x) **
                                 2 + (pred_y - target_y)**2)
        error_stats['error_distances'].append(error_distance)
        # Sum of squared errors
        error_stats['total_squared_error'] += error_distance**2
        error_stats['max_error'] = max(
            error_stats['max_error'], error_distance)

        # Plot error line
        plt.plot([pred_x, target_x], [pred_y, target_y],
                 color=colors[idx], linestyle=':', alpha=0.6)

        print(f"  Angle: {np.degrees(theta):.1f}°, Target: ({target_x:.2f}, {target_y:.2f}), Predicted: ({pred_x:.2f}, {pred_y:.2f}), Error: {error_distance:.3f}m")

    # Chart decorations
    avg_error = np.mean(
        error_stats['error_distances']) if error_stats['error_distances'] else 0
    plt.title(f'弹道拟合与实测数据对比 (优化后 Cd = {optimized_Cd:.6f})\n'
              f'平均落点误差: {avg_error:.3f}m | 最大落点误差: {error_stats["max_error"]:.3f}m')
    plt.xlabel('水平距离 (m)')
    plt.ylabel('高度 (m)')
    plt.axhline(0, color='black', linewidth=0.5)  # Ground line
    plt.axvline(0, color='black', linewidth=0.5)  # Origin line
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.gca().set_axisbelow(True)
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
    plt.legend(title="参数", bbox_to_anchor=(1.05, 1), loc='upper left')
    # Important for correct visual representation of trajectories
    plt.axis('equal')
    # Adjust layout to make space for legend
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # Error distribution histogram
    if error_stats['error_distances']:
        plt.figure(figsize=(8, 4))
        plt.hist(error_stats['error_distances'], bins=max(
            5, len(data_points)//2), color='steelblue', edgecolor='white')
        plt.title('落点误差分布')
        plt.xlabel('误差距离 (m)')
        plt.ylabel('频次')
        plt.grid(axis='y', alpha=0.7)
        plt.tight_layout()

    plt.show()
