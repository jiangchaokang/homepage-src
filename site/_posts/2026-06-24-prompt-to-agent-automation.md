---
layout: default
title: "从提示词到 Agent 自动化的发展路径"
description: "AI Agent 工程的四个阶段——提示词、上下文、harness、loop——不是替代关系而是嵌套关系。瓶颈每往后一层就迁移一次。"
date: 2026-06-24
hide_news: true
tags: ["llm", "agent", "engineering", "notes"]
category: ai-tools
cover: "/assets/media/blog/prompt_agent/cover.svg"
---
<article class="bx reveal">
  <header class="bx-hero">
    <div class="bx-hero-inner">
      <p class="eyebrow">工作笔记 · LLM Agent · 工程演进</p>
      <h1>{{ page.title }}</h1>
      <p class="bx-byline">四个工程阶段，分别在解决一个不同的问题；每解决一个，瓶颈就往后挪一格。把这条迁移线索讲清楚，比罗列方法重要得多。</p>
    </div>
    <blockquote class="bx-lede">
      这四层不是替代关系，是嵌套关系——每一层包住上一层。提示词工程没有消失，它下沉成了系统里的配置、模板和接口契约。核心竞争力正在从「会不会写提示词」，转向「会不会设计上下文、工具环境、反馈系统和验证机制」。
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
        <h2>一张图：四层嵌套，后一层包住前一层</h2>
        <p class="bx-note-line">点任意一层，右侧展开它的核心问题、本质、工程难点与未来方向。外层 loop 把里面三层整个裹住——这正是「嵌套而非并列」的意思。</p>

        <div class="nest-wrap" data-nest>
          <div class="nest">
            <div class="nlayer nl-loop is-sel" data-nl="loop" role="button" tabindex="0" aria-pressed="true">
              <span class="nl-head"><span class="nl-k">04</span><span class="nl-t">loop 工程</span><span class="nl-s">闭环控制</span></span>
              <div class="nlayer nl-harness" data-nl="harness" role="button" tabindex="0" aria-pressed="false">
                <span class="nl-head"><span class="nl-k">03</span><span class="nl-t">harness 工程</span><span class="nl-s">执行环境</span></span>
                <div class="nlayer nl-context" data-nl="context" role="button" tabindex="0" aria-pressed="false">
                  <span class="nl-head"><span class="nl-k">02</span><span class="nl-t">上下文工程</span><span class="nl-s">工作记忆</span></span>
                  <div class="nlayer nl-prompt" data-nl="prompt" role="button" tabindex="0" aria-pressed="false">
                    <span class="nl-head"><span class="nl-k">01</span><span class="nl-t">提示词工程</span><span class="nl-s">意图表达</span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <aside class="nest-panel" data-nest-panel>
            <div class="nest-block is-on" data-nl-detail="loop" style="--nbc: var(--accent-green)">
              <p class="nb-tag">04 · loop 工程</p>
              <h4>闭环控制</h4>
              <dl class="nest-dl">
                <div><dt>核心问题</dt><dd>能做一步，但怎么可靠完成长任务。</dd></div>
                <div><dt>本质</dt><dd>控制论：目标→计划→执行→观察→评估→修正→继续/停止，把模型从回答器变成自动执行系统。</dd></div>
                <div><dt>工程难点</dt><dd>没有终止条件的 loop 就是会烧钱、会漂移、会误操作的黑箱；要有评估标准、停止条件、预算上限、人工介入点，生成器与评估器分离。</dd></div>
                <div><dt>未来方向</dt><dd>适合可验证任务（有测试、有标准答案）；完全开放、无标准的高风险任务不适合。</dd></div>
              </dl>
            </div>
            <div class="nest-block" data-nl-detail="harness" style="--nbc: var(--accent-purple)">
              <p class="nb-tag">03 · harness 工程</p>
              <h4>执行环境</h4>
              <dl class="nest-dl">
                <div><dt>核心问题</dt><dd>模型会想，但怎么稳定地行动。</dd></div>
                <div><dt>本质</dt><dd>Agent = Model + Harness。不是模型的部分，就是 harness——它补上持久状态、执行代码、访问实时信息、配置环境。</dd></div>
                <div><dt>工程难点</dt><dd>工具集要最小可用、不重叠；工程师自己都说不清用哪个工具，agent 更不行。模型与 harness 耦合会过拟合。</dd></div>
                <div><dt>未来方向</dt><dd>工具协议标准化（MCP）、权限最小化、可观测性、领域专用 harness。</dd></div>
              </dl>
            </div>
            <div class="nest-block" data-nl-detail="context" style="--nbc: var(--accent)">
              <p class="nb-tag">02 · 上下文工程</p>
              <h4>工作记忆管理</h4>
              <dl class="nest-dl">
                <div><dt>核心问题</dt><dd>模型每一步到底看见了什么。</dd></div>
                <div><dt>本质</dt><dd>管理模型在每步看见什么；很多失败不是不会，而是看不见关键事实，或被噪声淹没。</dd></div>
                <div><dt>工程难点</dt><dd>context rot——token 越多召回越差，attention budget 有限。上下文是边际递减的稀缺资源，目标是最小的高信号 token 集。</dd></div>
                <div><dt>未来方向</dt><dd>从更大的窗口，转向更高质量的选择；预检索与按需取的混合策略。</dd></div>
              </dl>
            </div>
            <div class="nest-block" data-nl-detail="prompt" style="--nbc: var(--accent-cyan)">
              <p class="nb-tag">01 · 提示词工程</p>
              <h4>意图表达层</h4>
              <dl class="nest-dl">
                <div><dt>核心问题</dt><dd>人怎么把意图说清楚，让模型接得住。</dd></div>
                <div><dt>本质</dt><dd>人和模型之间的接口契约。好 prompt 像一份简短 PRD，不是一段漂亮文字。</dd></div>
                <div><dt>工程难点</dt><dd>right altitude——太硬编码则脆弱难维护，太宽泛则拿不到信号；关键认知是 minimal ≠ short。</dd></div>
                <div><dt>未来方向</dt><dd>不会消失，会下沉成模板、配置、自动生成与版本管理。</dd></div>
              </dl>
            </div>
          </aside>
        </div>

        <p class="bx-eq">人教 AI 说话 <span class="eq-arrow">→</span> 管理它看见什么 <span class="eq-arrow">→</span> 给它搭环境 <span class="eq-arrow">→</span> <b>设计闭环系统</b></p>

        <p class="bx-note-line" style="margin-top:1.2rem">三条贯穿全文的判断：四层是嵌套不是替代，每层都把上一层收进自己的配置与接口；每往后一层瓶颈就迁移一次——从人说不清楚，到 AI 看不见关键信息，到会想却不能稳定行动，再到能做一步却不能可靠完成长任务；随着模型变强，harness 里的规划、自我验证、长程一致性会被逐渐吸收进模型本身，但就像 prompt 工程至今仍有价值，harness/loop 工程也会长期存在。</p>
      </section>

      <section class="bx-section">
        <h2>提示词工程 —— 意图表达层</h2>
        <p>本质是人和模型之间的接口契约。好的 prompt 更像一份简短 PRD——角色、目标、背景、输入、约束、标准、输出格式，而不是一段漂亮文字。难点是 Anthropic 说的 right altitude：太硬编码则脆弱难维护，太宽泛则模型拿不到信号；一个常被搞反的认知是 minimal ≠ short，要给足信息但不冗余。取舍上，与其堆一长串 edge case，不如给少量典型示例，few-shot 往往一图胜千言。它不会消失，只会下沉成模板、配置、自动生成与版本管理——这也是「嵌套」的第一层证据。</p>
      </section>

      <section class="bx-section">
        <h2>上下文工程 —— 工作记忆管理</h2>
        <p>管的是模型每一步看见什么。很多失败不是模型不会，而是它看不见关键事实，或被噪声淹没。难点是 context rot：token 越多，召回反而越差；attention budget 有限，transformer 的 n² 关系让注意力被稀释。所以上下文是有边际递减的稀缺资源，目标是最小的高信号 token 集。</p>
        <p>常用手段有四个，各有代价：compaction 压缩历史，难在 recall 与 precision 的权衡——压太狠会丢掉后期才显现重要性的细节；structured note-taking 把记忆写到上下文外、需要时再拉回；sub-agent 隔离让子代理用几万 token 探索、只回传一两千的结论；just-in-time 检索用文件路径、查询等轻量标识按需加载。判断：重点已经从更大的窗口，转向更高质量的选择——预检索快但会过时，按需取新鲜但更慢，实际常用混合。</p>
      </section>

      <section class="bx-section">
        <h2>harness 工程 —— 执行环境</h2>
        <p>一句话：Agent = Model + Harness，不是模型的部分，就是 harness。它给模型补上天生不会的能力——持久状态、执行代码、访问实时信息、配置环境。最基础的 primitive 是文件系统：工作区、状态外置、多 agent 与人协作的共享账本，加上 git 还能版本化；再给它 bash/code 当通用工具，与其为每个动作预设工具，不如给它一台电脑让它自己写工具；外面套 sandbox 做隔离与按需开销。</p>
        <p>难点是工具集要最小可用、不重叠——如果工程师自己都说不清该用哪个工具，agent 更不行；模型训练与 harness 耦合还会过拟合，换掉 apply_patch 的编辑逻辑就能让模型变差。证据很硬：SWE-agent 证明 agent-computer interface 的设计显著影响性能，SWE-bench pass@1 做到 12.5%，远超非交互式基线；LangChain 也观察到同一个模型换 harness、分数差距巨大。能力不只来自模型，也来自接口。未来方向是工具协议标准化（MCP）、权限最小化、可观测性、领域专用 harness。</p>
      </section>

      <section class="bx-section">
        <h2>loop 工程 —— 闭环控制</h2>
        <p>本质是控制论：目标→计划→执行→观察→评估→修正→继续或停止，把模型从回答器变成自动执行系统。证据不少：Self-Refine 让同一个模型自己生成、自反馈、再迭代，七个任务平均提升约 20%，不需要训练；Reflexion 把语言化反思写进 episodic memory 指导后续决策，HumanEval pass@1 做到 91%，超过 GPT-4 的 80%；工程上的 Ralph Loop 用 hook 拦截模型的退出、在干净上下文里重注入原始目标，逼它继续，靠文件系统跨轮传状态。</p>
        <p>真正要强调的难点只有一句：没有终止条件的 loop，就是一个会烧钱、会漂移、会误操作的黑箱。必须设计明确的评估标准、停止条件、预算上限、失败处理、人工介入点，并且把生成器和评估器分开。取舍也清楚：loop 适合可验证任务——有测试、有标准答案；完全开放、无标准的高风险任务并不适合。</p>
      </section>

      <section class="bx-section">
        <h2>一句收尾</h2>
        <ul class="bx-takeaways">
          <li>四层不是替代关系，是嵌套关系。每一层包住上一层——提示词没消失，它变成了里面的配置、模板和接口契约。</li>
          <li>每往后一层，瓶颈迁移一次：人说不清楚 → AI 看不见 → 会想却不能稳定行动 → 能做一步却不能可靠完成长任务。</li>
          <li>模型变强会吸收 harness 里的能力，但不会清零它的价值——就像 prompt 工程至今还在。核心竞争力，已从写提示词，转向设计上下文、工具环境、反馈系统与验证机制。</li>
        </ul>
      </section>

    </div>
  </div>
</article>

<script>
(function () {
  document.querySelectorAll("[data-nest]").forEach(function (wrap) {
    var layers = wrap.querySelectorAll(".nlayer");
    var blocks = wrap.querySelectorAll("[data-nl-detail]");
    function select(nl) {
      layers.forEach(function (l) {
        var on = l.getAttribute("data-nl") === nl;
        l.classList.toggle("is-sel", on);
        l.setAttribute("aria-pressed", on ? "true" : "false");
      });
      blocks.forEach(function (b) {
        b.classList.toggle("is-on", b.getAttribute("data-nl-detail") === nl);
      });
    }
    layers.forEach(function (l) {
      var nl = l.getAttribute("data-nl");
      l.addEventListener("click", function (e) { e.stopPropagation(); select(nl); });
      l.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); e.stopPropagation(); select(nl); }
      });
    });
  });
})();
</script>
