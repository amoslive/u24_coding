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

# 参考圆轨迹
theta = np.linspace(0, 2 * np.pi, 200)
radius = 1.
ax.plot(radius * np.cos(theta), radius + radius * np.sin(theta), 'r--')

# 数据提取
x = np.array([s[0] for (s, u, es, _) in data])
y = np.array([s[1] for (s, u, es, _) in data])
psi = np.array([s[2] for (s, u, es, _) in data])

ax.set_aspect('equal', 'box')
ax.set_title("Car Trajectory (Simple)")

# 自动缩放视野
margin = 0.5
ax.set_xlim(x.min() - margin, x.max() + margin)
ax.set_ylim(y.min() - margin, y.max() + margin)

# 轨迹线
traj_line, = ax.plot([], [], 'b-', linewidth=1.5)

# ===== 小车（矩形）=====
car_length = 0.3
car_width = 0.15

car = Rectangle(
    (-car_length/2, -car_width/2),
    car_length,
    car_width,
    fc='black',
    ec='black'
)
ax.add_patch(car)

# ===== 动画更新 =====
def update(frame):
    # 更新轨迹
    traj_line.set_data(x[:frame], y[:frame])

    x_ = x[frame]
    y_ = y[frame]
    psi_ = psi[frame]

    # 核心：旋转 + 平移
    transform = Affine2D().rotate(psi_).translate(x_, y_)
    car.set_transform(transform + ax.transData)

    return traj_line, car


# 控制帧数（防卡）
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
if args.save_video:
    print("Saving video...")
    ani.save(f"{filename}_car_simple.mp4", writer="ffmpeg", fps=30)
else:
    plt.show()