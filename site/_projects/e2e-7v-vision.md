---
title: "One-Stage End-to-End Driving — 8V Pure Vision"
subtitle: "From pixels to planning in a single network: 8-camera surround vision → unified BEV → three perception heads → self-supervised future-BEV prediction → a Diffusion-Flow AI planner, all trained end-to-end with no hand-designed 3D-label interface."
description: "A one-stage, pure-vision end-to-end driving POC — 8 surround cameras into one BEV, three perception heads, future-BEV prediction, and a Diffusion-Flow planner, trained jointly."
date_range: "2025.12–2026.04"
partners: "Bosch (XC-CN)"
role: "World Models Algorithm Engineer"
category: "POC Project"
stage: "POC"
tags: ["research", "e2e", "world-model", "perception"]
cover: "/assets/media/projects/e2e_one_stage/E2E_vis.mp4"
cover_type: "video"
featured: false
order: 120
rich_body: true
summary: "A one-stage, pure-vision end-to-end driving POC that lifts 8 surround cameras into a single BEV feature, reads three structured perception heads (3D detection, HD map, occupancy) from it, predicts the next-frame BEV under generative scoring, and tokenizes everything into a Diffusion-Flow planner that emits the ego trajectory and neighbouring-agent states — perception, prediction, and planning optimised jointly."
privacy_note: "Bosch (XC-CN) POC. The architecture is presented at a conceptual, portfolio level; customer data, calibration, training corpora, and quantitative results are intentionally omitted or sanitized."
atlas:
  eyebrow: "Logic map"
  title: "Pixels to a planned trajectory — one differentiable pass"
  caption: "Hover a node to inspect its input, logic, output, and contribution. Lines show data flow; the planner reads one shared BEV."
  cols: 6
  nodes:
    - id: cams
      col: 2
      span: 4
      row: 1
      kind: input
      accent: cyan
      tag: "Input"
      title: "8V Surround"
      desc: "Multi-frame · pure vision"
      receives: "8 cameras, several frames"
      logic: "No LiDAR, no offline map"
      sends: "Raw multi-view images"
      gives: "Vision-only, low-cost sensing"
    - id: backbone
      col: 2
      span: 4
      row: 2
      kind: process
      accent: cyan
      tag: "Backbone"
      title: "Vision Backbone"
      desc: "Cross-view + temporal"
      receives: "Per-camera image streams"
      logic: "Cross-view attention + temporal fusion"
      sends: "Aligned view features"
      gives: "Motion-aware, geometry-aligned features"
    - id: bev
      col: 2
      span: 4
      row: 3
      kind: reason
      accent: purple
      tag: "Lift"
      title: "Unified BEV"
      desc: "One shared feature hub"
      receives: "All view features"
      logic: "Lift perspective → bird's-eye space"
      sends: "Single BEV feature"
      gives: "One representation every head shares"
    - id: det
      col: 1
      span: 2
      row: 4
      kind: output
      accent: cyan
      tag: "Head 1"
      title: "3D Detection"
      desc: "Dynamic objects"
      receives: "Shared BEV feature"
      logic: "Regress 3D boxes + motion"
      sends: "Dynamic agents"
      gives: "Where things move"
    - id: map
      col: 3
      span: 2
      row: 4
      kind: output
      accent: cyan
      tag: "Head 2"
      title: "Online HD Map"
      desc: "Static geometry"
      receives: "Shared BEV feature"
      logic: "Decode lanes + topology"
      sends: "Vectorized map"
      gives: "No pre-built map needed"
    - id: occ
      col: 5
      span: 2
      row: 4
      kind: output
      accent: cyan
      tag: "Head 3"
      title: "3D Occupancy"
      desc: "Volumetric semantics"
      receives: "Shared BEV feature"
      logic: "Dense class-labelled volume"
      sends: "Occupied space"
      gives: "Catches long-tail geometry"
    - id: future
      col: 1
      span: 2
      row: 5
      kind: reason
      accent: purple
      tag: "Predict"
      title: "Future BEV t+1"
      desc: "Self-supervised"
      receives: "Current BEV feature"
      logic: "Forecast next-frame BEV"
      sends: "Predicted BEV"
      gives: "Encodes scene dynamics"
    - id: critic
      col: 3
      span: 2
      row: 5
      kind: process
      accent: warn
      tag: "World prior"
      title: "Generative Critic"
      desc: "Frozen, pretrained"
      receives: "Predicted BEV"
      logic: "Score realism of forecast"
      sends: "Supervision signal"
      gives: "Keeps forecasts plausible"
    - id: tokens
      col: 5
      span: 2
      row: 5
      kind: process
      accent: blue
      tag: "Tokenize"
      title: "Scene Tokens"
      desc: "One planner language"
      receives: "Perception + BEV"
      logic: "Encode into token sequences"
      sends: "Conditioning tokens"
      gives: "Unifies inputs for planning"
    - id: plan
      col: 2
      span: 4
      row: 6
      kind: process
      accent: green
      tag: "Plan"
      title: "Diffusion-Flow Planner"
      desc: "Generative · multi-modal"
      receives: "Scene tokens"
      logic: "Denoise a trajectory from noise"
      sends: "Plan distribution"
      gives: "Replaces hand-tuned cost search"
    - id: traj
      col: 2
      span: 4
      row: 7
      kind: contribution
      accent: green
      tag: "Output"
      title: "Ego + Agent Futures"
      desc: "Joint · scene-consistent"
      media: "/assets/media/projects/e2e_one_stage/E2E_vis.mp4"
      media_type: video
      receives: "Denoised plan"
      logic: "Emit ego + neighbour states"
      sends: "Future trajectories"
      gives: "Pixels → planning, one network"
  edges:
    - { from: cams, to: backbone, kind: flow }
    - { from: backbone, to: bev, kind: flow }
    - { from: bev, to: det, kind: flow }
    - { from: bev, to: map, kind: flow }
    - { from: bev, to: occ, kind: flow }
    - { from: bev, to: future, kind: dashed }
    - { from: future, to: critic, kind: solid }
    - { from: det, to: tokens, kind: solid }
    - { from: map, to: tokens, kind: solid }
    - { from: occ, to: tokens, kind: solid }
    - { from: bev, to: tokens, kind: dashed }
    - { from: tokens, to: plan, kind: flow }
    - { from: plan, to: traj, kind: flow }
---
<div class="lawn-modules">

  <div class="tool-chips">
    <span class="chip">8V surround · pure vision</span>
    <span class="chip">Unified BEV feature</span>
    <span class="chip">3 perception heads</span>
    <span class="chip">Self-supervised future BEV</span>
    <span class="chip">Diffusion-Flow planner</span>
  </div>

  <div class="stat-band">
    <div class="stat"><b>8V</b><span>Surround cameras · multi-frame</span></div>
    <div class="stat accent"><b>1 BEV</b><span>One shared feature drives every head</span></div>
    <div class="stat"><b>3 heads</b><span>3D detection · HD map · occupancy</span></div>
    <div class="stat good"><b>One stage</b><span>Perception + prediction + planning, joint</span></div>
  </div>

  {% include logic-atlas.html %}

  <h2 class="lawn-h2">The architecture, end to end</h2>
  <div class="proj-figure on-white">
    <img src="{{ '/assets/media/projects/e2e_one_stage/E2E_8V_arch.png' | relative_url }}" alt="One-stage 8V end-to-end driving architecture" loading="lazy">
    <figcaption>One shared BEV feeds three perception heads and a future-BEV forecast; everything is tokenized into a Diffusion-Flow planner that denoises straight into the ego trajectory — no hand-designed 3D hand-off in the loop.</figcaption>
  </div>

  <h2 class="lawn-h2">On real test drives</h2>
  <div class="proj-figure">
    <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback>
      <source src="{{ '/assets/media/projects/e2e_one_stage/E2E_vis.mp4' | relative_url }}" type="video/mp4">
    </video>
    <figcaption>Surround perception (dynamic objects, online map, occupancy) and the generated ego trajectory — produced together by a single end-to-end network.</figcaption>
  </div>

  <h2 class="lawn-h2">Why one stage</h2>
  <div class="why-grid">
    <div class="why-card"><span class="why-x">Lossy 3D interfaces</span><span class="why-y">One shared BEV, no manual hand-off</span></div>
    <div class="why-card"><span class="why-x">Errors compound across modules</span><span class="why-y">Joint end-to-end optimisation</span></div>
    <div class="why-card"><span class="why-x">Boxes miss long-tail shapes</span><span class="why-y">Dense 3D occupancy head</span></div>
    <div class="why-card"><span class="why-x">A snapshot can't plan ahead</span><span class="why-y">Predict next-frame BEV</span></div>
    <div class="why-card"><span class="why-x">Forecasts drift off-manifold</span><span class="why-y">Frozen generative critic</span></div>
    <div class="why-card"><span class="why-x">Hand-tuned cost functions</span><span class="why-y">Diffusion-Flow generative planner</span></div>
  </div>

  <div class="ref-note">
    <strong>My role.</strong>
    <span>Integrated the static-perception, dynamic-perception, and AI-planner components into the single one-model POC, and ran the daily train / eval / visualization loop. Wording is high-level to protect enterprise confidentiality.</span>
  </div>

</div>
