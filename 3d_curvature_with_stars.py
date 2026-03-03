import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

fig = plt.figure(figsize=(9, 9))
fig.patch.set_facecolor('black')

# strictly bound the 3d plot to the top 70% of the window to prevent mouse grab overlap
# layout is [left, bottom, width, height]
ax = fig.add_axes([0.0, 0.30, 1.0, 0.70], projection='3d')
ax.set_facecolor('black')
ax.axis('off')

# base params
A_init = 0.85
N_init = 37.5
B_init = 6.4
C_init = 0.67
Ct_init = 0.296
T_init = 1.2
Zoom_init = 8.0


# scatter params
d_rad_init = 0.131 
d_z_init = 0.02 
p3 = 1330

# lock rng seed so stars dont regenerate on slider drag
np.random.seed(42)

t = np.linspace(0.001, 1.0, p3)

# pre-calc gaussian noise for radius and z-axis
n_r = [np.random.normal(0, 1, p3) * np.random.uniform(0, 1, p3) for _ in range(4)]
n_z = [np.random.normal(0, 1, p3) * np.random.uniform(0, 1, p3) for _ in range(4)]

# s_u magnitude variation
rand_s = np.random.rand(4, p3)
sd, sm = 5.0, 4.97
sizes = [np.clip((rand_s[i] - 0.4) * sd + sm, 0.1, None) for i in range(4)]

def calc_stars(A, N, B, C, Ct, T_rot, d_rad, d_z):
    # prevent division by zero crashes if slider hits 0 or C equals Ct
    if C == 0:
        C = 0.001
    if C == Ct:
        C += 0.001
        
    phi_1 = t * 2 * np.pi * C
    phi_2 = t * 2 * np.pi * (C + 0.35)
    
    a_dj = np.where(t < (Ct / C), 1.0, 1.0 - ((t * C - Ct) / (C - Ct)))
    
    tan_1 = np.tan(phi_1 / (2 * N))
    tan_2 = np.tan(phi_2 / (2 * N))
    
    v1, v2 = tan_1 > 0, tan_2 > 0
    r = [np.full_like(t, np.nan) for _ in range(4)]
    
    # apply G_g stochastic noise to numerator
    g = [n_r[i] * d_rad for i in range(4)]
    
    log_1 = np.log(B * tan_1[v1])
    r[0][v1] = (A + (g[0][v1] + 0.2) * a_dj[v1]) / log_1
    r[1][v1] = (-A - (g[1][v1] + 0.2) * a_dj[v1]) / log_1
    
    log_2 = np.log(B * tan_2[v2])
    r[2][v2] = (A + 0.06 + (g[2][v2] - 0.3) * a_dj[v2]) / log_2
    r[3][v2] = (-(A + 0.06) + (g[3][v2] + 0.3) * a_dj[v2]) / log_2
    
    for rad in r:
        rad[np.abs(rad) > 50] = np.nan
        
    theta_1 = phi_1 - (T_rot / np.abs(r[0]))
    theta_2 = phi_1 - (T_rot / np.abs(r[1]))
    theta_3 = phi_2 - (T_rot / np.abs(r[2]))
    theta_4 = phi_2 - (T_rot / np.abs(r[3]))
    
    x1, y1 = r[0] * np.cos(theta_1), r[0] * np.sin(theta_1)
    x2, y2 = r[1] * np.cos(theta_2), r[1] * np.sin(theta_2)
    x3, y3 = r[2] * np.cos(theta_3), r[2] * np.sin(theta_3)
    x4, y4 = r[3] * np.cos(theta_4), r[3] * np.sin(theta_4)
    
    # thicker bulge, flat outer disk
    z_taper = np.exp(-t * 2.5) + 0.15
    z1 = n_z[0] * d_z * z_taper
    z2 = n_z[1] * d_z * z_taper
    z3 = n_z[2] * d_z * z_taper
    z4 = n_z[3] * d_z * z_taper
    
    return [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3), (x4, y4, z4)]

arms = calc_stars(A_init, N_init, B_init, C_init, Ct_init, T_init, d_rad_init, d_z_init)
scatters = []
colors = ['#c88df5', '#c88df5', '#8d9cf5', '#8d9cf5']

# init scatter plots
for i in range(4):
    scat = ax.scatter(arms[i][0], arms[i][1], arms[i][2], c=colors[i], s=sizes[i], alpha=0.7, edgecolors='none')
    scatters.append(scat)

ax.set_xlim([-Zoom_init, Zoom_init])
ax.set_ylim([-Zoom_init, Zoom_init])
ax.set_zlim([-Zoom_init, Zoom_init])
ax.set_title('Stochastic Density Galaxy Model', color='white')

# left column ui params
ax_Zoom = plt.axes([0.15, 0.20, 0.20, 0.02], facecolor='darkgray')
ax_N = plt.axes([0.15, 0.15, 0.20, 0.02], facecolor='darkgray')
ax_B = plt.axes([0.15, 0.10, 0.20, 0.02], facecolor='darkgray')
ax_T = plt.axes([0.15, 0.05, 0.20, 0.02], facecolor='darkgray')

# right column ui params
ax_C = plt.axes([0.70, 0.20, 0.20, 0.02], facecolor='darkgray')
ax_Ct = plt.axes([0.70, 0.15, 0.20, 0.02], facecolor='darkgray')
ax_d = plt.axes([0.70, 0.10, 0.20, 0.02], facecolor='darkgray')
ax_Zthick = plt.axes([0.70, 0.05, 0.20, 0.02], facecolor='darkgray')

slider_Zoom = Slider(ax_Zoom, 'Zoom (Scale)', 0.2, 15.0, valinit=Zoom_init, color='#8d9cf5')
slider_N = Slider(ax_N, 'Winding (N)', 5.0, 50.0, valinit=N_init, color='#c88df5')
slider_B = Slider(ax_B, 'Bulge (B)', 0.1, 10.0, valinit=B_init, color='#c88df5')
slider_T = Slider(ax_T, 'Rotation (T)', 0.0, 3.0, valinit=T_init, color='#c88df5')
slider_C = Slider(ax_C, 'Length (C)', 0.0, 2.0, valinit=C_init, color='#8d9cf5')
slider_Ct = Slider(ax_Ct, 'End Width (Ct)', 0.0, 2.0, valinit=Ct_init, color='#8d9cf5')
slider_d = Slider(ax_d, 'Strand Width (d)', 0.0, 0.2, valinit=d_rad_init, color='#8d9cf5')
slider_Zthick = Slider(ax_Zthick, 'Thickness (Z)', 0.0, 0.5, valinit=d_z_init, color='#8d9cf5')

for s in [slider_Zoom, slider_N, slider_B, slider_T, slider_C, slider_Ct, slider_d, slider_Zthick]:
    s.label.set_color('white')
    s.valtext.set_color('white')

def update(val):
    n_arms = calc_stars(A_init, slider_N.val, slider_B.val, slider_C.val, slider_Ct.val, slider_T.val, slider_d.val, slider_Zthick.val)
    
    for idx, scat in enumerate(scatters):
        offsets = np.c_[n_arms[idx][0], n_arms[idx][1]]
        scat.set_offsets(offsets)
        scat.set_3d_properties(n_arms[idx][2], 'z')
        
    z_val = slider_Zoom.val 
    ax.set_xlim([-z_val, z_val])
    ax.set_ylim([-z_val, z_val])
    ax.set_zlim([-z_val, z_val])
        
    fig.canvas.draw_idle()

slider_Zoom.on_changed(update)
slider_N.on_changed(update)
slider_B.on_changed(update)
slider_T.on_changed(update)
slider_C.on_changed(update)
slider_Ct.on_changed(update)
slider_d.on_changed(update)
slider_Zthick.on_changed(update)

plt.show()