---
title: "Generative World Model for 7V Closed-Loop Driving Simulation"
subtitle: "A real-time streaming 7-camera world model powered by causal DiT architecture, 3-stage training paradigm, and interactive vector-to-neural closed-loop simulation."
description: "A streaming 7-camera surround-view generative world model for closed-loop autonomous driving simulation — featuring causal DiT, a 3-stage distillation paradigm, multi-weather simulation, and interactive policy rollout."
date_range: "2025.06–Present"
partners: "Frontier World Model Lab"
role: "Core Algorithm & System Architect"
category: "Generative World Models"
stage: "Production & Research"
tags: ["research", "world-model", "generative", "e2e", "deployment"]
cover: "/assets/media/projects/7v_closed_loop_sim/steaming_wm_high_speed_raw.mp4"
cover_type: "video"
featured: true
order: 150
rich_body: true
summary: "A production-grade 7-camera surround-view generative world model powering closed-loop autonomous driving simulation: streaming block-causal DiT, 3-stage training with self-forcing distillation, and interactive neural rendering across complex traffic scenarios and diverse weather conditions."
problem: "Real-world test drives cannot efficiently scale to rare long-tail hazards, while classical graphics simulators suffer from severe sim-to-real domain gaps. Existing surround video diffusion models are non-causal and require 30+ iterative denoising steps, making real-time closed-loop policy evaluation impossible."
built: "A real-time streaming 7V surround world model with block-causal spatio-temporal attention, cross-view epipolar conditioning, and a 3-stage training pipeline (Bidirectional Teacher → Causal Student → DMD Self-Forcing Distillation) that generates photorealistic 7-camera video streams from interactive BEV vector layouts."
result: "Achieved continuous streaming rollout with only 4 denoising steps per chunk, supporting interactive closed-loop simulation across highway merging, dense night traffic, cutting-in maneuvers, and controllable weather synthesis (dusk, rain, storm, snow)."
my_role: "Designed the 7V streaming DiT network architecture, formulated the cross-view causal attention mechanism, and developed the end-to-end 3-stage distillation and closed-loop vector-to-video rollout platform."
privacy_note: "All displayed scenarios, models, and evaluation benchmarks are based on sanitized open research configurations. Proprietary commercial calibration and confidential fleet telemetry are strictly excluded."
---
<div class="lawn-modules">

  <!-- ============================================================ -->
  <!-- 01. SYSTEM ARCHITECTURE & PARADIGM                           -->
  <!-- ============================================================ -->
  <div class="section-heading">
    <div>
      <p class="eyebrow">01 · System Architecture &amp; Methodology</p>
      <h2>Streaming 7V Generative Simulation Architecture</h2>
    </div>
  </div>

  <p class="module-intro">
    A complete closed-loop neural simulation framework translating high-level policy actions into photorealistic, spatially and temporally coherent 7-camera surround video streams.
  </p>

  <!-- Full Workflow Diagram -->
  <div class="proj-figure">
    <img src="{{ '/assets/media/projects/7v_closed_loop_sim/7v_closed_loop_sim_workflow.png' | relative_url }}" alt="7V Closed-Loop Simulation System Workflow" loading="lazy">
    <figcaption>
      <strong>Figure 1: End-to-end 7V closed-loop simulation pipeline.</strong>
      From policy action &amp; BEV vector dynamics, through multi-camera layout projection, to streaming neural world model rendering and closed-loop perception-action feedback.
    </figcaption>
  </div>

  <!-- DiT Architecture & 3-Stage Training Grid -->
  <div class="duo2" style="margin-top: 1.5rem;">
    <div>
      <div class="d2-tag">Model Architecture</div>
      <h4 style="margin-top: 0.3rem;">Streaming World Model DiT Block</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.5rem;">
        <img src="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_DiT.png' | relative_url }}" alt="Streaming World Model DiT Architecture" loading="lazy">
      </div>
      <p>
        28-layer DiT block with AdaLN modulation, intra-view temporal attention with KV-caching, localized cross-view spatial attention, and cross-attention text/vector conditioning.
      </p>
    </div>
    <div>
      <div class="d2-tag">Training Paradigm</div>
      <h4 style="margin-top: 0.3rem;">Three-Stage Progressive Training</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.5rem;">
        <img src="{{ '/assets/media/projects/7v_closed_loop_sim/train_3_stage.png' | relative_url }}" alt="Three-Stage Training Paradigm" loading="lazy">
      </div>
      <p>
        <strong>Stage 1 (L1b):</strong> Bidirectional Teacher pretraining.<br>
        <strong>Stage 2 (L2a):</strong> Causal Student conversion with block-causal mask.<br>
        <strong>Stage 3 (L3):</strong> Self-Forcing DMD distillation (35 steps → 4 steps).
      </p>
    </div>
  </div>

  <!-- ============================================================ -->
  <!-- 02. TEACHER & CAUSAL STUDENT PROGRESSION                     -->
  <!-- ============================================================ -->
  <div class="section-heading" style="margin-top: 3.5rem;">
    <div>
      <p class="eyebrow">02 · Model Evolution &amp; Data Engine</p>
      <h2>Teacher Denoising &amp; Causal Student Conversion</h2>
    </div>
  </div>

  <p class="module-intro">
    Comparing full-window bidirectional teacher generation against streaming causal student rollout and rare-case safety scenario synthesis.
  </p>

  <!-- Teacher Model 93-frame Generations -->
  <div class="duo2">
    <div>
      <div class="d2-tag">Stage 1 · Bidirectional Teacher</div>
      <h4 style="margin-top: 0.3rem;">Surround Generation Walkthrough — Case 1</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/compressed-teacher1_9s_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/compressed-teacher1_9s.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption><strong>Teacher Case 1 (93 frames @ 10Hz).</strong> Top: Condition Layout | Mid: World Model Output | Bottom: Ground Truth.</figcaption>
      </div>
    </div>
    <div>
      <div class="d2-tag">Stage 1 · Bidirectional Teacher</div>
      <h4 style="margin-top: 0.3rem;">Surround Generation Walkthrough — Case 2</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/compressed-teacher2_9s_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/compressed-teacher2_9s.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption><strong>Teacher Case 2 (93 frames @ 10Hz).</strong> Top: Condition Layout | Mid: World Model Output | Bottom: Ground Truth.</figcaption>
      </div>
    </div>
  </div>

  <!-- Rare-case Safety Scenario Generation with Smart Agent -->
  <div class="duo2" style="margin-top: 1.2rem;">
    <div>
      <div class="d2-tag">Smart Agent · Long-tail Generation</div>
      <h4 style="margin-top: 0.3rem;">Rare Interactive Safety Case — Example 1</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/teacher_e1_9s_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/teacher_e1_9s.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>Synthetic long-tail traffic injection: aggressive cut-in and emergency braking behavior generation.</figcaption>
      </div>
    </div>
    <div>
      <div class="d2-tag">Smart Agent · Long-tail Generation</div>
      <h4 style="margin-top: 0.3rem;">Rare Interactive Safety Case — Example 2</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/compressed-teacher_e2_9s_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/compressed-teacher_e2_9s.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>High-density interaction and corner-case scenario synthesis for stress-testing planner policies.</figcaption>
      </div>
    </div>
  </div>

  <!-- Stage 2 Causal Student Rollout -->
  <div class="duo2" style="margin-top: 1.2rem;">
    <div>
      <div class="d2-tag">Stage 2 · Causal Student</div>
      <h4 style="margin-top: 0.3rem;">Causal Block Rollout — Example 1</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/compressed-causal_student1_9s_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/compressed-causal_student1_9s.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>Streaming causal generation with KV cache (2-frame block autoregression).</figcaption>
      </div>
    </div>
    <div>
      <div class="d2-tag">Stage 2 · Causal Student</div>
      <h4 style="margin-top: 0.3rem;">Causal Block Rollout — Example 2</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/compressed-causal_student2_9s_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/compressed-causal_student2_9s.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>Long-horizon temporal consistency without future-frame leakage.</figcaption>
      </div>
    </div>
  </div>

  <!-- ============================================================ -->
  <!-- 03. STREAMING CLOSED-LOOP ROLLOUTS                           -->
  <!-- ============================================================ -->
  <div class="section-heading" style="margin-top: 3.5rem;">
    <div>
      <p class="eyebrow">03 · Stage 3 Self-Forcing &amp; Interactive Rollout</p>
      <h2>Streaming Closed-Loop Traffic Scenarios</h2>
    </div>
  </div>

  <p class="module-intro">
    Final self-forcing distilled model executing continuous real-time neural rollouts across interactive driving maneuvers in complex traffic environments.
  </p>

  <!-- Vector Layout to 7V Projection -->
  <div class="proj-figure">
    <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_high_speed_layout_converted_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
      <source src="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_high_speed_layout_converted.mp4' | relative_url }}" type="video/mp4">
    </video>
    <figcaption>
      <strong>Vector layout interaction &amp; 7V camera projection.</strong>
      Interactive policy maneuvers in BEV vector space mapped dynamically to 7 surround-view camera layout conditions.
    </figcaption>
  </div>

  <!-- Daytime Overtaking & Night Dense Grid -->
  <div class="duo2" style="margin-top: 1.5rem;">
    <div>
      <div class="d2-tag">Closed-Loop Scenario 01</div>
      <h4 style="margin-top: 0.3rem;">Daytime Highway Overtaking &amp; Lane Change</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_daytime_converted_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_daytime_converted.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>High-speed interactive overtaking with continuous cross-camera object tracking.</figcaption>
      </div>
    </div>
    <div>
      <div class="d2-tag">Closed-Loop Scenario 02</div>
      <h4 style="margin-top: 0.3rem;">Nighttime Congested Highway Traffic</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_nigth_converted_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_nigth_converted.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>Challenging low-light glare, tail-light reflections, and multi-agent interaction.</figcaption>
      </div>
    </div>
  </div>

  <!-- Highway Merge Baseline vs HDMap Comparison -->
  <div class="duo2" style="margin-top: 1.2rem;">
    <div>
      <div class="d2-tag">Closed-Loop Scenario 03</div>
      <h4 style="margin-top: 0.3rem;">Highway Confluence &amp; Ramp Merging</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_high_speed_raw_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_high_speed_raw.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>Multi-lane ramp merging scenario rendered in real-time streaming mode.</figcaption>
      </div>
    </div>
    <div>
      <div class="d2-tag">Benchmark Validation</div>
      <h4 style="margin-top: 0.3rem;">Dusk Generation vs Ground Truth Benchmark</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/sample_dusk_with_hdmap_converted_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/sample_dusk_with_hdmap_converted.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>Top: Input Layout | Mid: World Model Output | Bottom: Ground Truth Reference.</figcaption>
      </div>
    </div>
  </div>

  <!-- ============================================================ -->
  <!-- 04. MULTI-ENVIRONMENT WEATHER SIMULATION                     -->
  <!-- ============================================================ -->
  <div class="section-heading" style="margin-top: 3.5rem;">
    <div>
      <p class="eyebrow">04 · Zero-Shot Weather Transfer</p>
      <h2>Multi-Weather Controllable Generation</h2>
    </div>
  </div>

  <p class="module-intro">
    Demonstrating zero-shot style transfer on the identical trajectory layout across harsh weather conditions to test perception robustness.
  </p>

  <div class="duo2">
    <div>
      <div class="d2-tag">Condition A · Atmospheric Lighting</div>
      <h4 style="margin-top: 0.3rem;">Dusk / Sunset Simulation</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_high_speed_dusk_converted_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_high_speed_dusk_converted.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>Low-angle golden sunlight and long shadow rendering.</figcaption>
      </div>
    </div>
    <div>
      <div class="d2-tag">Condition B · Precipitation</div>
      <h4 style="margin-top: 0.3rem;">Heavy Rain Storm Simulation</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_high_speed_rain_converted_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_high_speed_rain_converted.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>Wet road specular reflections and windscreen droplet distortion.</figcaption>
      </div>
    </div>
  </div>

  <div class="duo2" style="margin-top: 1.2rem;">
    <div>
      <div class="d2-tag">Condition C · Complex Lighting + Water</div>
      <h4 style="margin-top: 0.3rem;">Night Rain Weather Simulation</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_highspeed_night_rain_converted_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_highspeed_night_rain_converted.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>Complex headlight bloom and wet asphalt light reflections.</figcaption>
      </div>
    </div>
    <div>
      <div class="d2-tag">Condition D · Extreme Winter</div>
      <h4 style="margin-top: 0.3rem;">Blizzard Snow Weather Simulation</h4>
      <div class="proj-figure" style="margin: 0.8rem 0 0.4rem;">
        <video autoplay muted loop playsinline preload="metadata" poster="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_highspeed_snow_converted_poster.jpg' | relative_url }}" disablepictureinpicture disableremoteplayback>
          <source src="{{ '/assets/media/projects/7v_closed_loop_sim/steaming_wm_highspeed_snow_converted.mp4' | relative_url }}" type="video/mp4">
        </video>
        <figcaption>Heavy snowfall occlusion and whiteout surface texture synthesis.</figcaption>
      </div>
    </div>
  </div>

  <!-- Highlight Metrics -->
  <div class="module-highlight" style="margin-top: 2.5rem;">
    <div class="metric"><strong>7 Cameras</strong><span>Synchronized 360° surround video</span></div>
    <div class="metric"><strong>4 Steps</strong><span>Self-forcing distilled real-time rollout</span></div>
    <div class="metric"><strong>Causal DiT</strong><span>Streaming block autoregression + KV cache</span></div>
    <div class="metric"><strong>Multi-Weather</strong><span>Day, night, dusk, rain, storm, snow</span></div>
  </div>

</div>