---
title: "4D Auto-Labeling & Pure LiDAR 3D Detection"
subtitle: "Two eras of autonomous-driving auto-labeling — a Tesla-inspired vision-only 4D pipeline, then a multi-modal and pure-LiDAR 3D detection system."
description: "A two-era auto-labeling journey: a Tesla-AI-Day-inspired vision-only 4D pipeline, then a multi-modal 4D auto-labeling and production pure-LiDAR 3D detection system."
date_range: "2022.11–2024"
partners: "Hozon Auto × SJTU IRMV · PhiGent Robotics"
role: "Perception Team Leader · 3D Perception Algorithm Engineer"
category: "Production + Research Project"
stage: "Production & R&D"
tags: ["production", "research", "3d-4d", "perception", "deployment"]
cover: "/assets/media/projects/offline-4d-labeling/offline_visual_auto_labeling.mp4"
cover_type: "video"
featured: true
order: 80
rich_body: true
summary: "Two eras of autonomous-driving auto-labeling: a vision-only 4D pipeline built with Hozon Auto and SJTU IRMV, then a multi-modal 4D auto-labeler and a production pure-LiDAR 3D detector at PhiGent Robotics."
problem: "3D annotation is the largest recurring cost in an autonomous-driving programme, and human labellers are the bottleneck on how fast a perception model can improve. The goal in both eras was the same: high-quality 4D labels with no human in the loop."
built: "First a vision-only pipeline in the Tesla AI Day spirit — surround depth into pseudo-LiDAR, static and dynamic reconstruction fused into a 4D scene. Then a multi-modal camera-plus-LiDAR auto-labeler hardened on the cases that actually break labelling (vulnerable road users, long range, articulated trailers), and a pure-LiDAR 3D detector taken to production, optimised at the data, model and loss levels."
result: "The vision-only era proved out the 4D reconstruction approach and fed its lessons into the multi-modal one, which shipped: an auto-labeler in the annotation loop and a production pure-LiDAR detector on a mass-production platform."
my_role: "Perception team leader for the auto-labeling effort and 3D perception algorithm engineer on the LiDAR detector — architecture, the failure-case hardening programme, and the production optimisation."
privacy_note: "Only public-level pipeline structure is shown. Internal datasets, labeling rules, exact metrics, model parameters, and customer-specific details are omitted; thresholds are illustrative."
atlas:
  eyebrow: "Logic map"
  title: "One goal, two eras — vision-only 4D, then multi-modal + pure LiDAR"
  caption: "Both columns chase the same prize: high-quality 4D labels with no human in the loop. The left column is the vision-only era, the right is the multi-modal one that shipped."
  cols: 4
  legend:
    - { accent: ink, label: "Shared goal" }
    - { accent: cyan, label: "Era 1 · vision-only 4D" }
    - { accent: blue, label: "Era 2 · multi-modal auto-labeling" }
    - { accent: green, label: "Shipped production model" }
  nodes:
    - id: goal
      col: 1
      span: 4
      row: 1
      kind: input
      accent: ink
      tag: "Shared goal"
      title: "High-Quality 4D Labels"
      desc: "Time × space × semantics × motion"
      receives: "Raw driving logs"
      logic: "Auto-generate labels, no annotators"
      sends: "Supervision for detection"
      gives: "Labels scale with mileage"
    - id: cams
      col: 1
      span: 2
      row: 2
      kind: input
      accent: cyan
      tag: "Era 1 · input"
      title: "Multi-Cam Video + IMU"
      desc: "Vision-only, Tesla-style"
      receives: "Surround cameras + IMU/GPS"
      logic: "Pose-refined multi-frame intake"
      sends: "Calibrated video streams"
      gives: "No LiDAR needed"
    - id: depth
      col: 1
      span: 2
      row: 3
      kind: process
      accent: cyan
      tag: "Era 1 · lift"
      title: "Surround Depth → Pseudo-LiDAR"
      desc: "Cost-volume + BEV fusion"
      receives: "Multi-cam video"
      logic: "Estimate depth, lift to 360° points"
      sends: "Pseudo-LiDAR geometry"
      gives: "Image becomes 3D"
    - id: fuse4d
      col: 1
      span: 2
      row: 4
      kind: process
      accent: cyan
      tag: "Era 1 · fuse"
      title: "Static + Dynamic → 4D Scene"
      desc: "NeRF ground · 3D boxes"
      receives: "Pseudo-LiDAR + flow + seg"
      logic: "Split motion, reconstruct, box"
      sends: "Fused 4D auto-labels"
      gives: "Novel-view supervision"
    - id: multimodal
      col: 3
      span: 2
      row: 2
      kind: input
      accent: blue
      tag: "Era 2 · input"
      title: "Camera + LiDAR"
      desc: "Multi-modal stack"
      receives: "Synced camera + LiDAR"
      logic: "BEVFusion-style encoding"
      sends: "Fused BEV features"
      gives: "Robust hard-case geometry"
    - id: autolabel
      col: 3
      span: 2
      row: 3
      kind: process
      accent: blue
      tag: "Era 2 · harden"
      title: "BEVFusion 4D Auto-Labeler"
      desc: "VRU · range · trailer fixes"
      receives: "Fused BEV features"
      logic: "Data + model + loss-level hardening"
      sends: "Hardened 4D labels"
      gives: "Wins on VRUs, far range, trailers"
    - id: lidardet
      col: 3
      span: 2
      row: 4
      kind: contribution
      accent: green
      tag: "Era 2 · ship"
      title: "Pure-LiDAR 3D Detection"
      desc: "Falcon K1 · production"
      receives: "Hardened auto-labels"
      logic: "Train solid-state LiDAR detector"
      sends: "On-vehicle 3D boxes"
      gives: "Shipped pure-LiDAR detector"
  edges:
    - { from: goal, to: cams, kind: flow }
    - { from: goal, to: multimodal, kind: flow }
    - { from: cams, to: depth, kind: flow }
    - { from: depth, to: fuse4d, kind: flow }
    - { from: multimodal, to: autolabel, kind: flow }
    - { from: autolabel, to: lidardet, kind: flow }
    - { from: fuse4d, to: autolabel, kind: cond, label: "lessons carried over" }
---
<div class="lawn-modules">

  <div class="section-heading">
    <div>
      <p class="eyebrow">Same Direction, Two Eras</p>
      <h2>From vision-only 4D labels to pure-LiDAR detection</h2>
    </div>
  </div>

  <p class="module-intro">
    Both phases share one goal — <strong>automatically producing high-quality 4D training labels</strong> for autonomous driving —
    but differ in era, team, and sensor stack. The timeline below moves from a <strong>Tesla-inspired vision-only</strong> pipeline
    to a <strong>multi-modal + pure-LiDAR</strong> production system.
  </p>

  {% include logic-atlas.html %}

  <div class="phase-track">

    <!-- ===================== PHASE 01 ===================== -->
    <section class="phase">
      <div class="phase-head">
        <span class="phase-step">01</span>
        <span class="phase-badge">2022.11 – 2023.04</span>
        <span class="phase-org">Hozon Auto × SJTU IRMV</span>
        <span class="phase-badge">Perception Team Leader</span>
      </div>
      <h3>Video Offline 4D Auto-Labeling</h3>
      <p class="phase-lead">
        A vision-only offline pipeline replicating the spirit of Tesla AI Day: from multi-camera video + IMU,
        estimate surround depth, lift to a 360° pseudo-LiDAR, separate static and dynamic, and fuse everything into a 4D scene.
      </p>

      <div class="proj-figure is-narrow" style="margin-top:1.1rem">
        <img src="{{ '/assets/media/projects/offline-4d-labeling/project_01_4d_labelling.png' | relative_url }}" alt="Overall 4D auto-labeling pipeline" loading="lazy">
        <figcaption><strong>System pipeline.</strong> Multi-camera + IMU → parallel perception features (flow / pose / depth / semantics) → three branches (3D detection · static reconstruction · ground reconstruction) → a fused 4D scene with novel-view synthesis.</figcaption>
      </div>

      <div class="module-grid" style="margin-top:1.1rem">
        <div class="flow">
          <div class="flow-step">
            <span class="step-tag">Step 1 · Depth</span>
            <h4>Surround-view depth → pseudo-LiDAR</h4>
            <ul><li>Multi-frame cost volume + Conv-LSTM + BEV fusion → 360° pseudo-LiDAR; IMU/GPS pose refinement</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Step 2 · Features</span>
            <h4>Perceptual features → motion state</h4>
            <ul><li>Optical flow · semantic/instance seg · scene flow → classify each point <span class="mono">dynamic / static</span></li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-branch">
            <div class="flow-step">
              <span class="step-tag">Step 3A · Static</span>
              <h4>Scene reconstruction</h4>
              <ul><li>Warp multi-frame → global map; NeRF implicit ground + novel views</li></ul>
            </div>
            <div class="flow-step">
              <span class="step-tag">Step 3B · Dynamic</span>
              <h4>3D box labeling</h4>
              <ul><li>Per-point scene flow → align frames → associate &amp; weighted-average 3D boxes</li></ul>
            </div>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Step 4 · Fuse</span>
            <h4>4D auto-labels</h4>
            <ul><li>HD-map + 3D tracks + segmentation + synthetic views → time × space × semantics × motion</li></ul>
          </div>
        </div>

        <div class="viz-box">
          <div class="viz-head">Foundation: pseudo-LiDAR</div>
          <div class="viz-media">
            <figure class="on-white">
              <img src="{{ '/assets/media/projects/offline-4d-labeling/Surround_view_depth_estimation.png' | relative_url }}" alt="Surround-view depth estimation network" loading="lazy">
              <figcaption>Surround-view depth → 360° pseudo-LiDAR, the geometric base for 4D reconstruction.</figcaption>
            </figure>
          </div>
        </div>
      </div>

      <div class="proj-figrow" style="margin-top:1.1rem">
        <figure class="proj-figure">
          <img src="{{ '/assets/media/projects/offline-4d-labeling/project_02_4d_labelling2.png' | relative_url }}" alt="Static element reconstruction pipeline" loading="lazy">
          <figcaption><strong>Static elements.</strong> Instance segmentation + implicit (NeRF-style) rendering, separated by depth-guided scene flow.</figcaption>
        </figure>
        <figure class="proj-figure on-white">
          <img src="{{ '/assets/media/projects/offline-4d-labeling/4DBBox_labelling.png' | relative_url }}" alt="Dynamic 3D box labeling pipeline" loading="lazy">
          <figcaption><strong>Dynamic objects.</strong> Scene-flow motion classification → cross-frame association → refined 3D boxes.</figcaption>
        </figure>
        <figure class="proj-figure">
          <img src="{{ '/assets/media/projects/offline-4d-labeling/nerf_recon.png' | relative_url }}" alt="NeRF-based simulation data synthesis" loading="lazy">
          <figcaption><strong>Simulation synthesis.</strong> Implicit MLP predicts height &amp; semantics; reprojection + cross-entropy drives high-quality synthetic labels.</figcaption>
        </figure>
      </div>

      <div class="proj-figure" style="margin-top:1.1rem">
        <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback controls>
          <source src="{{ '/assets/media/projects/offline-4d-labeling/offline_visual_auto_labeling.mp4' | relative_url }}" type="video/mp4">
          Your browser does not support embedded video.
        </video>
        <figcaption><strong>Deep-dive walkthrough.</strong> The design, logic, and a breakdown of a Tesla-style visual 4D auto-labeling system.</figcaption>
      </div>
    </section>

    <!-- ===================== PHASE 02 ===================== -->
    <section class="phase">
      <div class="phase-head">
        <span class="phase-step">02</span>
        <span class="phase-badge">2024 · Internal R&amp;D</span>
        <span class="phase-org">PhiGent Robotics</span>
        <span class="phase-badge">3D Perception Algorithm Engineer</span>
      </div>
      <h3>4D Auto-Labeling &amp; Pure LiDAR 3D Detection</h3>
      <p class="phase-lead">
        Moving to a multi-modal stack: harden a BEVFusion-based 4D auto-labeler on hard objects (VRUs, long trailers, far range),
        then ship a production <strong>pure-LiDAR</strong> 3D detector on solid-state LiDAR.
      </p>

      <div class="tech-modules" data-tabs style="margin-top:1.1rem">
        <div class="tech-tabs" role="tablist" aria-label="Phase 2 workstreams">
          <button class="tech-tab is-active" type="button" role="tab" data-tab="vru" aria-selected="true">
            <span class="tab-index">A</span>
            <span class="tab-label"><strong>VRU Augmentation</strong><small>Data-level rebalance</small></span>
          </button>
          <button class="tech-tab" type="button" role="tab" data-tab="bev" aria-selected="false">
            <span class="tab-index">B</span>
            <span class="tab-label"><strong>BEV Range &amp; Resolution</strong><small>Model-level, ≤210 m</small></span>
          </button>
          <button class="tech-tab" type="button" role="tab" data-tab="trailer" aria-selected="false">
            <span class="tab-index">C</span>
            <span class="tab-label"><strong>Long-Trailer Geometry Loss</strong><small>Loss-level, heading fix</small></span>
          </button>
          <button class="tech-tab" type="button" role="tab" data-tab="lidar" aria-selected="false">
            <span class="tab-index">D</span>
            <span class="tab-label"><strong>Pure LiDAR 3D Detection</strong><small>Falcon K1 · production</small></span>
          </button>
        </div>

        <!-- TAB A: VRU -->
        <div class="tech-panel is-active" role="tabpanel" data-panel="vru">
          <div class="module-head">
            <p class="eyebrow">Workstream A · Data level</p>
            <h3>Adaptive VRU instance augmentation</h3>
            <p class="module-oneliner">VRUs (pedestrians, cyclists) are safety-critical but heavily under-represented. We build a VRU instance database and adaptively paste real instances into scenes to rebalance training.</p>
            <div class="tool-chips">
              <span class="chip">VRU instance DB</span>
              <span class="chip">Adaptive paste</span>
              <span class="chip">Image + point-cloud joint align</span>
              <span class="chip">Depth-legal placement</span>
            </div>
          </div>
          <div class="module-grid">
            <div class="flow">
              <div class="flow-step">
                <span class="step-tag">① Collect</span>
                <h4>Instance mining</h4>
                <ul><li>Extract every VRU: RGB patch + LiDAR segment + spatial meta (position / depth / pose)</li></ul>
              </div>
              <div class="flow-arrow" aria-hidden="true"></div>
              <div class="flow-step">
                <span class="step-tag">② Database</span>
                <h4>Layered index</h4>
                <ul><li>Index by class / distance band / scene type → diverse coverage</li></ul>
              </div>
              <div class="flow-arrow" aria-hidden="true"></div>
              <div class="flow-step">
                <span class="step-tag">③ Fuse</span>
                <h4>Adaptive paste</h4>
                <ul><li>Scene depth → legal position; match scale / occlusion; paste into <span class="mono">image + point cloud</span> jointly</li></ul>
              </div>
              <div class="flow-arrow" aria-hidden="true"></div>
              <div class="flow-step">
                <span class="step-tag">④ Sync</span>
                <h4>Label synchronization</h4>
                <ul><li>Auto-generate 2D BBox / 3D BBox / mask → complete supervision</li></ul>
              </div>
            </div>
            <div class="viz-box">
              <div class="viz-head">Copy-paste augmentation</div>
              <div class="viz-media">
                <figure>
                  <img src="{{ '/assets/media/projects/autolabel4d-lidardet3d/Copy-Paste2.png' | relative_url }}" alt="Real-instance copy-paste in image and point cloud" loading="lazy">
                  <figcaption>Real VRU instances pasted with geometric consistency across both modalities.</figcaption>
                </figure>
              </div>
            </div>
          </div>
          <div class="proj-figure is-compact" style="margin-top:1.1rem">
            <img src="{{ '/assets/media/projects/autolabel4d-lidardet3d/metric.png' | relative_url }}" alt="VRU metric improvement comparison" loading="lazy">
            <figcaption><strong>Result.</strong> Measurable precision &amp; recall gains on VRU classes after adaptive instance augmentation.</figcaption>
          </div>
          <div class="ref-note">
            <strong>Builds on.</strong>
            <span>Real-instance paste from Real-Aug and adaptive geometric alignment from PGT-Aug (NeurIPS 2024), extended to joint Camera + LiDAR placement with depth-legal constraints and dynamic sampling.</span>
          </div>
        </div>

        <!-- TAB B: BEV -->
        <div class="tech-panel" role="tabpanel" data-panel="bev">
          <div class="module-head">
            <p class="eyebrow">Workstream B · Model level</p>
            <h3>BEV range &amp; resolution tuning</h3>
            <p class="module-oneliner">Clamp the perception range to ≤ 210 m and raise BEV resolution, so far-field features stay dense — directly improving very-long-range 3D detection during training and release.</p>
          </div>
          <div class="compare">
            <div class="compare-col before">
              <h5>Before</h5>
              <p class="big">Range &gt; 210 m</p>
              <p>Low BEV resolution</p>
              <p>Far-field features sparse → weak long-range recall</p>
            </div>
            <div class="compare-arrow" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13M13 6l6 6-6 6"/></svg>
            </div>
            <div class="compare-col after">
              <h5>After</h5>
              <p class="big">Range ≤ 210 m</p>
              <p>High BEV resolution</p>
              <p>Far-field features dense → stronger long-range 3D detection</p>
            </div>
          </div>
        </div>

        <!-- TAB C: TRAILER -->
        <div class="tech-panel" role="tabpanel" data-panel="trailer">
          <div class="module-head">
            <p class="eyebrow">Workstream C · Loss level</p>
            <h3>Ultra-long trailer: geometry-alignment loss</h3>
            <p class="module-oneliner">Articulated trailers bend when turning, so a single box never fits and heading drifts. We add multi-box labeling for multi-section trailers and a loss that forces box boundaries to hug the LiDAR surface.</p>
            <div class="tool-chips">
              <span class="chip">Multi-box labeling</span>
              <span class="chip">Point-to-boundary loss</span>
              <span class="chip">Heading correction</span>
            </div>
          </div>
          <div class="module-grid">
            <div class="flow">
              <div class="flow-step">
                <span class="step-tag">Problem</span>
                <h4>Articulated &amp; occluded</h4>
                <ul><li>Tractor + trailer 1 + trailer 2 … each section a different angle → single box distorts IoU; sparse points</li></ul>
              </div>
              <div class="flow-arrow" aria-hidden="true"></div>
              <div class="flow-step">
                <span class="step-tag">Labeling</span>
                <h4>Multi-box supervision</h4>
                <ul><li>Hand-label multi-section trailers so the model learns to emit several boxes per vehicle</li></ul>
              </div>
              <div class="flow-arrow" aria-hidden="true"></div>
              <div class="flow-step">
                <span class="step-tag">Loss</span>
                <h4>Point-to-boundary alignment</h4>
                <ul>
                  <li>For each LiDAR point <span class="mono">P</span>: cast a ray from box center through <span class="mono">P</span></li>
                  <li>Ray ∩ box boundary = <span class="mono">P_l</span> → <span class="mono">Loss = dist(P, P_l)</span></li>
                  <li>Point outside → loss rotates/translates the box onto the cloud; aligned → loss → 0</li>
                </ul>
              </div>
              <div class="flow-arrow" aria-hidden="true"></div>
              <div class="flow-step">
                <span class="step-tag">Result</span>
                <h4>Tight, correctly-oriented boxes</h4>
                <ul><li>Boxes hug the trailer surface; heading error sharply reduced</li></ul>
              </div>
            </div>
            <div class="viz-box">
              <div class="viz-head">Geometry-alignment loss</div>
              <div class="viz-media">
                <figure class="is-compact">
                  <img src="{{ '/assets/media/projects/autolabel4d-lidardet3d/loss2.png' | relative_url }}" alt="Point-to-boundary geometry loss construction" loading="lazy">
                  <figcaption>Top: heading too large → loss pulls the box. Bottom: aligned → loss ≈ 0.</figcaption>
                </figure>
              </div>
            </div>
          </div>
          <div class="proj-figrow two" style="margin-top:1.1rem">
            <figure class="proj-figure">
              <img src="{{ '/assets/media/projects/autolabel4d-lidardet3d/truck_heading_pred_failures.png' | relative_url }}" alt="Trailer heading prediction failures" loading="lazy">
              <figcaption><strong>Before.</strong> Boxes miss the trailer body with large heading errors.</figcaption>
            </figure>
            <figure class="proj-figure">
              <img src="{{ '/assets/media/projects/autolabel4d-lidardet3d/vis_auto_3ddet.gif' | relative_url }}" alt="Automatic 3D detection and labeling result" loading="lazy">
              <figcaption><strong>After.</strong> Stable, tightly-fitted automatic 3D detection and labeling.</figcaption>
            </figure>
          </div>
        </div>

        <!-- TAB D: PURE LIDAR -->
        <div class="tech-panel" role="tabpanel" data-panel="lidar">
          <div class="module-head">
            <p class="eyebrow">Workstream D · Production · Seyond Falcon K1</p>
            <h3>Pure LiDAR 3D detection</h3>
            <p class="module-oneliner">A production 3D detector for solid-state LiDAR — an open pipeline redesigned around reflectivity features and dilated convolutions, tuned for the sparse far field.</p>
            <div class="tool-chips">
              <span class="chip">Reflectivity feature</span>
              <span class="chip">Dilation FPN</span>
              <span class="chip">CenterHead · NMS-free</span>
              <span class="chip">INT8 · Orin</span>
            </div>
          </div>
          <div class="module-grid">
            <div class="flow">
              <div class="flow-step">
                <span class="step-tag">01 · Preprocess</span>
                <h4>Point-cloud preparation</h4>
                <ul><li>Range filter → RANSAC ground removal → reflectivity normalize → pillar voxelization</li></ul>
              </div>
              <div class="flow-arrow" aria-hidden="true"></div>
              <div class="flow-step">
                <span class="step-tag">02 · Pillars</span>
                <h4>PillarFeatureNet</h4>
                <ul><li>Feature <span class="mono">[x,y,z,intensity,x_c,y_c,z_c,x_p,y_p]</span>; reflectivity is the core cue; hash voxelization + INT8 MLP</li></ul>
              </div>
              <div class="flow-arrow" aria-hidden="true"></div>
              <div class="flow-step">
                <span class="step-tag">03 · Scatter</span>
                <h4>Sparse → dense BEV</h4>
                <ul><li>CUDA scatter via pillar-coordinate hash → dense pseudo-image (~35% faster end-to-end)</li></ul>
              </div>
              <div class="flow-arrow" aria-hidden="true"></div>
              <div class="flow-step">
                <span class="step-tag">04 · Backbone</span>
                <h4>SECOND + Dilation FPN</h4>
                <ul><li>Dilated deconv <span class="mono">d = 1,2,4</span> enlarges receptive field for sparse far-field context</li></ul>
              </div>
              <div class="flow-arrow" aria-hidden="true"></div>
              <div class="flow-step">
                <span class="step-tag">05 · Head</span>
                <h4>CenterHead</h4>
                <ul><li>Center heatmap (GaussianFocalLoss) + regression (offset / z / size / rotation / velocity); NMS-free peak extraction</li></ul>
              </div>
            </div>
            <div class="viz-box">
              <div class="viz-head">Algorithm framework</div>
              <div class="viz-media">
                <figure>
                  <img src="{{ '/assets/media/projects/autolabel4d-lidardet3d/pure_lidar_det3d.png' | relative_url }}" alt="Pure LiDAR 3D detection framework" loading="lazy">
                  <figcaption>Solid-state-LiDAR detector: pillars → scatter → SECOND + Dilation FPN → CenterHead.</figcaption>
                </figure>
              </div>
            </div>
          </div>

          <div class="module-head" style="margin-top:1.4rem">
            <p class="eyebrow">Ablation · mAP by class</p>
            <h3>What each idea contributes</h3>
          </div>
          <div class="ablation">
            <table>
              <thead>
                <tr><th>Method</th><th>mAP</th><th>Car</th><th>Bicycle</th><th>Pedestrian</th><th>Cone</th><th>Truck</th><th>Bus</th><th>Tricycle</th></tr>
              </thead>
              <tbody>
                <tr><td>Pillar features (baseline)</td><td>0.667</td><td>0.959</td><td>0.835</td><td>0.710</td><td>0.722</td><td>0.628</td><td>0.863</td><td>0.615</td></tr>
                <tr><td>+ Reflectivity</td><td>0.704</td><td>0.966</td><td>0.861</td><td>0.780</td><td>0.787</td><td>0.653</td><td>0.873</td><td>0.715</td></tr>
                <tr><td>+ Dilation FPN</td><td>0.719</td><td>0.964</td><td>0.865</td><td>0.793</td><td>0.819</td><td>0.701</td><td>0.887</td><td>0.722</td></tr>
                <tr><td>Voxel sparse features</td><td>0.714</td><td>0.954</td><td>0.874</td><td>0.838</td><td>0.844</td><td>0.586</td><td>0.839</td><td>0.775</td></tr>
                <tr class="best"><td>Reflectivity + dilated conv (final)</td><td>0.763</td><td>0.968</td><td>0.909</td><td>0.885</td><td>0.907</td><td>0.780</td><td>0.892</td><td>0.760</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

  </div>
</div>
