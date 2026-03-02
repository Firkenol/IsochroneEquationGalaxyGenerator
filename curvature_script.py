import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# setup basic figure and axes
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.25)
ax.set_aspect('equal')
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

# initial parameters based on ngc 1365 fit
A_init = 1.0
B_init = 0.4
N_init = 16.0

# define the domain for phi
# need to avoid log(0) or negative values in tan, so bound the domain based on N
phi = np.linspace(0.01, N_init * np.pi - 0.01, 1000)

def calculate_radius(phi_arr, A, B, N):
    # inner term of the log function
    tan_term = np.tan(phi_arr / (2 * N))
    
    # filter out invalid domain values where tan is negative or zero
    valid_mask = tan_term > 0
    r = np.zeros_like(phi_arr)
    
    # apply ringermacher-mead isochrone formula
    # r(phi) = A / log(B * tan(phi / 2N))
    r[valid_mask] = A / np.log(B * tan_term[valid_mask])
    
    # handle asymptotes
    r = np.where(np.abs(r) > 100, np.nan, r)
    return r

# polar to cartesian conversion for plotting
def get_cartesian(r, phi_arr):
    x = r * np.cos(phi_arr)
    y = r * np.sin(phi_arr)
    return x, y

r_init = calculate_radius(phi, A_init, B_init, N_init)
x_init, y_init = get_cartesian(r_init, phi)

# plot main arm and symmetric opposite arm
line1, = ax.plot(x_init, y_init, color='cyan', lw=2)
line2, = ax.plot(-x_init, -y_init, color='cyan', lw=2)

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_title('Ringermacher-Mead Isochrone Base Curvature', color='white')

# setup sliders for interactivity
ax_N = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='darkgray')
ax_B = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='darkgray')

slider_N = Slider(ax_N, 'Winding (N)', 1.0, 40.0, valinit=N_init, color='cyan')
slider_B = Slider(ax_B, 'Bulge (B)', 0.01, 2.0, valinit=B_init, color='cyan')

# labels color fix
slider_N.label.set_color('white')
slider_B.label.set_color('white')
slider_N.valtext.set_color('white')
slider_B.valtext.set_color('white')

# update function for when sliders are moved
def update(val):
    N_val = slider_N.val
    B_val = slider_B.val
    
    # recalculate domain dynamically based on winding number
    new_phi = np.linspace(0.01, N_val * np.pi - 0.01, 1000)
    new_r = calculate_radius(new_phi, A_init, B_val, N_val)
    
    new_x, new_y = get_cartesian(new_r, new_phi)
    
    line1.set_data(new_x, new_y)
    line2.set_data(-new_x, -new_y)
    fig.canvas.draw_idle()

slider_N.on_changed(update)
slider_B.on_changed(update)

plt.show()