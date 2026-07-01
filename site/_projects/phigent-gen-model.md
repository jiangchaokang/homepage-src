---
title: "Controllable Surround-View Driving Generation"
subtitle: "A controllable multi-view world model for driving: 3D layout + map + multi-granularity control signals injected into a diffusion process to generate geometrically-consistent 4V / 7V / 11V images and video — for data augmentation and open-loop simulation."
date_range: "2023.05–2024"
partners: "PhiGent Robotics"
role: "Generative Driving Algorithm Engineer"
category: "Research Project"
stage: "Pre-research"
tags: ["research", "world-model", "generative", "e2e"]
cover: "/assets/media/projects/phigent_gen_model/phigent_gen_7V_video2.mp4"
cover_type: "video"
featured: true
order: 90
rich_body: true
summary: "Built a controllable surround-view driving generator that compresses 3D boxes and maps into spatial conditions, encodes text / reference frames / lanes / camera calibration into condition tokens, and injects them into a UNet diffusion backbone — producing cross-camera-consistent 4V / 7V / 11V images and video for data augmentation and open-loop simulation, evolving from OpenSora 1.0 + SD 3.5 to a MagicDrive-fused in-house model."
privacy_note: "PhiGent Robotics research. Only sanitized generation results and high-level pipeline descriptions are shown; dataset details and internal evaluation metrics are omitted. The OmniNWM follow-up was led by former colleagues after my departure and is credited below."
atlas:
  eyebrow: "Logic map"
  title: "Noise to controllable surround worlds"
  caption: "Hover a node to inspect how structure, tokens, and denoising create geometry-aligned 4V / 7V / 11V output."
  cols: 6
  nodes:
    - id: noise
      col: 2
      span: 4
      row: 1
      kind: input
      accent: ink
      tag: "Start"
      title: "Gaussian Noise"
      desc: "Blank latent canvas"
      receives: "Pure random latents"
      logic: "Seed every camera view"
      sends: "Noisy surround latents"
      gives: "Enables diffusion generation"
    - id: structure
      col: 1
      span: 3
      row: 2
      kind: input
      accent: cyan
      tag: "Layout"
      title: "3D Boxes + Map"
      desc: "Projected per view"
      media: "/assets/media/projects/phigent_gen_model/phigent_7V_imggen_pipeline.png"
      media_type: image
      receives: "Boxes and HD map"
      logic: "Project into camera planes"
      sends: "View-space scene structure"
      gives: "Anchors object-road geometry"
    - id: encoders
      col: 1
      span: 3
      row: 3
      kind: process
      accent: cyan
      tag: "Encode"
      title: "Layout / Map Encoders"
      desc: "Spatial condition features"
      receives: "Projected boxes and map"
      logic: "E_Layout + E_Map compress"
      sends: "Spatial condition features"
      gives: "Keeps cameras aligned"
    - id: controls
      col: 4
      span: 3
      row: 2
      kind: input
      accent: blue
      tag: "Control"
      title: "Condition Tokens"
      desc: "Text · frames · rig"
      receives: "Text, refs, lanes, calibration"
      logic: "Encode multi-granularity controls"
      sends: "Condition token set"
      gives: "Steers appearance and rig"
    - id: unet
      col: 2
      span: 4
      row: 4
      kind: process
      accent: purple
      tag: "Backbone"
      title: "UNet Diffusion"
      desc: "Autoregressive generator"
      receives: "Noise + all conditions"
      logic: "Inject conditions each step"
      sends: "Refined surround latents"
      gives: "Unifies structure and style"
    - id: denoise
      col: 2
      span: 4
      row: 5
      kind: reason
      accent: purple
      tag: "Denoise"
      title: "Iterative Guidance"
      desc: "Semantic + geometric"
      receives: "Conditioned UNet updates"
      logic: "Repeated denoising rounds"
      sends: "Aligned multi-view latents"
      gives: "Holds cross-camera consistency"
    - id: decode
      col: 2
      span: 4
      row: 6
      kind: output
      accent: green
      tag: "Decode"
      title: "Surround RGB"
      desc: "4V / 7V / 11V"
      media: "/assets/media/projects/phigent_gen_model/same_scene_11V_map2.gif"
      media_type: image
      receives: "Geometry-aligned latents"
      logic: "Decoder restores pixels"
      sends: "Multi-view images / video"
      gives: "Generates controllable worlds"
    - id: augment
      col: 1
      span: 3
      row: 7
      kind: contribution
      accent: green
      tag: "Use"
      title: "Data Augmentation"
      desc: "Scene + style replacement"
      media: "/assets/media/projects/phigent_gen_model/same_scene_7V_map1.gif"
      media_type: image
      receives: "Generated surround scenes"
      logic: "Vary style, hold layout"
      sends: "Long-tail training data"
      gives: "Cuts collection burden"
    - id: simulation
      col: 4
      span: 3
      row: 7
      kind: contribution
      accent: green
      tag: "Use"
      title: "Open-Loop Simulation"
      desc: "Controllable rollouts"
      receives: "Generated videos"
      logic: "Replay requested conditions"
      sends: "Synthetic driving clips"
      gives: "Tests controlled scenarios"
    - id: evolution
      col: 1
      span: 3
      row: 8
      kind: process
      accent: warn
      tag: "Evolve"
      title: "OpenSora → MagicDrive"
      desc: "In-house fusion"
      receives: "OpenSora 1.0 + SD 3.5"
      logic: "Fuse with MagicDrive ideas"
      sends: "Specialized in-house model"
      gives: "Improves driving fidelity"
    - id: v2
      col: 4
      span: 3
      row: 8
      kind: contribution
      accent: blue
      tag: "V2"
      title: "Depth + Pose Control"
      desc: "Multi-modal output"
      media: "/assets/media/projects/phigent_gen_model/phigent_gen_7V_depth.MP4"
      media_type: video
      receives: "In-house model line"
      logic: "Add depth and ego control"
      sends: "RGB, depth, pose rollouts"
      gives: "Boosts trajectory controllability"
  edges:
    - { from: noise, to: unet, kind: flow }
    - { from: structure, to: encoders, kind: flow }
    - { from: encoders, to: unet, kind: flow }
    - { from: controls, to: unet, kind: flow }
    - { from: unet, to: denoise, kind: flow }
    - { from: denoise, to: decode, kind: flow }
    - { from: decode, to: augment, kind: solid }
    - { from: decode, to: simulation, kind: solid }
    - { from: decode, to: evolution, kind: dashed }
    - { from: evolution, to: v2, kind: flow }
---
<div class="lawn-modules">

  <div class="tool-chips">
    <span class="chip">4V / 7V / 11V surround</span>
    <span class="chip">3D layout + HD map</span>
    <span class="chip">Text · refs · lanes · rig tokens</span>
    <span class="chip">UNet diffusion backbone</span>
    <span class="chip">OpenSora → MagicDrive fusion</span>
  </div>

  <div class="stat-band">
    <div class="stat"><b>4V·7V·11V</b><span>Camera configurations supported</span></div>
    <div class="stat accent"><b>6+</b><span>Control signals per generation</span></div>
    <div class="stat"><b>2 uses</b><span>Augmentation · open-loop simulation</span></div>
    <div class="stat good"><b>V2</b><span>RGB, depth, ego-pose control</span></div>
  </div>

  {% include logic-atlas.html %}

  <h2 class="lawn-h2">Conditioned diffusion pipeline</h2>
  <div class="proj-figure on-white">
    <img src="{{ '/assets/media/projects/phigent_gen_model/phigent_7V_imggen_pipeline.png' | relative_url }}" alt="7V controllable image generation pipeline" loading="lazy">
    <figcaption>3D boxes and maps become spatial conditions; text, reference frames, lanes, and camera calibration become tokens. The UNet denoises from pure noise into aligned multi-view latents, then decodes pixels.</figcaption>
  </div>

  <h2 class="lawn-h2">Scene replacement for augmentation</h2>
  <div class="media-duo">
    <div class="proj-figure">
      <img src="{{ '/assets/media/projects/phigent_gen_model/same_scene_7V_map1.gif' | relative_url }}" alt="7V map-conditioned scene replacement" loading="lazy">
      <figcaption>7V scene/style replacement: geometry held, appearance varied.</figcaption>
    </div>
    <div class="proj-figure">
      <img src="{{ '/assets/media/projects/phigent_gen_model/same_scene_11V_map1.gif' | relative_url }}" alt="11V map-conditioned scene replacement" loading="lazy">
      <figcaption>11V replacement uses the same map-conditioned consistency logic.</figcaption>
    </div>
  </div>
  <div class="media-duo">
    <div class="proj-figure">
      <img src="{{ '/assets/media/projects/phigent_gen_model/Fov120-1V-0.png' | relative_url }}" alt="120 degree FOV single-view scene replacement" loading="lazy">
      <figcaption>1V 120° FOV variant: controlled single-view regeneration.</figcaption>
    </div>
    <div class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/phigent_gen_model/gen_cone_line.jpg' | relative_url }}" alt="Generated traffic cones and lane lines" loading="lazy">
      <figcaption>Long-tail cone and lane-line synthesis without field collection.</figcaption>
    </div>
  </div>

  <h2 class="lawn-h2">Surround video generation</h2>
  <div class="media-duo">
    <div class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/phigent_gen_model/daytime_4fisheye.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>4V fisheye daylight rollout, generated as a temporally coherent clip.</figcaption>
    </div>
    <div class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/phigent_gen_model/phigent_gen_7V_video.MP4' | relative_url }}" type="video/mp4"></video>
      <figcaption>Controllable 7V surround video after in-house driving pretraining.</figcaption>
    </div>
  </div>

  <h2 class="lawn-h2">V2: depth and ego control</h2>
  <div class="media-duo">
    <div class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/phigent_gen_model/phigent_gen_7V_depth.MP4' | relative_url }}" type="video/mp4"></video>
      <figcaption>v2 adds pixel-depth output as a second generated modality.</figcaption>
    </div>
    <div class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/phigent_gen_model/phigent_gen_7V_pose.MP4' | relative_url }}" type="video/mp4"></video>
      <figcaption>Ego-trajectory controllability improved for pose-guided rollouts.</figcaption>
    </div>
  </div>

  <div class="why-grid">
    <div class="why-card"><span class="why-x">Unbalanced real data</span><span class="why-y">Generate rare scenes on demand</span></div>
    <div class="why-card"><span class="why-x">Cross-camera drift</span><span class="why-y">Project boxes and maps per view</span></div>
    <div class="why-card"><span class="why-x">Style-only control</span><span class="why-y">Fuse layout, map, text, rig tokens</span></div>
    <div class="why-card"><span class="why-x">RGB-only worlds</span><span class="why-y">Extend to depth and ego-pose control</span></div>
  </div>

  <div class="ref-note">
    <strong>OmniNWM.</strong>
    <span>After my departure, former colleagues led the follow-up OmniNWM direction: <a href="https://github.com/Ma-Zhuang/OmniNWM" target="_blank" rel="noopener">github.com/Ma-Zhuang/OmniNWM</a>.</span>
  </div>

  <div class="ref-note">
    <strong>My role.</strong>
    <span>Built the controllable driving generation pipeline at a high level: structured conditions, diffusion integration, and sanitized visualization for augmentation and open-loop simulation.</span>
  </div>

</div>
