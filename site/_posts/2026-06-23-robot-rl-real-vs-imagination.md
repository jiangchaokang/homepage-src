---
layout: default
title: "机器人怎么\"练\"出来：在真实世界里，还是在想象里"
description: "以 RECAP / π*0.6（真实世界做 RL）和 RISE（世界模型内做 RL）为两条主线，讲清楚 VLA 为什么单靠模仿学不好、两种破局路线各自的本质与代价。"
date: 2026-06-23
hide_news: true
tags: ["vla", "world-model", "rl", "reading"]
category: embodied-ai
cover: "/assets/media/blog/rise_pi06/rise_methodology_Compositional_world_model.mp4"
cover_type: video
atlas:
  variant: noir
  eyebrow: "Reading · RISE × π*0.6 / RECAP"
  title: "模仿撞上复合误差，分叉成两条破局路线"
  caption: "起点是模仿学习，瓶颈是 compounding error，往下分出真实世界 RL 与想象空间 RL；底部是两条路共享的内核。点击任一节点固定详情。"
  cols: 4
  legend:
    - { accent: ink, label: "起点 · 模仿学习" }
    - { accent: warn, label: "瓶颈" }
    - { accent: blue, label: "路线 A · 真实世界 RL" }
    - { accent: purple, label: "路线 B · 想象空间 RL" }
    - { accent: cyan, label: "两条路共享的内核" }
  nodes:
    - id: imitation
      col: 1
      span: 4
      row: 1
      kind: input
      accent: ink
      tag: "Start"
      title: "模仿学习"
      desc: "有时成功，难次次成功"
      receives: "演示数据（专家轨迹）"
      logic: "监督拟合动作，不与环境闭环纠错"
      sends: "一个会模仿、但会漂移的策略"
      gives: "VLA 的起点，也是它的天花板"
    - id: bottleneck
      col: 1
      span: 4
      row: 2
      kind: reason
      accent: warn
      pulse: true
      tag: "Bottleneck"
      title: "compounding error"
      desc: "小错→更陌生状态→失败"
      receives: "模仿策略在闭环里持续执行"
      logic: "一旦偏离演示分布，错误开始累积（covariate shift）"
      sends: "次次成功的障碍"
      gives: "控制策略特有，LLM 没有这个困境"
      note: "这就是 LLM 靠监督够、VLA 不够的根因——静态输出不与环境连续交互，自然没有复合误差。"
    - id: recap
      col: 1
      span: 2
      row: 3
      kind: process
      accent: blue
      tag: "真实世界 RL"
      title: "RECAP / π*0.6"
      desc: "在真实世界里练"
      receives: "演示 + 自主运行 + 专家干预"
      logic: "价值函数算优势 → 转成优势条件化的监督学习"
      sends: "难任务成功率 >90%"
      gives: "把真实世界 RL 做对"
      note: "RECAP＝RL with Experience and Corrections via Advantage-conditioned Policies；监督基座 π0.6 经 RECAP 训练得到 π*0.6。"
    - id: rise
      col: 3
      span: 2
      row: 3
      kind: process
      accent: purple
      tag: "想象空间 RL"
      title: "RISE"
      desc: "在想象里练"
      receives: "真实数据（离线，占比 0.6）"
      logic: "组合式世界模型里 rollout，优势条件化训练"
      sends: "brick +35% / backpack +45% / box +35%"
      gives: "进一步做到不依赖真机在线 RL"
      note: "暖身阶段沿用 RECAP 的优势条件化框架——所以二者是递进，不是对立。"
    - id: kernel
      col: 2
      span: 2
      row: 4
      kind: contribution
      accent: cyan
      tag: "共享内核"
      title: "优势条件化 + flow matching"
      desc: "把 RL 变监督，保留全部数据"
      receives: "好动作与坏动作都留下"
      logic: "二值或分箱优势当条件；flow matching 生成连续动作"
      sends: "可 scale 的策略提取"
      gives: "两条路共享的地基"
      note: "对扩散/流匹配策略直接做策略梯度很难；条件化把 RL 变监督、还能吃下全部数据，是当前最务实的 scale 路线。"
  edges:
    - { from: imitation, to: bottleneck, kind: flow }
    - { from: bottleneck, to: recap, kind: flow }
    - { from: bottleneck, to: rise, kind: flow }
    - { from: recap, to: rise, kind: dashed }
    - { from: kernel, to: recap, kind: solid }
    - { from: kernel, to: rise, kind: solid }
atlas_rise:
  variant: noir
  eyebrow: "RISE · Compositional World Model"
  title: "把 RL 环境搬进想象空间"
  caption: "真实数据离线锚定 → 动态模型与价值模型分别优化 → 想象里 rollout/算优势 → 策略优化 → 真机推理零额外开销。"
  cols: 2
  legend:
    - { accent: warn, label: "离线真实数据" }
    - { accent: blue, label: "动态模型 D" }
    - { accent: purple, label: "价值模型 V" }
    - { accent: cyan, label: "想象空间 rollout" }
    - { accent: green, label: "策略优化与部署" }
  nodes:
    - id: rdata
      col: 1
      span: 2
      row: 1
      kind: input
      accent: warn
      tag: "Offline 0.6"
      title: "真实数据（离线）"
      desc: "占比 0.6 锚定"
      receives: "真机演示与经验"
      logic: "用真实数据锚住，防止策略在想象里钻空子漂移"
      sends: "离线锚 + 策略暖身"
      gives: "对冲世界模型保真度风险"
      note: "消融显示 offline 占比 0.6 最优；online 的 action 与 state 都不可或缺。"
    - id: dyn
      col: 1
      span: 1
      row: 2
      kind: process
      accent: blue
      tag: "Model D"
      title: "动态模型 D"
      desc: "想象多视角未来"
      receives: "当前状态 + 动作"
      logic: "高效视频扩散预测多视角未来画面"
      sends: "想象出的下一状态"
      gives: "可控的物理"
    - id: val
      col: 2
      span: 1
      row: 2
      kind: process
      accent: purple
      tag: "Model V"
      title: "价值模型 V"
      desc: "评估状态 → 优势"
      receives: "想象出的状态"
      logic: "进度敏感的价值评估"
      sends: "优势信号"
      gives: "想象里的裁判"
    - id: rollout
      col: 1
      span: 2
      row: 3
      kind: reason
      accent: cyan
      pulse: true
      tag: "Imagine"
      title: "想象空间 rollout"
      desc: "以最优优势为条件"
      receives: "D 的未来 + V 的优势"
      logic: "策略在世界模型里交互，产生 rollout 数据"
      sends: "rollout 数据"
      gives: "全程无需真机交互"
    - id: opt
      col: 1
      span: 2
      row: 4
      kind: process
      accent: green
      tag: "Train"
      title: "策略优化"
      desc: "优势条件化训练"
      receives: "rollout 数据 + 离线锚"
      logic: "behavior policy 在优势条件化方案下训练"
      sends: "更强的策略"
      gives: "自改进闭环"
    - id: infer
      col: 1
      span: 2
      row: 5
      kind: contribution
      accent: green
      tag: "Deploy"
      title: "真机推理"
      desc: "零额外开销"
      receives: "训练好的策略"
      logic: "直接部署到真机"
      sends: "动作"
      gives: "想象里练好，真机零额外开销"
  edges:
    - { from: rdata, to: dyn, kind: flow }
    - { from: rdata, to: val, kind: flow }
    - { from: dyn, to: rollout, kind: flow }
    - { from: val, to: rollout, kind: flow }
    - { from: rollout, to: opt, kind: flow }
    - { from: opt, to: infer, kind: flow }
    - { from: opt, to: rollout, kind: loop }
---
<article class="bx reveal">
  <header class="bx-hero">
    <div class="bx-hero-inner">
      <p class="eyebrow">工作笔记 · VLA · 强化学习</p>
      <h1>机器人怎么“练”出来：在真实世界里，还是在想象里</h1>
      <p class="bx-byline">模仿能让 VLA 有时成功，却很难次次成功。两条破局路线攻的是同一个根问题的不同瓶颈——一条在真机上练，一条在世界模型里练。</p>
    </div>
    <blockquote class="bx-lede">
      VLA 单靠模仿学不好，根子在 compounding error：模型一旦犯小错，就进入演示数据没覆盖的状态，于是更容易犯更大的错，误差累积直至失败。这是控制策略特有的困境——LLM 这类静态输出系统没有。RECAP 和 RISE 给了两种答案：把真实世界 RL 做对，或者干脆不依赖真实世界 RL。
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
        <h2>发展脉络：一个瓶颈，两条破局路线</h2>
        <p class="bx-note-line">主图先把全局摆出来：模仿学习撞上复合误差，分叉成真实世界 RL（RECAP / π*0.6）与想象空间 RL（RISE）。两条路共享同一个内核——优势条件化加 flow matching；RISE 的暖身还直接复用了 RECAP 的框架，所以是递进关系。</p>
        {% include logic-atlas.html %}
      </section>

      <section class="bx-section">
        <h2>从模仿学习的天花板讲起</h2>
        <p>VLA 用模仿学习，能「有时成功」，难「次次成功」。原因是 compounding error，也就是 covariate shift：策略只在演示分布里见过世界，一旦犯个小错，就滑进演示没覆盖的状态，在陌生状态里更容易犯更大的错，越错越陌生，直到失败。</p>
        <p>要点在于，这是控制策略特有的问题——它持续和环境交互，错误会沿时间复合。LLM 这类静态输出系统没有这个困境，给定输入就给一次输出，不存在「上一步的错把下一步推向更糟」。这也正是「LLM 靠监督就够、VLA 不够」的根因。</p>
        <div class="cyc">
          <span class="cyc-step">小错误</span><span class="cyc-arr">→</span>
          <span class="cyc-step">进入演示未覆盖的状态</span><span class="cyc-arr">→</span>
          <span class="cyc-step">更大的错误</span><span class="cyc-arr">→</span>
          <span class="cyc-step">更陌生的状态</span><span class="cyc-arr">→</span>
          <span class="cyc-step is-fail">失败</span>
          <p class="cyc-back">误差在闭环里累积——这就是模仿的天花板，也是控制策略区别于静态 LLM 的地方。</p>
        </div>
      </section>

      <section class="bx-section">
        <h2>路线 A：RECAP / π*0.6 —— 在真实世界里练</h2>
        <p>RECAP 的全称是 RL with Experience and Corrections via Advantage-conditioned Policies。监督学习基座 π0.6 经 RECAP 训练后，得到 π*0.6。学习过程像人掌握一门手艺：先看演示模仿，再让教练边做边实时纠错，最后自己自主练习。</p>
        <div class="cyc">
          <span class="cyc-step">演示（模仿）</span><span class="cyc-arr">→</span>
          <span class="cyc-step">专家实时纠错（intervention）</span><span class="cyc-arr">→</span>
          <span class="cyc-step">自主练习（RL）</span><span class="cyc-arr">↺</span>
          <span class="cyc-step">回到数据池 D<sub>ℓ</sub></span>
          <p class="cyc-back">三步对应三种数据，闭环回灌；真正难的是把功劳/过错算到正确的那一步上。</p>
        </div>
        <p>RL 的核心难点是 credit assignment。举个具体例子：portafilter 插不进去，真正的错误往往在更早的「抓取角度」，而不是插入那一下。RECAP 用价值函数来解：价值函数预测到任务完成还差多少（负的步数），1.0 表示成功；优势就是价值的变化量——让价值上升的动作是好的，下降的是坏的。</p>
        <p>最精妙的一步，是 policy extraction 用优势条件化、而不是策略梯度。做法是把 RL 转成条件化的监督学习：训练时给每个动作打上二值标签（Advantage: positive 或 negative）作为额外的文本输入，好的坏的全部数据都留下来训练；推理时永远输入 positive，于是学出的策略优于它的训练数据。</p>
        <div class="duo2">
          <div>
            <p class="d2-tag">训练 Training</p>
            <h4>全部数据都入训</h4>
            <p>(状态, 动作, 优势标签) 一起喂进去。好动作标 <span class="pos">positive</span>，坏动作标 <span class="neg">negative</span>——坏样本不丢，照样从中学。</p>
          </div>
          <div>
            <p class="d2-tag">推理 Inference</p>
            <h4>永远输入 positive</h4>
            <p>固定输入 <span class="pos">Advantage: positive</span> → 只生成高优势动作。于是策略优于它见过的训练数据。</p>
          </div>
        </div>
        <p>三种异质数据分工明确，标签设计正是关键：</p>
        <div class="bx-contribs">
          <article class="bx-contrib"><span class="bx-cnum">A</span><h3>专家演示</h3><p class="bx-src">固定 positive</p><p class="bx-res"><span aria-hidden="true">→</span> 定义行为，给出该做什么</p></article>
          <article class="bx-contrib"><span class="bx-cnum">B</span><h3>自主运行</h3><p class="bx-src">价值函数算优势</p><p class="bx-res"><span aria-hidden="true">→</span> 探索，好坏都留下用于训练</p></article>
          <article class="bx-contrib"><span class="bx-cnum">C</span><h3>专家干预</h3><p class="bx-src">固定 positive</p><p class="bx-res"><span aria-hidden="true">→</span> 覆盖犯错后如何恢复，鲁棒性关键来源</p></article>
        </div>
        <p>模型这边，π0.6 是基于 5B 参数视觉语言模型加动作专家的 VLA，支持异质 prompt（文本指令加执行质量/优势标注）。补充几个 model card 上的细节：Gemma 3 4B 骨干、860M 动作专家、用 flow matching 生成连续动作。结果给具体数字：最难任务上吞吐量翻倍以上、失败率降低 2 倍以上；espresso 从连续 5 分半做到 23 分半，在新家折叠 50 件新衣物，在工厂组装并贴标 59 个真实包装盒，难任务成功率超过 90%。</p>
        <figure class="bx-video is-wide">
          <video muted loop playsinline preload="none" disablepictureinpicture disableremoteplayback data-autoplay-in-view><source src="{{ '/assets/media/blog/rise_pi06/pi06.mp4' | relative_url }}" type="video/mp4"></video>
          <figcaption><strong>RECAP 整体框架。</strong>奖励反馈加专家干预，把演示、自主经验、纠错三类数据拧成一条优势条件化的监督学习。</figcaption>
        </figure>
      </section>

      <section class="bx-section">
        <h2>路线 B：RISE —— 在想象里练</h2>
        <p>RISE 面对同一个根问题——接触密集、动态任务里偏差会复合成失败——但攻的是另一个瓶颈：真机在线 RL 受限于安全风险、硬件成本和环境重置。试错、人工重置、再试，这个循环慢、贵、有风险。</p>
        <p>核心做法是把 RL 环境从物理世界搬进想象空间，用一个组合式世界模型（Compositional World Model）：一个可控的动态模型，基于高效视频扩散预测多视角未来画面；一个进度敏感的价值模型，评估想象出来的状态、产出优势。两个模块各自用最合适的架构和目标独立优化——这正是「组合式」的含义，也是它的好处。</p>
        <figure class="bx-video is-wide">
          <video muted loop playsinline preload="none" disablepictureinpicture disableremoteplayback data-autoplay-in-view><source src="{{ '/assets/media/blog/rise_pi06/rise_methodology_Compositional_world_model.mp4' | relative_url }}" type="video/mp4"></video>
          <figcaption><strong>组合式世界模型。</strong>动态模型负责想象未来，价值模型负责评估优势，两者分头优化、再合到一起。</figcaption>
        </figure>
        {% include logic-atlas.html atlas=page.atlas_rise %}
        <p>自改进是一个闭环：Rollout 阶段，策略以最优优势为条件，在世界模型里交互产生 rollout 数据；Training 阶段，behavior policy 在优势条件化方案下训练。整个过程不碰真机，真机推理也零额外开销。关键设计来自消融——offline 数据占比 0.6 最优，用真实数据把策略锚住，防止它在想象里钻世界模型的空子、漂移掉；online 的 action 与 state 也都不可或缺。</p>
        <figure class="bx-video is-wide">
          <video muted loop playsinline preload="none" disablepictureinpicture disableremoteplayback data-autoplay-in-view><source src="{{ '/assets/media/blog/rise_pi06/rise_self_improve_loop.mp4' | relative_url }}" type="video/mp4"></video>
          <figcaption><strong>自改进闭环。</strong>在想象空间里 rollout、算优势、更新策略，再回到 rollout——真机不参与。</figcaption>
        </figure>
        <p>结果同样给绝对成功率的提升：相对此前方法，dynamic brick sorting 提升 35%、backpack packing 提升 45%、box closing 提升 35%。对照的基线包含 RECAP、π0.5 以及 π0.5+DSRL。</p>
      </section>

      <section class="bx-section">
        <h2>两条路的本质与代价</h2>
        <p>先说关系：二者是递进，不是对立。RECAP 解决「真实世界 RL 怎么做对」，RISE 进一步解决「怎么不依赖真实世界 RL」，而且 RISE 在策略暖身阶段沿用了 RECAP 的优势条件化框架。再说代价：成本是被转移，不是被消除。RECAP 把成本压在物理侧——真机加人工干预；RISE 把成本压在世界模型的保真度上——动态模型一旦幻觉、失真，想象出来的优势就是错的，而 offline ratio 0.6 对冲的正是这个风险。</p>
        <div class="cmp-wrap">
        <table class="cmp">
          <thead><tr><th>维度</th><th>RECAP / π*0.6</th><th>RISE</th></tr></thead>
          <tbody>
            <tr><td>RL 场所</td><td>真实世界（真机 + 人工）</td><td>想象空间（世界模型内）</td></tr>
            <tr><td>主要成本</td><td>物理侧：真机、环境重置、专家干预</td><td>世界模型保真度</td></tr>
            <tr><td>优势表示</td><td>二值 positive / negative</td><td>更细的分箱</td></tr>
            <tr><td>需真机交互</td><td>需要（自主练习在真机上）</td><td>不需要，真机推理零额外开销</td></tr>
            <tr><td>价值函数</td><td>到完成的负步数，1.0 = 成功</td><td>进度敏感，产出优势</td></tr>
            <tr><td>VLA 基座</td><td>π0.6（5B VLM + 动作专家）</td><td>沿用优势条件化框架暖身</td></tr>
            <tr><td>核心风险</td><td>采集慢、贵、有安全风险</td><td>动态模型幻觉 → 优势算错</td></tr>
          </tbody>
        </table>
        </div>
        <p class="cmp-foot"><b>优势表示的取舍：</b>RECAP 用二值标签，信号粗但好学、能吃 VLA 的语言理解、泛化好；RISE 用更细的分箱，信号更密但更依赖价值估计准确——这是「可学性 vs 信息量」的经典权衡。两边都从策略梯度转向优势条件化加 flow matching，因为对扩散/流匹配策略做 PG 很难，条件化把 RL 变监督、还能保留全部数据，是当前最务实的 scale 路线。</p>
        <p class="bx-eq">RECAP 把 RL 变成<b>被语言条件化的监督学习</b><span class="eq-arrow">；</span>RISE 把物理 RL 变成<span class="eq-cyan">带裁判的思维实验</span></p>
      </section>

      <section class="bx-section">
        <h2>展望</h2>
        <p>数据来源的分工大概会固化下来：演示负责定义新行为，coaching 负责精修策略，自主经验是潜在最大的数据来源、用来打磨细节，甚至走向超越人类。真正待回答的问题只有一个——想象和现实，哪条曲线 scale 得更好？世界模型的保真度，能不能随算力持续逼近真机？这个判断留作开放问题更诚实，不必现在下绝对结论。</p>
        <p class="bx-note-line">数字与机制以两份原文为准；covariate shift、DAgger、offline RL、credit assignment 等背景用于补充理解，未虚构任何具体实验结果。</p>
      </section>

    </div>
  </div>
</article>
