from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D

mpl.rcParams['figure.dpi'] = 300

import glob
import os
import torch
import argparse
import numpy as np

# ===================== Arguments =====================
parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, default=None)
parser.add_argument("--save_video", action="store_true")
args = parser.parse_args()

# ===================== Load data =====================
if args.filename is None:
    list_of_files = glob.glob('data/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    filename = latest_file
else:
    filename = args.filename

print(f"Loading: {filename}")
data = torch.load(filename)

# ===================== State curves =====================
fig, axs = plt.subplots(6, 1, sharex=True)

axs[0].plot([es[7] for (s, u, es, _) in data])
axs[0].set_ylabel(r"$\beta$")

axs[1].plot([es[6] for (s, u, es, _) in data])
axs[1].set_ylabel(r"$V$")

axs[2].plot([u[0] for (s, u, es, _) in data])
axs[2].set_ylabel(r"$\delta$")

axs[3].plot([u[1] for (s, u, es, _) in data], label="f")
axs[3].plot([u[2] for (s, u, es, _) in data], label="r")
axs[3].legend()
axs[3].set_ylabel(r"$\omega$")

axs[4].plot([es[16] for (s, u, es, _) in data], label="f")
axs[4].plot([es[17] for (s, u, es, _) in data], label="r")
axs[4].legend()
axs[4].set_ylabel(r"$s$")

axs[5].plot([es[12] for (s, u, es, _) in data], label="f")
axs[5].plot([es[14] for (s, u, es, _) in data], label="r")
axs[5].legend()
axs[5].set_ylabel(r"$s_x$")
axs[5].set_xlabel("Step")

plt.tight_layout()
plt.savefig(f"{filename}_state.png")
plt.close()

# ===================== Animation =====================
fig, ax = plt.subplots()

# Reference circular trajectory
theta = np.linspace(0, 2 * np.pi, 200)
radius = 1.
ax.plot(radius * np.cos(theta), radius + radius * np.sin(theta), 'r--')

# Extract data
x = np.array([s[0] for (s, u, es, _) in data])
y = np.array([s[1] for (s, u, es, _) in data])
psi = np.array([s[2] for (s, u, es, _) in data])
delta = np.array([u[0] for (s, u, es, _) in data])
beta = np.array([es[7] for (s, u, es, _) in data])  # Key variable

ax.set_aspect('equal', 'box')
ax.set_title("Car Trajectory (β colored)")

# Auto scaling
margin = 0.5
ax.set_xlim(x.min() - margin, x.max() + margin)
ax.set_ylim(y.min() - margin, y.max() + margin)

# Trajectory line
traj_line, = ax.plot([], [], 'b-', linewidth=1.5)

# ===== Car body =====
car_length = 0.3
car_width = 0.15
wheel_length = 0.08
wheel_width = 0.03

car_body = Rectangle(
    (-car_length / 2, -car_width / 2),
    car_length, car_width,
    fc='black', ec='black'
)
ax.add_patch(car_body)


def create_wheel():
    return Rectangle(
        (-wheel_length / 2, -wheel_width / 2),
        wheel_length, wheel_width,
        fc='gray', ec='black'
    )


front_left = create_wheel()
front_right = create_wheel()
rear_left = create_wheel()
rear_right = create_wheel()

for w in [front_left, front_right, rear_left, rear_right]:
    ax.add_patch(w)

# ===== Beta color mapping =====
norm = mpl.colors.Normalize(vmin=beta.min(), vmax=beta.max())
cmap = plt.cm.jet

arrow = None

# ===== Update function =====
def update(frame):
    global arrow

    traj_line.set_data(x[:frame], y[:frame])

    x_ = x[frame]
    y_ = y[frame]
    psi_ = psi[frame]
    delta_ = delta[frame]
    beta_ = beta[frame]

    # Remove the previous arrow
    if arrow is not None:
        arrow.remove()

    # ===== Car body =====
    body_tf = Affine2D().rotate(psi_).translate(x_, y_)
    car_body.set_transform(body_tf + ax.transData)

    # ===== Wheels =====
    offsets = {
        "fl": (car_length / 2,  car_width / 2),
        "fr": (car_length / 2, -car_width / 2),
        "rl": (-car_length / 2,  car_width / 2),
        "rr": (-car_length / 2, -car_width / 2),
    }

    wheels = {
        "fl": front_left,
        "fr": front_right,
        "rl": rear_left,
        "rr": rear_right
    }

    for key in wheels:
        ox, oy = offsets[key]

        wx = x_ + ox * np.cos(psi_) - oy * np.sin(psi_)
        wy = y_ + ox * np.sin(psi_) + oy * np.cos(psi_)

        angle = psi_ + delta_ if key in ["fl", "fr"] else psi_

        tf = Affine2D().rotate(angle).translate(wx, wy)
        wheels[key].set_transform(tf + ax.transData)

    # ===== Beta-colored heading arrow =====
    color = cmap(norm(beta_))

    length = 0.25
    dx = length * np.cos(psi_)
    dy = length * np.sin(psi_)

    arrow = ax.arrow(
        x_, y_, dx, dy,
        head_width=0.08,
        head_length=0.08,
        fc=color,
        ec=color
    )

    return traj_line,


# ===== Animation setup =====
step = max(1, len(x) // 2000)
frames = range(0, len(x), step)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=20,
    blit=False
)

# ===== Output =====
if args.save_video:
    print("Saving video...")
    ani.save(f"{filename}_car_beta.mp4", writer="ffmpeg", fps=30)
else:
    plt.show()