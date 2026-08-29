---
layout: default
title: "从 3DGRUT 到 ArtiFixer3D：一个“先重建、再生成、再蒸馏回 3D”的闭环"
description: "Reading ArtiFixer (SIGGRAPH 2026, NVIDIA Toronto AI Lab) — an interactive 3D logic atlas of the reconstruct → generate → distill-back-to-3D loop."
date: 2026-06-26
hide_news: true
tags: ["world-model", "3d", "generative", "reading"]
category: scene-reconstruction
cover: "/assets/media/blog/artifixer/teaser_v5-1.jpg"
atlas:
  variant: noir
  eyebrow: "Reasoning loop · ArtiFixer"
  title: "重建出一个一致的底，生成把它修干净，再用 3D 强行对齐——然后再修一遍"
  caption: "主轴 ①→⑥ 是推理闭环，⑤ 画一条发光曲线回 ④ 就是题眼；下面一排是训练三阶段，权重虚线汇入 ④。点击任一节点固定四行细节与我的判断。"
  cols: 8
  legend:
    - { accent: ink, label: "输入与评测" }
    - { accent: blue, label: "3D 重建底座 / Stage 1" }
    - { accent: cyan, label: "条件与 2D 修复 / Stage 3" }
    - { accent: purple, label: "3D 仲裁 / Stage 2" }
    - { accent: green, label: "输出" }
    - { accent: warn, label: "数据引擎" }
  nodes:
    - id: capture
      col: 2
      span: 6
      row: 1
      kind: input
      accent: ink
      tag: "Start"
      title: "① Capture / COLMAP"
      desc: "随手拍 → 接进 3D 流水线"
      receives: "随手拍图像/视频，视角稀疏"
      logic: "COLMAP 跑稀疏位姿与点云"
      sends: "相机内外参 + 稀疏点"
      gives: "把“随手拍”接进 3D 流水线"
    - id: grut
      col: 2
      span: 6
      row: 2
      kind: process
      accent: blue
      tag: "Base"
      title: "② 3DGRUT 重建（底座）"
      desc: "有瑕疵但 3D 一致"
      receives: "COLMAP 结果"
      logic: "3DGRUT/3DGUT 优化（MCMC，默认 10k 步）"
      sends: "有瑕疵但 3D 一致的渲染 + opacity + depth"
      gives: "提供“一致但不干净”的底"
      note: "选 3DGUT 不是随手选的——它用 unscented transform 直接吃带畸变的相机（OpenCV/鱼眼）和 rolling shutter，省掉去畸变重采样。底座越规整，后面要纠的偏差越少。"
    - id: cond
      col: 2
      span: 6
      row: 3
      kind: process
      accent: cyan
      tag: "Condition"
      title: "③ Conditioning（条件）"
      desc: "几何 + 语义条件"
      receives: "渲染 + opacity + depth"
      logic: "MoGe 估单目深度做 metric scale，写 caption 文本嵌入"
      sends: "几何 + 语义条件"
      gives: "让生成“有据可依”"
      note: "opacity 这个条件容易被忽略却很关键——等于告诉模型“哪里重建有把握、哪里是空的”，别把有把握的地方也一起改了。metric scale 是为了让不同场景的深度条件落在同一尺度，否则条件本身就是病态的。"
    - id: artifixer
      col: 2
      span: 6
      row: 4
      kind: reason
      accent: cyan
      pulse: true
      tag: "Core · 2D Repair"
      title: "④ ArtiFixer（自回归扩散 · 2D 修复）"
      desc: "Wan2.1 14B 视频扩散"
      media: "/assets/media/blog/artifixer/artifixer_overview_v2-1.jpg"
      media_type: image
      receives: "重建渲染 + 条件"
      logic: "Wan2.1 14B 视频扩散，沿相机轨迹自回归生成"
      sends: "干净且帧间一致的修复帧"
      gives: "给重建装上“想象力”"
      note: "最关键的一个判断是——把 NVS 当视频生成来做。沿轨迹看一个场景本质就是一段视频；视频模型天生管时序一致，挪到 NVS 上就是视角一致。用 14B 视频底模而不是图像底模，这步棋是整篇的地基。"
    - id: a3d
      col: 2
      span: 6
      row: 5
      kind: process
      accent: purple
      tag: "3D Arbiter"
      title: "⑤ ArtiFixer3D（蒸馏回 3D）"
      desc: "把生成帧揉进一个 3DGRUT"
      receives: "真实锚点帧 + ArtiFixer 生成帧"
      logic: "重新优化一个 3DGRUT，把两者揉进同一个 3D"
      sends: "干净且 3D 一致的重建"
      gives: "用 3D 当“仲裁”，强行让 2D 生成自洽"
      note: "我觉得这步是题眼。2D 生成再好也会帧间打架，而一个 3D 表示只能有一个几何——把所有生成帧塞进一次重建，等于逼它们投票出一致解。锚点用真值、目标帧用生成，角色分工正好对上 diffusion forcing 里“已知 vs 待生成”。"
    - id: output
      col: 1
      span: 5
      row: 6
      kind: contribution
      accent: green
      tag: "Output"
      title: "⑥ ArtiFixer3D+ / Output"
      desc: "再修 → 一致漫游"
      media: "/assets/media/blog/artifixer/teaser_v5-1.jpg"
      media_type: image
      receives: "ArtiFixer3D 的新渲染"
      logic: "把 ArtiFixer 再跑一次"
      sends: "进一步精修的漫游 / 一致 3D"
      gives: "闭环迭代，越修越干净"
      note: "闭环就是 3D→2D→3D→2D。底子干净了，生成要纠的就少，输出更稳。本质像一轮 EM——生成负责“提议”，3D 负责“对齐”。"
    - id: eval
      col: 6
      span: 3
      row: 6
      kind: output
      accent: ink
      tag: "Eval"
      title: "⑪ Evaluation"
      desc: "四步逐一对比"
      media: "/assets/media/blog/artifixer/different-steps-1.jpg"
      media_type: image
      logic: "四行对比 3DGUT / ArtiFixer / ArtiFixer3D / ArtiFixer3D+"
      sends: "DL3DV + NerfBusters 上评测"
      gives: "把“每一步到底有没有用”拆开看"
    - id: dataengine
      col: 1
      span: 2
      row: 7
      kind: input
      accent: warn
      tag: "Data Engine"
      title: "⑦ 数据引擎"
      desc: "少视角造退化样本"
      logic: "DL3DV 用少视角(2/3/6/12)重建造退化样本，留出视角当 GT；half-covisibility 切分"
      sends: "(有瑕疵渲染, 干净 GT) 配对"
      gives: "不用人工标注白嫖监督对"
      note: "这个自监督造数据思路能直接搬走——任何“重建增强”任务，都能用“少喂几张视角”人为制造退化、拿全量视角当监督。便宜、可扩展。"
    - id: sft
      col: 3
      span: 2
      row: 7
      kind: process
      accent: blue
      tag: "Train · S1"
      title: "⑧ Stage 1 SFT"
      desc: "render → clean"
      logic: "监督微调，学 render→clean 的条件映射"
      sends: "会基本修复的底模"
    - id: df
      col: 5
      span: 2
      row: 7
      kind: process
      accent: purple
      tag: "Train · S2"
      title: "⑨ Stage 2 Diffusion Forcing"
      desc: "每帧独立噪声"
      logic: "每帧独立噪声等级，自回归 rollout"
      sends: "能拉长轨迹、保持一致的模型"
      note: "选 diffusion forcing 而非普通视频扩散，因为每帧独立噪声天然能表达“这帧是给定锚点(低噪)、那帧要生成(高噪)”，正好对上推理时锚点/目标的分工。工具和问题是咬合的。"
    - id: dmd
      col: 7
      span: 2
      row: 7
      kind: process
      accent: cyan
      tag: "Train · S3"
      title: "⑩ Stage 3 DMD 蒸馏"
      desc: "蒸馏成少步生成器"
      logic: "分布匹配蒸馏成少步生成器；s2 当 student、s1 当 critic"
      sends: "跑得快的生成器"
      note: "DMD 不只是为了部署快。闭环要把模型跑好几遍，几十步采样扛不住——是“闭环”这个算法设计反过来要求了“少步蒸馏”。算法和系统是一起设计的。"
  edges:
    - { from: capture, to: grut, kind: flow }
    - { from: grut, to: cond, kind: flow }
    - { from: cond, to: artifixer, kind: flow }
    - { from: artifixer, to: a3d, kind: flow }
    - { from: a3d, to: output, kind: flow }
    - { from: a3d, to: artifixer, kind: loop }
    - { from: output, to: eval, kind: dashed }
    - { from: dataengine, to: sft, kind: dashed }
    - { from: sft, to: df, kind: dashed }
    - { from: df, to: dmd, kind: dashed }
    - { from: dmd, to: artifixer, kind: dashed }
---
<article class="bx reveal">
  <header class="bx-hero">
    <div class="bx-hero-media" aria-hidden="true">
      <img src="{{ '/assets/media/blog/artifixer/teaser_v5-1.jpg' | relative_url }}" alt="">
    </div>
    <div class="bx-hero-inner">
      <p class="eyebrow">阅读 · ArtiFixer · SIGGRAPH 2026 · NVIDIA Toronto AI Lab</p>
      <h1>{{ page.title }}</h1>
      <p class="bx-byline">显式 3D 重建负责一致，生成式先验负责想象，两者轮流出手——一个能闭环迭代的修复管线。</p>
    </div>
    <blockquote class="bx-lede">
      我对这篇的兴趣不在“又一个修 artifact 的模型”，而在它把两个一直互相看不顺眼的东西——显式 3D 重建和生成式先验——用一个闭环缝在了一起。重建的强项是 3D 一致，弱项是没见过的地方只能瞎填；生成模型正好反过来，能脑补但帧间对不上。ArtiFixer 让它们轮流出手：重建出一个有瑕疵但一致的底，生成模型把它修干净，再把修过的帧蒸馏回一个新的 3D 表示里强行对齐，然后再修一遍。
    </blockquote>
  </header>

  <div class="bx-shell" data-proj-shell>
    <nav class="proj-toc" data-proj-toc aria-label="On this page">
      <button class="proj-toc-toggle" type="button" data-toc-toggle aria-expanded="true" aria-label="Toggle contents">
        <span class="toc-title">Contents</span>
        <svg class="toc-chevron" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
      </button>
      <nav class="proj-toc-nav"><ol data-toc-list></ol></nav>
    </nav>

    <div class="project-body-main bx-body">

      <section class="bx-section">
        <h2>核心问题</h2>
        <p class="bx-callout">
          稀疏视角重建在训练视角附近好看，相机一走开就开始飘 floater、糊、破洞。原因很朴素：重建是拟合，没有“世界本来该长什么样”的先验。纯 3DGS/NeRF 是 3D 一致但不会脑补；纯逐帧 2D 修复会脑补但换个角度就闪。ArtiFixer 不二选一，让两者轮流。
        </p>
      </section>

      <section class="bx-section">
        <h2>推理闭环：重建 → 生成 → 蒸馏回 3D</h2>
        <p class="bx-note-line">主轴 ①→⑥ 是一次推理；真正的题眼是 ⑤ 回到 ④ 的那条发光曲线——3D 与 2D 来回振荡，越修越干净。下面一排 ⑦→⑩ 是训练三阶段，把权重以虚线喂给 ④。</p>
        {% include logic-atlas.html %}
      </section>

      <section class="bx-section">
        <h2>三条贡献</h2>
        <div class="bx-contribs">
          <article class="bx-contrib" tabindex="0" data-atlas-link="artifixer,a3d">
            <span class="bx-cnum">01</span>
            <h3>把生成先验装进 3D 重建</h3>
            <p class="bx-src">来源 ④ + ⑤</p>
            <p class="bx-res"><span aria-hidden="true">→</span> 没观测到的区域也能补出合理内容</p>
          </article>
          <article class="bx-contrib" tabindex="0" data-atlas-link="a3d">
            <span class="bx-cnum">02</span>
            <h3>3D 仲裁带来视角一致</h3>
            <p class="bx-src">来源 ⑤</p>
            <p class="bx-res"><span aria-hidden="true">→</span> 比逐帧 2D 修复更不闪、几何更稳</p>
          </article>
          <article class="bx-contrib" tabindex="0" data-atlas-link="a3d,artifixer,output">
            <span class="bx-cnum">03</span>
            <h3>闭环可迭代精修</h3>
            <p class="bx-src">来源 ⑤ → ④ → ⑥</p>
            <p class="bx-res"><span aria-hidden="true">→</span> ArtiFixer3D+ 在更干净的底上再修</p>
          </article>
        </div>
      </section>

      <section class="bx-section">
        <h2>结果</h2>
        <p class="bx-note-line">只用三张原图，绑在对应模块上：teaser 是输出 ⑥，方法总览是核心 ④，去噪步骤挂在评测旁——悬停图里的节点也会浮出同一张图。</p>
        <div class="bx-media">
          <figure class="bx-fig">
            <img src="{{ '/assets/media/blog/artifixer/teaser_v5-1.jpg' | relative_url }}" alt="ArtiFixer teaser — clean novel-view roaming" loading="lazy">
            <figcaption><strong>Fig.1 · ⑥ Output.</strong> 随手拍进去，干净一致的漫游出来。</figcaption>
          </figure>
          <figure class="bx-fig">
            <img src="{{ '/assets/media/blog/artifixer/artifixer_overview_v2-1.jpg' | relative_url }}" alt="ArtiFixer method overview" loading="lazy">
            <figcaption><strong>Fig.2 · ④ ArtiFixer.</strong> 把 NVS 当视频生成：沿轨迹自回归修复，时序一致即视角一致。</figcaption>
          </figure>
          <figure class="bx-fig">
            <img src="{{ '/assets/media/blog/artifixer/different-steps-1.jpg' | relative_url }}" alt="ArtiFixer denoising steps" loading="lazy">
            <figcaption><strong>Fig.11 · 去噪步骤.</strong> 一步步把瑕疵渲染收敛到干净帧。</figcaption>
          </figure>
        </div>
      </section>

      <section class="bx-section">
        <h2>我的判断 / 后续</h2>
        <ul class="bx-takeaways">
          <li>这套“想象力来自生成、一致性来自显式表示、两者轮流”的范式不止能修重建。任何“先有个粗结构、再补全/精修”的活都能套：粗 mesh → 生成贴图 → 烤回 mesh；粗动作 → 生成补全 → 约束回骨架。</li>
          <li>要小心的地方：生成先验会“合理地编错”——纹理几何看着对、其实不是真值。3D 仲裁能压一部分，但压不干净。做数字孪生、检测这类要测量精度的活，得对这点有数。</li>
          <li>我自己会怎么用：当成“随手拍 → 干净漫游”的工具链。COLMAP → prepare → ArtiFixer → ArtiFixer3D 这条线，基本就是一个 capture-to-clean-3D 的成品。</li>
        </ul>
      </section>

    </div>
  </div>
</article>
