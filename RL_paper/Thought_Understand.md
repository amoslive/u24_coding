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


## Policy Gradient

[GPT对policy gradient的解释](../doc/policy_gradient_gpt.md)

πθ​(a∣s)是个概率，而logπθ(a∣s)就是对这个概率值取了个对数。∇θ是𝜃的变化如何影响这个概率。

>先别管 log 为啥加。你先把它当成：“对这个概率做了一个数学变形，方便算梯度”
>
>最后用一句特别土的话收尾
>
>𝜋𝜃(𝑎∣𝑠)是“这个动作现在有多容易被选到”
>
>∇𝜃log𝜋𝜃(𝑎∣𝑠)是“想让它更容易被选到，该拧哪些旋钮”

可能自己一直都不太理解的，梯度∇这个东西。

实际上梯度∇就是有一个数，它受很多个参数的影响，这些参数旋钮怎么拧，这个数会变大。

而πθ​(a∣s)是个输出概率数值的函数，它的输入是(a|s)，它的参数是θ。对它的梯度∇，就是参数旋钮怎么调，输出的概率数值会变大。

>你现在的理解，我帮你整理成一个更标准的版本
>
>你可以把它记成下面这段：
>设有一个标量函数𝑓(𝜃)，它受很多参数𝜃影响。
>
>梯度 ∇𝜃𝑓(𝜃)不是单个数，而是一组数，表示每个参数分别怎么调，能让𝑓增大得最快。
>
>在策略梯度里，𝜋𝜃(𝑎∣𝑠)πθ(a∣s) 表示在状态𝑠下选择动作𝑎的概率。因此，∇𝜃𝜋𝜃(𝑎∣𝑠) 或 ∇𝜃log𝜋𝜃(𝑎∣𝑠)表示：如果想改变这个动作被选中的倾向，参数该怎么调。

这版就很准了。

## 计算机

如何用好计算机，就好比是摸金校尉有个法器，如何用它一样。


## 一些blog

>[现代游戏引擎 - 游戏引擎中物理系统的基础理论和算法（十）](https://cherry-white.github.io/posts/de5d97c9.html)
>
>[注]：这里面力学部分都挺全的，从游戏的角度理解这些力学基本元素，开了一个新视角。

整个从0到有，是什么来的，想一下怎么讲清楚，下次给讲一下。

还有一个四轮全部独立转向的。

imu,路由器，


还有一个活，是做一个四轮独立转向驱动加四轮独立电机驱动的小车，相当于四个转向舵机和四个驱动电机，你要能做的话可以一块交给你。