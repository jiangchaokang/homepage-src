---
title: "End-to-End Driving: 11V + LiDAR Fusion"
subtitle: "A sparse-centric end-to-end autonomous-driving stack fusing 11 cameras (7 pinhole + 4 fisheye) with LiDAR. I owned the BEV-fusion CUDA operator and the AI-planner training."
date_range: "2024 · Collaboration"
partners: "Lantu"
role: "BEV Fusion & AI-Planner Engineer"
category: "POC Project"
stage: "Pre-research / POC"
tags: ["research", "e2e", "perception", "3d-4d"]
cover: "/assets/media/projects/e2e/video_turn_around_e2e.mp4"
cover_type: "video"
featured: false
order: 100
rich_body: true
summary: "An end-to-end autonomous-driving system that fuses 11 surround cameras (7 pinhole + 4 fisheye) with LiDAR under a sparse-centric (SparseDrive-style) paradigm. My two core deliverables: a fused BEV-fusion CUDA operator that aligns 11-camera and LiDAR features in a single kernel, and the training of an AI planner that outputs motion and planning in parallel from a shared query decoder."
privacy_note: "Only high-level architecture and sanitized visual materials are shown. Customer-specific data, calibration, and internal performance numbers are omitted. The original source listed an inconsistent interval; a neutral '2024 · Collaboration' label is shown instead."
atlas:
  eyebrow: "Logic map"
  title: "11V LiDAR to trajectory"
  caption: "Hover a node to inspect the sparse data path. Green and amber mark my owned modules."
  cols: 6
  nodes:
    - id: sensors
      col: 2
      span: 4
      row: 1
      kind: input
      accent: cyan
      tag: "Input"
      title: "11V + LiDAR"
      desc: "7 pinhole · 4 fisheye"
      receives: "Surround images + LiDAR sweep"
      logic: "Multi-modal sensing"
      sends: "Raw camera and LiDAR data"
      gives: "Covers near + surround geometry"
    - id: encoders
      col: 2
      span: 4
      row: 2
      kind: process
      accent: blue
      tag: "Encode"
      title: "Sparse Encoders"
      desc: "Image + voxel features"
      receives: "Images and LiDAR sweep"
      logic: "ViT/ResNet-FPN + voxel/pillar"
      sends: "Multi-scale sparse features"
      gives: "Cuts dense BEV overhead"
    - id: queries
      col: 1
      span: 2
      row: 3
      kind: reason
      accent: purple
      tag: "Query"
      title: "3D Queries"
      desc: "Boxes to keypoints"
      receives: "Instance anchors"
      logic: "Center + face keypoints"
      sends: "Projected sampling points"
      gives: "SparseDrive-style carrier"
    - id: cuda
      col: 3
      span: 2
      row: 3
      kind: contribution
      accent: green
      tag: "Owned"
      title: "Fused CUDA Op"
      desc: "Deformable aggregation"
      receives: "11V × 4-scale projections"
      logic: "Sample × weight × reduce"
      sends: "Aligned instance features"
      gives: "Unifies fusion in one kernel"
    - id: bev
      col: 5
      span: 2
      row: 3
      kind: reason
      accent: purple
      tag: "Fuse"
      title: "Sparse BEV Fusion"
      desc: "Camera-LiDAR aligned"
      receives: "Image + LiDAR features"
      logic: "Project, sample, aggregate"
      sends: "Fused sparse BEV"
      gives: "Stabilizes downstream tasks"
    - id: perception
      col: 1
      span: 2
      row: 4
      kind: output
      accent: cyan
      tag: "Perceive"
      title: "Sparse Perception"
      desc: "Detect · track · map"
      receives: "Fused sparse BEV"
      logic: "Shared transformer decoding"
      sends: "Objects, tracks, map"
      gives: "Scene state for planning"
    - id: decoder
      col: 3
      span: 2
      row: 4
      kind: process
      accent: blue
      tag: "Decode"
      title: "Query Decoder"
      desc: "Ego + obstacles"
      receives: "Temporal, map, vision, LiDAR"
      logic: "L-layer query refinement"
      sends: "Shared planning queries"
      gives: "Connects motion and ego"
    - id: planner
      col: 5
      span: 2
      row: 4
      kind: contribution
      accent: warn
      tag: "Owned"
      title: "AI Planner"
      desc: "Parallel heads trained"
      receives: "Shared decoder queries"
      logic: "Motion + planning together"
      sends: "Agent and ego futures"
      gives: "Bidirectional, game-aware planning"
    - id: trajectory
      col: 2
      span: 4
      row: 5
      kind: output
      accent: green
      tag: "Output"
      title: "Turn-around Trajectory"
      desc: "E2E result clip"
      media: "/assets/media/projects/e2e/video_turn_around_e2e.mp4"
      media_type: video
      receives: "Perception + planner outputs"
      logic: "Select executable future path"
      sends: "Final ego trajectory"
      gives: "Sensors to planning, end-to-end"
  edges:
    - { from: sensors, to: encoders, kind: flow }
    - { from: encoders, to: queries, kind: flow }
    - { from: encoders, to: cuda, kind: flow }
    - { from: queries, to: cuda, kind: solid }
    - { from: cuda, to: bev, kind: flow }
    - { from: bev, to: perception, kind: flow }
    - { from: perception, to: decoder, kind: solid }
    - { from: bev, to: decoder, kind: dashed }
    - { from: decoder, to: planner, kind: flow }
    - { from: planner, to: trajectory, kind: flow }
---
<div class="lawn-modules">

  <div class="tool-chips">
    <span class="chip">11V surround + LiDAR</span>
    <span class="chip">SparseDrive-style sparse stack</span>
    <span class="chip">Fused CUDA operator</span>
    <span class="chip">Detection · tracking · map</span>
    <span class="chip">Parallel motion + planning</span>
  </div>

  <div class="stat-band">
    <div class="stat"><b>11V</b><span>7 pinhole + 4 fisheye cameras</span></div>
    <div class="stat accent"><b>1 kernel</b><span>Sample, weight, and reduce fused</span></div>
    <div class="stat"><b>&lt;3 pts</b><span>3D gap vs dense BEVDet-style baseline</span></div>
    <div class="stat good"><b>2 owned</b><span>CUDA fusion + AI-planner training</span></div>
  </div>

  {% include logic-atlas.html %}

  <h2 class="lawn-h2">System logic</h2>
  <div class="media-duo">
    <div class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/e2e/arch1.png' | relative_url }}" alt="11V plus LiDAR sparse end-to-end driving pipeline" loading="lazy">
      <figcaption>11-camera + LiDAR input is encoded sparsely, fused in BEV, and decoded into perception, prediction, motion, and planning outputs.</figcaption>
    </div>
    <div class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/e2e/arch2.png' | relative_url }}" alt="AI planner shared query decoder architecture" loading="lazy">
      <figcaption>Ego and obstacle queries aggregate temporal history, map, multi-view images, and LiDAR BEV, then branch into motion and planning heads.</figcaption>
    </div>
  </div>

  <h2 class="lawn-h2">Fusion operator</h2>
  <div class="proj-figure">
    <img src="{{ '/assets/media/projects/e2e/vis1.png' | relative_url }}" alt="LiDAR and 11-camera alignment visualization" loading="lazy">
    <figcaption>The owned CUDA operator projects 3D keypoints into 11 cameras across 4 scales, then bilinear-samples, weights, and reduces aligned features in one pass.</figcaption>
  </div>

  <div class="why-grid">
    <div class="why-card"><span class="why-x">Dense BEV cost</span><span class="why-y">Sparse representation for efficiency</span></div>
    <div class="why-card"><span class="why-x">Naive 3 passes</span><span class="why-y">One fused kernel, HBM ×1</span></div>
    <div class="why-card"><span class="why-x">Serial planning</span><span class="why-y">Parallel motion + ego planning</span></div>
    <div class="why-card"><span class="why-x">One-way prediction</span><span class="why-y">Bidirectional, game-aware queries</span></div>
  </div>

  <h2 class="lawn-h2">Turn-around result</h2>
  <div class="proj-figure">
    <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/e2e/video_turn_around_e2e.mp4' | relative_url }}" type="video/mp4"></video>
    <figcaption>End-to-end surround replay: fused sparse perception and the AI planner produce the turn-around trajectory from 11V + LiDAR inputs.</figcaption>
  </div>

  <div class="ref-note">
    <strong>My role.</strong>
    <span>2024 · Collaboration with Lantu; author owned the fused BEV-fusion CUDA operator and AI-planner training. Details are high-level and sanitized.</span>
  </div>

</div>
