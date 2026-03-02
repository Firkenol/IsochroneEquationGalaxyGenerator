import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# initialize figure and 2d axis
fig, ax = plt.subplots(figsize=(9, 9))
plt.subplots_adjust(bottom=0.35)
ax.set_aspect('equal')
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

# milky way parameters from the paper
A_init = 0.85
N_init = 37.5
B_init = 6.4
C_init = 0.67
Ct_init = 0.296
T_init = 1.2
d1_init = 4.4
a_init = 0.8
a2_init = 2.7

# parameter domain t = i/p
t = np.linspace(0.001, 1.0, 2000)

def c_toc(x, y, a, a2, d1):
    yaw_x = np.sqrt(x**2 + y**2)
    proj_denom = d1 - np.cos(a2) * yaw_x
    yaw_angle = a + np.arctan2(y, x)
    
    x_screen = proj_denom * np.cos(yaw_angle)
    y_screen = yaw_x * np.sin(a2) * np.sin(yaw_angle)
    return x_screen, y_screen

def calculate_galaxy(A, N, B, C, Ct, T_rot, a, a2, d1):
    phi_1 = t * 2 * np.pi * C
    phi_2 = t * 2 * np.pi * (C + 0.35)
    
    # taper function for strand ends
    a_dj = np.where(t < (Ct / C), 1.0, 1.0 - ((t * C - Ct) / (C - Ct)))
    
    tan_term_1 = np.tan(phi_1 / (2 * N))
    tan_term_2 = np.tan(phi_2 / (2 * N))
    
    valid_mask_1 = tan_term_1 > 0
    valid_mask_2 = tan_term_2 > 0
    
    r1, r2, r3, r4 = (np.full_like(t, np.nan) for _ in range(4))
    
    # arm 1 & 2
    log_term_1 = np.log(B * tan_term_1[valid_mask_1])
    r1[valid_mask_1] = (A + 0.2 * a_dj[valid_mask_1]) / log_term_1
    r2[valid_mask_1] = (-A - 0.2 * a_dj[valid_mask_1]) / log_term_1
    
    # arm 3 & 4
    log_term_2 = np.log(B * tan_term_2[valid_mask_2])
    r3[valid_mask_2] = (A + 0.06 - 0.3 * a_dj[valid_mask_2]) / log_term_2
    r4[valid_mask_2] = (-(A + 0.06) + 0.3 * a_dj[valid_mask_2]) / log_term_2
    
    # filter asymptotes
    r1 = np.where(np.abs(r1) > 50, np.nan, r1)
    r2 = np.where(np.abs(r2) > 50, np.nan, r2)
    r3 = np.where(np.abs(r3) > 50, np.nan, r3)
    r4 = np.where(np.abs(r4) > 50, np.nan, r4)
    
    # apply differential rotation
    theta_1 = phi_1 - (T_rot / np.abs(r1))
    theta_2 = phi_1 - (T_rot / np.abs(r2))
    theta_3 = phi_2 - (T_rot / np.abs(r3))
    theta_4 = phi_2 - (T_rot / np.abs(r4))
    
    x1, y1 = r1 * np.cos(theta_1), r1 * np.sin(theta_1)
    x2, y2 = r2 * np.cos(theta_2), r2 * np.sin(theta_2)
    x3, y3 = r3 * np.cos(theta_3), r3 * np.sin(theta_3)
    x4, y4 = r4 * np.cos(theta_4), r4 * np.sin(theta_4)
    
    # project 3d coords to 2d screen
    xs1, ys1 = c_toc(x1, y1, a, a2, d1)
    xs2, ys2 = c_toc(x2, y2, a, a2, d1)
    xs3, ys3 = c_toc(x3, y3, a, a2, d1)
    xs4, ys4 = c_toc(x4, y4, a, a2, d1)
    
    return (xs1, ys1), (xs2, ys2), (xs3, ys3), (xs4, ys4)

# initial plot setup
arms = calculate_galaxy(A_init, N_init, B_init, C_init, Ct_init, T_init, a_init, a2_init, d1_init)
lines = []
colors = ['#c88df5', '#c88df5', '#8d9cf5', '#8d9cf5']

for i in range(4):
    line, = ax.plot(arms[i][0], arms[i][1], color=colors[i], lw=1.5)
    lines.append(line)

ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.set_title('Parametric Milky Way Implementation (4-Arm Scaffold)', color='white')

# interactive sliders
ax_N = plt.axes([0.15, 0.25, 0.7, 0.02], facecolor='darkgray')
ax_B = plt.axes([0.15, 0.20, 0.7, 0.02], facecolor='darkgray')
ax_T = plt.axes([0.15, 0.15, 0.7, 0.02], facecolor='darkgray')
ax_a = plt.axes([0.15, 0.10, 0.7, 0.02], facecolor='darkgray')
ax_a2 = plt.axes([0.15, 0.05, 0.7, 0.02], facecolor='darkgray')

slider_N = Slider(ax_N, 'Winding (N)', 5.0, 50.0, valinit=N_init, color='#c88df5')
slider_B = Slider(ax_B, 'Bulge (B)', 0.1, 10.0, valinit=B_init, color='#c88df5')
slider_T = Slider(ax_T, 'Rotation (T)', 0.0, 3.0, valinit=T_init, color='#c88df5')
slider_a = Slider(ax_a, 'Azimuth (a)', 0.0, np.pi, valinit=a_init, color='#8d9cf5')
slider_a2 = Slider(ax_a2, 'Elevation (a2)', 0.0, np.pi, valinit=a2_init, color='#8d9cf5')

for s in [slider_N, slider_B, slider_T, slider_a, slider_a2]:
    s.label.set_color('white')
    s.valtext.set_color('white')

def update(val):
    N_val = slider_N.val
    B_val = slider_B.val
    T_val = slider_T.val
    a_val = slider_a.val
    a2_val = slider_a2.val
    
    new_arms = calculate_galaxy(A_init, N_val, B_val, C_init, Ct_init, T_val, a_val, a2_val, d1_init)
    
    for idx, line in enumerate(lines):
        line.set_data(new_arms[idx][0], new_arms[idx][1])
        
    fig.canvas.draw_idle()

slider_N.on_changed(update)
slider_B.on_changed(update)
slider_T.on_changed(update)
slider_a.on_changed(update)
slider_a2.on_changed(update)

plt.show()