---
title: "J6M Static & Dynamic Perception"
subtitle: "A production driving-perception stack — a shared-BEV static OneModel, a 4D-sparse dynamic model, and on-board latency compression — shipped on a mass-production mid-trim platform."
description: "Production driving perception on a mass-production platform — a shared-BEV static OneModel, a 4D-sparse dynamic model, and on-board latency compression to ~13.88 ms."
date_range: "2025.04–2026.03"
partners: "Bosch (XC-CN)"
role: "Perception Algorithm Engineer"
category: "Production Project"
stage: "Mass production"
tags: ["production", "perception", "bev", "deployment", "quantization"]
cover: "/assets/media/projects/perception_onemodel/st_vis_single_fream.mp4"
cover_type: "video"
featured: false
order: 110
protected: true
rich_body: true
summary: "Production perception on a mid-trim J6E / J6M platform: a static OneModel driving every static element from one shared BEV feature, a 4D-sparse model that fuses detection and tracking, and a latency-compression effort that took inference from ~42.65 ms to ~13.88 ms."
problem: "On a mid-trim platform the compute budget is fixed and small, while the number of things perception has to output keeps growing. Running a separate model per task is affordable on paper and impossible on the ECU."
built: "Three shipped systems sharing one representation-first design. A multi-task static OneModel reads lanes, curbs, road geometry and topology out of a single shared BEV feature; a 4D-sparse dynamic model fuses detection and tracking into one query pipeline instead of a detector followed by an association stage; and a unified data pipeline feeds all tasks from the same source in one forward pass."
result: "On-board inference compressed from ~42.65 ms to <strong>~13.88 ms</strong> through anchor reduction, caching, channel pruning and quantization-aware training — with the multi-task stack validated and released for mass production."
my_role: "Architecture, the unified data pipeline, heterogeneous multi-task training, release engineering, and quantization-aware deployment. The platform integration and validation are shared with the wider perception team."
glossary:
  - term: "OneModel"
    def: "One network with many task heads reading a single shared BEV feature, instead of one model per task — the only way the task list fits the compute budget."
  - term: "4D sparse"
    def: "Sparse queries carried through space and time (X, Y, Z, T), so detection and tracking are the same computation rather than two stages."
  - term: "QAT"
    def: "Quantization-aware training: the model learns with quantization simulated in the loop, so INT8 deployment does not cost accuracy after the fact."
  - term: "LSS"
    def: "Lift-Splat-Shoot. Lifts image features into 3D using predicted depth, then splats them into the BEV grid."
privacy_note: "Bosch (XC-CN) production project. The architecture and engineering methodology shown here are presented at a technical, portfolio level; customer-specific data, calibration, raw release artefacts, and proprietary training corpora are intentionally omitted or sanitized."
atlas:
  eyebrow: "Logic map"
  title: "One representation, many production heads"
  caption: "Two branches, one principle: build the representation once, then decode it many ways. The left column is static perception, the right is dynamic; the dashed links are training-time only, everything solid runs on the vehicle."
  cols: 6
  legend:
    - { accent: ink, label: "Platform constraint" }
    - { accent: cyan, label: "Static representation & data" }
    - { accent: blue, label: "Static decoding" }
    - { accent: purple, label: "Dynamic branch" }
    - { accent: green, label: "Deployment & release" }
  nodes:
    - id: platform
      col: 2
      span: 4
      row: 1
      kind: input
      accent: ink
      tag: "Platform"
      title: "J6E / J6M"
      desc: "Mid-trim production compute"
      receives: "Mass-production vehicle constraints"
      logic: "Fit perception to on-board budgets"
      sends: "Camera streams + timing targets"
      gives: "Grounds every design choice"
    - id: static_bev
      col: 1
      span: 3
      row: 2
      kind: reason
      accent: cyan
      tag: "Static"
      title: "Shared Static BEV"
      desc: "One feature hub"
      media: "/assets/media/projects/perception_onemodel/st_onemodel_vis.mp4"
      media_type: video
      receives: "4V / 5V camera features"
      logic: "LSS / IPM + SD prior"
      sends: "Final BEV feature"
      gives: "Unifies all static tasks"
    - id: static_heads
      col: 1
      span: 3
      row: 3
      kind: output
      accent: blue
      tag: "Heads"
      title: "Dense + Vector"
      desc: "Independent task decoders"
      receives: "One static BEV"
      logic: "Query heads + seg heads"
      sends: "Lanes, curbs, map geometry"
      gives: "Extensible static outputs"
    - id: static_v2
      col: 1
      span: 3
      row: 4
      kind: process
      accent: blue
      tag: "v2"
      title: "Topology Upgrade"
      desc: "MapFormer-BEVRG"
      receives: "Depth-aware BEV features"
      logic: "Dense raster + polylines"
      sends: "Topology, regions, ego path"
      gives: "HD-map-light road geometry"
    - id: data_train
      col: 1
      span: 3
      row: 5
      kind: process
      accent: cyan
      lane: aux
      tag: "Train"
      title: "Unified Pipeline"
      desc: "Same source, every task"
      receives: "Regular and badcase data"
      logic: "Index mapping plus round-robin task sampling"
      sends: "Task-tagged batches"
      why: "One forward pass carrying many losses is what makes multi-task training affordable; separate loaders per task would multiply both epoch time and drift."
      role: "Built the unified data pipeline and the heterogeneous multi-task training loop."
    - id: dynamic_query
      col: 4
      span: 3
      row: 2
      kind: reason
      accent: purple
      tag: "Dynamic"
      title: "4D Sparse Query"
      desc: "X Y Z T hub"
      receives: "7V + optional LiDAR"
      logic: "Query-driven sensor fusion"
      sends: "Sparse scene tokens"
      gives: "Unifies space and time"
    - id: dynamic_decode
      col: 4
      span: 3
      row: 3
      kind: process
      accent: purple
      tag: "Decode"
      title: "Temporal Decoder"
      desc: "Attention + ego-motion"
      receives: "Sparse queries + history"
      logic: "Deformable + temporal attention"
      sends: "Refined 3D anchors"
      gives: "Aligns multi-frame evidence"
    - id: dynamic_track
      col: 4
      span: 3
      row: 4
      kind: output
      accent: purple
      tag: "Track"
      title: "Detection + Tracking"
      desc: "One memory bank"
      media: "/assets/media/projects/perception_onemodel/dy_vis.mp4"
      media_type: video
      receives: "Refined anchors + memory"
      logic: "IoU-aware classes + velocity"
      sends: "Tracked dynamic agents"
      gives: "Cuts serial hand-offs"
    - id: compression
      col: 4
      span: 3
      row: 5
      kind: process
      accent: green
      tag: "Deploy"
      title: "Latency Compression"
      desc: "Graph shrink and INT8"
      spec: "42.65 ms → 13.88 ms"
      receives: "The 42.65 ms baseline graph"
      logic: "Anchor reduction, caching, channel pruning, quantization-aware training"
      sends: "A 13.88 ms executable"
      why: "Latency is not an optimisation here, it is the admission criterion — above the budget the model does not ship at any accuracy."
      tradeoff: "Every one of the four levers costs a little accuracy; quantization-aware training is what keeps the total loss inside the release bar."
      role: "Owned the latency-compression effort and quantization-aware deployment."
    - id: release
      col: 2
      span: 4
      row: 6
      kind: contribution
      accent: green
      tag: "Ship"
      title: "Validated Release"
      desc: "Three systems shipped"
      media: "/assets/media/projects/perception_onemodel/vis_pred.mp4"
      media_type: video
      receives: "Static, dynamic, deployment loops"
      logic: "Train, eval, compile, time"
      sends: "Production perception stack"
      gives: "Representation-first mass production"
  edges:
    - { from: platform, to: static_bev, kind: flow, label: "4V / 5V" }
    - { from: static_bev, to: static_heads, kind: flow, label: "one shared BEV" }
    - { from: static_heads, to: static_v2, kind: flow }
    - { from: static_v2, to: data_train, kind: train }
    - { from: data_train, to: static_bev, kind: train, label: "task-tagged batches" }
    - { from: platform, to: dynamic_query, kind: flow, label: "7V (+ LiDAR)" }
    - { from: dynamic_query, to: dynamic_decode, kind: flow }
    - { from: dynamic_decode, to: dynamic_track, kind: flow }
    - { from: dynamic_track, to: compression, kind: flow }
    - { from: data_train, to: release, kind: cond }
    - { from: compression, to: release, kind: flow, label: "13.88 ms" }
---
<div class="lawn-modules">

  <div class="tool-chips">
    <span class="chip">J6E / J6M production</span>
    <span class="chip">Shared BEV OneModel</span>
    <span class="chip">4D-sparse detection + tracking</span>
    <span class="chip">Unified data + training</span>
    <span class="chip">QAT · INT8 deployment</span>
  </div>

  <div class="stat-band">
    <div class="stat"><b>3</b><span>Shipped perception systems</span></div>
    <div class="stat accent"><b>1 BEV</b><span>Static tasks read one feature</span></div>
    <div class="stat"><b>4D</b><span>Dynamic queries unify time and tracking</span></div>
    <div class="stat good"><b>42.65 → 13.88 ms</b><span>On-board inference after compression</span></div>
  </div>

  {% include logic-atlas.html %}

  <h2 class="lawn-h2">Static OneModel: one feature, many heads</h2>
  <div class="proj-figure on-white">
    <img src="{{ '/assets/media/projects/perception_onemodel/OneModel_Static.jpg' | relative_url }}" alt="OneModel static perception architecture" loading="lazy">
    <figcaption>4 surround cameras enter a ResNet + FPN image backbone, Lift-Splat-Shoot view transform, and shared BEV. An SD-map vector prior is rasterized, CNN-encoded, and summed into the final BEV; query heads decode lanes, curbs, centerlines, goal points, and markings while convolutional heads decode drivable area and general elements.</figcaption>
  </div>

  <div class="media-duo">
    <div class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/perception_onemodel/st_onemodel_vis.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>First-release static OneModel output from the shared-BEV stack.</figcaption>
    </div>
    <div class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/perception_onemodel/st_onemodel_vis_night.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>Night replay: the multi-task model matched dedicated single-task models across static elements.</figcaption>
    </div>
  </div>

  <h2 class="lawn-h2">Data, training, and release loop</h2>
  <div class="media-duo">
    <div class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/perception_onemodel/onemodel_data_pipeline.png' | relative_url }}" alt="Unified static perception data pipeline" loading="lazy">
      <figcaption>One preprocessing pipeline generates every static sub-task from the same source data, with CPU / memory / GPU throughput tuned for regular and badcase dataset iteration.</figcaption>
    </div>
    <div class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/perception_onemodel/onemodel_heterogeneous_training.png' | relative_url }}" alt="Heterogeneous OneModel training" loading="lazy">
      <figcaption>Index mapping aligns heterogeneous tasks; round-robin sampling builds task-tagged batches. One shared Backbone + ViewTransformer forward pass is sliced by task index, then independent heads decode and back-propagate separately.</figcaption>
    </div>
  </div>

  <div class="media-duo">
    <div class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/perception_onemodel/onemodel_v2.png' | relative_url }}" alt="MapFormer-BEVRG static perception architecture" loading="lazy">
      <figcaption>v2 keeps the shared BEV and adds pure-vision MapFormer-BEVRG: 5V input, HENet + FPN-LSS, depth-aware multi-height IPM, optional temporal fusion, SD-map cross-attention, dense raster segmentation, vector polylines, topology, regions, and training-only depth / PV semantic / image-consistency heads.</figcaption>
    </div>
    <div class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/perception_onemodel/Onemodel_Release_History.jpg' | relative_url }}" alt="OneModel release history" loading="lazy">
      <figcaption>Each release iterated on acceleration, data, new features, training and inference frameworks, architecture, and evaluation before entering the production release flow.</figcaption>
    </div>
  </div>

  <h2 class="lawn-h2">Dynamic perception: 4D sparse memory</h2>
  <div class="proj-figure on-white">
    <img src="{{ '/assets/media/projects/perception_onemodel/dy_rch.png' | relative_url }}" alt="4D sparse dynamic perception architecture" loading="lazy">
    <figcaption>7 cameras, with optional LiDAR, feed a ResNet / VoVNet + BiFPN backbone and 4D sparse queries over X, Y, Z, and T. Sparse deformable cross-attention retrieves image and point features; temporal self-attention uses ego-motion compensation; anchor refinement and an instance memory bank unify detection, velocity, classification, and tracking.</figcaption>
  </div>

  <div class="media-duo">
    <div class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/perception_onemodel/dy_vis.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>Deployed quantized 4D-sparse dynamic perception running on-board.</figcaption>
    </div>
    <div class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/perception_onemodel/vis_pred.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>v2 static prediction: dense raster and vectorized geometry decoded from one BEV feature.</figcaption>
    </div>
  </div>

  <h2 class="lawn-h2">Deployment compression</h2>
  <div class="proj-figure on-white">
    <img src="{{ '/assets/media/projects/perception_onemodel/dy_qat_acc.png' | relative_url }}" alt="Latency compression summary" loading="lazy">
    <figcaption>The head dominated latency, so deployment followed two routes: shrink the Sparse4D graph and lower precision. Anchors moved 768 → 640 → 600, temporal cache 256 → 200, channels 256 → 192, and the large current_features tensor moved to INT8 while bbox regression stayed INT16.</figcaption>
  </div>

  <div class="ablation wrap">
    <table>
      <thead><tr><th>Configuration</th><th>Latency</th><th>Key change</th><th>Accuracy</th></tr></thead>
      <tbody>
        <tr><td>Baseline v3.30 · J6E</td><td>42.65 ms</td><td>Sparse4D Head ~55%</td><td>—</td></tr>
        <tr><td>Anchor compression · J6E</td><td>35.28 ms</td><td>768 → 640 anchors; cache 256 → 200</td><td>controlled</td></tr>
        <tr><td>QAT baseline · J6M</td><td>22.50 ms</td><td>PTQ → QAT → .bc → .hbm</td><td>—</td></tr>
        <tr><td>Pruned + full INT8 · J6M</td><td>13.88 ms</td><td>256 → 192 channels; bandwidth −47.6%</td><td>−1~2% AP</td></tr>
      </tbody>
    </table>
  </div>

  <div class="why-grid">
    <div class="why-card"><span class="why-x">Many static tasks</span><span class="why-y">One BEV, independent heads</span></div>
    <div class="why-card"><span class="why-x">Heterogeneous labels</span><span class="why-y">Index mapping + round-robin batches</span></div>
    <div class="why-card"><span class="why-x">Flat-ground BEV holes</span><span class="why-y">Depth-aware multi-height IPM</span></div>
    <div class="why-card"><span class="why-x">Need topology</span><span class="why-y">SGNN + LCLC adjacency</span></div>
    <div class="why-card"><span class="why-x">Serial detection / tracking</span><span class="why-y">4D queries + memory bank</span></div>
    <div class="why-card"><span class="why-x">Mixed INT8 too small</span><span class="why-y">Quantize current_features too</span></div>
  </div>

  <div class="ref-note">
    <strong>My role.</strong>
    <span>Contributed to static OneModel architecture, unified data and heterogeneous training, release engineering, dynamic 4D-sparse deployment, and QAT / INT8 latency compression. Details are high-level and sanitized for enterprise confidentiality.</span>
  </div>

</div>
