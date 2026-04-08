## RL库
[强化学习库比较](https://docs.robotsfan.com/isaaclab/source/overview/reinforcement-learning/rl_frameworks.html)

[注]：就好像MPC的库，OPT的库一样。

>[英伟达](https://www.nvidia.cn/use-cases/robot-learning/?deeplink=content-tab--2)
>
>首先，在各种环境中配置种类繁多的机器人，定义 RL 任务，并使用 GPU 优化库 (例如 RSL RL、RL-Games、SKRL 和 Stable Baselines3) 训练模型

>http://github.com/Denys88/rl_games
>
>给出了参数yaml文件的各个参数含义



## 关于物理仿真引擎
>【GPT】:所有现代物理引擎本质就是数值动力学仿真器，画面只是“渲染结果”，和物理计算是分离的。
>
>👉 区别只是：怎么解接触（contact dynamics）、怎么渲染、怎么加速（GPU）
>
>👉 Mujoco用的是：soft constraint（优化问题） + convex optimization（不是传统硬碰撞）。👉 更平滑👉 更适合控制研究
>
>Isaac / PhysX：iterative solver（近似解）👉 更快👉 更偏游戏/工程
>
>核心区别是如何解约束，各种机器人常用环境里，mujoco是精度最高的。


【注】：不过暂时还没懂物理引擎是怎么数值解算的？

**【注】：所以也没理解用于RL训练的数据是怎么产生的呢？**

## 动力学库

[机器人动力学求解库使用笔记](https://zhuanlan.zhihu.com/p/231351878)

[注]：通过urdf和运算实时给出M等矩阵。

[pinocchio-overview](https://gepettoweb.laas.fr/doc/stack-of-tasks/pinocchio/devel/doxygen-html/)

## 计算机

如何用好计算机，就好比是摸金校尉有个法器，如何用它一样。


## 一些blog

>[现代游戏引擎 - 游戏引擎中物理系统的基础理论和算法（十）](https://cherry-white.github.io/posts/de5d97c9.html)
>
>[注]：这里面力学部分都挺全的，从游戏的角度理解这些力学基本元素，开了一个新视角。