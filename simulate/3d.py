import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

# Define the lengths of the arm segments
L1 = 120.0  # Length of the first segment
L2 = 120.0  # Length of the second segment

# Initial angles in degrees (remapped to achieve 90 degrees position at 0)
theta1_init = 0  # Joint angle 1 (rotation around x-axis)
theta2_init = 0  # Joint angle 2 (rotation around x-axis)

# Convert degrees to radians
def deg_to_rad(degrees):
    return np.deg2rad(degrees)

# Function to update the plot
def update_plot(theta1, theta2):
    ax.cla()
    
    # Calculate the positions of the arm segments
    x0, y0, z0 = 0, 0, 0  # Base position

    # Joint 1 (rotation around the x-axis)
    theta1_rad = deg_to_rad(theta1 - 90)  # Offset by -90 degrees
    x1 = x0  # x remains the same
    y1 = y0 + L1 * np.sin(theta1_rad)  # Adjust y based on theta1
    z1 = z0 + L1 * np.cos(theta1_rad)  # Adjust z based on theta1

    # Joint 2 (also rotating around the x-axis)
    theta2_rad = deg_to_rad(theta2 - 90)  # Offset by -90 degrees
    # The end effector position
    x2 = x1  # x remains the same for joint 2
    y2 = y1 + L2 * np.sin(theta2_rad)  # Adjust y based on theta2
    z2 = z1 + L2 * np.cos(theta2_rad)  # Adjust z based on theta2

    # Plot the segments with colors
    ax.plot([x0, x1], [y0, y1], [z0, z1], marker='o', color='blue', label='Segment 1')
    ax.plot([x1, x2], [y1, y2], [z1, z2], marker='o', color='green', label='Segment 2')

    # Set labels and title
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('2DOF Robotic Arm Visualization in 3D')
    ax.set_xlim([-240, 240])
    ax.set_ylim([-240, 240])
    ax.set_zlim([-120, 240])
    ax.legend()
    
    # Add grid
    ax.grid(True)
    
    plt.draw()

# Create the main plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
update_plot(theta1_init, theta2_init)

# Create sliders for joint angles
axcolor = 'lightgoldenrodyellow'
ax_theta1 = plt.axes([0.1, 0.01, 0.65, 0.03], facecolor=axcolor)
ax_theta2 = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=axcolor)

s_theta1 = Slider(ax_theta1, 'Rotation Theta 1 (deg)', 0, 360, valinit=theta1_init)
s_theta2 = Slider(ax_theta2, 'Rotation Theta 2 (deg)', 0, 360, valinit=theta2_init)

# Update the plot when sliders are adjusted
def update(val):
    update_plot(s_theta1.val, s_theta2.val)

s_theta1.on_changed(update)
s_theta2.on_changed(update)

plt.show()
