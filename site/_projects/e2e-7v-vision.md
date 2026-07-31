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
summary: "A one-stage, pure-vision end-to-end driving POC: eight surround cameras lifted into a single BEV feature, three perception heads and a Diffusion-Flow planner trained together, with no hand-designed 3D interface in between."
problem: "A modular driving stack hands 3D boxes from perception to planning. That interface quantises away everything the planner was not told to expect, and it blocks gradients — so nothing downstream can tell perception what it actually needed."
built: "One network from pixels to trajectory. Eight surround cameras are lifted into a single shared BEV feature; 3D detection, online HD mapping and 3D occupancy all read that same feature; a self-supervised next-frame BEV forecast, scored by a frozen generative prior, makes the representation carry dynamics; and everything is tokenised into a Diffusion-Flow planner that denoises the ego trajectory and its neighbours' futures together."
result: "Perception, prediction and planning are optimised jointly: the planner's loss reaches back through the tokeniser and the BEV into the backbone, so perception is trained for what planning needs rather than for a detection benchmark."
my_role: "I integrated the static-perception, dynamic-perception and AI-planner components into the single one-model POC, and ran the daily train / eval / visualisation loop. Wording is kept high-level for enterprise confidentiality."
glossary:
  - term: "BEV"
    def: "Bird's-eye view. A top-down feature grid in ego coordinates — the common frame that lets multiple cameras and multiple tasks share one representation."
  - term: "3D occupancy"
    def: "A dense, class-labelled volume of what space is filled. Unlike boxes, it can describe objects with no category and no canonical shape."
  - term: "Diffusion-Flow planner"
    def: "A generative planner that denoises a trajectory out of noise, so genuinely ambiguous situations come out as several distinct plans rather than an averaged one."
  - term: "One-stage"
    def: "Perception, prediction and planning trained in a single differentiable pass, with no hand-designed 3D hand-off between them."
privacy_note: "Bosch (XC-CN) POC. The architecture is presented at a conceptual, portfolio level; customer data, calibration, training corpora, and quantitative results are intentionally omitted or sanitized."
atlas:
  eyebrow: "Logic map"
  title: "Pixels to a planned trajectory — one differentiable pass"
  caption: "The centre column is what runs in the car. The right lane exists only while training. The pink arrow is the point of the whole project: the planner's loss reaches all the way back into the backbone."
  cols: 9
  legend:
    - { accent: cyan, label: "Sensing & perception" }
    - { accent: purple, label: "Representation & forecast" }
    - { accent: blue, label: "Planner interface" }
    - { accent: green, label: "Planning & output" }
    - { accent: warn, label: "Generative prior" }
  nodes:
    - id: cams
      col: 1
      span: 6
      row: 1
      kind: input
      accent: cyan
      lane: main
      tag: "Input"
      title: "8V Surround Cameras"
      desc: "Multi-frame, vision only"
      spec: "8 views · no LiDAR · no offline map"
      receives: "Eight surround cameras, several consecutive frames"
      logic: "Sample a synchronised multi-view, multi-frame clip"
      sends: "Raw multi-view image streams"
      why: "Cameras are the only sensor already on every trim level, so a vision-only stack is the one that can actually ship at volume."
    - id: backbone
      col: 1
      span: 6
      row: 2
      kind: process
      accent: cyan
      lane: main
      tag: "Backbone"
      title: "Vision Backbone"
      desc: "Cross-view + temporal fusion"
      receives: "Per-camera image streams"
      logic: "Cross-view attention across cameras, temporal fusion across frames"
      sends: "Geometry-aligned, motion-aware view features"
      why: "Fusing across views and time before the lift means overlap regions and motion are resolved once, not re-derived by every downstream head."
    - id: bev
      col: 1
      span: 6
      row: 3
      kind: reason
      accent: purple
      lane: main
      core: true
      tag: "Lift"
      title: "Unified BEV Feature"
      desc: "The single hub every head reads"
      spec: "1 shared feature · 4 consumers"
      receives: "Aligned multi-view features"
      logic: "Lift perspective features into one bird's-eye feature volume"
      sends: "One BEV feature, shared by every downstream branch"
      why: "One shared hub instead of a per-task neck: the heads cannot drift apart, and adding a head costs a decoder rather than a second pyramid."
      tradeoff: "A shared trunk means head losses compete for capacity — the joint loss weighting becomes the thing you actually tune."
      role: "Owned the integration that made a single BEV serve static perception, dynamic perception and the planner in one model."
    - id: det
      col: 1
      span: 2
      row: 4
      kind: output
      accent: cyan
      lane: main
      tag: "Perception"
      title: "3D Detection"
      desc: "Dynamic agents"
      receives: "Shared BEV feature"
      logic: "Regress 3D boxes and per-object motion"
      sends: "Dynamic agents with velocity"
      why: "Reading boxes off the shared BEV keeps detection in the same frame as the map and the planner, so no re-projection step can lose accuracy."
    - id: map
      col: 3
      span: 2
      row: 4
      kind: output
      accent: cyan
      lane: main
      tag: "Perception"
      title: "Online HD Map"
      desc: "Static geometry"
      receives: "Shared BEV feature"
      logic: "Decode lane elements and their topology"
      sends: "Vectorised local map"
      why: "Building the map online removes the dependency on a pre-surveyed HD map, which is the single biggest cost blocker for wide deployment."
    - id: occ
      col: 5
      span: 2
      row: 4
      kind: output
      accent: cyan
      lane: main
      tag: "Perception"
      title: "3D Occupancy"
      desc: "Volumetric semantics"
      receives: "Shared BEV feature"
      logic: "Predict a dense, class-labelled occupancy volume"
      sends: "Occupied and free space"
      why: "Boxes cannot describe a fallen ladder or an open tailgate; a dense volume catches the long-tail geometry that boxes silently drop."
      tradeoff: "Dense volumes are the most expensive head in the stack — resolution is traded directly against latency."
    - id: future
      col: 7
      span: 3
      row: 3
      kind: reason
      accent: purple
      lane: aux
      tag: "Auxiliary"
      title: "Future BEV t+1"
      desc: "Self-supervised forecast"
      receives: "Current BEV feature"
      logic: "Forecast the next-frame BEV; the real next frame is the label"
      sends: "Predicted next-frame BEV (training only)"
      why: "Forcing the BEV to predict its own future makes it encode scene dynamics, not just a snapshot — and it costs no extra annotation."
      tradeoff: "It is free supervision but not free compute: it is dropped at inference, so the car never pays for it."
    - id: critic
      col: 7
      span: 3
      row: 4
      kind: process
      accent: warn
      lane: prior
      tag: "Prior"
      title: "Generative Critic"
      desc: "Scores how plausible a forecast is"
      receives: "Predicted next-frame BEV"
      logic: "Score realism against a pretrained generative prior"
      sends: "Realism signal for the forecast loss"
      why: "A pure regression loss lets forecasts blur into the mean; a frozen generative prior keeps them on the manifold of scenes that actually occur."
      tradeoff: "Frozen means cheap and stable, but the prior can only judge what its pretraining covered."
    - id: tokens
      col: 1
      span: 6
      row: 5
      kind: process
      accent: blue
      lane: main
      tag: "Interface"
      title: "Scene Tokens"
      desc: "One language for the planner"
      spec: "3 heads + BEV → 1 sequence"
      receives: "Detection, map, occupancy and the BEV feature"
      logic: "Encode heterogeneous outputs into one token sequence"
      sends: "Conditioning tokens"
      why: "Tokens replace the hand-designed 3D interface between perception and planning — the piece that normally quantises away information and blocks gradients."
    - id: plan
      col: 1
      span: 6
      row: 6
      kind: process
      accent: green
      lane: main
      core: true
      tag: "Plan"
      title: "Diffusion-Flow Planner"
      desc: "Generative, multi-modal"
      receives: "Scene tokens"
      logic: "Denoise a trajectory out of noise, conditioned on the tokens"
      sends: "A distribution over plans, not a single guess"
      why: "A generative planner represents genuinely ambiguous situations (yield or go) as multiple modes, where a regression planner averages them into an unsafe middle."
      tradeoff: "Multi-step denoising costs more than a single forward pass — the step count is the knob between plan diversity and latency."
      role: "Integrated the planner with the perception stack and ran the daily train / eval / visualisation loop for the joint model."
    - id: traj
      col: 1
      span: 6
      row: 7
      kind: contribution
      accent: green
      lane: main
      tag: "Output"
      title: "Ego + Agent Futures"
      desc: "Joint and scene-consistent"
      media: "/assets/media/projects/e2e_one_stage/E2E_vis.mp4"
      media_type: video
      receives: "Denoised plan"
      logic: "Emit the ego trajectory together with neighbouring-agent states"
      sends: "Scene-consistent future trajectories"
      why: "Planning the ego and its neighbours in one shot keeps the plan internally consistent — the ego cannot assume a future the other agents contradict."
  edges:
    - { from: cams, to: backbone, kind: flow, label: "8 views · T frames" }
    - { from: backbone, to: bev, kind: flow, label: "lift to BEV" }
    - { from: bev, to: det, kind: flow }
    - { from: bev, to: map, kind: flow, label: "one shared feature" }
    - { from: bev, to: occ, kind: flow }
    - { from: det, to: tokens, kind: cond }
    - { from: map, to: tokens, kind: cond, label: "3 heads → 1 sequence" }
    - { from: occ, to: tokens, kind: cond }
    - { from: bev, to: tokens, kind: cond }
    - { from: tokens, to: plan, kind: flow, label: "conditioning tokens" }
    - { from: plan, to: traj, kind: flow, label: "denoised plan" }
    - { from: bev, to: future, kind: train, label: "next-frame target" }
    - { from: future, to: critic, kind: train }
    - { from: plan, to: backbone, kind: grad, label: "∇ planner loss" }
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
