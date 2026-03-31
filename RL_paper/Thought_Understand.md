#### 关于物理仿真引擎
MuJoCo 本质就是数值动力学仿真器，画面只是“渲染结果”，和物理计算是分离的。

🔥 为什么 MuJoCo 很强？因为它在解：接触问题（contact dynamics）👉 包括：碰撞、摩擦、约束👉 它用的是：soft constraint + convex optimization（不是传统硬碰撞）。

Issac也是如此，区别是数值物理引擎是NVIDIA PhysX，渲染是NVIDIA Omniverse（RTX光追）。和 MuJoCo 的核心区别：

🧠 1️⃣ 接触模型不同
MuJoCo：soft constraint（优化问题）👉 更平滑👉 更适合控制研究

Isaac / PhysX：iterative solver（近似解）👉 更快👉 更偏游戏/工程

🧠 2️⃣ GPU 支持
引擎	GPU

MuJoCo	❌（基本CPU）

Isaac Gym	✅（全GPU）