#### 关于物理仿真引擎
>所有现代物理引擎本质就是数值动力学仿真器，画面只是“渲染结果”，和物理计算是分离的。

👉 区别只是：怎么解接触（contact dynamics）、怎么渲染、怎么加速（GPU）

👉 Mujoco用的是：soft constraint（优化问题） + convex optimization（不是传统硬碰撞）。👉 更平滑👉 更适合控制研究

Isaac / PhysX：iterative solver（近似解）👉 更快👉 更偏游戏/工程

核心区别是如何解约束，各种机器人常用环境里，mujoco是精度最高的。