---
title: "3D Scene Flow: Auto-Labeling & Production Deployment"
subtitle: "An unsupervised point- and occupancy-level 3D scene-flow auto-labeling system, two deployable flow networks, an ultra-light production head, and full ONNX → TensorRT / Horizon J6E deployment."
description: "An unsupervised 3D scene-flow auto-labeling system, two deployable flow networks, an ultra-light production head, and full ONNX → TensorRT / Horizon J6E deployment."
date_range: "2023.08–2023.12"
partners: "PhiGent Robotics"
role: "3D Scene Flow Algorithm Engineer"
category: "Research + Deployment Project"
stage: "Deployment-oriented research"
tags: ["research", "3d-4d", "scene-flow", "deployment"]
cover: "/assets/media/projects/scene-flow-deployment/autoflow_vis.mp4"
cover_type: "video"
featured: true
order: 70
rich_body: true
summary: "A 3D motion-estimation stack for autonomous driving: an unsupervised auto-labeling system that assigns a 3D scene-flow vector to every LiDAR point and every occupancy cell, validated by lifting the accuracy of existing flow estimators, distilled into an ultra-light production head, and deployed end-to-end through ONNX, TensorRT (Orin) and the Horizon J6E toolchain."
privacy_note: "Only the general pipeline and deployment concepts are shown. Internal data, exact metrics, model parameters, and hardware-specific optimization details are omitted; any figures are illustrative."
atlas:
  eyebrow: "Logic map"
  title: "From unsupervised labels to on-vehicle occupancy flow"
  caption: "One label engine feeds a tiny production head; a single ONNX source fans out to two silicon targets. Hover a node."
  cols: 4
  nodes:
    - id: sweeps
      col: 1
      span: 4
      row: 1
      kind: input
      accent: ink
      tag: "Input"
      title: "Consecutive LiDAR Sweeps"
      desc: "Paired clouds + ego-pose"
      receives: "Raw LiDAR Pt, Pt+1"
      logic: "Compensate ego-motion"
      sends: "Aligned sweep pairs"
      gives: "Raw signal, zero labels"
    - id: autolabel
      col: 1
      span: 4
      row: 2
      kind: process
      accent: cyan
      tag: "Core IP"
      title: "Unsupervised Auto-Labeler"
      desc: "Point- + occ-level flow"
      receives: "Aligned sweep pairs"
      logic: "Geometry / cycle / smoothness constraints"
      sends: "Dense 3D motion labels"
      gives: "Labels scale with mileage"
    - id: validate
      col: 1
      span: 2
      row: 3
      kind: reason
      accent: blue
      tag: "Proof"
      title: "Lifts Existing Estimators"
      desc: "Labels make others better"
      receives: "Auto-labels → baselines"
      logic: "Retrain established methods"
      sends: "Consistent accuracy gains"
      gives: "Evidence the labels are right"
    - id: head
      col: 3
      span: 2
      row: 3
      kind: process
      accent: purple
      tag: "Productize"
      title: "Ultra-Light Head"
      desc: "Graph-conv vs pure DL"
      receives: "Auto-labels as supervision"
      logic: "Distill into embedded-size net"
      sends: "Tiny flow predictor"
      gives: "On-vehicle compute budget"
    - id: export
      col: 1
      span: 4
      row: 4
      kind: process
      accent: warn
      tag: "Export"
      title: "Single ONNX Graph"
      desc: "One source of truth"
      receives: "Trained / quantized head"
      logic: "Export portable .onnx"
      sends: "Graph to both runtimes"
      gives: "Train ↔ deploy stay aligned"
    - id: trt
      col: 1
      span: 2
      row: 5
      kind: output
      accent: green
      tag: "Target A"
      title: "TensorRT · Orin"
      desc: "High-compute tier"
      receives: "ONNX graph"
      logic: "Graph + precision optimize"
      sends: "Orin runtime engine"
      gives: "Fast NVIDIA inference"
    - id: horizon
      col: 3
      span: 2
      row: 5
      kind: output
      accent: green
      tag: "Target B"
      title: "Horizon J6E"
      desc: "Cost-optimized tier"
      receives: "ONNX graph"
      logic: "Convert + quantize via SDK"
      sends: "J6E runtime engine"
      gives: "Cheap embedded inference"
    - id: onvehicle
      col: 1
      span: 4
      row: 6
      kind: contribution
      accent: green
      tag: "Output"
      title: "On-Vehicle Occupancy Flow"
      desc: "Live per-cell motion"
      receives: "Optimized runtime engine"
      logic: "Preprocess → infer → parse"
      sends: "Dense scene-flow field"
      gives: "Production motion estimation"
  edges:
    - { from: sweeps, to: autolabel, kind: flow }
    - { from: autolabel, to: validate, kind: solid }
    - { from: autolabel, to: head, kind: flow }
    - { from: validate, to: head, kind: dashed }
    - { from: head, to: export, kind: flow }
    - { from: export, to: trt, kind: flow }
    - { from: export, to: horizon, kind: flow }
    - { from: trt, to: onvehicle, kind: flow }
    - { from: horizon, to: onvehicle, kind: flow }
---
<div class="lawn-modules">

  <!-- ===================== OVERVIEW ===================== -->
  <div class="section-heading">
    <div>
      <p class="eyebrow">Overview</p>
      <h2>Give every point — and every occupancy cell — a motion vector, with no human labels</h2>
    </div>
  </div>

  <p class="module-intro">
    <strong>3D scene flow</strong> is the dense per-point 3D motion field between two LiDAR sweeps — the geometric
    backbone for dynamic-object reasoning, velocity estimation and occupancy-flow prediction. Hand-labeling it is
    effectively impossible. This project built an <strong>unsupervised auto-labeling system</strong> that assigns a
    motion vector to <strong>every point and every occupancy (occ) cell</strong>, used those labels to
    <strong>sharpen existing flow estimators</strong>, distilled the result into an <strong>ultra-light production
    head</strong>, and shipped the whole stack through <strong>ONNX → TensorRT (NVIDIA Orin)</strong> and the
    <strong>Horizon J6E</strong> toolchain.
  </p>

  <div class="tool-chips">
    <span class="chip">Unsupervised auto-labeling</span>
    <span class="chip">Point-level + Occ-level flow</span>
    <span class="chip">Graph-conv + math constraints</span>
    <span class="chip">ONNX · TensorRT · Horizon J6E</span>
  </div>

  {% include logic-atlas.html %}

  <div class="phase-track">

    <!-- ===================== MODULE 01 · AUTO-LABELING ===================== -->
    <section class="phase">
      <div class="phase-head">
        <span class="phase-step">01</span>
        <span class="phase-badge">The core IP</span>
        <span class="phase-org">Auto-Flow labeling</span>
      </div>
      <h3>An unsupervised 3D scene-flow &amp; occ-flow auto-labeler</h3>
      <p class="phase-lead">
        The heart of the project: a self-supervised system that takes raw LiDAR sweeps and produces a dense
        3D motion label for <strong>every point</strong> and <strong>every occupancy cell</strong> — no manual
        annotation in the loop. These auto-labels become the training signal for every downstream flow model.
      </p>

      <div class="proj-figure on-white" style="margin-top:1.1rem">
        <img src="{{ '/assets/media/projects/scene-flow-deployment/flow_model_arch.jpg' | relative_url }}" alt="3D scene-flow and occupancy-flow auto-labeling architecture" loading="lazy">
        <figcaption><strong>Auto-labeling architecture.</strong> From consecutive LiDAR sweeps, the system jointly estimates a per-point 3D scene-flow field and a per-occ 3D motion field, supervised only by geometric and temporal consistency — so high-quality flow labels are generated automatically, at scale.</figcaption>
      </div>

      <div class="module-grid" style="margin-top:1.1rem">
        <div class="flow">
          <div class="flow-step">
            <span class="step-tag">Step 1 · Input</span>
            <h4>Consecutive LiDAR sweeps</h4>
            <ul><li>Paired point clouds <span class="mono">P<sub>t</sub>, P<sub>t+1</sub></span> + ego-pose; no flow ground truth required</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Step 2 · Estimate</span>
            <h4>Dense motion field</h4>
            <ul><li>Predict a 3D vector per point and per occ cell; ego-motion compensated so only true object motion remains</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Step 3 · Self-supervise</span>
            <h4>Consistency objectives</h4>
            <ul><li>Nearest-neighbour / cycle / smoothness constraints replace human labels with geometry</li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">Step 4 · Emit</span>
            <h4>Point- &amp; occ-flow labels</h4>
            <ul><li>A reusable label bank that trains and stress-tests every downstream estimator</li></ul>
          </div>
        </div>

        <div class="viz-box">
          <div class="viz-head">Why unsupervised</div>
          <div class="viz-media">
            <figure>
              <figcaption style="margin-top:0">
                Dense 3D flow has no scalable human-labeling route — a single sweep holds <strong>100k+ points</strong>.
                Driving geometry (rigid ego-motion, locally smooth object motion, cross-frame correspondence) supplies
                the supervision instead, so labels scale with raw mileage rather than with annotation budget.
              </figcaption>
            </figure>
          </div>
        </div>
      </div>
    </section>

    <!-- ===================== MODULE 02 · VALIDATION ===================== -->
    <section class="phase">
      <div class="phase-head">
        <span class="phase-step">02</span>
        <span class="phase-badge">Does it actually help?</span>
        <span class="phase-org">Validation</span>
      </div>
      <h3>Auto-labels lift existing flow estimators</h3>
      <p class="phase-lead">
        The acid test for a labeling system is whether its labels make <em>other</em> models better. Feeding our
        auto-labels into established 3D scene-flow estimators improved their prediction accuracy
        <strong>substantially</strong> — direct evidence that the generated supervision is both correct and useful.
      </p>

      <div class="compare" style="margin-top:1.1rem">
        <div class="compare-col before">
          <h5>Baseline estimators</h5>
          <p class="big">Original supervision</p>
          <p>Trained on their native, limited flow signals</p>
          <p>Weaker on fast, distant and sparse objects</p>
        </div>
        <div class="compare-arrow" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </div>
        <div class="compare-col after">
          <h5>+ our auto-labels</h5>
          <p class="big">Substantially sharper</p>
          <p>Same architectures, richer dense supervision</p>
          <p>Consistent accuracy gains across methods</p>
        </div>
      </div>

      <div class="proj-figure on-white" style="margin-top:1.1rem">
        <img src="{{ '/assets/media/projects/scene-flow-deployment/flow_model_exp.jpg' | relative_url }}" alt="Accuracy improvement after applying our auto-labels to existing scene-flow methods" loading="lazy">
        <figcaption><strong>Result.</strong> Existing 3D scene-flow estimation methods, retrained with labels from our auto-labeling system, show a clear, consistent jump in prediction accuracy — the labeling system pays for itself across architectures.</figcaption>
      </div>
    </section>

    <!-- ===================== MODULE 03 · PRODUCTION HEAD ===================== -->
    <section class="phase">
      <div class="phase-head">
        <span class="phase-step">03</span>
        <span class="phase-badge">From research to silicon</span>
        <span class="phase-org">Production head</span>
      </div>
      <h3>An ultra-light 3D scene-flow head — two design routes</h3>
      <p class="phase-lead">
        For mass production the flow predictor must be tiny and embedded-friendly. We explored two routes for the
        production head and compared them head-to-head: a <strong>graph-convolution + mathematical-constraint</strong>
        design, and a <strong>pure point-cloud deep-learning</strong> design fit directly to supervision.
      </p>

      <div class="proj-figure on-white" style="margin:1.1rem auto 0;max-width:560px">
        <img src="{{ '/assets/media/projects/scene-flow-deployment/m1_conv.png' | relative_url }}" alt="Ultra-light 3D scene-flow production head — graph-convolution variant (top) and pure deep-learning variant (bottom)" loading="lazy">
        <figcaption><strong>Two production heads.</strong> <em>Top</em> — graph convolution with explicit mathematical (rigidity / smoothness) constraints. <em>Bottom</em> — a pure point-cloud network that regresses flow directly from supervision. Both are budgeted for on-vehicle compute.</figcaption>
      </div>

      <div class="compare" style="margin-top:1.1rem">
        <div class="compare-col before">
          <h5>Route A · Graph-conv + math</h5>
          <p class="big">Geometry-guided</p>
          <p>Graph convolution over local neighbourhoods</p>
          <p>Explicit rigidity / smoothness constraints</p>
          <p>Robust &amp; interpretable on structured motion</p>
        </div>
        <div class="compare-arrow" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </div>
        <div class="compare-col after">
          <h5>Route B · Pure deep-learning</h5>
          <p class="big">Data-driven</p>
          <p>Point-cloud network regresses flow end-to-end</p>
          <p>Fit directly to the auto-generated labels</p>
          <p>Simplest graph to export and quantize</p>
        </div>
      </div>
    </section>

    <!-- ===================== MODULE 04 · DEPLOYMENT ===================== -->
    <section class="phase">
      <div class="phase-head">
        <span class="phase-step">04</span>
        <span class="phase-badge">On-vehicle</span>
        <span class="phase-org">Deployment</span>
      </div>
      <h3>ONNX → TensorRT / Horizon J6E, with occ-flow inference</h3>
      <p class="phase-lead">
        The trained head was exported to <strong>ONNX</strong>, optimized with <strong>TensorRT</strong> for NVIDIA
        Orin, and converted with the <strong>Horizon</strong> SDK toolchain for J6E. Against existing production
        options our solution held up well, and the same export produces the live occupancy-flow inference below.
      </p>

      <div class="proj-figure on-white" style="margin:1.1rem auto 0;max-width:720px">
        <img src="{{ '/assets/media/projects/scene-flow-deployment/occ_flow_onnx_infer.png' | relative_url }}" alt="Production-solution comparison and occupancy-flow prediction visualized from ONNX inference" loading="lazy">
        <figcaption><strong>Deployment evidence.</strong> Our production flow solution compared against other existing options, alongside an occupancy-flow prediction visualized directly from the exported <span class="mono">ONNX</span> inference — confirming that the optimized graph behaves on-target as it does in training.</figcaption>
      </div>

      <div class="module-grid" style="margin-top:1.2rem">
        <div class="flow">
          <div class="flow-step">
            <span class="step-tag">① Export</span>
            <h4>Trained model → ONNX</h4>
            <ul><li>Floating-point or quantized graph exported to a portable <span class="mono">.onnx</span></li></ul>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-branch">
            <div class="flow-step">
              <span class="step-tag">②A · NVIDIA</span>
              <h4>TensorRT on Orin</h4>
              <ul><li>Graph &amp; precision optimization for the Orin runtime</li></ul>
            </div>
            <div class="flow-step">
              <span class="step-tag">②B · Horizon</span>
              <h4>SDK on J6E</h4>
              <ul><li>Convert &amp; quantize through the Horizon J6E toolchain</li></ul>
            </div>
          </div>
          <div class="flow-arrow" aria-hidden="true"></div>
          <div class="flow-step">
            <span class="step-tag">③ Runtime</span>
            <h4>On-vehicle inference loop</h4>
            <ul><li>Point-cloud preprocess → cache init → normalize → inference → output parsing → perf stats</li></ul>
          </div>
        </div>

        <div class="viz-box">
          <div class="viz-head">Deployment targets</div>
          <div class="viz-media">
            <figure>
              <figcaption style="margin-top:0">
                One trained head, two silicon paths: <strong>TensorRT / Orin</strong> for the high-compute tier and
                <strong>Horizon J6E</strong> for the cost-optimized tier — sharing a single ONNX source of truth so
                training and on-vehicle behaviour stay aligned.
              </figcaption>
            </figure>
          </div>
        </div>
      </div>
    </section>

  </div><!-- /phase-track -->

  <!-- ===================== DEMO ===================== -->
  <div class="module-head" style="margin-top:2.4rem">
    <p class="eyebrow">Visualization</p>
    <h2>Auto-Flow, running</h2>
    <p class="module-oneliner">The end-to-end result — dense 3D scene flow auto-labeled and predicted on real driving sequences. Plays automatically and loops.</p>
  </div>

  <div class="proj-figure" style="margin-top:1.1rem">
    <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback>
      <source src="{{ '/assets/media/projects/scene-flow-deployment/autoflow_vis.mp4' | relative_url }}" type="video/mp4">
    </video>
    <figcaption><strong>Auto-Flow demo.</strong> Per-point 3D motion estimated across a full sequence — the colour field encodes the predicted scene-flow direction and magnitude.</figcaption>
  </div>

</div>
