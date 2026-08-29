---
title: "Generative Autonomous-Driving Simulation Platform"
subtitle: "A Cosmos-Transfer2.5 world model turned into a production simulation platform: sensor-level 7V generation, real-map scenarios, a WorldSim↔WorldModel bridge, 4-step distillation of 7V surround video, and one denoiser that serves three jobs."
description: "A Cosmos-Transfer2.5-based generative simulation platform — 7V surround generation, real-map (OSM) scenarios, a WorldSim↔WorldModel gRPC bridge, 4-step video distillation for ~13.9× faster rollouts, and a unified OneModel."
date_range: "2025.03–Present"
partners: "Bosch (XC-CN)"
role: "World Models Algorithm Engineer"
category: "Research Platform"
stage: "Ongoing"
tags: ["research", "world-model", "generative", "e2e"]
cover: "/assets/media/projects/gen_ad_sim/ingolstadt_gen_video_grid.mp4"
cover_type: "video"
featured: true
order: 140
protected: false
rich_body: true
summary: "A generative simulation platform built on Cosmos-Transfer2.5: a 7-camera surround world model, real-map scenario generation, and a 4-step distilled sampler that makes surround rollouts fast enough to sit inside a closed loop."
problem: "Real driving logs cannot cover the rare interactions that matter most, and collecting them is slow, expensive and unsafe. Generated video could fill the gap — but a 35-step surround-video diffusion model is far too slow to sit inside a closed simulation loop."
built: "A 7-camera surround world model on Cosmos-Transfer2.5, driven by real-map layouts (Ingolstadt OSM → BEV layout → 7V video) and connected to our closed-loop simulator over a semantic bridge, so a scenario can be authored, generated and edited rather than waited for."
result: "Four-step distillation (bridge consistency plus distribution matching) cut the sampler from 35 steps to 4 for up to <strong>~13.9× faster</strong> rollouts, and a single denoiser now serves layout generation, Gaussian-Splatting repair and harmonization instead of three separately trained models."
my_role: "I own the distillation track end to end — schedule design, the alternating student/critic training loop, and the progressive 35→4→2→1 cascade — and the OneModel unification that collapsed three task-specific models into one. The platform itself is a team effort; scenario authoring and simulator integration are shared work."
relation: "This platform is the parent effort. Vector Traffic Generation & Sensor-Level Closed-Loop Simulation is the track inside it that decides what the traffic does and how the result is re-rendered."
glossary:
  - term: "Cosmos-Transfer2.5"
    def: "NVIDIA's video world-model backbone; the pretrained diffusion model this platform generates surround video with."
  - term: "rCM"
    def: "Bridge-consistency distillation: the student must reproduce the teacher's average velocity across a whole span of denoising steps, so one big step stays on the teacher's trajectory."
  - term: "DMD2"
    def: "Distribution Matching Distillation: a trainable critic scores the student's current samples, pushing the few-step output back toward the real data distribution and restoring sharpness."
  - term: "OSM"
    def: "OpenStreetMap. Real road geometry is converted into a BEV layout so generated scenarios sit on a genuine map rather than an invented one."
  - term: "gRPC bridge"
    def: "The semantic interface between the closed-loop simulator (WorldSim) and the world model, so simulation state and generated sensor frames can be exchanged per step."
  - term: "Gaussian Splatting"
    def: "An explicit 3D representation optimised from real frames; used here to render photorealistic backgrounds from viewpoints the car never actually drove."
privacy_note: "Bosch (XC-CN) ongoing platform. Architecture, method, and the acceleration results the author measured are shown at a portfolio level; customer data, calibration, and product details are intentionally omitted or sanitized."
atlas:
  eyebrow: "Logic map · distillation"
  title: "35 steps → 4 — compress the teacher's path, keep the picture sharp"
  caption: "Everything except the student is scaffolding: the teacher is frozen, the critic and both losses exist only during training, and only the student ships. Two losses because a big step can go wrong in two different ways — off the path, or off the data distribution."
  cols: 4
  legend:
    - { accent: ink, label: "Frozen teacher" }
    - { accent: cyan, label: "Step schedule" }
    - { accent: blue, label: "Student · path loss" }
    - { accent: purple, label: "Critic · distribution loss" }
    - { accent: warn, label: "Training loop" }
    - { accent: green, label: "Shipped result" }
  nodes:
    - id: teacher
      col: 1
      span: 2
      row: 1
      kind: input
      accent: ink
      lane: prior
      tag: "Teacher"
      title: "35-step Teacher"
      desc: "Defines the trajectory to imitate"
      spec: "35 steps · never updated"
      receives: "Real frames and their conditions"
      logic: "Run the slow, exact denoising trajectory"
      sends: "Reference path plus the student's initial weights"
      why: "Freezing the teacher gives the student a target that cannot drift; if both moved, there would be nothing anchoring the compression to reality."
    - id: student
      col: 3
      span: 2
      row: 1
      kind: process
      accent: blue
      lane: main
      core: true
      tag: "Student"
      title: "4-step Student"
      desc: "The only model that ships"
      spec: "4 steps · CFG baked in"
      receives: "Teacher weights as initialisation"
      logic: "Take four large denoising steps, with classifier-free guidance folded into a single forward"
      sends: "Few-step samples"
      why: "Baking guidance into the weights removes the second forward pass per step — the speedup compounds with the step reduction rather than fighting it."
      role: "Designed and trained the student; owned the distillation track end to end."
    - id: schedule
      col: 1
      span: 2
      row: 2
      kind: reason
      accent: cyan
      lane: aux
      tag: "Schedule"
      title: "Sparsify Timesteps"
      desc: "Choose the four landing points"
      receives: "The teacher's noise-level schedule"
      logic: "Index-mapped sub-sampling of the teacher's timesteps"
      sends: "Four student steps, each covering a teacher span"
      why: "Where the four steps land matters more than how many there are — a bad schedule wastes a step on a range where almost nothing changes."
    - id: critic
      col: 3
      span: 2
      row: 2
      kind: process
      accent: purple
      lane: aux
      tag: "Critic"
      title: "Dynamic Critic"
      desc: "Scores the student as it is now"
      receives: "The student's current samples"
      logic: "Learn a score for the student's evolving output distribution"
      sends: "A direction back toward the real distribution"
      why: "A fixed critic goes stale the moment the student improves; retraining it alongside keeps the supervision meaningful for the whole run."
      tradeoff: "A trainable critic doubles the moving parts — the price is the alternating loop below."
    - id: bridge
      col: 1
      span: 2
      row: 3
      kind: process
      accent: blue
      lane: aux
      tag: "Loss · path"
      title: "Bridge Consistency"
      desc: "Is the big step still on the path?"
      receives: "A teacher span and the matching student step"
      logic: "Match the average velocity across the bridged span"
      sends: "Path gradient"
      why: "Matching average velocity over a span, rather than the endpoint, is what lets one student step legitimately replace many teacher steps."
    - id: dmd
      col: 3
      span: 2
      row: 3
      kind: process
      accent: purple
      lane: aux
      tag: "Loss · look"
      title: "Distribution Matching"
      desc: "Does it still look real?"
      receives: "Teacher and critic scores"
      logic: "Push the student's output distribution toward the real one"
      sends: "Distribution gradient"
      why: "Path correctness alone yields blurry frames; this is the loss that buys back the sharpness few-step sampling normally loses."
    - id: alt
      col: 1
      span: 4
      row: 4
      kind: process
      accent: warn
      lane: aux
      tag: "Loop"
      title: "Alternating Optimisation"
      desc: "Freeze one, train the other"
      receives: "Student and critic"
      logic: "Update the critic and the student in alternation, never in one graph"
      sends: "A stable training loop"
      why: "Two adversarial-style networks in one backward graph is where 7-view video distillation runs out of memory; alternating keeps the graph small enough to fit."
      tradeoff: "Alternating costs wall-clock steps, but it is the difference between training and not training at all at this resolution."
    - id: cascade
      col: 1
      span: 2
      row: 5
      kind: process
      accent: green
      lane: aux
      tag: "Cascade"
      title: "Progressive Compression"
      desc: "35 → 4 → 2 → 1"
      receives: "The model from the previous level"
      logic: "Halve the step count, initialise from the level above"
      sends: "The next-level student"
      why: "Jumping straight to one step diverges; halving keeps every level close enough to its teacher that the optimisation stays well-behaved."
    - id: fourstep
      col: 3
      span: 2
      row: 5
      kind: contribution
      accent: green
      lane: main
      core: true
      tag: "Result"
      title: "4-step 7V Model"
      desc: "Fast enough for a closed loop"
      spec: "up to ~13.9× faster"
      media: "/assets/media/projects/gen_ad_sim/7v_distil_vis.mp4"
      media_type: video
      receives: "Path and distribution gradients"
      logic: "Four forward passes, seven views kept mutually consistent"
      sends: "Surround video at interactive speed"
      why: "Speed is not a vanity metric here: below a certain rollout time the world model simply cannot sit inside the simulation loop at all."
      role: "Measured the speedup and integrated the distilled sampler into the platform."
  edges:
    - { from: teacher, to: student, kind: cond, label: "init weights" }
    - { from: teacher, to: schedule, kind: cond }
    - { from: schedule, to: bridge, kind: train, label: "4 spans" }
    - { from: teacher, to: bridge, kind: train }
    - { from: student, to: bridge, kind: train }
    - { from: student, to: critic, kind: train }
    - { from: student, to: dmd, kind: train }
    - { from: teacher, to: dmd, kind: train }
    - { from: critic, to: dmd, kind: train }
    - { from: student, to: alt, kind: cond }
    - { from: critic, to: alt, kind: cond }
    - { from: bridge, to: fourstep, kind: train, label: "∇ path" }
    - { from: dmd, to: fourstep, kind: train, label: "∇ look" }
    - { from: fourstep, to: cascade, kind: train, label: "next level" }
atlas2:
  eyebrow: "Logic map · OneModel"
  title: "Three jobs, one denoiser"
  caption: "Layout generation, Gaussian-Splatting repair and harmonization look like three different problems. They differ only in what the sampler starts from and what it is conditioned on — so they can share one backbone."
  cols: 3
  legend:
    - { accent: purple, label: "Shared backbone" }
    - { accent: blue, label: "Mode 1 · layout generation" }
    - { accent: cyan, label: "Mode 2 · GS repair" }
    - { accent: green, label: "Mode 3 · harmonization" }
    - { accent: warn, label: "Shared control path" }
  nodes:
    - id: backbone
      col: 1
      span: 3
      row: 1
      kind: input
      accent: purple
      core: true
      tag: "Backbone"
      title: "Shared Backbone"
      desc: "Cosmos-Transfer2.5"
      spec: "1 set of weights · 3 tasks"
      receives: "Conditions and a start latent"
      logic: "One 7-view video diffusion model"
      sends: "The same weights, driven three ways"
      why: "Three task-specific models meant three trainings, three checkpoints and three sets of drift. One backbone means an improvement anywhere lands everywhere."
      tradeoff: "A shared backbone cannot be tuned to death for any single task — worth it while all three tasks are still moving."
      role: "Designed and owned the OneModel unification."
    - id: mode1
      col: 1
      span: 1
      row: 2
      kind: process
      accent: blue
      tag: "Mode 1"
      title: "Layout Generation"
      desc: "Controllable scene"
      receives: "Layout video + camera/time/7V"
      logic: "Generate from pure noise"
      sends: "Driving-scene video"
      gives: "Controllable surround generation"
    - id: mode2
      col: 2
      span: 1
      row: 2
      kind: process
      accent: cyan
      tag: "Mode 2"
      title: "GS Fix"
      desc: "Repair reconstruction"
      receives: "Degraded GS video + optional layout"
      logic: "Denoise from degraded start"
      sends: "Clean video"
      gives: "Fills holes / artifacts"
    - id: mode3
      col: 3
      span: 1
      row: 2
      kind: process
      accent: green
      tag: "Mode 3"
      title: "Harmonizer"
      desc: "Blend inserted assets"
      receives: "Disharmonized video + mask"
      logic: "ControlNet harmonization"
      sends: "Harmonized video"
      gives: "Natural fg/bg lighting"
    - id: start1
      col: 1
      span: 1
      row: 3
      kind: reason
      accent: blue
      tag: "Start"
      title: "Pure Noise"
      desc: "Generate from scratch"
      receives: "Gaussian noise"
      logic: "Standard diffusion start"
      sends: "Latent to adapter"
      gives: "Maximum freedom"
    - id: start2
      col: 2
      span: 1
      row: 3
      kind: reason
      accent: cyan
      tag: "Start"
      title: "Degraded GS Latent"
      desc: "Start from the flaw"
      receives: "Low-quality GS render"
      logic: "Noise = the degradation itself"
      sends: "Latent to adapter"
      gives: "Keeps the real structure"
    - id: start3
      col: 3
      span: 1
      row: 3
      kind: reason
      accent: green
      tag: "Start"
      title: "Disharmonized Video"
      desc: "Condition on the clash"
      receives: "Inserted-asset video"
      logic: "Disharmony as the condition"
      sends: "Latent to adapter"
      gives: "Targets only the mismatch"
    - id: adapter
      col: 1
      span: 3
      row: 4
      kind: process
      accent: warn
      tag: "Control"
      title: "Unified Condition Adapter"
      desc: "One injection path"
      receives: "Layout / GS / disharmony / mask"
      logic: "Encode + inject into denoiser"
      sends: "Conditioned features"
      gives: "Three tasks, one control path"
    - id: denoiser
      col: 1
      span: 3
      row: 5
      kind: process
      accent: purple
      tag: "Denoise"
      title: "Shared Denoiser"
      desc: "Temporal + multi-view"
      receives: "Conditioned latent"
      logic: "Predict clean, consistent 7V"
      sends: "Denoised latent"
      gives: "One model holds all consistency"
    - id: out
      col: 1
      span: 3
      row: 6
      kind: contribution
      accent: green
      tag: "Output"
      title: "7V Video Output"
      desc: "Three results, one model"
      receives: "Decoded latent"
      logic: "Layout · GS-fix · harmonized"
      sends: "High-quality surround video"
      gives: "One model serves three tasks"
  edges:
    - { from: backbone, to: mode1, kind: cond }
    - { from: backbone, to: mode2, kind: cond, label: "same weights" }
    - { from: backbone, to: mode3, kind: cond }
    - { from: mode1, to: start1, kind: flow }
    - { from: mode2, to: start2, kind: flow }
    - { from: mode3, to: start3, kind: flow }
    - { from: start1, to: adapter, kind: flow }
    - { from: start2, to: adapter, kind: flow, label: "one control path" }
    - { from: start3, to: adapter, kind: flow }
    - { from: adapter, to: denoiser, kind: flow }
    - { from: denoiser, to: out, kind: flow }
---
<div class="lawn-modules">

  <div class="tool-chips">
    <span class="chip">Cosmos-Transfer2.5 base</span>
    <span class="chip">7V surround · sensor-level</span>
    <span class="chip">OSM → layout → video</span>
    <span class="chip">WorldSim ↔ model gRPC</span>
    <span class="chip">First 7V 4-step distillation</span>
    <span class="chip">Flux → 7V style transfer</span>
    <span class="chip">All-in-one OneModel</span>
  </div>

  <div class="stat-band">
    <div class="stat"><b>7V</b><span>Surround-view, multi-view consistent</span></div>
    <div class="stat accent"><b>4-step</b><span>Distilled from a 35-step teacher</span></div>
    <div class="stat good"><b>~13.9×</b><span>Peak measured inference speedup</span></div>
    <div class="stat"><b>1 model</b><span>Layout gen · GS-fix · harmonizer</span></div>
  </div>

  <h2 class="lawn-h2">01 · Cosmos-Transfer2.5 on internal driving data</h2>
  <p class="module-oneliner">A 7V generative world model, built on Cosmos-Transfer2.5 and validated on internal data.</p>
  <div class="proj-figrow two">
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/transfer2.5_gen_vis_tsl0.mp4' | relative_url }}" type="video/mp4"></video>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/transfer2.5_gen_vis_tsl1.mp4' | relative_url }}" type="video/mp4"></video>
    </figure>
  </div>

  <h2 class="lawn-h2">02 · Real maps → 7V video (Ingolstadt OSM)</h2>
  <p class="module-oneliner">Download a real city map (OSM), convert it to the model's layout, and generate surround video — including a snow variant.</p>
  <div class="proj-figrow three">
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/ingolstadt_control_grid.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>Control layout from OSM.</figcaption>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/ingolstadt_gen_video_grid.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>Generated 7V sensor video.</figcaption>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/ingolstadt_gen_video_grid2.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>Same scene, snow weather.</figcaption>
    </figure>
  </div>

  <h2 class="lawn-h2">03 · Flux → single-frame 7V: weather, season &amp; style transfer</h2>
  <p class="module-oneliner">Lift a single-image Flux generator into a 7V surround model — one synchronized frame across every camera — then drive it with text to restyle the whole rig into new weather, seasons, and looks while the underlying geometry stays put.</p>
  <div class="why-grid">
    <div class="why-card"><span class="why-x">Single-camera Flux</span><span class="why-y">Extended to a 7V surround rig, one consistent frame</span></div>
    <div class="why-card"><span class="why-x">One fixed look</span><span class="why-y">Text-driven weather / season / style swaps</span></div>
    <div class="why-card"><span class="why-x">Per-view drift</span><span class="why-y">Cross-camera geometry held while appearance changes</span></div>
  </div>
  <div class="proj-figure" style="margin-top:1.1rem">
    <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/gen_model_style_transformation.mp4' | relative_url }}" type="video/mp4"></video>
    <figcaption><strong>Surround style transfer.</strong> A single synchronized 7V frame restyled across weather, season, and visual style — rain, snow, dusk and more — from one shared, text-controllable generator, with cross-camera consistency preserved.</figcaption>
  </div>

  <h2 class="lawn-h2">04 · WorldSim ↔ World Model gRPC bridge</h2>
  <div class="proj-figure on-white">
    <img src="{{ '/assets/media/projects/gen_ad_sim/WorldSim_gRPC_sys.png' | relative_url }}" alt="WorldSim to World Model gRPC system" loading="lazy">
    <figcaption>WorldSim serializes scene data (calibration, ego trajectory, dynamic obstacles, static map) over OSI semantics to the World Model server, which validates, caches, converts to Parquet, and asynchronously triggers Cosmos rendering — a semantic + async bridge between simulation and generation.</figcaption>
  </div>

  <h2 class="lawn-h2">05 · First 4-step distillation of 7V surround video</h2>
  {% include logic-atlas.html %}

  <div class="ablation wrap">
    <table>
      <thead><tr><th>Mode</th><th>Spec</th><th>Original</th><th>Distilled</th><th>Speedup</th></tr></thead>
      <tbody>
        <tr><td>Single clip (first)</td><td>29 / 203 frames</td><td>796.76 s</td><td>106.32 s</td><td><strong>7.49×</strong></td></tr>
        <tr><td>Single clip (steady)</td><td>29 / 203 frames</td><td>744.16 s</td><td>53.68 s</td><td><strong>13.86×</strong></td></tr>
        <tr><td>Auto-regressive (long)</td><td>57 / 399 frames</td><td>1546.87 s</td><td>165.87 s</td><td><strong>9.33×</strong></td></tr>
      </tbody>
    </table>
  </div>

  <p class="module-oneliner">Distilled 4-step model — surround generation at a fraction of the cost.</p>
  <div class="proj-figrow two">
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/7v_distil_vis.mp4' | relative_url }}" type="video/mp4"></video>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/7v_distil_vis2.mp4' | relative_url }}" type="video/mp4"></video>
    </figure>
  </div>

  <h2 class="lawn-h2">Editable platform — rare interaction scenarios</h2>
  <p class="module-oneliner">Edit the layout on a real clip, then regenerate with the 4-step model to produce hard-to-collect interaction data.</p>
  <div class="proj-figrow three">
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/1942452852756152320_raw_rgb.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>Raw captured clip.</figcaption>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/1942452852756152320_edit_layout.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>Edited control layout.</figcaption>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/1942452852756152320_4step_rgb.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>4-step regenerated result.</figcaption>
    </figure>
  </div>

  <h2 class="lawn-h2">06 · All-in-one OneModel — three modes, one denoiser</h2>
  {% include logic-atlas.html atlas=page.atlas2 %}

  <h3 class="sub-head"><span class="ver">Data</span> Training-set construction</h3>
  <div class="why-grid">
    <div class="why-card">
      <span class="why-x">GS-fix needs paired GT</span>
      <span class="why-y">Same trajectory: degraded GS render → input, original real video → GT (~35W clips)</span>
    </div>
    <div class="why-card">
      <span class="why-x">Harmonizer needs disharmony pairs</span>
      <span class="why-y">SAM3 vehicle masks → match by object ID/IoU → build (disharmonized → harmonized) pairs</span>
    </div>
  </div>

  <h3 class="sub-head"><span class="ver v2">Vis</span> The two new modes</h3>
  <div class="proj-figrow two">
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/Gaussian_fix_vis.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption><strong>GS-fix.</strong> Bottom: input · top: single-frame baseline · middle: our video result · then GT.</figcaption>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/gen_ad_sim/harmonization_combined_top10_vstack.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption><strong>Harmonizer.</strong> Third column — our Cosmos-based result blends inserted assets most naturally.</figcaption>
    </figure>
  </div>

  <div class="ref-note">
    <strong>My role.</strong>
    <span>Built the platform end-to-end: the 7V world model on Cosmos-Transfer2.5, the OSM→layout→7V pipeline, the WorldSim↔model gRPC bridge, the 4-step distillation of 7-camera surround video (rCM + DMD2) — to our knowledge the first in our setting — the editable data platform, and the all-in-one OneModel. Numbers are the author's own measurements; details are sanitized.</span>
  </div>

</div>
