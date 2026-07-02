---
title: "Generative Autonomous-Driving Simulation Platform"
subtitle: "A Cosmos-Transfer2.5 world model turned into a production simulation platform: sensor-level 7V generation, real-map (OSM) scenarios, a WorldSim↔WorldModel gRPC bridge, the first 4-step distillation of 7V surround video, and an all-in-one OneModel that unifies layout generation, GS-fix, and harmonization."
description: "A Cosmos-Transfer2.5-based generative simulation platform — 7V surround generation, real-map (OSM) scenarios, a WorldSim↔WorldModel gRPC bridge, 4-step video distillation, and a unified OneModel."
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
protected: true
rich_body: true
summary: "Built a Cosmos-Transfer2.5-based generative simulation platform: a 7V surround world model validated on internal data, real-map (Ingolstadt OSM → layout → 7V) scenario generation, a gRPC semantic bridge between WorldSim and the world model, the first 4-step distillation of 7V surround video (rCM + DMD2) for up to ~13.9× speedup, an editable platform for rare interaction data, and an all-in-one OneModel that serves layout generation, Gaussian-Splatting fix, and harmonization from a single denoiser."
privacy_note: "Bosch (XC-CN) ongoing platform. Architecture, method, and the acceleration results the author measured are shown at a portfolio level; customer data, calibration, and product details are intentionally omitted or sanitized."
atlas:
  eyebrow: "Logic map · distillation"
  title: "35 steps → 4 steps — compress the teacher's path, keep the picture sharp"
  caption: "A frozen teacher anchors the truth, a student learns the big strides, a dynamic critic keeps it sharp. Hover any node."
  cols: 4
  nodes:
    - id: teacher
      col: 1
      span: 2
      row: 1
      kind: input
      accent: ink
      tag: "Teacher"
      title: "35-step Teacher"
      desc: "Frozen · accurate"
      receives: "Real frames + conditions"
      logic: "Slow, exact denoising trajectory"
      sends: "Ground-truth path + init weights"
      gives: "A non-drifting truth anchor"
    - id: student
      col: 3
      span: 2
      row: 1
      kind: process
      accent: blue
      tag: "Student"
      title: "4-step Student"
      desc: "Trainable · fast"
      receives: "Teacher weights (init)"
      logic: "Bake CFG into one forward"
      sends: "Few-step samples"
      gives: "1 forward per step, not 2"
    - id: schedule
      col: 1
      span: 2
      row: 2
      kind: reason
      accent: cyan
      tag: "Schedule"
      title: "Sparsify Timesteps"
      desc: "35 → 4 landing points"
      receives: "Teacher noise levels"
      logic: "Index-mapped sub-sampling"
      sends: "4 student steps"
      gives: "Each big step maps to a teacher span"
    - id: critic
      col: 3
      span: 2
      row: 2
      kind: process
      accent: purple
      tag: "Critic"
      title: "Dynamic Critic"
      desc: "Trainable scorer"
      receives: "Student's current samples"
      logic: "Score how it looks now"
      sends: "Distribution direction"
      gives: "Always-fresh supervision"
    - id: bridge
      col: 1
      span: 2
      row: 3
      kind: process
      accent: blue
      tag: "Loss · path"
      title: "Bridge Consistency"
      desc: "Trajectory correctness"
      receives: "Teacher span + student step"
      logic: "Match bridge average velocity"
      sends: "Path gradient"
      gives: "Big step stays on the path"
    - id: dmd
      col: 3
      span: 2
      row: 3
      kind: process
      accent: purple
      tag: "Loss · look"
      title: "DMD Matching"
      desc: "Sharpness"
      receives: "Teacher + critic scores"
      logic: "Push student → real distribution"
      sends: "Distribution gradient"
      gives: "Restores few-step sharpness"
    - id: alt
      col: 1
      span: 4
      row: 4
      kind: process
      accent: warn
      tag: "Loop"
      title: "Alternating Optim"
      desc: "DMD2 / rCM"
      receives: "Student + critic"
      logic: "Freeze one, train the other"
      sends: "Stable training loop"
      gives: "Single graph → no OOM"
    - id: cascade
      col: 1
      span: 2
      row: 5
      kind: process
      accent: green
      tag: "Cascade"
      title: "Progressive Compress"
      desc: "35 → 4 → 2 → 1"
      receives: "Each level's model"
      logic: "Halve steps, init from previous"
      sends: "Next-level student"
      gives: "Stable, controllable convergence"
    - id: fourstep
      col: 3
      span: 2
      row: 5
      kind: contribution
      accent: green
      tag: "Result"
      title: "4-step 7V Model"
      desc: "First of its kind"
      media: "/assets/media/projects/gen_ad_sim/7v_distil_vis.mp4"
      media_type: video
      receives: "Path + look gradients"
      logic: "4 forwards, 7 views consistent"
      sends: "Real-time surround video"
      gives: "Up to ~13.9× faster inference"
  edges:
    - { from: teacher, to: student, kind: solid }
    - { from: teacher, to: schedule, kind: solid }
    - { from: schedule, to: bridge, kind: flow }
    - { from: teacher, to: bridge, kind: dashed }
    - { from: student, to: bridge, kind: flow }
    - { from: student, to: critic, kind: flow }
    - { from: student, to: dmd, kind: flow }
    - { from: teacher, to: dmd, kind: dashed }
    - { from: critic, to: dmd, kind: dashed }
    - { from: student, to: alt, kind: solid }
    - { from: critic, to: alt, kind: solid }
    - { from: bridge, to: fourstep, kind: flow }
    - { from: dmd, to: fourstep, kind: flow }
    - { from: fourstep, to: cascade, kind: flow }
atlas2:
  eyebrow: "Logic map · OneModel"
  title: "Three modes, one denoiser"
  caption: "Layout generation, GS-fix, and harmonization differ only in their start latent and condition — one shared Cosmos backbone serves all three."
  cols: 3
  nodes:
    - id: backbone
      col: 1
      span: 3
      row: 1
      kind: input
      accent: purple
      tag: "Backbone"
      title: "Shared Backbone"
      desc: "Cosmos Transfer 2.5"
      receives: "Conditions + start latent"
      logic: "One 7V video diffusion model"
      sends: "Same weights, three modes"
      gives: "Train + serve once, not thrice"
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
    - { from: backbone, to: mode1, kind: solid }
    - { from: backbone, to: mode2, kind: solid }
    - { from: backbone, to: mode3, kind: solid }
    - { from: mode1, to: start1, kind: flow }
    - { from: mode2, to: start2, kind: flow }
    - { from: mode3, to: start3, kind: flow }
    - { from: start1, to: adapter, kind: flow }
    - { from: start2, to: adapter, kind: flow }
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
    <span>Built the platform end-to-end: the 7V world model on Cosmos-Transfer2.5, the OSM→layout→7V pipeline, the WorldSim↔model gRPC bridge, the first 7V 4-step distillation (rCM + DMD2), the editable data platform, and the all-in-one OneModel. Numbers are the author's own measurements; details are sanitized.</span>
  </div>

</div>
