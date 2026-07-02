---
layout: default
title: "从互联网到物理世界：具身智能的数据革命从哪里开始？"
description: "一份关于具身智能数据采集的工作笔记——在保真·接触、规模·成本、跨本体三者难以兼得的约束下，遥操作、仿真、UMI、Ego 各自下了什么赌注。"
date: 2026-06-25
hide_news: true
tags: ["embodied-ai", "data", "vla", "reading"]
category: embodied-ai
cover: "/assets/media/blog/embodied_ai_data/remote_data_acquisition.mp4"
cover_type: video
atlas:
  variant: noir
  eyebrow: "Data · Embodied AI"
  title: "在不可能三角上推进：保真·接触 / 规模·成本 / 跨本体，三者难以兼得"
  caption: "左→右是时间与轻量化方向。每个节点三根竖条＝它在三角上的取舍（高＝该轴更优）。Hover 看原理·难点·判断。"
  cols: 6
  nodes:
    - id: teleop
      col: 1
      row: 1
      kind: input
      accent: ink
      tag: "保真锚点"
      title: "① 遥操作"
      desc: "主从 / VR 直驱真机"
      score: [95, 22, 16]
      receives: "操作员经主从臂 / VR / 外骨骼直驱真机，同步记录关节角、夹爪、相机"
      logic: "动作直接产生在目标本体，无重定向误差，保真度最高；但成本高、依赖真机、难放大"
      sends: "Open X-Embodiment 汇集 22 平台、140 万条轨迹，RT-X 约 50% 正向跨形态迁移；DROID 7.6 万条、564 场景"
      gives: "保真上限高、规模上限低的参照系"
      note: "数据与本体强绑定，形成一机一数据的孤岛。后面每条路线都在回答同一个问题——能不能不要真机。"
    - id: sim
      col: 2
      row: 1
      kind: process
      accent: blue
      tag: "边际趋零"
      title: "② 仿真合成"
      desc: "模拟器批量造场景"
      score: [40, 95, 60]
      receives: "Isaac Sim / MuJoCo 批量生成场景，边际成本接近零，能安全覆盖碰撞、跌落等长尾"
      logic: "Sim-to-Real Gap——接触动力学、传感器噪声、光影难以复现"
      sends: "对 locomotion / 全身控制 / 导航很好用；接触密集的精细操作纯仿真仍吃力"
      gives: "好用，但精细接触是它的天花板"
      note: "接触密集任务采不动的那部分，正是后文世界模型做数据引擎想接管的地方。"
    - id: humanvideo
      col: 3
      row: 1
      kind: process
      accent: cyan
      tag: "互联网级"
      title: "③ 人类视频"
      desc: "被动观察，无动作标签"
      score: [20, 98, 42]
      receives: "直接用互联网上的人类操作视频做预训练"
      logic: "只有结果没有控制量——看得到做什么，学不到怎么发力、走什么轨迹"
      sends: "数据层级：互联网视频 → ego 视频 → 带动作机器人数据 → 特定机器人数据，越往下越稀缺、质量越高"
      gives: "适合做物理常识与任务规划先验，不能直接当底层控制信号"
      note: "这条层级结构解释了为什么要一路往 ego、往带动作的数据走——稀缺的那端才是控制信号。"
    - id: umi
      col: 4
      row: 1
      kind: process
      accent: purple
      tag: "砍掉真机"
      title: "④ UMI"
      desc: "手持夹爪 + 一颗 GoPro"
      score: [80, 70, 90]
      receives: "斯坦福 2024（RSS）：手持平行夹爪 + 一颗 GoPro 作唯一传感器，配相对轨迹动作与推理期延迟匹配，策略与硬件无关"
      logic: "最难的不是拍画面，而是恢复精确 6-DoF 末端位姿；依赖 ORB-SLAM3，是整条流水线最脆弱一环，尺度模糊、运动模糊直接限制精度"
      sends: "155° 鱼眼 + 夹爪两侧镜面给隐式立体；演进 FastUMI（T265 直读位姿）/ UMI-3D（末端激光雷达）/ TacUMI（指尖触觉）"
      gives: "末端把动作与接触采到最准，但先天看不到全局——这是定位决定的，不是 bug"
      note: "纯视觉里接触帧通常不足 10%，面对易碎/可变形物体鲁棒性不足；数据集在斯坦福一个雨周采的，强直射阳光下就不灵。"
    - id: ego
      col: 5
      row: 1
      kind: process
      accent: green
      tag: "人类行为级"
      title: "⑤ Ego"
      desc: "头显相机 + 3D 手姿"
      score: [55, 76, 50]
      receives: "戴头显相机（Aria / Vision Pro / GoPro），双手最自然地完成任务，记录第一人称视频 + 头动 + 3D 手指姿态"
      logic: "具身鸿沟——人手 20+ 自由度对夹爪 1 自由度（通俗类比），直接重定向常导致操作失败；头动带来分布偏移"
      sends: "Ego4D 约 3,670 小时；EgoDex（Apple 2025）829 小时、194 桌面任务，目前最大的灵巧操作数据集"
      gives: "把脑/小脑那层采得最全，末端精度与接触是短板——和 UMI 正好互补"
      note: "反直觉但最有说服力：1 小时 Aria 人手数据对性能的贡献超过多采 1 小时机器人遥操作；2 小时机器人 + 1 小时手部强于 3 小时纯机器人。"
    - id: converge
      col: 6
      row: 1
      kind: contribution
      accent: warn
      pulse: true
      tag: "2026 共识"
      title: "⑥ Ego + UMI / 世界模型"
      desc: "脑手协同 + 数据引擎"
      score: [85, 85, 88]
      receives: "Ego＝脑与小脑（在哪、去哪、干什么、长程规划）；UMI＝末端执行器（抓取、用力、毫米微操、接触控制）"
      logic: "纯堆量会负迁移；前沿转向把数据当可生成资源——世界模型做数据引擎，但要防具身幻觉"
      sends: "GEN-0 超 27 万小时验证 scaling law；GigaBrain-0 约 1000 小时真机 + 生成数据，0.1 放大到 1 万小时"
      gives: "从在目标机器人上采动作，走向在真实世界采人类意图与接触、再重定向/生成到任意本体"
      note: "human-transfer 用 SAM2 + 逆运动学把第一人称人类视频转成机器人视角——这恰好是 Ego 路线的天然出口。"
  edges:
    - { from: teleop, to: sim, kind: flow }
    - { from: sim, to: humanvideo, kind: flow }
    - { from: humanvideo, to: umi, kind: flow }
    - { from: umi, to: ego, kind: flow }
    - { from: ego, to: converge, kind: flow }
atlas_b:
  variant: noir
  eyebrow: "Convergence"
  title: "脑手协同：Ego 给全局，UMI 给末端"
  caption: "上泳道＝感知/规划（Ego），下泳道＝末端/接触（UMI），向右汇入完整具身数据。"
  cols: 2
  nodes:
    - id: ego2
      col: 1
      row: 1
      kind: process
      accent: green
      tag: "Brain"
      title: "Ego · 感知 / 规划"
      desc: "在哪、去哪、怎么协同"
      receives: "第一人称视频 + 头动 + 3D 手姿"
      logic: "全局空间上下文 + 任务规划 + 失败/恢复闭环"
      sends: "环境与意图"
      gives: "回答在哪、去哪、长程怎么协同"
    - id: umi2
      col: 1
      row: 3
      kind: process
      accent: purple
      tag: "Hand"
      title: "UMI · 末端 / 接触"
      desc: "抓取、用力、毫米微操"
      receives: "手持夹爪 + 视觉（+ 触觉/力觉的演进）"
      logic: "恢复末端 6-DoF 位姿与接触力，做毫米级交互"
      sends: "精细动作与接触信号"
      gives: "回答怎么抓、怎么用力、怎么贴合"
    - id: data2
      col: 2
      row: 2
      kind: contribution
      accent: warn
      pulse: true
      tag: "Output"
      title: "完整具身数据"
      desc: "环境—动作—接触—结果闭环"
      receives: "Ego 全局 + UMI 末端"
      logic: "同手佩戴 Ego 设备 + 手持/穿戴带触觉力觉的无本体采集件"
      sends: "不引入真机成本的闭环数据"
      gives: "全局规划 ＋ 末端接触，缺一不可"
  edges:
    - { from: ego2, to: data2, kind: flow }
    - { from: umi2, to: data2, kind: flow }
---
<article class="bx reveal">
  <header class="bx-hero">
    <div class="bx-hero-inner">
      <p class="eyebrow">工作笔记 · 具身智能 · 数据采集</p>
      <h1>{{ page.title }}</h1>
      <p class="bx-byline">表面是模型与算法之争，底层是数据从哪来、质量够不够、能不能跨本体复用之争。下面每一种采集范式，都是在同一个三角约束下的一个不同赌注。</p>
    </div>
    <blockquote class="bx-lede">
      当前领域的共识是：约束 VLA 进展的是数据，而不是架构或算力。但要写出深度，得点破第二层——瓶颈已经不是机器人数据不够多。把异构机器人数据简单混合常引发负迁移；一个精挑的 5% 子集就能恢复整套数据 85–90% 的性能；真正决定泛化的，是采集时刻意制造的多样性。所以问题不是采更多，而是怎样同时拿到动作/接触高保真、采集低成本可规模化、跨本体可复用——这三者难以兼得。
    </blockquote>
  </header>

  <div class="bx-shell" data-proj-shell>
    <nav class="proj-toc" data-proj-toc aria-label="On this page">
      <button class="proj-toc-toggle" type="button" data-toc-toggle aria-expanded="true" aria-label="Toggle contents">
        <span class="toc-title">目录</span>
        <svg class="toc-chevron" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
      </button>
      <nav class="proj-toc-nav"><ol data-toc-list></ol></nav>
    </nav>

    <div class="project-body-main bx-body">

      <section class="bx-section">
        <h2>瓶颈不在数据多少，在数据从哪来</h2>
        <p class="bx-callout">
          把异构机器人数据简单混合常常让模型变差；现有语料里大量数据其实在做无用功；而只覆盖训练分布内的数据几乎无法迁移到新环境。结论很直接：决定上限的不是数据量，是数据的来源与多样性。
        </p>
        <p class="bx-note-line">
          于是所有采集范式都被同一个三角钉住——保真·接触、规模·成本、跨本体，按下一个就翘起另一个。把这条「在三角约束下推帕累托前沿」的线索讲清楚，就是这篇的骨架。
        </p>

        <figure class="tri">
          <svg viewBox="0 0 200 170" role="img" aria-label="不可能三角">
            <polygon class="tri-edge" points="100,18 22,150 178,150"/>
            <circle class="tri-dot" cx="100" cy="18" r="4"/>
            <circle class="tri-dot" cx="22" cy="150" r="4"/>
            <circle class="tri-dot" cx="178" cy="150" r="4"/>
            <text class="tri-v" x="100" y="12" text-anchor="middle">保真·接触</text>
            <text class="tri-v" x="20" y="165" text-anchor="middle">规模·成本</text>
            <text class="tri-v" x="180" y="165" text-anchor="middle">跨本体</text>
          </svg>
          <p class="tri-note"><b>三者难以兼得。</b>遥操作锚住保真却放不大；仿真把规模做到极致却隔着现实鸿沟；UMI 用硬件解耦换跨本体，却丢了全局视野与触觉。没有谁三个顶点全占，所有进展都是在这条边上挪动。</p>
        </figure>

        <p class="bx-note-line">下图把六种范式排到这条演进轴上。三根竖条直观给出每种范式在三角上的得分；hover 任一节点，看它的一句原理、一个核心难点、一句判断。</p>
        {% include logic-atlas.html %}
      </section>

      <section class="bx-section">
        <h2>遥操作：保真锚点，但不可规模化</h2>
        <p>操作员通过主从臂、VR 或外骨骼直接驱动真机，关节角、夹爪、相机同步落盘。动作直接产生在目标本体上，没有重定向误差，保真度是所有路线里最高的。Open X-Embodiment 把 22 个平台、140 万条轨迹拼起来，训出的 RT-X 表现出约 50% 的正向跨形态迁移；DROID 又补了 7.6 万条轨迹、564 个场景。</p>
        <p>代价也最直接：成本高、依赖真机、受制于人工，对操作员还不直观、缺力反馈。更关键的是数据与本体强绑定，形成「一机一数据」的孤岛。把它当成参照系就好——保真上限高、规模上限低，后面所有路线本质都在问同一句：能不能不要真机。</p>
        <figure class="bx-video">
          <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/blog/embodied_ai_data/remote_data_acquisition.mp4' | relative_url }}" type="video/mp4"></video>
          <figcaption><strong>遥操作。</strong>主从直驱真机，动作落在目标本体上——保真最高，但放不大。</figcaption>
        </figure>
      </section>

      <section class="bx-section">
        <h2>仿真：边际成本趋零，但隔着现实鸿沟</h2>
        <p>物理模拟器（Isaac Sim / MuJoCo）批量生成场景，边际成本接近零，还能安全覆盖碰撞、跌落这类长尾。对 locomotion、全身控制、导航非常好用。难点是 Sim-to-Real Gap——接触动力学、传感器噪声、光影都不好复现。判断很清楚：越是接触密集的精细操作，纯仿真越吃力，而这恰恰是后面世界模型想接管的那块。</p>
        <figure class="bx-video">
          <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/blog/embodied_ai_data/sim_data.mp4' | relative_url }}" type="video/mp4"></video>
          <figcaption><strong>仿真。</strong>边际成本趋零、长尾可控；接触密集任务仍隔着一道现实鸿沟。</figcaption>
        </figure>
      </section>

      <section class="bx-section">
        <h2>人类视频：互联网级规模，但没有动作标签</h2>
        <p>直接拿互联网上的人类操作视频做预训练，规模一步到位。问题是只有「结果」没有「控制量」：看得到做什么，学不到怎么发力、怎么走轨迹。机器人数据有一条清晰的层级——互联网视频 → 第一人称 ego 视频 → 带动作的机器人数据 → 特定机器人带动作数据，越往下越稀缺、质量越高。判断：人类视频适合做物理常识与任务规划的先验，但当不了底层控制信号。这条层级也解释了为什么后面要一路往 ego、往带动作的数据走。</p>
      </section>

      <section class="bx-section">
        <h2>UMI：砍掉真机，但视野与触觉是代价</h2>
        <p>斯坦福 2024（RSS）的 UMI 给出一个很省的方案：一个手持平行夹爪加一颗 GoPro 作为唯一传感器，配合相对轨迹动作表示和推理期延迟匹配，让学到的策略与硬件无关、可跨多种机器人部署。155° 鱼眼广角，夹爪两侧加物理镜面提供隐式立体信息。</p>
        <p>真正的脏细节在位姿。手持设备最难的不是拍画面，而是恢复精确的 6-DoF 末端位姿——UMI 依赖 ORB-SLAM3，这是整条流水线里最脆弱的一环，尺度模糊、运动模糊会直接限制能做的任务精度。纯视觉里接触帧通常不足 10%，面对易碎、可变形物体鲁棒性不足；数据集是在斯坦福一个雨周采的，策略在强直射阳光下就不灵。</p>
        <p>领域在主动给它打补丁，这才是深度所在：FastUMI 用 RealSense T265 直接读 6-DoF 位姿，绕开笨重的离线 SLAM，FastUMI-100K 给到 10 万+ 轨迹、54 个任务；UMI-3D 把激光雷达放到末端，拿到米制尺度，让拉窗帘、开门、严重遮挡这些原本采不了的任务变得可规模采集；TacUMI 在指尖加触觉、腕部加六维力，用可锁夹爪把操作员手部施力从力数据里剔除；MV-UMI / ActiveUMI 补多视角，解决腕部视角的环境盲区。判断：UMI 的本质是在末端把动作和接触采到最准，但先天看不到全局——这是定位决定的，不是 bug。</p>
        <figure class="bx-video">
          <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/blog/embodied_ai_data/UMI_data.mp4' | relative_url }}" type="video/mp4"></video>
          <figcaption><strong>UMI。</strong>手持夹爪 + 一颗相机，眼在手上→毫米级接触细节；代价是全局上下文与触觉。</figcaption>
        </figure>
      </section>

      <section class="bx-section">
        <h2>Ego：人类行为级，但具身鸿沟难跨</h2>
        <p>戴上头显相机（Aria / Vision Pro / GoPro），用双手最自然地完成任务，记录第一人称视频、头动和 3D 手指姿态。规模上，Ego4D 约 3,670 小时，EgoDex（Apple 2025）829 小时、194 个桌面任务，是目前最大的灵巧操作数据集。</p>
        <p>最有说服力的是一个反直觉结果：EgoMimic 发现用 Aria 采的 1 小时人类第一人称手部数据，对策略性能的贡献超过多采 1 小时机器人遥操作；2 小时机器人数据加 1 小时手部数据，强于 3 小时纯机器人数据——这直接改写了成本账。方法上，EgoVLA 先在大规模人类第一人称数据上预训练，再用少量机器人演示微调，用 IK 重定向把人手动作转成机器人动作。短板也明确：具身鸿沟让直接重定向常常失败，头部相机在毫米级微操时易遮挡，人主动协调头手带来的分布偏移机器人复刻不了。判断：Ego 把脑/小脑那层采得最全，末端精度和接触正好是它的缺口——和 UMI 互补。</p>
        <figure class="bx-video">
          <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/blog/embodied_ai_data/Ego_data.mp4' | relative_url }}" type="video/mp4"></video>
          <figcaption><strong>Ego。</strong>第一人称带来全局上下文、任务规划与真实手感，外加失败/恢复的闭环数据。</figcaption>
        </figure>
      </section>

      <section class="bx-section">
        <h2>收敛：Ego + UMI（2026 的共识，不是二选一）</h2>
        <p>分工已经很清楚：Ego 是脑与小脑，负责在哪、去哪、干什么、身体如何协同、长程规划；UMI 是末端执行器，负责精准抓取、用力、毫米微操、接触控制。落地形态也不复杂——同手佩戴 Ego 设备，再加一个手持或穿戴、带触觉力觉的无本体采集件，在不引入真机成本的前提下，同时留下环境、动作、接触、结果的闭环。</p>
        <p class="bx-eq">完整具身数据　＝　<b>Ego</b>（全局环境与任务规划）<span class="eq-arrow">＋</span><span class="eq-cyan">UMI</span>（末端精细操作与接触控制）</p>
        {% include logic-atlas.html atlas=page.atlas_b %}
        <figure class="bx-video is-wide">
          <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/blog/embodied_ai_data/egoguide_umi.mp4' | relative_url }}" type="video/mp4"></video>
          <figcaption><strong>Ego + UMI 融合。</strong>头上采全局与意图，手上采动作与接触——两条信息流汇成一条闭环。</figcaption>
        </figure>
      </section>

      <section class="bx-section">
        <h2>趋势：把数据当作可生成的资源</h2>
        <p>规模正在到来。GEN-0 用超过 27 万小时真实交互数据训练通用操作策略，验证了机器人领域的 scaling law；Build AI 在 2025 年底放出 10 万小时来自真实工厂工人的第一人称数据集；模仿学习的性能也确实随高质量数据量呈幂律提升。</p>
        <p>但纯堆量不是答案——负迁移和 coreset 已经说明问题。于是前沿转向把数据当作可生成的资源，让世界模型做数据引擎：GigaBrain-0 用约 1000 小时真机数据加世界模型生成数据训练，显著降低对真机的依赖，0.1 版把规模放大到 1 万小时；GigaWorld-0 把视频生成、3D 高斯泼溅、可微系统辨识与可执行运动规划缝在一起，当高保真数据引擎；其中 human-transfer 用 SAM2 加逆运动学，把第一人称人类视频转成机器人视角——这正是 Ego 路线的天然出口。要给生成留个冷静的注脚：现有方法要么只做表面视觉增强，要么会产生具身幻觉、生成物理上不可行的动作，所以把生成锚定在渲染出的机器人运动上，正在成为必要手段。</p>
      </section>

      <section class="bx-section">
        <h2>几条判断</h2>
        <ul class="bx-takeaways">
          <li>整条演进的方向，是从「在目标机器人上采动作」，走向「在真实世界里采人类意图与接触，再重定向或生成到任意本体」。</li>
          <li>两个长期不变的硬问题：一是从人类演示里恢复准确的动作与力标签；二是闭合具身差异加观测差异。每个系统都是对这两点的一个赌注。</li>
          <li>力觉/触觉是下一道真正的护城河——视频永远拍不到力信号，这条缺口靠加大视频量补不上。</li>
          <li>真正的瓶颈也许不在采集，而在评测——真实世界评测昂贵、耗时、常常不安全。采集解决了「从哪来」，评测才决定「能不能用」。</li>
        </ul>
        <p class="bx-note-line" style="margin-top:1.1rem">注：遥操作成本（约 100–200 美元/小时）、熟练操作员吞吐（约每小时 5–50 段）、Ego 单人日产出（约 8 小时以上、人民币百元/小时级），以及人手「20+ 自由度 vs 夹爪 1 自由度」的对比，均为业内估算或通俗类比，非已核实定值。</p>
      </section>

    </div>
  </div>
</article>
