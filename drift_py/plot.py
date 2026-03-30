from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation
mpl.rcParams['figure.dpi'] = 300

import glob
import os
import torch
import argparse
import numpy as np
#动画只有箭头
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

# ===================== 动画部分 =====================
fig, ax = plt.subplots()

# 圆轨迹（参考轨道）
theta = np.linspace(0, 2 * np.pi, 200)
radius = 1.
ax.plot(radius * np.cos(theta), radius + radius * np.sin(theta), 'r--')

# 数据提取
x = [s[0] for (s, u, es, _) in data]
y = [s[1] for (s, u, es, _) in data]
psi = [s[2] for (s, u, es, _) in data]
beta = [es[7] for (s, u, es, _) in data]  # 用来上色（可选）

ax.set_aspect('equal', 'box')
ax.set_title("Trajectory Animation")

# 动态轨迹
traj_line, = ax.plot([], [], 'b-', linewidth=1.5)

arrow = None

# 颜色映射（可选）
norm = mpl.colors.Normalize(vmin=min(beta), vmax=max(beta))
cmap = plt.cm.jet


def update(frame):
    global arrow

    # 更新轨迹
    traj_line.set_data(x[:frame], y[:frame])

    # 删除旧箭头
    if arrow is not None:
        arrow.remove()

    x_ = x[frame]
    y_ = y[frame]
    psi_ = psi[frame]

    length = 0.15
    dx = length * np.cos(psi_)
    dy = length * np.sin(psi_)

    # 根据 beta 上色（漂移越大颜色越变）
    color = cmap(norm(beta[frame]))

    arrow = ax.arrow(
        x_, y_, dx, dy,
        head_width=0.08,
        head_length=0.08,
        fc=color,
        ec=color
    )

    return traj_line,


# 为了避免太慢，可以跳帧
step = max(1, len(x) // 2000)  # 自动控制帧数
frames = range(0, len(x), step)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=20,
    blit=False
)

# ===================== 保存 or 显示 =====================
if args.save_video:
    print("Saving video...")
    ani.save(f"{filename}_trajectory.mp4", writer="ffmpeg", fps=30)
else:
    plt.show()