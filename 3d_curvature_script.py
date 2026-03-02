import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 3d plot setup
fig = plt.figure(figsize=(9, 9))
plt.subplots_adjust(bottom=0.3)
fig.patch.set_facecolor('black')

# native 3d projection
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

# remove grid and background panels
ax.axis('off')

# init vars
Zoom_init = 8.0
A_init = 0.85
N_init = 37.5
B_init = 6.4
C_init = 0.67
Ct_init = 0.296
T_init = 1.2

t = np.linspace(0.001, 1.0, 2000)

def calc_3d(A, N, B, C, Ct, T_rot):
    phi_1 = t * 2 * np.pi * C
    phi_2 = t * 2 * np.pi * (C + 0.35)
    
    # taper ends
    a_dj = np.where(t < (Ct / C), 1.0, 1.0 - ((t * C - Ct) / (C - Ct)))
    
    tan_1 = np.tan(phi_1 / (2 * N))
    tan_2 = np.tan(phi_2 / (2 * N))
    
    valid_1 = tan_1 > 0
    valid_2 = tan_2 > 0
    
    r1, r2, r3, r4 = (np.full_like(t, np.nan) for _ in range(4))
    
    # arms 1 and 2
    log_1 = np.log(B * tan_1[valid_1])
    r1[valid_1] = (A + 0.2 * a_dj[valid_1]) / log_1
    r2[valid_1] = (-A - 0.2 * a_dj[valid_1]) / log_1
    
    # arms 3 and 4
    log_2 = np.log(B * tan_2[valid_2])
    r3[valid_2] = (A + 0.06 - 0.3 * a_dj[valid_2]) / log_2
    r4[valid_2] = (-(A + 0.06) + 0.3 * a_dj[valid_2]) / log_2
    
    # kill asymptotes
    r1 = np.where(np.abs(r1) > 50, np.nan, r1)
    r2 = np.where(np.abs(r2) > 50, np.nan, r2)
    r3 = np.where(np.abs(r3) > 50, np.nan, r3)
    r4 = np.where(np.abs(r4) > 50, np.nan, r4)
    
    # apply rotation twist
    theta_1 = phi_1 - (T_rot / np.abs(r1))
    theta_2 = phi_1 - (T_rot / np.abs(r2))
    theta_3 = phi_2 - (T_rot / np.abs(r3))
    theta_4 = phi_2 - (T_rot / np.abs(r4))
    
    x1, y1 = r1 * np.cos(theta_1), r1 * np.sin(theta_1)
    x2, y2 = r2 * np.cos(theta_2), r2 * np.sin(theta_2)
    x3, y3 = r3 * np.cos(theta_3), r3 * np.sin(theta_3)
    x4, y4 = r4 * np.cos(theta_4), r4 * np.sin(theta_4)
    
    # flat z plane for base curvature
    z = np.zeros_like(t)
    
    return (x1, y1, z), (x2, y2, z), (x3, y3, z), (x4, y4, z)

arms = calc_3d(A_init, N_init, B_init, C_init, Ct_init, T_init)
lines = []
colors = ['#c88df5', '#c88df5', '#8d9cf5', '#8d9cf5']

for i in range(4):
    line, = ax.plot(arms[i][0], arms[i][1], arms[i][2], color=colors[i], lw=1.5)
    lines.append(line)

ax.set_xlim([-Zoom_init, Zoom_init])
ax.set_ylim([-Zoom_init, Zoom_init])
ax.set_zlim([-Zoom_init, Zoom_init])
ax.set_title('Native 3D Milky Way (Click and Drag to Rotate)', color='white')

# slider ui
ax_Zoom = plt.axes([0.15, 0.20, 0.7, 0.02], facecolor='darkgray')
ax_N = plt.axes([0.15, 0.15, 0.7, 0.02], facecolor='darkgray')
ax_B = plt.axes([0.15, 0.10, 0.7, 0.02], facecolor='darkgray')
ax_T = plt.axes([0.15, 0.05, 0.7, 0.02], facecolor='darkgray')

slider_Zoom = Slider(ax_Zoom, 'Zoom (Scale)', 2.0, 20.0, valinit=Zoom_init, color='#8d9cf5')
slider_N = Slider(ax_N, 'Winding (N)', 5.0, 50.0, valinit=N_init, color='#c88df5')
slider_B = Slider(ax_B, 'Bulge (B)', 0.1, 10.0, valinit=B_init, color='#c88df5')
slider_T = Slider(ax_T, 'Rotation (T)', 0.0, 3.0, valinit=T_init, color='#c88df5')

for s in [slider_Zoom, slider_N, slider_B, slider_T]:
    s.label.set_color('white')
    s.valtext.set_color('white')

def update(val):
    z_val = slider_Zoom.val
    ax.set_xlim([-z_val, z_val])
    ax.set_ylim([-z_val, z_val])
    ax.set_zlim([-z_val, z_val])
    new_arms = calc_3d(A_init, slider_N.val, slider_B.val, C_init, Ct_init, slider_T.val)
    
    for idx, line in enumerate(lines):
        line.set_data(new_arms[idx][0], new_arms[idx][1])
        line.set_3d_properties(new_arms[idx][2])
        
    fig.canvas.draw_idle()

slider_N.on_changed(update)
slider_B.on_changed(update)
slider_T.on_changed(update)
slider_Zoom.on_changed(update)

plt.show()