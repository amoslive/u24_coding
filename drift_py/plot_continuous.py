from matplotlib import pyplot as plt
from pandas import read_csv 
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

# ===================== 参数 =====================
parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, default=None)
parser.add_argument("--save_gif", action="store_true")
args = parser.parse_args()

# ===================== 读取数据 =====================
list_of_files = glob.glob('data/*')
latest_file = max(list_of_files, key=os.path.getctime)
data = torch.load(latest_file)

list_of_files_traj = glob.glob('data/traj*')
latest_file_traj = max(list_of_files_traj, key=os.path.getctime)
data_traj = read_csv(latest_file_traj, header=None)

filename = latest_file if args.filename is None else args.filename

# ===================== 状态图 =====================
fig, axs = plt.subplots(3, 1, sharex=True)

axs[0].plot([es[7] for (s, u, es, _) in data])
axs[0].set_ylabel(r"$\beta$")

axs[1].plot([es[6] for (s, u, es, _) in data])
axs[1].set_ylabel(r"$V$")

axs[2].plot([u[0] for (s, u, es, _) in data])
axs[2].set_ylabel(r"$\delta$")
axs[2].set_xlabel("Step")

plt.tight_layout()
plt.savefig(f"{filename}_state.png")
plt.close()

# ===================== 动画 =====================
fig, ax = plt.subplots()

# ✅ 正确参考轨迹（关键！！）
ax.plot(data_traj[0], data_traj[1], 'r--', label="reference")

# 数据
x = np.array([s[0] for (s, u, es, _) in data])
y = np.array([s[1] for (s, u, es, _) in data])
psi = np.array([s[2] for (s, u, es, _) in data])
delta = np.array([u[0] for (s, u, es, _) in data])
beta = np.array([es[7] for (s, u, es, _) in data])

ax.set_aspect('equal', 'box')
ax.set_title("Continuous Drift (β colored)")

# 自动缩放
margin = 0.5
ax.set_xlim(min(x.min(), data_traj[0].min()) - margin,
            max(x.max(), data_traj[0].max()) + margin)
ax.set_ylim(min(y.min(), data_traj[1].min()) - margin,
            max(y.max(), data_traj[1].max()) + margin)

# 轨迹
traj_line, = ax.plot([], [], 'b-', linewidth=1.5)

# ===== 小车 =====
car_length = 0.3
car_width = 0.15
wheel_length = 0.08
wheel_width = 0.03

car_body = Rectangle(
    (-car_length/2, -car_width/2),
    car_length, car_width,
    fc='black', ec='black'
)
ax.add_patch(car_body)

def create_wheel():
    return Rectangle(
        (-wheel_length/2, -wheel_width/2),
        wheel_length, wheel_width,
        fc='gray', ec='black'
    )

front_left = create_wheel()
front_right = create_wheel()
rear_left = create_wheel()
rear_right = create_wheel()

for w in [front_left, front_right, rear_left, rear_right]:
    ax.add_patch(w)

# β颜色
norm = mpl.colors.Normalize(vmin=beta.min(), vmax=beta.max())
cmap = plt.cm.jet

arrow = None

# ===================== 更新 =====================
def update(frame):
    global arrow

    traj_line.set_data(x[:frame], y[:frame])

    x_ = x[frame]
    y_ = y[frame]
    psi_ = psi[frame]
    delta_ = delta[frame]
    beta_ = beta[frame]

    if arrow is not None:
        arrow.remove()

    # ===== 车身 =====
    body_tf = Affine2D().rotate(psi_).translate(x_, y_)
    car_body.set_transform(body_tf + ax.transData)

    # ===== 轮子 =====
    offsets = {
        "fl": ( car_length/2,  car_width/2),
        "fr": ( car_length/2, -car_width/2),
        "rl": (-car_length/2,  car_width/2),
        "rr": (-car_length/2, -car_width/2),
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

    # ===== β 上色箭头 =====
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

# ===================== 动画 =====================
step = max(1, len(x) // 2000)
frames = range(0, len(x), step)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=20,
    blit=False
)

# ===================== 输出 =====================
if args.save_gif:
    print("Saving GIF...")
    ani.save(f"{filename}_car_beta.gif", writer="pillow", fps=30)
else:
    plt.show()