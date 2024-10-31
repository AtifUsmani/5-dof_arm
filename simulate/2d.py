import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from sympy import symbols, Eq, solve

# Initialize figure
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)
ax.set_xlim([-2, 30])  # Increase x-axis limit
ax.set_ylim([-2, 15])  # Adjust y-axis limit
ax.set_aspect('equal')
plt.grid()
plt.plot([-2, 30], [0, 0], 'k-')  # Ground

# Robot parameters
link1 = 12  # Length of link 1
link2 = 12  # Length of link 2

# Initial angles
theta1 = 0
theta2 = 0
theta3 = 0

# Create sliders
ax_theta1 = plt.axes([0.1, 0.1, 0.65, 0.03])
ax_theta2 = plt.axes([0.1, 0.15, 0.65, 0.03])
ax_theta3 = plt.axes([0.1, 0.2, 0.65, 0.03])

s_theta1 = Slider(ax_theta1, 'Theta 1', -180, 180, valinit=theta1)
s_theta2 = Slider(ax_theta2, 'Theta 2', -180, 180, valinit=theta2)
s_theta3 = Slider(ax_theta3, 'Theta 3', -180, 180, valinit=theta3)

def update(val):
    ax.cla()  # Clear the axes
    ax.set_xlim([-2, 30])  # Increase x-axis limit
    ax.set_ylim([-2, 15])  # Adjust y-axis limit
    ax.set_aspect('equal')
    plt.grid()
    plt.plot([-2, 30], [0, 0], 'k-')  # Ground

    # Get angles from sliders
    theta1 = s_theta1.val
    theta2 = s_theta2.val
    theta3 = s_theta3.val

    # First link
    x1 = link1 * np.cos(np.radians(theta1))
    y1 = link1 * np.sin(np.radians(theta1))
    ax.plot(0, 0, 'bo', markersize=10)
    ax.plot([0, x1], [0, y1], 'b-', linewidth=3)

    # Second link
    x2 = x1 + link2 * np.cos(np.radians(theta1 + theta2))
    y2 = y1 + link2 * np.sin(np.radians(theta1 + theta2))
    ax.plot(x1, y1, 'go', markersize=10)
    ax.plot([x1, x2], [y1, y2], 'g-', linewidth=3)

    # End-effector (gripper)
    x3 = x2 + 0.001 * np.cos(np.radians(theta1 + theta2 + theta3))
    y3 = y2 + 0.001 * np.sin(np.radians(theta1 + theta2 + theta3))
    ax.plot(x3, y3, 'r.', markersize=20)

    # Calculate the intersection for collision detection
    m1 = (y3 - y2) / (x3 - x2) if x3 != x2 else float('inf')
    m2 = -1 / m1 if m1 != 0 else float('inf')
    c = y2 - (m2 * x2)
    x, y = symbols('x y')

    # Define the equations
    func1 = Eq(y, m2 * x + c)
    func2 = Eq((x - x2)**2 + (y - y3)**2, 0.3**2)

    # Solve for intersections
    solutions = solve((func1, func2), (x, y))

    # Plot collision lines or points
    if len(solutions) == 1:
        ax.plot([x2, x2], [y2 - 0.3, y2 + 0.3], 'r-', linewidth=3)
        ax.plot([x2, x2 + 0.1], [y2 + 0.3, y2 + 0.3], 'r-', linewidth=3)
        ax.plot([x2, x2 + 0.1], [y2 - 0.3, y2 - 0.3], 'r-', linewidth=3)
    else:
        for sol in solutions:
            ax.plot([sol[0], sol[0] + 300 * (x3 - x2)],
                    [sol[1], sol[1] + 300 * (y3 - y2)], 'r-', linewidth=3)

    plt.draw()

# Connect sliders to the update function
s_theta1.on_changed(update)
s_theta2.on_changed(update)
s_theta3.on_changed(update)

# Show initial plot
update(None)  # Call update to initialize the plot
plt.show()