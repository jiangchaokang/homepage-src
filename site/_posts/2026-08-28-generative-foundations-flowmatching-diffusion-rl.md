---
layout: default
title: "Generative Foundations: Flow Matching, Score-based Diffusion & Reinforcement Learning"
seo_title: "Flow Matching, Diffusion SDE/ODE & RL Foundations | Chaokang Jiang"
description: "A systematic mathematical and engineering study across continuous normalizing flows (Flow Matching), score-based diffusion SDE/ODE dynamics, and reinforcement learning (Policy Gradient, TRPO, PPO, GAE)."
date: 2026-08-28
hide_news: false
tags: ["generative", "flow-matching", "diffusion", "rl", "notes"]
category: generative-models
cover: "/assets/media/blog/generative_foundations/cover.svg"
---
<article class="bx reveal">
  <header class="bx-hero">
    <div class="bx-hero-inner">
      <p class="eyebrow">基础理论与工程实践 · 生成模型与强化学习</p>
      <h1>生成模型与强化学习核心底座推导与架构演进</h1>
      <p class="bx-byline">
        系统梳理连续归一化流（Flow Matching）、扩散生成与随机微分方程（Diffusion &amp; SDE/ODE）、以及强化学习策略优化（Policy Gradient → TRPO → PPO → GRPO）。
        通过严格的数理逻辑剖析与工程实现图解，打通现代物理世界模型与自主决策智能的底层脉络。
      </p>
    </div>
    <blockquote class="bx-lede">
      现代生成式世界模型与具身决策系统正在走向深度收敛：从确定性 ODE 驱动的极速 Flow Matching 采样，到连续随机微积分统一的扩散分值建模，再到基于优势函数与策略梯度的强化学习对齐。
      深入理解这三大支柱的数学本质与工程落地机制，是构建高保真生成系统与稳健决策智能体的关键基石。
    </blockquote>
  </header>

  <div class="study-shell" data-tabs>
    <!-- Segmented Navigation Bar -->
    <nav class="study-nav-bar" role="tablist" aria-label="Learning notes modules">
      <button class="study-tab-btn is-active" type="button" role="tab" data-tab="flow-matching" aria-selected="true">
        <span class="tab-num">PART 01</span>
        <span>Flow Matching 理论推导</span>
      </button>
      <button class="study-tab-btn" type="button" role="tab" data-tab="diffusion" aria-selected="false">
        <span class="tab-num">PART 02</span>
        <span>Diffusion 与 SDE/ODE 范式</span>
      </button>
      <button class="study-tab-btn" type="button" role="tab" data-tab="rl" aria-selected="false">
        <span class="tab-num">PART 03</span>
        <span>强化学习与现代策略优化</span>
      </button>
    </nav>

    <!-- =================================================================== -->
    <!-- SECTION 1: Flow Matching                                            -->
    <!-- =================================================================== -->
    <div class="study-panel is-active" data-panel="flow-matching" id="flow-matching" role="tabpanel">
      <div class="study-sec-head" style="--card-accent: var(--accent-cyan);">
        <p class="eyebrow">第 1 篇章 · 连续时间归一化流</p>
        <h2>Flow Matching &amp; Continuous Normalizing Flows (连续归一化流与流匹配理论推导)</h2>
        <p>
          Flow Matching 摒弃了传统扩散模型依赖布朗运动随机漫步的繁琐多步采样，通过在连续时间域构建确定性常微分方程（ODE）向量场，
          直接回归线性概率路径与速度场，实现了轨迹直线性质优越、推理步数大幅压缩的全新生成范式。
        </p>
      </div>

      <div class="study-grid" style="--card-accent: var(--accent-cyan);">

        <!-- FM 01: Vector Field & Core Concept -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">01</span>
              <span>向量场（Vector Field）与速度场概念</span>
            </h3>
            <span class="study-topic-tag">连续时空动力系统</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p003_02.png' | relative_url }}" alt="向量场与速度场概念" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>连续时空速度映射</strong>：向量场 v_t(x) 定义了高维状态空间中每个点在时刻 t 的瞬时演化速度与移动方向。</li>
              <li><strong>从分布传输看生成本质</strong>：Flow Matching 的核心是训练神经网络 v_θ(x, t) 拟合理想速度场，将简易先验分布 p_0(x) 平滑输运至目标数据分布 p_1(x)。</li>
              <li><strong>确定性输运优势</strong>：相比传统 Diffusion SDE，基于确定性连续向量场的 ODE 轨迹更加平滑规整，显著降低离散化积分截断误差。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">ODE 输运基本方程</span>
              <span class="formula-math">d x_t / dt = v_t(x_t), &nbsp; x_0 ~ p_0(x), &nbsp; x_1 ~ p_data(x)</span>
            </div>
          </div>
        </article>

        <!-- FM 02: Trajectory -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">02</span>
              <span>积分轨迹（Trajectory）与状态演化</span>
            </h3>
            <span class="study-topic-tag">ODE 初值问题解</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p004_03.png' | relative_url }}" alt="轨迹定义与积分形式" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>初值问题解曲线</strong>：给定初始位置 x_0，在向量场 v_t 作用下粒子沿时间演化的连续路径构成了状态轨迹 φ_t(x_0)。</li>
              <li><strong>微积分基本定理联系</strong>：粒子在时刻 t 的空间位置严格由速度场沿轨迹的时间积分累积决定。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">轨迹积分定义</span>
              <span class="formula-math">φ_t(x_0) = x_0 + ∫[0 → t] v_τ(φ_τ(x_0)) dτ</span>
            </div>
          </div>
        </article>

        <!-- FM 03: Flow mapping -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">03</span>
              <span>流（Flow）作为轨迹集合的微分同胚映射</span>
            </h3>
            <span class="study-topic-tag">空间拓扑变换</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p005_04.png' | relative_url }}" alt="流是轨迹的集合" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>全空间集合映射</strong>：流 ψ_t 是所有粒子轨迹的集合，构成了状态空间到自身的可逆、光滑微分同胚（Diffeomorphism）。</li>
              <li><strong>前向推移机制</strong>：初始分布 p_0 经由流 ψ_t 变换，生成随时间连续演化的概率密度路径 p_t(x) = [ψ_t]_* p_0(x)。</li>
            </ul>
          </div>
        </article>

        <!-- FM 04: Vector field matching example -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">04</span>
              <span>向量场与流公式的匹配性解析</span>
            </h3>
            <span class="study-topic-tag">解析一致性验证</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p006_05.png' | relative_url }}" alt="判断向量场和流公式匹配" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>流与向量场的微分绑定</strong>：通过对显式流方程关于时间 t 求一阶偏导数，并代入逆映射解出空间位置，验证是否满足速度场约束。</li>
              <li><strong>解析闭式推导验证</strong>：在构造线性或仿射流时，解析验证确保设计的动力系统在全时空域自洽且无奇点。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">向量场一致性约束</span>
              <span class="formula-math">∂ψ_t(x) / ∂t = v_t( ψ_t(x) )</span>
            </div>
          </div>
        </article>

        <!-- FM 05: Sampling -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">05</span>
              <span>Flow Matching 采样生成机制</span>
            </h3>
            <span class="study-topic-tag">ODE 数值积分</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p007_06.png' | relative_url }}" alt="Flow matching 采样方法" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>标准常微分求解</strong>：采样从标准正态分布采样 x_0 ~ N(0, I) 开始，利用数值求解器（如 Euler 法或 Midpoint）沿预测速度场前向积分至 t = 1。</li>
              <li><strong>直线性带来的步数压缩</strong>：最优传输与线性流生成的轨迹接近直线，极少发生轨迹交叉，仅需 10~25 步数值积分即可生成高质量样本。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">Euler 数值离散迭代</span>
              <span class="formula-math">x_{t + Δt} = x_t + Δt · v_θ(x_t, t), &nbsp; t ∈ [0, 1]</span>
            </div>
          </div>
        </article>

        <!-- FM 06: Linear Flow Definition -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">06</span>
              <span>线性流构建与条件速度场推导</span>
            </h3>
            <span class="study-topic-tag">条件概率路径</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p008_07.png' | relative_url }}" alt="线性流公式推导" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>线性插值概率路径</strong>：定义条件流为基底噪声与目标样本间的极简直线插值：ψ_t(x | x_1) = (1 - t) x_0 + t x_1。</li>
              <li><strong>常数条件速度场</strong>：条件速度场具有极简优雅的闭式形式 u_t(x | x_0, x_1) = x_1 - x_0（方向恒定指向真实数据点）。</li>
              <li><strong>规避未知的边际分布</strong>：真实数据边缘分布未知导致全局速度场 u_t(x) 无法直接求取，构造条件流是实现可计算训练的核心突破。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">条件线性流与速度场</span>
              <span class="formula-math">ψ_t(x_0 | x_1) = (1 - t) x_0 + t x_1 &nbsp; ⇒ &nbsp; u_t(x | x_0, x_1) = x_1 - x_0</span>
            </div>
          </div>
        </article>

        <!-- FM 07: Vector field distribution connection -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">07</span>
              <span>先验分布到目标分布的动态平移</span>
            </h3>
            <span class="study-topic-tag">分布输运几何</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p009_08.png' | relative_url }}" alt="线性流与目标分布" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>高斯先验到复杂多模态数据</strong>：高斯先验分布在时刻 t=0 通过连续线性流扩散、变形，最终完美收敛至多模态目标数据分布。</li>
              <li><strong>最优传输路径特性</strong>：点对点直连路径最大程度降低了传输动能损失，避免了类似 Diffusion 的能量耗散与迂回漫步。</li>
            </ul>
          </div>
        </article>

        <!-- FM 08: Marginal Vector Field Definition -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">08</span>
              <span>边缘向量场公式与流体力学连续性方程</span>
            </h3>
            <span class="study-topic-tag">物理守恒定律</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p010_09.png' | relative_url }}" alt="边缘向量场与连续性方程" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>连续性方程（Continuity Equation）约束</strong>：概率密度演化必须满足流体力学质量守恒律：∂p_t(x)/∂t + ∇ · (p_t(x) u_t(x)) = 0。</li>
              <li><strong>边缘速度场积分表示</strong>：边缘速度场通过后验概率期望给出：u_t(x) = ∫ u_t(x | x_1) [ p_t(x | x_1) q(x_1) / p_t(x) ] dx_1。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">流体力学连续性方程</span>
              <span class="formula-math">∂ p_t(x) / ∂t + ∇ · ( p_t(x) u_t(x) ) = 0</span>
            </div>
          </div>
        </article>

        <!-- FM 09: Proof of Continuity Equation -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">09</span>
              <span>连续性方程与概率路径严格数学证明</span>
            </h3>
            <span class="study-topic-tag">数学严格性证明</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p012_11.png' | relative_url }}" alt="连续性方程证明过程" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>莱布尼茨积分法则</strong>：利用散度算子的线性性质与积分求导交换律，证明边缘向量场驱动的流精确复现目标边际密度。</li>
              <li><strong>条件守恒推导全局守恒</strong>：只要每个条件概率路径满足条件连续性方程，积分求和后的全局密度路径自然满足守恒方程。</li>
            </ul>
          </div>
        </article>

        <!-- FM 10: CFM Loss Equivalence -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">10</span>
              <span>条件流匹配（CFM）目标与边际损失等价定理</span>
            </h3>
            <span class="study-topic-tag">训练目标转化核心定理</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p013_12.jpeg' | relative_url }}" alt="CFM等价性证明" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>梯度无偏等价定理</strong>：边际损失 L_FM(θ) 与条件损失 L_CFM(θ) 具有完全相同的参数梯度：∇_θ L_FM(θ) ≡ ∇_θ L_CFM(θ)。</li>
              <li><strong>差值与网络参数无关</strong>：代数展开证明两者的差值仅由条件场与边际场的方差项决定，不含待优化的参数 θ。</li>
              <li><strong>工程可训练性</strong>：将无法直接计算的边际目标转化为单对样本 (x_0, x_1) 蒙特卡洛采样的均方误差回归任务。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">CFM 条件损失函数</span>
              <span class="formula-math">L_CFM(θ) = E_{t, q(x_1), p_t(x|x_1)} [ || v_θ(x, t) - u_t(x | x_1) ||² ]</span>
            </div>
          </div>
        </article>

        <!-- FM 11: Algebraic Proof Details -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">11</span>
              <span>CFM 损失代数展开与梯度一致性推导</span>
            </h3>
            <span class="study-topic-tag">代数推导细节</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p014_13.png' | relative_url }}" alt="CFM代数展开证明" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>交叉项期望等价</strong>：对条件交叉项关于联合分布求期望后，条件速度场 u_t(x|x_1) 自然退化为边缘速度场 u_t(x)。</li>
              <li><strong>凸优化性质保持</strong>：均方误差损失保证了损失曲面的良好几何性质，使神经网络训练过程极度稳定。</li>
            </ul>
          </div>
        </article>

        <!-- FM 12: Gaussian Reparameterization -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">12</span>
              <span>高斯重参数化与闭式采样插值</span>
            </h3>
            <span class="study-topic-tag">微批次采样参数化</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p016_15.png' | relative_url }}" alt="高斯重参数化" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>显式线性插值</strong>：将中间状态显式写为 x_t = (1 - (1 - σ_min) t) x_0 + t x_1，其中 x_0 ~ N(0, I)。</li>
              <li><strong>极速训练构造</strong>：训练时只需均匀采样时间步 t ~ U(0, 1) 和噪声 x_0，单步构造插值点 x_t 即可进行反向传播。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">重参数化采样表达式</span>
              <span class="formula-math">x_t = (1 - t) x_0 + t x_1 &nbsp; (σ_min → 0)</span>
            </div>
          </div>
        </article>

        <!-- FM 13: ODE vs SDE comparison -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">13</span>
              <span>Flow Matching 与 Diffusion 的本质区别</span>
            </h3>
            <span class="study-topic-tag">范式机制对比</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p017_16.png' | relative_url }}" alt="ODE与SDE对比" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>动力学本质不同</strong>：Flow Matching 基于纯确定性 ODE 速度场，轨迹笔直；Diffusion 原生基于布朗运动 SDE，存在高频随机抖动。</li>
              <li><strong>采样效率跨越</strong>：Flow Matching 避免了扩散模型在小步长下的布朗随机漂移，以极少计算量实现了更高的生成保真度。</li>
            </ul>
          </div>
        </article>

        <!-- FM 14: PyTorch Implementation - Training -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">14</span>
              <span>Flow Matching 核心算法实现：训练流程</span>
            </h3>
            <span class="study-topic-tag">PyTorch 算法实现</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p018_17.png' | relative_url }}" alt="Flow matching 训练源码" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>极简损失计算</strong>：核心损失代码仅需计算模型预测速度与目标直线位移 (x1 - x0) 的均方误差。</li>
              <li><strong>高效批处理</strong>：无需预设繁琐的离散加噪 schedule 数组，时间 t 连续连续采样，计算开销极低。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">PyTorch 训练核心代码</span>
              <span class="formula-math">loss = torch.mean((model(x_t, t) - (x1 - x0)) ** 2)</span>
            </div>
          </div>
        </article>

        <!-- FM 15: PyTorch Implementation - Sampling -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">15</span>
              <span>Flow Matching 核心算法实现：采样生成</span>
            </h3>
            <span class="study-topic-tag">PyTorch 采样循环</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/flow_matching/p018_18.png' | relative_url }}" alt="Flow matching 采样源码" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>确定性前向积分</strong>：推理时以 x_0 ~ N(0, I) 为初值，采用简单的 Euler 或 Midpoint 积分步进更新。</li>
              <li><strong>无随机注入</strong>：采样过程无额外高斯噪声注入，生成结果完全由初始潜码与速度场确定，便于潜空间插值与编辑。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">PyTorch 采样核心循环</span>
              <span class="formula-math">x = x + dt * model(x, t)</span>
            </div>
          </div>
        </article>

      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SECTION 2: Diffusion & Continuous SDE/ODE                           -->
    <!-- =================================================================== -->
    <div class="study-panel" data-panel="diffusion" id="diffusion" role="tabpanel">
      <div class="study-sec-head" style="--card-accent: var(--accent-purple);">
        <p class="eyebrow">第 2 篇章 · 扩散动力学与微积分统一</p>
        <h2>Diffusion Models, Score Matching &amp; Stochastic Differential Equations (扩散生成模型、分值匹配与 SDE/ODE 统一范式)</h2>
        <p>
          从离散马尔可夫链 DDPM 逐步演化至基于朗之万动力学（Langevin Dynamics）的分值匹配（Score Matching），
          最终统一于由随机微分方程（SDE）与伴随常微分方程（Probability Flow ODE）构成的连续时空微积分大一统理论。
        </p>
      </div>

      <div class="study-grid" style="--card-accent: var(--accent-purple);">

        <!-- Diff 01: Landscape -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">01</span>
              <span>现代生成模型演进脉络与技术全景</span>
            </h3>
            <span class="study-topic-tag">技术路线全景</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p004_02.png' | relative_url }}" alt="生成模型技术脉络" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>技术演进脉络</strong>：DDPM → DiT（Transformer 骨干） → 分类器引导（CFG） → Flow Matching → 在线强化学习（Flow-GRPO）。</li>
              <li><strong>代表性前沿应用</strong>：扩散模型在自动驾驶端到端规划（Diffusion-Planner）与世界模型构建中成为事实标准。</li>
            </ul>
          </div>
        </article>

        <!-- Diff 02: World Models -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">02</span>
              <span>扩散模型在交互式世界模型中的落地应用</span>
            </h3>
            <span class="study-topic-tag">具身交互仿真</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p005_04.png' | relative_url }}" alt="世界模型交互框架" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>交互式多视角推演</strong>：扩散模型作为几何一致的仿真引擎，实现动作条件触发下的未来物理世界推演。</li>
              <li><strong>强化学习闭环微调</strong>：结合 RL 微调（如 WorldRFT），强化生成轨迹与自车规划的鲁棒对齐。</li>
            </ul>
          </div>
        </article>

        <!-- Diff 03: DDPM Forward Process -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">03</span>
              <span>DDPM 前向加噪过程与闭式解析式</span>
            </h3>
            <span class="study-topic-tag">马尔可夫加噪链</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p007_11.png' | relative_url }}" alt="DDPM前向加噪" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>马尔可夫高斯加噪链</strong>：前向过程按方差调度 β_t 逐步注入高斯噪声：q(x_t | x_{t-1}) = N(x_t; √(1 - β_t) x_{t-1}, β_t I)。</li>
              <li><strong>跨步闭式表达</strong>：利用独立高斯分布的可加性，任意时刻状态可由初始数据 x_0 单步解析采样生成。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">前向任意步闭式采样</span>
              <span class="formula-math">q(x_t | x_0) = N( x_t; &nbsp; √(ᾱ_t) x_0, &nbsp; (1 - ᾱ_t) I ), &nbsp; ᾱ_t = ∏[i=1 → t] (1 - β_i)</span>
            </div>
          </div>
        </article>

        <!-- Diff 04: Posterior derivation -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">04</span>
              <span>反向去噪过程与后验条件高斯分布</span>
            </h3>
            <span class="study-topic-tag">贝叶斯后验推导</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p008_12.png' | relative_url }}" alt="后验分布推导" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>真实后验解析解</strong>：在给定 x_0 条件下，单步逆向条件转移概率 q(x_{t-1} | x_t, x_0) 严格构成高斯分布。</li>
              <li><strong>后验参数闭式计算</strong>：均值 μ̃_t(x_t, x_0) 与方差 β̃_t 由当前状态 x_t 与原始状态 x_0 线性组合解析表达。</li>
            </ul>
          </div>
        </article>

        <!-- Diff 05: ELBO and KL Divergence -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">05</span>
              <span>变分下界（ELBO）逐项分解与 KL 散度匹配</span>
            </h3>
            <span class="study-topic-tag">变分下界优化</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p010_14.png' | relative_url }}" alt="ELBO变分下界" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>变分下界展开</strong>：对数似然下界分解为先验匹配项、重建项以及各中间步条件高斯分布之间的 KL 散度之和。</li>
              <li><strong>高斯 KL 散度闭式解</strong>：两个同方差高斯分布的 KL 散度直接退化为均值向量之间的 L2 欧式距离平方。</li>
            </ul>
          </div>
        </article>

        <!-- Diff 06: Noise Prediction parameterization -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">06</span>
              <span>参数重构：从预测均值转化为预测高斯噪声</span>
            </h3>
            <span class="study-topic-tag">网络输出参数化</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p011_15.png' | relative_url }}" alt="均值到噪声预测参数化" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>网络目标转化</strong>：将预测后验均值 μ_θ(x_t, t) 等价参数化为预测注入的高斯噪声 ε_θ(x_t, t)。</li>
              <li><strong>简化 MSE 损失</strong>：去除非关键加权因子后的无加权 MSE 损失大幅提升了生成样本的视觉保真度。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">DDPM 简化训练目标</span>
              <span class="formula-math">L_simple(θ) = E_{t, x_0, ε} [ || ε - ε_θ(x_t, t) ||² ]</span>
            </div>
          </div>
        </article>

        <!-- Diff 07: Tweedie and Score Matching -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">07</span>
              <span>分值函数（Score Function）与 Tweedie 恒等式</span>
            </h3>
            <span class="study-topic-tag">分值匹配联系</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p017_21.jpeg' | relative_url }}" alt="Score Matching与DDPM统一" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>分值函数物理定义</strong>：Score Function 定义为对数概率密度的空间梯度 ∇_x log p(x)，指向高维流形密度上升最快方向。</li>
              <li><strong>DDPM 与 Score 的精确等价</strong>：网络预测噪声与分值函数满足恒等式：∇_{x_t} log q_t(x_t) = - ε_θ(x_t, t) / √(1 - ᾱ_t)。</li>
              <li><strong>去噪分值匹配（DSM）</strong>：通过在加噪样本上优化条件分值模型，彻底规避了传统能量模型配分函数不可求的难题。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">Tweedie 公式与分值关系</span>
              <span class="formula-math">∇_{x_t} log q_t(x_t) = - ε_θ(x_t, t) / √(1 - ᾱ_t)</span>
            </div>
          </div>
        </article>

        <!-- Diff 08: ODE vs SDE math background -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">08</span>
              <span>常微分方程（ODE）与随机微分方程（SDE）数学基础</span>
            </h3>
            <span class="study-topic-tag">连续微积分理论</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p019_27.png' | relative_url }}" alt="ODE与SDE数学基础" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>ODE 确定性输运</strong>：由 dx/dt = f(x, t) 描述，给定初始状态后轨迹严格确定且唯一。</li>
              <li><strong>Itô SDE 随机过程</strong>：引入布朗运动增量 dw：dx = f(x, t) dt + g(t) dw，包含确定性漂移项与随机扩散项。</li>
            </ul>
          </div>
        </article>

        <!-- Diff 09: Langevin Dynamics -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">09</span>
              <span>退火朗之万动力学（Annealed Langevin Dynamics）</span>
            </h3>
            <span class="study-topic-tag">梯度流形采样</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p020_28.png' | relative_url }}" alt="朗之万动力学原理" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>分值引导物理漫步</strong>：利用预测分值梯度沿对数概率密度攀升，配合注入的高斯扰动跨越低概率势垒。</li>
              <li><strong>多尺度退火机制</strong>：从极大噪声尺度逐步降低至极小尺度，引导粒子从全局空间平稳收敛至高维数据流形。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">退火朗之万单步迭代</span>
              <span class="formula-math">x_{k+1} = x_k + (α_i / 2) ∇_x log p(x_k) + √(α_i) z_k, &nbsp; z_k ~ N(0, I)</span>
            </div>
          </div>
        </article>

        <!-- Diff 10: Continuous SDE Formulation -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">10</span>
              <span>连续时间 Itô SDE 统一加噪与逆向微积分</span>
            </h3>
            <span class="study-topic-tag">宋飏 Score SDE 范式</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p024_36.png' | relative_url }}" alt="连续时间SDE统一加噪" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>无限步长连续加噪</strong>：离散 DDPM 与 SMLD 被统一抽象为前向随机微分方程：dx = f(x, t) dt + g(t) dw。</li>
              <li><strong>安德森时间逆转定理</strong>：逆向去噪过程同样构成精确的 SDE，扩散项相同，漂移项依赖当前时刻分值函数修正。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">逆向去噪 Itô SDE</span>
              <span class="formula-math">dx = [ f(x, t) - g(t)² ∇_x log p_t(x) ] dt + g(t) dw̄</span>
            </div>
          </div>
        </article>

        <!-- Diff 11: Probability Flow ODE -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">11</span>
              <span>伴随概率流常微分方程（Probability Flow ODE）</span>
            </h3>
            <span class="study-topic-tag">确定性可逆采样</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p028_44.png' | relative_url }}" alt="伴随概率流ODE" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>伴随确定性系统</strong>：每一个扩散 SDE 都存在唯一的伴随常微分方程，其轨迹在每个时刻与 SDE 共享相同的瞬时边际概率分布。</li>
              <li><strong>双向可逆编码与精确似然</strong>：支持从数据精确反算唯一潜码，并能通过瞬时变量变化定理计算精确对数似然（Exact Likelihood）。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">伴随概率流 ODE</span>
              <span class="formula-math">dx = [ f(x, t) - (1/2) g(t)² ∇_x log p_t(x) ] dt</span>
            </div>
          </div>
        </article>

        <!-- Diff 12: PC Sampler & EMA -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">12</span>
              <span>预测器-校正器（PC）采样器与 EMA 权重平滑</span>
            </h3>
            <span class="study-topic-tag">工程数值稳定性</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/diffusion/p027_43.png' | relative_url }}" alt="PC采样器与EMA" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>预测器-校正器协同</strong>：数值求解器（Predictor）沿逆向 ODE 推进一个时间步，校正器（Corrector）运行退火朗之万 MCMC 消除数值积累误差。</li>
              <li><strong>EMA 参数滑动平均</strong>：指数滑动平均平滑了神经网络训练过程中的高频梯度抖动，显著提升生成图像质量与鲁棒性。</li>
            </ul>
          </div>
        </article>

      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SECTION 3: Reinforcement Learning                                   -->
    <!-- =================================================================== -->
    <div class="study-panel" data-panel="rl" id="rl" role="tabpanel">
      <div class="study-sec-head" style="--card-accent: var(--accent-green);">
        <p class="eyebrow">第 3 篇章 · 策略优化与对齐进化</p>
        <h2>Reinforcement Learning: From Policy Gradient to TRPO, PPO &amp; Post-Training Alignment (强化学习从策略梯度到 TRPO、PPO 与现代对齐架构)</h2>
        <p>
          从马尔可夫决策过程（MDP）与贝尔曼期望方程出发，系统解析策略梯度定理、值函数逼近（Actor-Critic）、
          信任域约束优化（TRPO）、近端策略优化（PPO）以及现代生成大模型在线强化学习对齐（GRPO / Flow-GRPO）。
        </p>
      </div>

      <div class="study-grid" style="--card-accent: var(--accent-green);">

        <!-- RL 01: MDP & Core Foundations -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">01</span>
              <span>马尔可夫决策过程（MDP）与强化学习形式化</span>
            </h3>
            <span class="study-topic-tag">MDP 决策框架</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/rl/p005_05.png' | relative_url }}" alt="MDP 决策链图解" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>五元组形式化定义</strong>：MDP 由 (S, A, P, R, γ) 构成，核心马尔可夫性指出未来状态转移仅取决于当前状态与动作，与历史轨迹条件独立。</li>
              <li><strong>交互与累计回报目标</strong>：智能体依据策略 π(a|s) 执行动作，目标是最大化折扣累计回报期望 G_t = ∑_{k=0}^∞ γ^k r_{t+k}。</li>
            </ul>
          </div>
        </article>

        <!-- RL 02: Value & Action-Value Functions -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">02</span>
              <span>状态价值 V(s) 与动作价值 Q(s, a) 的贝尔曼期望联系</span>
            </h3>
            <span class="study-topic-tag">贝尔曼自洽性方程</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/rl/p008_08.png' | relative_url }}" alt="状态价值与动作价值定义" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>概率加权转换关系</strong>：状态价值 V^π(s) 严格等于该状态下所有可选动作的动作价值 Q^π(s, a) 依策略分布 π(a|s) 的概率加权和。</li>
              <li><strong>贝尔曼自洽递推</strong>：Q^π(s, a) 由即时奖励加上后继状态的折现期望状态价值构成。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">状态价值与动作价值转换</span>
              <span class="formula-math">V^π(s) = ∑_{a ∈ A} π(a | s) Q^π(s, a), &nbsp; Q^π(s, a) = R(s, a) + γ ∑_{s'} P(s' | s, a) V^π(s')</span>
            </div>
          </div>
        </article>

        <!-- RL 03: TD Learning -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">03</span>
              <span>时序差分（TD）更新与自举（Bootstrapping）</span>
            </h3>
            <span class="study-topic-tag">单步低方差估计</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/rl/p010_10.png' | relative_url }}" alt="时序差分更新图解" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>自举估计机制</strong>：TD 算法利用一步真实奖励结合后继状态估计构成 TD Target：r_t + γ V(s_{t+1})，无需等待全轨迹结束。</li>
              <li><strong>低方差单步更新</strong>：通过计算 TD 误差 δ_t 实现参数在线微调，相比 Monte Carlo 具有更低的估计方差。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">时序差分误差（TD Error）</span>
              <span class="formula-math">δ_t = r_t + γ V(s_{t+1}) - V(s_t)</span>
            </div>
          </div>
        </article>

        <!-- RL 04: On-Policy vs Off-Policy -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">04</span>
              <span>同策略（On-Policy）与异策略（Off-Policy）本质</span>
            </h3>
            <span class="study-topic-tag">策略分类学</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/rl/p011_11.png' | relative_url }}" alt="On-Policy与Off-Policy对比" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>数据来源与优化目标</strong>：采样产生交互数据的行为策略（Behavior Policy）与待评估优化的目标策略（Target Policy）相同时为 On-Policy。</li>
              <li><strong>样本效率与稳定性折中</strong>：On-Policy（如 PPO）稳定性优越但数据用后即弃；Off-Policy（如 SAC, Q-Learning）支持经验回放池，样本效率极高。</li>
            </ul>
          </div>
        </article>

        <!-- RL 05: REINFORCE to Actor-Critic -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">05</span>
              <span>REINFORCE 蒙特卡洛策略梯度到 Actor-Critic</span>
            </h3>
            <span class="study-topic-tag">基线与方差削减</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/rl/p014_14.png' | relative_url }}" alt="REINFORCE与Actor-Critic差异" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>从全轨迹采样到状态价值评估</strong>：经典 REINFORCE 采用全轨迹回报 G_t 作为权重，方差巨大；引入 Critic 网络估计状态价值基线，将权重替换为优势函数。</li>
              <li><strong>策略梯度定理核心形式</strong>：策略梯度的期望形式由对数策略概率梯度乘以优势评估构成。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">策略梯度定理基本形式</span>
              <span class="formula-math">∇_θ J(θ) = E_{τ ~ π_θ} [ ∑_{t=0}^T ∇_θ log π_θ(a_t | s_t) · Q^π(s_t, a_t) ]</span>
            </div>
          </div>
        </article>

        <!-- RL 06: Actor-Critic Architecture -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">06</span>
              <span>Actor-Critic 双网络闭环协同机制</span>
            </h3>
            <span class="study-topic-tag">双网络闭环交互</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/rl/p019_19.png' | relative_url }}" alt="Actor-Critic闭环协同" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>Actor 策略决策</strong>：根据当前状态 s_t 输出动作分布 π_θ(a_t | s_t)，负责环境探索与动作执行。</li>
              <li><strong>Critic 价值打分</strong>：估计状态价值 V_ϕ(s_t)，计算时序差分误差 δ_t 作为 Actor 权重更新的自适应反馈评分。</li>
              <li><strong>协同更新闭环</strong>：Critic 沿 MSE 梯度最小化 TD Error，Actor 沿 Policy Gradient 方向最大化高分动作发生概率。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">Actor 参数更新表达式</span>
              <span class="formula-math">∇_θ J(θ) ≈ ∇_θ log π_θ(a_t | s_t) · [ r_t + γ V_ϕ(s_{t+1}) - V_ϕ(s_t) ]</span>
            </div>
          </div>
        </article>

        <!-- RL 07: TRPO Trust Region -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">07</span>
              <span>信任域策略优化（TRPO）与重要性采样约束</span>
            </h3>
            <span class="study-topic-tag">单调性能提升约束</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/rl/p020_20.png' | relative_url }}" alt="TRPO爬山直观比喻" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>防止策略崩溃的步长约束</strong>：策略更新步长过大会导致进入性能退化区域，TRPO 引入平均 KL 散度约束保证策略单调提升。</li>
              <li><strong>重要性采样比率</strong>：引入重要性采样比率 r_t(θ) = π_θ(a_t|s_t) / π_old(a_t|s_t)，支持利用旧策略轨迹多次优化新策略。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">TRPO 约束优化问题</span>
              <span class="formula-math">max_θ &nbsp; E[ r_t(θ) Â_t ], &nbsp; s.t. &nbsp; E[ D_KL( π_old(·|s) || π_θ(·|s) ) ] ≤ δ</span>
            </div>
          </div>
        </article>

        <!-- RL 08: PPO Clipped Surrogate -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">08</span>
              <span>近端策略优化（PPO）与裁剪目标函数（Clipped Surrogate Objective）</span>
            </h3>
            <span class="study-topic-tag">一阶高效工程优化</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/rl/p022_22.png' | relative_url }}" alt="PPO 裁剪目标曲线" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>一阶近似替代二阶共轭梯度</strong>：TRPO 求解二阶费雪信息矩阵（FIM）极其昂贵，PPO 巧妙提出一阶裁剪目标函数，兼具极高稳定度与计算效率。</li>
              <li><strong>保守悲观估计</strong>：通过 clip(r_t(θ), 1 - ε, 1 + ε) 截断概率比率，当优势 Â_t > 0 时抑制过度自信，当 Â_t < 0 时防止毁灭性负向更新。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">PPO 裁剪目标损失（Clipped Surrogate）</span>
              <span class="formula-math">L_CLIP(θ) = E_t [ min( r_t(θ) Â_t, &nbsp; clip(r_t(θ), 1 - ε, 1 + ε) Â_t ) ]</span>
            </div>
          </div>
        </article>

        <!-- RL 09: GAE Generalized Advantage Estimation -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">09</span>
              <span>广义优势估计（GAE）：偏差与方差的优雅平衡</span>
            </h3>
            <span class="study-topic-tag">优势函数优化</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/rl/p023_23.png' | relative_url }}" alt="GAE多步优势融合" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>多步 TD 误差指数加权</strong>：GAE 定义为不同跨度 TD 优势估计的指数加权平均：Â_t^GAE(γ, λ) = ∑_{l=0}^∞ (γ λ)^l δ_{t+l}^V。</li>
              <li><strong>λ 调节杠杆</strong>：λ = 0 退化为单步 TD（低方差高偏差），λ = 1 退化为 Monte Carlo（无偏高方差），λ ∈ [0.9, 0.95] 达成最优收敛性能。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">GAE 优势函数表达式</span>
              <span class="formula-math">Â_t^GAE(γ, λ) = ∑_{l=0}^∞ (γ λ)^l δ_{t+l}^V, &nbsp; δ_t^V = r_t + γ V(s_{t+1}) - V(s_t)</span>
            </div>
          </div>
        </article>

        <!-- RL 10: End-to-End PPO Loop -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">10</span>
              <span>PPO 完整训练流水线与多目标联合优化</span>
            </h3>
            <span class="study-topic-tag">工程执行流程</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/rl/p024_24.png' | relative_url }}" alt="PPO训练伪代码与流程" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>多目标联合损失</strong>：联合最小化裁剪策略损失、Critic 价值回归均方误差损失，并加入策略熵正则项 S[π_θ] 鼓励持续探索。</li>
              <li><strong>流水线迭代步骤</strong>：环境交互采样（Rollout） → 计算 GAE 优势值 → 构造 Mini-batch 执行 K 轮参数更新。</li>
            </ul>
            <div class="study-formula-box">
              <span class="formula-title">PPO 总目标函数</span>
              <span class="formula-math">L_TOTAL(θ) = E_t [ L_CLIP(θ) - c_1 · L_VF(θ) + c_2 · S[π_θ](s_t) ]</span>
            </div>
          </div>
        </article>

        <!-- RL 11: Modern Alignment & GRPO -->
        <article class="study-card">
          <header class="study-card-header">
            <h3 class="study-card-title">
              <span class="study-badge">11</span>
              <span>前沿演进：GRPO 与 Flow-GRPO 生成对齐</span>
            </h3>
            <span class="study-topic-tag">生成模型后训练对齐</span>
          </header>
          <figure class="study-card-media">
            <img src="{{ '/assets/media/blog/generative_foundations/rl/p028_28.png' | relative_url }}" alt="DiT与生成骨干结合" loading="lazy">
            <span class="zoom-hint">点击放大</span>
          </figure>
          <div class="study-card-body">
            <ul class="study-takeaways">
              <li><strong>GRPO 去 Critic 架构</strong>：对同一提示词采样一组生成结果计算相对优势值，完全省去独立的价值网络，大幅节省训练显存。</li>
              <li><strong>Flow-GRPO 赋能扩散与流匹配</strong>：将策略优化直接作用于 Flow Matching / Diffusion 的去噪轨迹，使世界模型直接面向规划与任务指标优化。</li>
            </ul>
          </div>
        </article>

      </div>
    </div>

    <!-- Acknowledgement Footer Note -->
    <footer class="study-ack-card">
      <div class="study-ack-icon">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
        </svg>
      </div>
      <p class="study-ack-text">
        <strong>学习记录与致谢说明</strong>：
        本篇学习笔记基于连续流匹配理论、连续时间随机微分方程与现代强化学习策略梯度的数学推导和开源技术生态整理构建。
        部分推导逻辑与架构学习记录参考同事 <strong>niu yao</strong> 的研讨分享，特此记录致谢。
      </p>
    </footer>

  </div>
</article>