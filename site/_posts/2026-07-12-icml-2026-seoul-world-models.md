---
layout: default
title: "ICML 2026 in Seoul: the shift toward real-time, closed-loop, verifiable world models"
description: "Notes from ICML 2026 in Seoul, where our VectorWorld paper was a Spotlight — five signals on one-step generation, explicit structure, reward design, control theory, and automating research."
date: 2026-07-12
hide_news: true
tags: ["world-model", "icml", "conference-notes", "generative-models"]
category: world-models
cover: "/assets/media/blog/icml2026_seoul/VectorWorld_Spotlight_Poster_LiveExchange.jpg"
---
<article class="bx reveal">
  <header class="bx-hero">
    <div class="bx-hero-media" aria-hidden="true">
      <img src="{{ '/assets/media/blog/icml2026_seoul/VectorWorld_Spotlight_Poster_LiveExchange.jpg' | relative_url }}" alt="">
    </div>
    <div class="bx-hero-inner">
      <p class="eyebrow">Conference Notes · ICML 2026 · Seoul</p>
      <h1>{{ page.title }}</h1>
      <p class="bx-byline">A week at COEX with our Spotlight paper, VectorWorld — and five signals worth carrying home, from one-step generation to the first real AI-scientist tools.</p>
    </div>
    <blockquote class="bx-lede">
      I spent July 6–11 at COEX for the 43rd ICML, showing our Spotlight paper, VectorWorld. Between poster sessions, the more interesting question was what generative models, world models, and ML systems are actually optimizing for now. The clearest answer: less for a better single sample, more for a system that is faster, steadier, easier to control, and easier to verify.
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

      <figure class="bx-fig">
        <img src="{{ '/assets/media/blog/icml2026_seoul/ICML2026_COEX_Entrance.jpg' | relative_url }}" alt="Welcome to COEX banner for ICML 2026 in Seoul" loading="lazy">
        <figcaption><strong>COEX, Seoul.</strong> Main conference, tutorials, expo, and workshops, all under one roof, July 6–11.</figcaption>
      </figure>

      <section class="bx-section">
        <h2>1. One-step generation becomes closed-loop infrastructure</h2>
        <p>MeanFlow reframes the learning target from an instantaneous velocity to an average velocity over an interval, so a single forward pass replaces what used to take dozens of denoising steps — I covered that line of work in more depth in <a href="{{ '/blog/2026/06/28/one-step-generative-models/' | relative_url }}">a paper-by-paper walkthrough</a>. <a href="{{ '/publications/#jiang2026vectorworld' | relative_url }}">VectorWorld</a> applies the same idea to streaming vector-scene completion: roughly 5.6&nbsp;ms per tile for one-step inference, holding up over kilometer-scale closed-loop rollouts. PointDiT pushes the same one-step instinct into dense 3D geometry. Once a system runs closed-loop, latency stops being an engineering footnote — it becomes part of what the model can actually do.</p>
      </section>

      <section class="bx-section">
        <h2>2. Explicit structure still earns its keep</h2>
        <p>PointDiT skips the Point VAE and the usual two-stage latent pipeline entirely: a plain ViT runs pixel-space diffusion directly on raw 3D point-map patches, conditioned on DINOv3 features, and keeps sharper boundaries around ambiguous regions like transparent objects. VectorWorld makes the same bet at the scene level — an explicit lane-agent vector graph in place of a fully implicit visual latent. For geometry, traffic, and physical worlds, explicit structure is still one of the more reliable paths to controllability, interpretability, and verifiability.</p>
      </section>

      <section class="bx-section">
        <h2>3. Generation, reward, and evaluation have to be designed together</h2>
        <p><a href="https://arxiv.org/abs/2602.01624" target="_blank" rel="noopener">PISCES</a> uses optimal transport to align text and video representations, then builds two separate rewards on that alignment — one for overall quality, one for fine-grained semantics — and post-trains video generation with no human preference labels at all. <a href="https://arxiv.org/abs/2606.28322" target="_blank" rel="noopener">PerceptionRubrics</a> does the equivalent for evaluation: it splits multimodal understanding into atomic "must-right" facts and "easy-wrong" details, then gates the score so one missed must-right fact can't be smoothed over by everything else being fine. The same instinct showed up outside vision-language work, too, in a medical-imaging poster (<a href="https://openreview.net/pdf?id=wWl4AE7KXS" target="_blank" rel="noopener">IPOD</a>) that learns a reusable INR initialization for MRI reconstruction straight from undersampled k-space, with no clean reference scan in sight.</p>
        <p>None of this is just "a bigger generator." Progress here depends as much on getting the reward and the rubric right as on making the generator itself bigger. For driving world models specifically, visual realism was never the bar — topology, collisions, feasible motion, and long-rollout drift deserve to be independent, hard checks, not folded into one aggregate score.</p>
      </section>

      <section class="bx-section">
        <h2>4. Control theory and generative models are converging again</h2>
        <p><a href="https://arxiv.org/abs/2601.23231" target="_blank" rel="noopener">MPC-Flow</a> reframes conditional generation with a flow model as a sequence of model-predictive-control sub-problems — plan over a short horizon, act, observe, replan — with no need to back-propagate through the full generative trajectory. VectorWorld's ΔSim leans on the same idea, constraining NPC behavior with differentiable kinematics to cut down physical drift over long closed loops. Learning and control were never really competing approaches: the generative model supplies the prior, and control plus physical constraints are what make that prior something you can deploy.</p>
      </section>

      <section class="bx-section">
        <h2>On the show floor</h2>
        <p class="bx-note-line">Five more posters that stuck with me — each one a different bet on the same shift.</p>
        <div class="bx-media">
          <figure class="bx-fig">
            <img src="{{ '/assets/media/blog/icml2026_seoul/PointDiT_poster.jpg' | relative_url }}" alt="PointDiT poster at ICML 2026" loading="lazy">
            <figcaption><strong>PointDiT.</strong> A simpler pixel-space diffusion recipe still yields sharper, more robust monocular 3D geometry.</figcaption>
          </figure>
          <figure class="bx-fig">
            <img src="{{ '/assets/media/blog/icml2026_seoul/PISCES_poster.jpg' | relative_url }}" alt="PISCES poster at ICML 2026" loading="lazy">
            <figcaption><strong>PISCES.</strong> Align the reward space first, then post-train text-to-video generation without human labels.</figcaption>
          </figure>
          <figure class="bx-fig">
            <img src="{{ '/assets/media/blog/icml2026_seoul/PerceptionRubrics.jpg' | relative_url }}" alt="PerceptionRubrics poster at ICML 2026" loading="lazy">
            <figcaption><strong>PerceptionRubrics.</strong> From a fuzzy overall similarity score to an auditable checklist of visual facts.</figcaption>
          </figure>
          <figure class="bx-fig">
            <img src="{{ '/assets/media/blog/icml2026_seoul/MPC-Flow.jpg' | relative_url }}" alt="MPC-Flow poster at ICML 2026" loading="lazy">
            <figcaption><strong>MPC-Flow.</strong> Treat conditional generation as closed-loop control — plan, act, and replan inside every short horizon.</figcaption>
          </figure>
          <figure class="bx-fig">
            <img src="{{ '/assets/media/blog/icml2026_seoul/Reference-Free-Meta-Learning-MRI.jpg' | relative_url }}" alt="Reference-free meta-learning for MRI reconstruction poster at ICML 2026" loading="lazy">
            <figcaption><strong>IPOD.</strong> A generalizable INR initialization learned straight from undersampled MRI scans, no clean reference required.</figcaption>
          </figure>
        </div>
      </section>

      <section class="bx-section">
        <h2>5. The AI-scientist bottleneck isn't just code</h2>
        <p>Google's <a href="https://arxiv.org/abs/2601.23265" target="_blank" rel="noopener">PaperBanana</a> — since renamed PaperVizAgent — turns five agents loose on one job: a retriever, a planner, a stylist, a renderer, and a critic, working together to draft and revise method figures and result plots. A companion Google poster, on why machine-learning engineering (MLE) is the harder half of automating research, made the sharper point: ordinary software fails loudly and reproduces in seconds, while a machine-learning experiment can take hours or days to fail, and the regression could be the data, a hyperparameter, the random seed, or the training run itself — the root cause is genuinely harder to pin down. <a href="https://research.google/pubs/mle-star-machine-learning-engineering-agent-via-search-and-targeted-refinement/" target="_blank" rel="noopener">MLE-STAR</a> answers with web-search-seeded starting points and targeted, ablation-guided refinement of individual pipeline components, instead of rewriting the whole thing at once.</p>
        <p>Automating research was never only about generating a plausible-looking method. It's whether you can run the experiment reliably, trace why performance actually moved, and keep the evidence to prove it.</p>
        <div class="bx-media cols-2">
          <figure class="bx-fig">
            <img src="{{ '/assets/media/blog/icml2026_seoul/PaperBanana.jpg' | relative_url }}" alt="Google PaperBanana poster at ICML 2026" loading="lazy">
            <figcaption><strong>PaperBanana.</strong> Five agents — retrieve, plan, style, render, critique — collaborating to draft and revise research figures.</figcaption>
          </figure>
          <figure class="bx-fig">
            <img src="{{ '/assets/media/blog/icml2026_seoul/MLE.jpg' | relative_url }}" alt="Google MLE poster at ICML 2026" loading="lazy">
            <figcaption><strong>MLE.</strong> Automating research means executing costly experiments, not only generating code that looks right.</figcaption>
          </figure>
        </div>
      </section>

      <section class="bx-section">
        <h2>The most striking demo on the floor</h2>
        <p>My own footage, from the <a href="https://mira-wm.com/" target="_blank" rel="noopener">MIRA</a> booth: a real-time, four-player world model by General Intuition, Kyutai, and Epic Games, generating a driving game live from nothing but controller input — no engine, no renderer, just a model predicting what comes next, smoothly enough that you forget it is being generated at all. It was the clearest proof on the floor that "real-time, interactive world model" is no longer a future-tense claim.</p>
        <figure class="bx-video is-wide">
          <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/blog/icml2026_seoul/mira-wm.mp4' | relative_url }}" type="video/mp4"></video>
          <figcaption><strong>MIRA.</strong> Four players, one neural network — a playable driving world generated live, frame by frame, no game engine involved.</figcaption>
        </figure>
      </section>

      <section class="bx-section">
        <h2>VectorWorld at the poster</h2>
        <p>The valuable part of a poster session was never finishing the walkthrough — it was explaining one system, in a few minutes, clearly enough that a stranger could restate what problem it solves, why it works, where its edges are, and how it might fail. In front of the VectorWorld poster, I kept boiling the system down to three steps:</p>
        <p class="bx-eq">History-compatible warm start <span class="eq-arrow">→</span> one-step frontier completion <span class="eq-arrow">→</span> <b>physics-aligned closed loop</b></p>
        <figure class="bx-fig">
          <img src="{{ '/assets/media/blog/icml2026_seoul/VectorWorld_Poster.jpg' | relative_url }}" alt="VectorWorld Spotlight poster at ICML 2026" loading="lazy">
          <figcaption><strong>VectorWorld.</strong> A streaming vector-graph world model — one-step diffusion flow completes the map frontier as the vehicle moves, closed by physics-aligned NPC behavior.</figcaption>
        </figure>
        <p>The conversations sharpened what I think a world model still has to answer before it earns a place in a production loop: a valid initialization, topological consistency, real-time inference, safe agent behavior, and stability over long rollouts.</p>
      </section>

      <section class="bx-section">
        <h2>One more lens: from least action to score and flow</h2>
        <p>A personal aside I keep coming back to: classical mechanics, stochastic processes, score-based diffusion, and flow matching all read, in spirit, as the same question — what is the right evolution law over a space of paths.</p>
        <p class="bx-note-line">Read the poster below as a conceptual throughline, not a rigorous derivation chain: a score model learns the gradient of a probability density, while flow matching learns a deterministic velocity field that transports noise to data directly. They rhyme more than they reduce to one another.</p>
        <figure class="bx-fig">
          <img src="{{ '/assets/media/blog/icml2026_seoul/min_power.jpg' | relative_url }}" alt="A conceptual diagram connecting least action, Euler-Lagrange, Fokker-Planck, score matching, and flow matching" loading="lazy">
          <figcaption><strong>From least action to probability transport.</strong> One way to read diffusion and flow models: both search for the right evolution law over a space of paths.</figcaption>
        </figure>
      </section>

      <section class="bx-section">
        <h2>What I'm taking home</h2>
        <p>ICML 2026 mostly confirmed a direction I was already leaning toward:</p>
        <ul class="bx-takeaways">
          <li>Move world models from offline generation toward real-time, interactive closed loops.</li>
          <li>Connect vector-world priors to sensor-level video generation.</li>
          <li>Build atomic evaluation for structure, physics, and safety — not just an aggregate visual score.</li>
          <li>Automate the experiment loop, but keep the evidence, the reproduction steps, and a human check at the end of it.</li>
        </ul>
        <p class="bx-callout">Bigger models still matter. But what actually moves a system forward is a shorter generation path, more explicit structure, a more reliable closed loop, and stricter verification.</p>
        <figure class="bx-fig">
          <img src="{{ '/assets/media/blog/icml2026_seoul/VectorWorld_Spotlight_Poster_LiveExchange2.jpg' | relative_url }}" alt="Chaokang Jiang with a fellow researcher at the VectorWorld poster, ICML 2026" loading="lazy">
          <figcaption>ICML is more than papers — it's the researchers a shared question connects you to.</figcaption>
        </figure>
      </section>

    </div>
  </div>
</article>
