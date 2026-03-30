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

# ===================== 参数 =====================
parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, default=None)
parser.add_argument("--save_video", action="store_true")
args = parser.parse_args()

# ===================== 读取数据 =====================
if args.filename is None:
    list_of_files = glob.glob('data/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    filename = latest_file
else:
    filename = args.filename

print(f"Loading: {filename}")
data = torch.load(filename)

# ===================== 状态曲线 =====================
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

# ===================== 动画 =====================
fig, ax = plt.subplots()

# 参考圆轨迹
theta = np.linspace(0, 2 * np.pi, 200)
radius = 1.
ax.plot(radius * np.cos(theta), radius + radius * np.sin(theta), 'r--')

# 数据提取
x = np.array([s[0] for (s, u, es, _) in data])
y = np.array([s[1] for (s, u, es, _) in data])
psi = np.array([s[2] for (s, u, es, _) in data])
delta = np.array([u[0] for (s, u, es, _) in data])

ax.set_aspect('equal', 'box')
ax.set_title("Car Trajectory Animation")

# 自动缩放视野
margin = 0.5
ax.set_xlim(x.min() - margin, x.max() + margin)
ax.set_ylim(y.min() - margin, y.max() + margin)

# 轨迹线
traj_line, = ax.plot([], [], 'b-', linewidth=1.5)

# ===== 小车尺寸 =====
car_length = 0.3
car_width = 0.15
wheel_length = 0.08
wheel_width = 0.03

# ===== 创建车体 =====
car_body = Rectangle((-car_length/2, -car_width/2),
                     car_length, car_width,
                     fc='black', ec='black')

ax.add_patch(car_body)

# ===== 四个轮子 =====
def create_wheel():
    return Rectangle((-wheel_length/2, -wheel_width/2),
                     wheel_length, wheel_width,
                     fc='gray', ec='black')

front_left = create_wheel()
front_right = create_wheel()
rear_left = create_wheel()
rear_right = create_wheel()

for w in [front_left, front_right, rear_left, rear_right]:
    ax.add_patch(w)

# ===== 动画更新 =====
def update(frame):
    # 更新轨迹
    traj_line.set_data(x[:frame], y[:frame])

    x_ = x[frame]
    y_ = y[frame]
    psi_ = psi[frame]
    delta_ = delta[frame]

    # ===== 车身 =====
    body_tf = Affine2D().rotate(psi_).translate(x_, y_)
    car_body.set_transform(body_tf + ax.transData)

    # ===== 轮子位置（车体坐标系）=====
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

        # 转到世界坐标
        wx = x_ + ox * np.cos(psi_) - oy * np.sin(psi_)
        wy = y_ + ox * np.sin(psi_) + oy * np.cos(psi_)

        # 前轮带转向
        if key in ["fl", "fr"]:
            angle = psi_ + delta_
        else:
            angle = psi_

        tf = Affine2D().rotate(angle).translate(wx, wy)
        wheels[key].set_transform(tf + ax.transData)

    return traj_line,

# ===== 动画 =====
step = max(1, len(x) // 2000)
frames = range(0, len(x), step)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=20,
    blit=False
)

# ===== 输出 =====
if args.save_video:
    print("Saving video...")
    ani.save(f"{filename}_car.mp4", writer="ffmpeg", fps=30)
else:
    plt.show()