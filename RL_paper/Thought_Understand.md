#### 关于物理仿真引擎
所有现代物理引擎本质就是数值动力学仿真器，画面只是“渲染结果”，和物理计算是分离的。

每一步在都在做：状态 → 力 → 积分 → 新状态，包括解接触问题（contact dynamics）👉 包括：碰撞、摩擦、约束
👉 区别只是：怎么解接触、怎么渲染、怎么加速（GPU）

👉 Mujoco用的是：soft constraint + convex optimization（不是传统硬碰撞）。



🧠 1️⃣ 接触模型不同
MuJoCo：soft constraint（优化问题）👉 更平滑👉 更适合控制研究

Isaac / PhysX：iterative solver（近似解）👉 更快👉 更偏游戏/工程

