---
title: "Autonomous Lawn-Mower Robot Perception"
subtitle: "A safety-critical LiDAR and multimodal perception stack for autonomous loading/unloading, slope traversal, grass-obstacle detection, and embedded deployment."
description: "A safety-critical LiDAR and multimodal perception stack for an autonomous lawn-mower robot — self loading/unloading, grass-obstacle detection, and an MCU-deployed BEV safety detector."
date_range: "2021.09–2023.03"
partners: "SJTU IRMV × Positec Technology"
role: "Perception Algorithm Developer · 2D–3D Fusion Researcher"
category: "Production + Research Project"
stage: "Production-oriented + Pre-research"
tags: ["production", "research", "robotics", "3d-4d", "deployment"]
cover: "/assets/media/projects/lawn-mower/project_05_up_down_slope.gif"
cover_type: "image"
featured: true
order: 40
rich_body: true
summary: "The safety-critical perception stack for a robot that has to drive itself off a transport vehicle, reach the lawn, mow it, and come back — four modules from ramp detection to an MCU-deployed BEV safety net."
problem: "A consumer mowing robot operates unsupervised around people and pets, on a compute budget of a microcontroller. Every stage of its mission — unloading itself, crossing to the lawn, mowing, returning — has its own way of going wrong, and the whole thing has to be safe by default."
built: "Four modules on one shared sensor set. Ramp detection so the robot can load and unload itself; 3D grass-obstacle detection, first geometric and then camera–LiDAR fused; a 2D BEV safety detector small enough to run on the on-board MCU; and a dual-attention LiDAR–vision fusion study for the next generation."
result: "The safety detector runs at roughly 110 fps on an STM32H7, so the safety net is always on rather than budget-dependent — and obstacle detection moved from geometry-only to fused perception without changing the sensor set."
my_role: "Perception algorithm developer across all four modules; the dual-attention fusion work was a research study that informed the next version rather than shipping."
privacy_note: "Only high-level algorithmic information is shown. Thresholds listed here are illustrative; product parameters, calibration data, and deployment details are sanitized."
atlas:
  eyebrow: "Logic map"
  title: "From the transport vehicle to the lawn and back — one safety stack"
  caption: "Every mission stage hangs off the same two sensors and feeds one outcome. Three stages shipped on the robot; the fusion study informed the next version rather than being deployed."
  cols: 4
  legend:
    - { accent: ink, label: "On-robot sensing" }
    - { accent: cyan, label: "Ramp detection · load & unload" }
    - { accent: blue, label: "MCU safety net" }
    - { accent: green, label: "Obstacle detection & mission outcome" }
    - { accent: purple, label: "Fusion study · research, not deployed" }
  nodes:
    - id: sensors
      col: 1
      span: 4
      row: 1
      kind: input
      accent: ink
      tag: "Input"
      title: "Solid-State LiDAR + Camera"
      desc: "On-robot sensing"
      receives: "Point clouds + RGB frames"
      logic: "Calibrate and time-sync"
      sends: "Aligned 2D / 3D streams"
      gives: "One sensing base for all stages"
    - id: ramp
      col: 1
      span: 2
      row: 2
      kind: process
      accent: cyan
      tag: "Stage A"
      title: "Ramp Detection"
      desc: "Self load / unload"
      receives: "LiDAR point cloud"
      logic: "Fit ramp plane + four edges"
      sends: "Drive-on geometry"
      gives: "Robot boards the transporter"
    - id: embedded
      col: 3
      span: 2
      row: 2
      kind: process
      accent: blue
      tag: "Stage C"
      title: "Embedded BEV Safety"
      desc: "STM32H7 · ~110 fps"
      receives: "Projected BEV grid"
      logic: "MCU-side 2D safety detector"
      sends: "Real-time hazard flags"
      gives: "Always-on emergency stop"
    - id: obstacle
      col: 1
      span: 2
      row: 3
      kind: process
      accent: green
      tag: "Stage B"
      title: "Grass Obstacle Detection"
      desc: "Geometry V1 → fusion V2"
      receives: "Point cloud + image"
      logic: "Geometry first, then 2D–3D fusion"
      sends: "3D obstacles in grass"
      gives: "Avoids what mowers miss"
    - id: fusion
      col: 3
      span: 2
      row: 3
      kind: reason
      accent: purple
      tag: "Stage D"
      title: "Dual-Attention Fusion"
      desc: "LiDAR–vision research"
      receives: "LiDAR + camera features"
      logic: "Dual cross / self attention"
      sends: "Stronger fused detector"
      gives: "Research feeds production"
    - id: safe
      col: 1
      span: 4
      row: 4
      kind: contribution
      accent: green
      tag: "Outcome"
      title: "Safe Autonomous Mowing"
      desc: "Load → mow → return"
      receives: "All four stage outputs"
      logic: "Arbitrate perception for control"
      sends: "Safe motion commands"
      gives: "Closes the mission loop"
  edges:
    - { from: sensors, to: ramp, kind: flow }
    - { from: sensors, to: embedded, kind: flow }
    - { from: sensors, to: obstacle, kind: flow }
    - { from: fusion, to: obstacle, kind: cond, label: "informs V2" }
    - { from: ramp, to: safe, kind: cond }
    - { from: embedded, to: safe, kind: flow }
    - { from: obstacle, to: safe, kind: flow }
---
<div class="lawn-modules">
  <div class="section-heading">
    <div>
      <p class="eyebrow">System Architecture</p>
      <h2>Four perception modules, one safety stack</h2>
    </div>
  </div>

  <p class="module-intro">
    From a transport vehicle to the lawn and back, the robot leans on a layered perception stack.
    Switch between the four modules below to see <strong>what each one does</strong>, the <strong>tools</strong> behind it,
    the <strong>algorithm pipeline</strong>, and the <strong>on-vehicle result</strong>.
  </p>

  {% include logic-atlas.html %}

  <div class="tech-modules" data-tabs>
    <div class="tech-tabs" role="tablist" aria-label="Perception modules">
      <button class="tech-tab is-active" type="button" role="tab" data-tab="slope" aria-selected="true">
        <span class="tab-index">A</span>
        <span class="tab-label"><strong>Ramp Detection</strong><small>Slope up/down for loading</small></span>
      </button>
      <button class="tech-tab" type="button" role="tab" data-tab="obstacle" aria-selected="false">
        <span class="tab-index">B</span>
        <span class="tab-label"><strong>Grass Obstacle Detection</strong><small>Geometry V1 → fusion V2</small></span>
      </button>
      <button class="tech-tab" type="button" role="tab" data-tab="embedded" aria-selected="false">
        <span class="tab-index">C</span>
        <span class="tab-label"><strong>Embedded Safety</strong><small>STM32H7 · 110 fps</small></span>
      </button>
      <button class="tech-tab" type="button" role="tab" data-tab="fusion" aria-selected="false">
        <span class="tab-index">D</span>
        <span class="tab-label"><strong>Dual-Attention Fusion</strong><small>LiDAR–vision research</small></span>
      </button>
    </div>

    <!-- ============ MODULE A: RAMP DETECTION ============ -->
    <div class="tech-panel is-active" role="tabpanel" data-panel="slope">
      <div class="module-head">
        <p class="eyebrow">Module A · PCL + Eigen + OpenCV</p>
        <h3>Up / down ramp detection</h3>
        <p class="module-oneliner">
          Detect a drive-on ramp and its four boundary lines from a solid-state LiDAR point cloud,
          so the robot can autonomously and stably load and unload itself onto a transport vehicle.
        </p>
        <div class="tool-chips">
          <span class="chip">PCL · RANSAC / normals / filtering</span>
          <span class="chip">Eigen3 · SVD / matrix transforms</span>
          <span class="chip">OpenCV · 2D line post-processing</span>
        </div>
      </div>

      <div class="module-grid">
        <div class="flow">
          <div class="flow-step">
            <span class="step-tag">01 · Input</span>
            <h4>Raw point cloud</h4>
            <ul><li>Solid-state LiDAR stream, vehicle-front field of view</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">02 · Preprocessing — PCL</span>
            <h4>Crop, downsample, denoise</h4>
            <ul>
              <li>ROI crop: <span class="mono">x∈[0,20] · y∈[−5,5] · z∈[−2,2] m</span></li>
              <li>VoxelGrid downsample, <span class="mono">leaf = 0.05 m</span></li>
              <li>StatisticalOutlierRemoval denoising</li>
            </ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">03 · Segmentation — PCL</span>
            <h4>Normals + candidate tilted planes</h4>
            <ul>
              <li>KdTree radius search <span class="mono">r = 0.3 m</span> → per-point normals</li>
              <li>Tilt constraint: normal–Z angle <span class="mono">θ∈[5°,35°]</span></li>
              <li>RegionGrowing (normal diff &lt;5°, point–plane &lt;0.05 m) → N candidate clusters</li>
            </ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">04 · Fitting — PCL SAC + Eigen SVD</span>
            <h4>RANSAC-like plane refinement</h4>
            <ul>
              <li>×100 iters: weighted 3-point sampling → plane; validity <span class="mono">θ∈[5°,20°]</span>; count inliers (&lt;0.05 m); keep max set</li>
              <li>SVD least-squares on inliers → precise plane <span class="mono">{n, d}</span></li>
            </ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">05 · Selection</span>
            <h4>Multi-rule scoring → best ramp</h4>
            <ul>
              <li>Weighted score <span class="mono">Score = Σ wᵢ·sᵢ</span> → highest candidate is the target ramp (<span class="mono">Score &lt; 0.4</span> → “not detected”)</li>
            </ul>
            <div class="scoring">
              <table>
                <thead>
                  <tr><th>Criterion</th><th>Weight</th><th>Rule</th></tr>
                </thead>
                <tbody>
                  <tr><td>Slope plausibility</td><td class="w">0.30</td><td>θ∈[5°,20°] scores full</td></tr>
                  <tr><td>Projected area</td><td class="w">0.20</td><td>larger is better (cap 15 ㎡)</td></tr>
                  <tr><td>Position / heading</td><td class="w">0.20</td><td>front, 2–15 m</td></tr>
                  <tr><td>Planarity (RMSE)</td><td class="w">0.15</td><td>smaller residual is better</td></tr>
                  <tr><td>Shape compactness</td><td class="w">0.10</td><td>reasonable aspect ratio</td></tr>
                  <tr><td>Ground connection</td><td class="w">0.05</td><td>low end joins the ground</td></tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">06 · Geometry — Eigen</span>
            <h4>Local frame + boundary points</h4>
            <ul>
              <li>Frame: <span class="mono">n</span> = Z-axis, downhill = X-axis; project inliers → 2D <span class="mono">(u, v)</span></li>
              <li>Longitudinal 20 strips → 2 long edges; lateral 10 strips → 2 short edges → 4 boundary sets</li>
            </ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">07 · Cleanup — PCL + custom</span>
            <h4>Outlier removal</h4>
            <ul>
              <li>1D spacing-jump: gap &gt; 3× mean → drop isolated points</li>
              <li>Sliding-window median (win = 5): deviation &gt; 0.1 m → drop → 4 clean edge sets</li>
            </ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">08 · Lines — Eigen SVD + RANSAC</span>
            <h4>Four boundary-line fitting</h4>
            <ul>
              <li>RANSAC (30 iters) 2-point line + inliers</li>
              <li>TLS total least squares via SVD → precise line; endpoints by projection → 4 directed segments</li>
            </ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">09 · Output</span>
            <h4>Post-processing + RampInfo</h4>
            <ul>
              <li>Pairwise intersection → 4 corners; validate (opposite edges ∥ &lt;5°, width [1.5,5] m, length [2,20] m); EMA smoothing <span class="mono">α = 0.3</span></li>
              <li>Output <span class="mono">RampInfo { slope_angle, width, length, corners[4], boundary_lines[4], plane, confidence }</span></li>
            </ul>
          </div>
        </div>

        <div class="viz-box">
          <div class="viz-head">On-vehicle result</div>
          <div class="viz-media">
            <figure>
              <img src="{{ '/assets/media/projects/lawn-mower/project_05_up_down_slope.gif' | relative_url }}" alt="Autonomous up and down slope traversal" loading="lazy">
              <figcaption>Autonomous up/down slope traversal for loading and unloading.</figcaption>
            </figure>
            <figure>
              <img src="{{ '/assets/media/projects/lawn-mower/project_03_ob_on_slope1.gif' | relative_url }}" alt="Ramp boundary and obstacle perception" loading="lazy">
              <figcaption>Ramp-boundary and obstacle perception on ramp-like scenes.</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </div>

    <!-- ============ MODULE B: GRASS OBSTACLE DETECTION ============ -->
    <div class="tech-panel" role="tabpanel" data-panel="obstacle">
      <div class="module-head">
        <p class="eyebrow">Module B · two versions</p>
        <h3>Grass obstacle detection</h3>
        <p class="module-oneliner">
          Detect 3D obstacles on grass — first with a pure point-cloud geometric pipeline (V1),
          then upgraded with camera–LiDAR semantic fusion for class-aware, more robust detection (V2).
        </p>
      </div>

      <div class="sub-head">
        <span class="ver">V1</span>
        <h4>Geometry-only pipeline — PCL</h4>
      </div>
      <div class="tool-chips">
        <span class="chip">PCL · filtering / RANSAC / clustering / PCA</span>
      </div>

      <div class="module-grid">
        <div class="flow">
          <div class="flow-step">
            <span class="step-tag">01 · Input</span>
            <h4>Raw point cloud</h4>
            <ul><li>Solid-state LiDAR</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">02 · Preprocessing</span>
            <h4>Filter chain</h4>
            <ul><li>PassThrough crop → VoxelGrid downsample → StatisticalOutlierRemoval</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">03 · Ground</span>
            <h4>Ground segmentation</h4>
            <ul><li>PMF morphological filter → RANSAC plane (<span class="mono">normal∠Z &lt; 15°</span>); ground points discarded</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">04 · Clustering</span>
            <h4>Euclidean clustering</h4>
            <ul><li>KD-Tree neighbor search <span class="mono">r = 0.4 m · min 20 · max 5000 pts</span></li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">05 · Filter</span>
            <h4>PCA bounding box + rules</h4>
            <ul><li>PCA → OBB; constraints <span class="mono">h∈[0.1,2] · w∈[0.1,3] · l∈[0.1,5] m · h/w &lt; 5</span></li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">06 · Output</span>
            <h4>3D obstacles</h4>
            <ul><li>Position / size / distance <span class="mono">= √(cx² + cy²)</span></li></ul>
          </div>
        </div>

        <div class="viz-box">
          <div class="viz-head">V1 result</div>
          <div class="viz-media">
            <figure>
              <img src="{{ '/assets/media/projects/lawn-mower/project_04_obstacle_detection.gif' | relative_url }}" alt="Rule-based 3D obstacle detection" loading="lazy">
              <figcaption>Rule-based 3D obstacle detection from point-cloud clustering.</figcaption>
            </figure>
          </div>
        </div>
      </div>

      <div class="sub-head">
        <span class="ver v2">V2</span>
        <h4>Camera–LiDAR semantic fusion — TensorRT</h4>
      </div>
      <div class="tool-chips">
        <span class="chip">YOLOv5 · 2D detection</span>
        <span class="chip">SegFormer · semantic segmentation</span>
        <span class="chip">TensorRT · inference</span>
        <span class="chip">Camera–LiDAR extrinsics</span>
      </div>

      <div class="module-grid">
        <div class="flow">
          <div class="flow-inputs">
            <div class="flow-step">
              <span class="step-tag">① Input</span>
              <h4>Point cloud</h4>
              <ul><li>Solid-state LiDAR</li></ul>
            </div>
            <div class="flow-step">
              <span class="step-tag">② Input</span>
              <h4>Image</h4>
              <ul><li>RGB camera</li></ul>
            </div>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-note">Image → two TensorRT models</div>
          <div class="flow-branch">
            <div class="flow-step">
              <span class="step-tag">YOLOv5</span>
              <h4>2D bounding boxes</h4>
              <ul><li>Per-frame 2D BBox list</li></ul>
            </div>
            <div class="flow-step">
              <span class="step-tag">SegFormer</span>
              <h4>Semantic mask</h4>
              <ul><li>Ground / obstacle pixel mask</li></ul>
            </div>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">Projection</span>
            <h4>Extrinsic point ↔ pixel</h4>
            <ul><li>Camera–LiDAR extrinsics inject semantics into each 3D point</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-branch">
            <div class="flow-step">
              <span class="step-tag">Semantic ground</span>
              <h4>Mask-based segmentation</h4>
              <ul><li><span class="mono">mask = ground</span> → discard; <span class="mono">obstacle</span> → keep (replaces RANSAC)</li></ul>
            </div>
            <div class="flow-step">
              <span class="step-tag">ROI clustering</span>
              <h4>2D-guided clustering</h4>
              <ul><li>Cluster points inside each BBox; associate 2D detection ↔ 3D cluster</li></ul>
            </div>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">Filter</span>
            <h4>Geometric filter</h4>
            <ul><li>PCA → OBB with the same V1 rule constraints</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">Fusion</span>
            <h4>Triple-score fusion</h4>
            <ul><li><span class="mono">0.4 × geometry + 0.4 × 2D IoU + 0.2 × semantic consistency</span></li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">Output</span>
            <h4>Class-aware 3D obstacles</h4>
            <ul><li>3D obstacles with category label and confidence</li></ul>
          </div>
        </div>

        <div class="viz-box">
          <div class="viz-head">V2 result</div>
          <div class="viz-media">
            <figure>
              <img src="{{ '/assets/media/projects/lawn-mower/project_09_lawn_ai_fusion.gif' | relative_url }}" alt="Image segmentation and LiDAR clustering fusion" loading="lazy">
              <figcaption>Image segmentation and LiDAR clustering fusion.</figcaption>
            </figure>
            <figure>
              <img src="{{ '/assets/media/projects/lawn-mower/project_10_lawn_fusion.gif' | relative_url }}" alt="2D-3D fusion obstacle perception" loading="lazy">
              <figcaption>2D–3D fusion for class-aware obstacle perception.</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </div>

    <!-- ============ MODULE C: EMBEDDED SAFETY ============ -->
    <div class="tech-panel" role="tabpanel" data-panel="embedded">
      <div class="module-head">
        <p class="eyebrow">Module C · STM32H7 MCU</p>
        <h3>Embedded 2D BEV safety detection</h3>
        <p class="module-oneliner">
          A lightweight 2D BEV obstacle detector deployed on an STM32H7 microcontroller — static memory
          plus integer optimization deliver 110 fps real-time detection that passes functional-safety testing.
        </p>
        <div class="tool-chips">
          <span class="chip">STM32H7 · bare-metal C</span>
          <span class="chip">Static memory allocation</span>
          <span class="chip">Integer / fixed-point optimization</span>
        </div>
      </div>

      <div class="module-grid">
        <div class="flow">
          <div class="flow-step">
            <span class="step-tag">Input</span>
            <h4>Raw point cloud</h4>
            <ul><li>Solid-state LiDAR stream</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Step 1 · Preprocess</span>
            <h4>Point-cloud preprocessing</h4>
            <ul>
              <li>ROI crop (5 m × 5 m); ground removal <span class="mono">z &lt; −0.1 m</span></li>
              <li>Invalid filter (range = 0 / NaN); height clamp <span class="mono">0.05–2.5 m</span></li>
            </ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Step 2 · BEV</span>
            <h4>BEV projection</h4>
            <ul>
              <li>Cell index <span class="mono">idx = (x − origin) / reso</span></li>
              <li>Per-cell point count; height diff <span class="mono">max_z − min_z</span></li>
            </ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Step 3 · Decide</span>
            <h4>Obstacle decision</h4>
            <ul>
              <li>Density threshold <span class="mono">count &gt; 3</span>; height diff <span class="mono">&gt; 0.1 m</span></li>
              <li>Connected components (8-neighbor merge)</li>
            </ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Step 4 · Output</span>
            <h4>BEV obstacle list</h4>
            <ul><li>Danger level + nearest-obstacle BEV coordinate</li></ul>
          </div>

          <div class="module-highlight">
            <div class="metric"><strong>110 fps</strong><span>real-time on MCU</span></div>
            <div class="metric"><strong>Static</strong><span>fixed memory, no heap</span></div>
            <div class="metric"><strong>Integer</strong><span>fixed-point math</span></div>
            <div class="metric"><strong>Safety</strong><span>passed functional-safety test</span></div>
          </div>
        </div>

        <div class="viz-box">
          <div class="viz-head">Safety-test result</div>
          <div class="viz-media">
            <figure>
              <img src="{{ '/assets/media/projects/lawn-mower/project_06_angui.gif' | relative_url }}" alt="Lightweight 2D BEV safety detection" loading="lazy">
              <figcaption>Lightweight 2D BEV detector running on STM32H7 for safety-standard testing.</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </div>

    <!-- ============ MODULE D: DUAL-ATTENTION FUSION ============ -->
    <div class="tech-panel" role="tabpanel" data-panel="fusion">
      <div class="module-head">
        <p class="eyebrow">Module D · pre-research</p>
        <h3>Dual-attention LiDAR–vision fusion</h3>
        <p class="module-oneliner">
          A pre-research study (toward a company paper KPI) on dual-attention fusion that correlates
          scene geometry and texture features for stronger LiDAR–vision 3D detection.
        </p>
        <div class="tool-chips">
          <span class="chip">Dual-attention fusion</span>
          <span class="chip">Soft + hard association</span>
          <span class="chip">LiDAR–camera 3D detection</span>
        </div>
      </div>

      <div class="module-grid">
        <div class="flow">
          <div class="flow-inputs">
            <div class="flow-step">
              <span class="step-tag">Geometry branch</span>
              <h4>LiDAR features</h4>
              <ul><li>3D scene-geometry encoding</li></ul>
            </div>
            <div class="flow-step">
              <span class="step-tag">Texture branch</span>
              <h4>Image features</h4>
              <ul><li>2D appearance / texture encoding</li></ul>
            </div>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">Pre-built index</span>
            <h4>Fast correspondence</h4>
            <ul><li>Pre-compute point ↔ pixel index so fusion stays cheap at runtime</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-branch">
            <div class="flow-step">
              <span class="step-tag">Hard association</span>
              <h4>Explicit correspondence</h4>
              <ul><li>Geometric point ↔ pixel matching</li></ul>
            </div>
            <div class="flow-step">
              <span class="step-tag">Soft association</span>
              <h4>Query-style attention</h4>
              <ul><li>Learned cross-modal attention weights</li></ul>
            </div>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">Dual attention</span>
            <h4>Geometry × texture interaction</h4>
            <ul><li>Two attention streams couple structure and appearance into a shared representation</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>

          <div class="flow-step">
            <span class="step-tag">Output</span>
            <h4>Robust 3D detection</h4>
            <ul><li>Stronger on small objects, sparse LiDAR, and degraded images</li></ul>
          </div>

          <div class="ref-note">
            <strong>Reference.</strong>
            <span>Connected to FFPA-Net and soft/hard bi-modality fusion research.</span>
            <a class="tiny-link" href="{{ '/assets/media/projects/lawn-mower/fusion-sh.pdf' | relative_url }}" target="_blank" rel="noopener">Study PDF</a>
          </div>
        </div>

        <div class="viz-box">
          <div class="viz-head">Research visualization</div>
          <div class="viz-media">
            <figure>
              <img src="{{ '/assets/media/projects/lawn-mower/project_13_soft_hard.gif' | relative_url }}" alt="Soft and hard association for bi-modality fusion" loading="lazy">
              <figcaption>Soft- and hard-association idea for bi-modality fusion.</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
