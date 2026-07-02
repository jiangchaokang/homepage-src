---
title: "Integrated Perception, Planning, and Decision-Making Network"
subtitle: "A unified multi-task network that fuses RGB, LiDAR, and infrared for closed-loop perception, planning, and decision-making in simulation."
description: "A unified multi-task network fusing RGB, LiDAR, and infrared for closed-loop perception, planning, and decision-making, trained end-to-end in simulation."
date_range: "2021.08–2022.10"
partners: "The Future Laboratory of the Second Aerospace Academy"
role: "Perception and Simulation Developer"
category: "Research Project"
stage: "Pre-research"
tags: ["research", "e2e", "perception"]
cover: "/assets/media/projects/integrated-driving/project_11_simulation_exploration.gif"
cover_type: "image"
featured: false
order: 30
rich_body: true
summary: "A unified multi-task framework that fuses multi-modal sensors (RGB, LiDAR, infrared) through attention-based feature fusion — jointly solving geometric–semantic mapping, unsupervised depth and odometry, multi-object detection and tracking, and closed-loop behavior decisions inside one end-to-end trainable network."
privacy_note: "Only high-level system modules are shown. Mission-specific and customer-specific details are omitted."
atlas:
  eyebrow: "Logic map"
  title: "One model, four abilities, one closed loop"
  caption: "Heterogeneous sensors fuse into a shared representation that drives perception, mapping, planning, and decisions — then the action loops back. Hover a node."
  cols: 4
  nodes:
    - id: sensors
      col: 1
      span: 4
      row: 1
      kind: input
      accent: ink
      tag: "Input"
      title: "Multi-Modal Sensors"
      desc: "RGB · LiDAR · Infrared"
      receives: "Heterogeneous sensor streams"
      logic: "Modality-specific encoders"
      sends: "Per-modality features"
      gives: "Robust to lighting / weather"
    - id: fusion
      col: 1
      span: 4
      row: 2
      kind: process
      accent: purple
      tag: "Fuse"
      title: "Attention Fusion"
      desc: "Cross + self attention"
      receives: "Per-modality features"
      logic: "Align and merge interactively"
      sends: "Shared representation"
      gives: "One feature, many heads"
    - id: detect
      col: 1
      span: 2
      row: 3
      kind: process
      accent: cyan
      tag: "Perceive"
      title: "Detection & Tracking"
      desc: "Stable IDs + trajectories"
      receives: "Shared representation"
      logic: "Detect → Hungarian + Kalman"
      sends: "Targets and velocities"
      gives: "Knows the dynamic agents"
    - id: estimate
      col: 3
      span: 2
      row: 3
      kind: process
      accent: cyan
      tag: "Perceive"
      title: "Geometry–Semantic"
      desc: "Depth · seg · odometry"
      receives: "Shared representation"
      logic: "Four co-trained auxiliary tasks"
      sends: "Dense scene + ego motion"
      gives: "Knows the static structure"
    - id: slam
      col: 2
      span: 2
      row: 4
      kind: reason
      accent: blue
      tag: "Map"
      title: "Dense SLAM + Map"
      desc: "Track → optimize → fuse"
      receives: "Geometry + ego pose"
      logic: "Front-end / back-end / dense map"
      sends: "Global 3D map"
      gives: "A consistent world to plan in"
    - id: planning
      col: 1
      span: 2
      row: 5
      kind: process
      accent: warn
      tag: "Plan"
      title: "Planning"
      desc: "Global + local path"
      receives: "Targets + map"
      logic: "A* / Dijkstra → DWA / MPC"
      sends: "Collision-free path"
      gives: "A safe route to follow"
    - id: decision
      col: 3
      span: 2
      row: 5
      kind: contribution
      accent: green
      tag: "Decide"
      title: "Decision (FSM / RL)"
      desc: "Act and evaluate"
      receives: "Planned path + state"
      logic: "Reward-shaped agent acts"
      sends: "Accelerate / brake / steer"
      gives: "Closes the loop"
  edges:
    - { from: sensors, to: fusion, kind: flow }
    - { from: fusion, to: detect, kind: flow }
    - { from: fusion, to: estimate, kind: flow }
    - { from: detect, to: slam, kind: flow }
    - { from: estimate, to: slam, kind: flow }
    - { from: detect, to: planning, kind: solid }
    - { from: slam, to: planning, kind: flow }
    - { from: planning, to: decision, kind: flow }
    - { from: decision, to: sensors, kind: dashed }
---
<div class="lawn-modules">

  <!-- ===================== SYSTEM ARCHITECTURE ===================== -->
  <div class="section-heading">
    <div>
      <p class="eyebrow">System Architecture</p>
      <h2>One model, four interdependent abilities</h2>
    </div>
  </div>

  <p class="module-intro">
    Heterogeneous sensor streams are encoded by modality-specific extractors, then fused by interactive
    cross- and self-attention into a single representation that drives perception, reconstruction, and decision
    heads — forming a closed-loop <strong>perception → planning → decision</strong> pipeline.
  </p>

  {% include logic-atlas.html %}

  <div class="proj-figure">
    <img src="{{ '/assets/media/projects/integrated-driving/unified_rl_network_framework.png' | relative_url }}" alt="Unified multi-task network architecture" loading="lazy">
    <figcaption><strong>Unified network.</strong> Camera / LiDAR / infrared are independently encoded, dynamically fused via cross- and self-attention, then decoded into structure reconstruction, uncertainty-aware segmentation, and multi-target detection — while feeding a hierarchically pre-trained branch for state perception and behavior decisions.</figcaption>
  </div>

  <!-- ===================== FOUR MODULES (TABS) ===================== -->
  <div class="section-heading" style="margin-top:2rem">
    <div>
      <p class="eyebrow">Module Breakdown</p>
      <h2>Four research modules</h2>
    </div>
  </div>

  <p class="module-intro">
    Switch between the four modules to see <strong>what each one does</strong>, the <strong>pipeline</strong> behind it,
    and the <strong>simulation result</strong>.
  </p>

  <div class="tech-modules" data-tabs>
    <div class="tech-tabs" role="tablist" aria-label="Network modules">
      <button class="tech-tab is-active" type="button" role="tab" data-tab="detect" aria-selected="true">
        <span class="tab-index">01</span>
        <span class="tab-label"><strong>Detection &amp; Tracking</strong><small>Webots × deep learning</small></span>
      </button>
      <button class="tech-tab" type="button" role="tab" data-tab="estimate" aria-selected="false">
        <span class="tab-index">02</span>
        <span class="tab-label"><strong>Geometry–Semantic Estimation</strong><small>Depth · Seg · Odometry · Map</small></span>
      </button>
      <button class="tech-tab" type="button" role="tab" data-tab="slam" aria-selected="false">
        <span class="tab-index">03</span>
        <span class="tab-label"><strong>Monocular Dense SLAM</strong><small>Real-time on ROS</small></span>
      </button>
      <button class="tech-tab" type="button" role="tab" data-tab="decision" aria-selected="false">
        <span class="tab-index">04</span>
        <span class="tab-label"><strong>Planning &amp; Decision</strong><small>Closed-loop simulation</small></span>
      </button>
    </div>

    <!-- MODULE 01 -->
    <div class="tech-panel is-active" role="tabpanel" data-panel="detect">
      <div class="module-head">
        <p class="eyebrow">Module 01 · Webots + YOLOv8</p>
        <h3>2D detection and multi-object tracking</h3>
        <p class="module-oneliner">Render a virtual scene in Webots, detect objects per frame, then keep stable IDs and trajectories across time.</p>
      </div>
      <div class="module-grid">
        <div class="flow">
          <div class="flow-step">
            <span class="step-tag">01 · Input</span>
            <h4>Webots simulation</h4>
            <ul><li>Virtual scene → sensor model → RGB camera → frame stream</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">02 · Detection</span>
            <h4>YOLOv8 inference</h4>
            <ul><li>Preprocess / normalize → inference → confidence filter + <span class="mono">NMS</span> → boxes + class + score</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">03 · Tracking</span>
            <h4>Hungarian + Kalman</h4>
            <ul><li>IoU / feature matching → Kalman predict &amp; update → ID assignment and track management</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">04 · Output</span>
            <h4>ID + trajectory + velocity</h4>
            <ul><li>ID-tagged video stream with trajectories overlaid in the simulator</li></ul>
          </div>
        </div>
        <div class="viz-box">
          <div class="viz-head">Simulation result</div>
          <div class="viz-media">
            <figure>
              <img src="{{ '/assets/media/projects/integrated-driving/project_11_simulation_exploration.gif' | relative_url }}" alt="Simulation exploration with detection and tracking" loading="lazy">
              <figcaption>Detection and tracking during simulation exploration.</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </div>

    <!-- MODULE 02 -->
    <div class="tech-panel" role="tabpanel" data-panel="estimate">
      <div class="module-head">
        <p class="eyebrow">Module 02 · 2D ResNet ‖ 3D Sparse CNN</p>
        <h3>Joint geometry–semantic estimation</h3>
        <p class="module-oneliner">Encode image and point cloud separately, fuse them with dual-channel attention, and co-train four auxiliary tasks for a geometry–semantic consistent representation.</p>
        <div class="tool-chips">
          <span class="chip">Unsup. depth</span>
          <span class="chip">Self-sup. segmentation</span>
          <span class="chip">Point-distance odometry</span>
          <span class="chip">Metric-learning recognition</span>
        </div>
      </div>
      <div class="module-grid">
        <div class="flow">
          <div class="flow-inputs">
            <div class="flow-step">
              <span class="step-tag">Input</span>
              <h4>Image (2D)</h4>
              <ul><li>2D residual CNN encoder</li></ul>
            </div>
            <div class="flow-step">
              <span class="step-tag">Input</span>
              <h4>Point cloud (3D)</h4>
              <ul><li>3D sparse CNN encoder</li></ul>
            </div>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Fusion</span>
            <h4>Dual-channel attention</h4>
            <ul><li>Align &amp; merge features → joint geometry–semantic representation</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-branch">
            <div class="flow-step">
              <span class="step-tag">Depth + Seg</span>
              <h4>Dense scene</h4>
              <ul><li>Depth-aware semantics</li></ul>
            </div>
            <div class="flow-step">
              <span class="step-tag">Odometry + Map</span>
              <h4>Ego motion</h4>
              <ul><li>Scaled pose → 3D map</li></ul>
            </div>
          </div>
        </div>
        <div class="viz-box">
          <div class="viz-head">Architecture &amp; demo</div>
          <div class="viz-media">
            <figure>
              <img src="{{ '/assets/media/projects/integrated-driving/slam.png' | relative_url }}" alt="Multi-modal fusion network architecture" loading="lazy">
              <figcaption>2D / 3D dual-encoder fusion with four parallel auxiliary tasks.</figcaption>
            </figure>
            <figure>
              <img src="{{ '/assets/media/projects/integrated-driving/project_12_slam_demo.gif' | relative_url }}" alt="Multi-task estimation demo" loading="lazy">
              <figcaption>Geometry–semantic estimation in motion.</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </div>

    <!-- MODULE 03 -->
    <div class="tech-panel" role="tabpanel" data-panel="slam">
      <div class="module-head">
        <p class="eyebrow">Module 03 · ROS</p>
        <h3>Monocular visual SLAM with dense mapping</h3>
        <p class="module-oneliner">A real-time ROS pipeline: track the camera, optimize the graph, and reconstruct a dense map from a single camera.</p>
      </div>
      <div class="module-grid">
        <div class="flow">
          <div class="flow-step">
            <span class="step-tag">01 · Front-end</span>
            <h4>Tracking</h4>
            <ul><li>ORB features → init → keyframe selection → pose optimization (+ relocalization)</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">02 · Back-end</span>
            <h4>Graph optimization</h4>
            <ul><li>Local BA ↔ loop closure (<span class="mono">DBoW</span>) ↔ global pose-graph</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">03 · Dense map</span>
            <h4>Reconstruction</h4>
            <ul><li>Monocular depth → reprojection → <span class="mono">TSDF / OctoMap</span> fusion + voxel denoising</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">04 · Output</span>
            <h4>Three map products</h4>
            <ul><li><span class="mono">/dense_pointcloud</span> · <span class="mono">/octomap_3d</span> · <span class="mono">/map_2d_grid</span></li></ul>
          </div>
        </div>
        <div class="viz-box">
          <div class="viz-head">Real-time result</div>
          <div class="viz-media">
            <figure>
              <img src="{{ '/assets/media/projects/integrated-driving/project_07_auto_driving2.gif' | relative_url }}" alt="Monocular SLAM dense mapping" loading="lazy">
              <figcaption>Real-time monocular SLAM with dense mapping.</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </div>

    <!-- MODULE 04 -->
    <div class="tech-panel" role="tabpanel" data-panel="decision">
      <div class="module-head">
        <p class="eyebrow">Module 04 · Webots closed-loop</p>
        <h3>Perception → planning → decision</h3>
        <p class="module-oneliner">Perception feeds planning, planning feeds an FSM / RL decision agent, and the action loops back to the vehicle in simulation.</p>
      </div>
      <div class="module-grid">
        <div class="flow">
          <div class="flow-step">
            <span class="step-tag">Perception layer</span>
            <h4>Understand the scene</h4>
            <ul><li>Detection → obstacles · segmentation → drivable area · depth → distance · SLAM → map · odometry → ego pose</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Planning layer</span>
            <h4>Find a path</h4>
            <ul><li>Global <span class="mono">A* / Dijkstra</span> → local <span class="mono">DWA / MPC</span> → collision check &amp; avoidance</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Decision layer</span>
            <h4>Choose an action</h4>
            <ul><li>FSM / RL agent with reward shaping → accelerate / brake / steer</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Closed loop</span>
            <h4>Act &amp; evaluate</h4>
            <ul><li>Vehicle executes → metrics (success / collision rate, ATE, map IoU) → iterate</li></ul>
          </div>
        </div>
        <div class="viz-box">
          <div class="viz-head">Closed-loop roadmap</div>
          <div class="viz-media">
            <figure>
              <img src="{{ '/assets/media/projects/integrated-driving/technology_roadmap.png' | relative_url }}" alt="Closed-loop perception-planning-decision roadmap" loading="lazy">
              <figcaption>System roadmap: four modules forming a closed perception–planning–decision loop.</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ===================== LOGIC OVERVIEW ===================== -->
  <div class="ref-note" style="margin-top:1.6rem">
    <strong>How they connect.</strong>
    <span>Detection &amp; tracking and geometry–semantic estimation supply targets and structure; dense SLAM builds the global map; planning &amp; decision close the loop and feed evaluation back into every module.</span>
  </div>

</div>

