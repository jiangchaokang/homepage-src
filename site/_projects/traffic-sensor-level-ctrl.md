---
title: "Vector Traffic Generation & Sensor-Level Closed-Loop Simulation"
subtitle: "Two halves of a controllable driving simulator: a structure-aware temporal vector world model that generates traffic as latents, and a sensor-level pipeline that reconstructs, populates and re-renders photorealistic surround video."
description: "A two-level controllable driving simulator — a temporal vector world model that generates traffic as latents, and a sensor-level closed-loop pipeline for photorealistic re-rendering."
date_range: "2025.05–Present"
partners: "Bosch (XC-CN)"
role: "World Models Algorithm Engineer"
category: "Research Platform"
stage: "Ongoing"
tags: ["research", "world-model", "generative", "e2e"]
cover: "/assets/media/projects/recon_gen_simulation/1.Gen_fg_bg_Diff_light.mp4"
cover_type: "video"
featured: true
order: 130
rich_body: true
summary: "A two-level driving simulator: a vector world model that decides what the traffic does, and a sensor-level pipeline that decides what the cameras see — reconstruction, generated traffic, and a mask-guided video editor in one closed loop."
problem: "A simulator has to be controllable and photorealistic at the same time. Vector simulators let you author behaviour but render nothing a perception model believes; video generators look real but cannot be steered scenario by scenario."
built: "Two levels that meet in the middle. A structure-aware temporal autoencoder (STAR-AE) compresses variable numbers of agents and lanes into a fixed latent, and a conditional latent diffusion model (STRIDENet) rolls that latent forward into history-consistent future traffic. Beneath it, a sensor-level loop fuses Gaussian-Splatting reconstruction of the real background with the generated traffic through a mask-guided DiT video editor built on MagicDrive-V2."
result: "Behaviour is authored as vectors and rendered as photoreal 7-camera surround video in the same loop, so a scenario can be changed at the level a person thinks about it — and the editor only regenerates the masked foreground instead of the whole frame."
my_role: "I designed and trained the vector level — the STAR-AE latent structure and the STRIDENet conditioning — and integrated it with the sensor-level pipeline. Reconstruction and the video editor are built on shared platform components."
relation: "This is one track inside the Generative Autonomous-Driving Simulation Platform: that project supplies the surround world model and the distilled sampler, this one supplies the traffic behaviour and the closed-loop re-rendering."
glossary:
  - term: "STAR-AE"
    def: "Structure-aware temporal autoencoder. Turns a scene with a variable number of agents and lanes into a fixed-size latent, which is what makes diffusion over traffic possible at all."
  - term: "STRIDENet"
    def: "The conditional latent diffusion model that denoises the next traffic latent, conditioned on the observed history through adaptive layer norm."
  - term: "Gaussian Splatting"
    def: "An explicit 3D scene representation optimised from real frames; renders the true background from viewpoints the vehicle never drove."
  - term: "Mask-guided DiT"
    def: "A diffusion transformer video editor that regenerates only the masked foreground and blends the seam, instead of resynthesising the whole frame."
  - term: "MagicDrive-V2"
    def: "The multi-view driving video generation base this editor is built on."
privacy_note: "Bosch (XC-CN) ongoing research. Architecture and method are presented at a portfolio level; internal data, calibration, metrics, and product details are intentionally omitted or sanitized."
atlas:
  eyebrow: "Logic map"
  title: "Two control levels — vectors decide what happens, sensors decide what cameras see"
  caption: "Left column generates traffic as latents; right column reconstructs the real background. They meet in a mask-guided editor, which is the only place the two levels have to agree."
  cols: 4
  legend:
    - { accent: cyan, label: "Real capture & reconstruction" }
    - { accent: purple, label: "Vector compression" }
    - { accent: blue, label: "Traffic generation" }
    - { accent: warn, label: "Composition" }
    - { accent: green, label: "Simulator output" }
  nodes:
    - id: scene
      col: 1
      span: 4
      row: 1
      kind: input
      accent: cyan
      tag: "Input"
      title: "Driving Scene"
      desc: "Real logs, HD map, surround sensors"
      receives: "Recorded drives with map and sensor data"
      logic: "Split the same scene into a vector level and a sensor level"
      sends: "One scene into two parallel representations"
      why: "Splitting once at the source is what allows behaviour and appearance to be controlled independently and recombined later."
    - id: starae
      col: 1
      span: 2
      row: 2
      kind: process
      accent: purple
      tag: "Encode"
      title: "STAR-AE"
      desc: "Structure-aware temporal autoencoder"
      spec: "variable agents → fixed latent"
      receives: "A variable number of agents and lane elements over time"
      logic: "Assign elements to slots, then factorise attention over space and time"
      sends: "Per-slot latents"
      why: "Diffusion needs a fixed-size, continuous space. Traffic is neither — this is the component that makes the rest of the vector level possible."
      tradeoff: "Slots impose a ceiling on scene density; too few drops agents, too many wastes capacity on empty slots."
      role: "Designed and trained the latent structure."
    - id: gs
      col: 3
      span: 2
      row: 2
      kind: process
      accent: cyan
      tag: "Reconstruct"
      title: "Gaussian Splatting"
      desc: "Real background, any viewpoint"
      receives: "Real frames plus auto-labels"
      logic: "Optimise Gaussians, then render at an arbitrary pose"
      sends: "Background renders"
      why: "Reconstruction supplies the one thing generation is worst at: a background that is verifiably the real world, from a camera pose that was never actually driven."
    - id: latent
      col: 1
      span: 2
      row: 3
      kind: reason
      accent: purple
      tag: "Latent"
      title: "Structured Latent"
      desc: "Fixed size, samplable"
      receives: "Encoder posteriors"
      logic: "Reparameterise to a continuous latent"
      sends: "Continuous latent"
      why: "A smooth latent is what makes interpolation and sampling meaningful — without it, diffusion over discrete traffic has nothing to move through."
    - id: bg
      col: 3
      span: 2
      row: 3
      kind: output
      accent: cyan
      tag: "Background"
      title: "Photoreal Background"
      desc: "Free-viewpoint plates"
      receives: "Gaussian-Splatting renders"
      logic: "Render the static world at the simulated pose"
      sends: "Conditioning frames"
      why: "Perception models are unusually sensitive to background realism; a synthetic background is the fastest way to make a simulator useless for closed-loop evaluation."
    - id: stridenet
      col: 1
      span: 2
      row: 4
      kind: process
      accent: blue
      tag: "Generate"
      title: "STRIDENet"
      desc: "Conditional latent diffusion"
      receives: "A noised latent plus the observed history"
      logic: "Denoise, conditioning on history through adaptive layer norm"
      sends: "A clean future latent"
      why: "Conditioning on history rather than on a single frame is what keeps generated traffic continuous with what already happened, instead of teleporting."
      role: "Designed the conditioning scheme and trained the generator."
    - id: vtraffic
      col: 1
      span: 2
      row: 5
      kind: output
      accent: green
      tag: "Output"
      title: "Future Traffic"
      desc: "Vector trajectories"
      media: "/assets/media/projects/traffic_sensor_level_ctrl/gen_vector_vis.mp4"
      media_type: video
      receives: "Decoded latent"
      logic: "Decode back to agents and lanes"
      sends: "The what-happens layer"
      why: "Traffic stays editable as vectors right up to the moment it is rendered, which is the only level at which a scenario can actually be authored."
    - id: maskdit
      col: 1
      span: 4
      row: 6
      kind: process
      accent: warn
      core: true
      tag: "Compose"
      title: "Mask-guided DiT Editor"
      desc: "Edit the frame, don't regenerate it"
      spec: "keep · context · edge · generate"
      receives: "Generated traffic and the reconstructed background"
      logic: "Freeze the background, synthesise the foreground, resolve the seam"
      sends: "Edited latents"
      why: "Regenerating a whole frame throws away a background that was already correct; masking spends the model's capacity only where something actually changed."
      tradeoff: "Masked editing depends on the mask being right — a bad boundary shows up as a visible seam rather than a soft error."
    - id: video
      col: 1
      span: 4
      row: 7
      kind: contribution
      accent: green
      tag: "Output"
      title: "7V Surround Video"
      desc: "Closed-loop rollout"
      media: "/assets/media/projects/recon_gen_simulation/3.Pure_noise_gen.mp4"
      media_type: video
      receives: "The composed latent"
      logic: "Decode to surround frames"
      sends: "Photorealistic surround video"
      why: "This is the closing of the loop: the simulator's output is the same thing the perception stack consumes in the car."
  edges:
    - { from: scene, to: starae, kind: flow, label: "agents + lanes" }
    - { from: scene, to: gs, kind: flow, label: "frames + poses" }
    - { from: starae, to: latent, kind: flow }
    - { from: gs, to: bg, kind: flow }
    - { from: latent, to: stridenet, kind: flow, label: "history τ" }
    - { from: stridenet, to: vtraffic, kind: flow }
    - { from: vtraffic, to: maskdit, kind: flow, label: "what happens" }
    - { from: bg, to: maskdit, kind: flow, label: "what it looks like" }
    - { from: maskdit, to: video, kind: flow }
---
<div class="lawn-modules">

  <div class="tool-chips">
    <span class="chip">Structure-aware temporal VAE</span>
    <span class="chip">Conditional latent diffusion</span>
    <span class="chip">Gaussian-Splatting reconstruction</span>
    <span class="chip">Mask-guided DiT editor</span>
    <span class="chip">MagicDrive-V2 base</span>
  </div>

  <div class="stat-band">
    <div class="stat accent"><b>2 levels</b><span>Vector control · sensor control</span></div>
    <div class="stat"><b>Fixed z</b><span>Variable agents/lanes → one latent</span></div>
    <div class="stat"><b>4 masks</b><span>Keep · context · edge · generate</span></div>
    <div class="stat good"><b>Closed loop</b><span>Reconstruct → populate → re-render</span></div>
  </div>

  {% include logic-atlas.html %}

  <h2 class="lawn-h2">Temporal vector AE in motion</h2>
  <p class="module-oneliner">The VAE encodes sparse, variable scenes into a fixed latent and reconstructs them — agents and lanes stay temporally coherent.</p>
  <div class="proj-figrow three">
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/traffic_sensor_level_ctrl/temporal_AE_0.mp4' | relative_url }}" type="video/mp4"></video>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/traffic_sensor_level_ctrl/temporal_AE_1.mp4' | relative_url }}" type="video/mp4"></video>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/traffic_sensor_level_ctrl/temporal_AE_2.mp4' | relative_url }}" type="video/mp4"></video>
    </figure>
  </div>

  <h2 class="lawn-h2">Architecture, both halves</h2>
  <div class="proj-figrow two">
    <figure class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/traffic_sensor_level_ctrl/Tokenzier.jpg' | relative_url }}" alt="STAR-AE structure-aware temporal vector VAE" loading="lazy">
      <figcaption>STAR-AE — slotify variable agents/lanes, then factorize time / space / cross-domain attention into one fixed latent.</figcaption>
    </figure>
    <figure class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/traffic_sensor_level_ctrl/vector_DiT_arch.png' | relative_url }}" alt="STRIDENet conditional latent diffusion architecture" loading="lazy">
      <figcaption>STRIDENet — denoise in the standardized latent space, conditioned on history, with decode-domain physics regularization.</figcaption>
    </figure>
  </div>

  <h2 class="lawn-h2">Sensor-level closed loop</h2>
  <div class="proj-figure on-white">
    <img src="{{ '/assets/media/projects/recon_gen_simulation/arch_recon_gen.jpg' | relative_url }}" alt="WorldSim closed-loop simulation framework" loading="lazy">
    <figcaption>Three pipelines close the loop: Gaussian-Splatting <strong>reconstruction</strong> builds the real background, <strong>traffic generation</strong> populates it, and a DiT <strong>video world</strong> renders the surround result.</figcaption>
  </div>

  <h2 class="lawn-h2">Mask-guided DiT — edit, don't regenerate</h2>
  <p class="module-oneliner">Four semantic masks partition every frame so the model only computes what must change.</p>
  <div class="ablation wrap">
    <table>
      <thead><tr><th>Mask</th><th>Region</th><th>Action</th></tr></thead>
      <tbody>
        <tr><td><span class="mono">M_keep</span></td><td>Known background</td><td>Frozen — skip all compute</td></tr>
        <tr><td><span class="mono">M_ctx</span></td><td>Reference background</td><td>Cached — provide K/V only</td></tr>
        <tr><td><span class="mono">M_edge</span></td><td>Fg/bg boundary</td><td>Active — repair the seam</td></tr>
        <tr><td><span class="mono">M_gen</span></td><td>Foreground</td><td>Active — generate by condition</td></tr>
      </tbody>
    </table>
  </div>
  <div class="proj-figure on-white">
    <img src="{{ '/assets/media/projects/recon_gen_simulation/mask_DiT_MagicDriveV2.png' | relative_url }}" alt="Mask-guided DiT architecture on MagicDrive-V2" loading="lazy">
    <figcaption>Background is locked every step; foreground tokens align to BBox trajectories and read background appearance for seamless style fusion.</figcaption>
  </div>

  <h2 class="lawn-h2">Before vs after the mask-guided editor</h2>
  <div class="proj-figrow two">
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/recon_gen_simulation/gen_scene_completion_fail_case_01.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption><strong>Direct baseline.</strong> Applying the original paper as-is — scene completion breaks down.</figcaption>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/recon_gen_simulation/1.Gen_fg_bg_Diff_light.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption><strong>Mask-guided DiT.</strong> Foreground generated under different lighting, background untouched.</figcaption>
    </figure>
  </div>

  <h2 class="lawn-h2">Closed-loop results</h2>
  <div class="proj-figrow two">
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/recon_gen_simulation/2.PreciseCtrl_RainyWx.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>Precise control under a rainy-weather condition.</figcaption>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback><source src="{{ '/assets/media/projects/recon_gen_simulation/3.Pure_noise_gen.mp4' | relative_url }}" type="video/mp4"></video>
      <figcaption>Pure-noise generation — full surround scene from scratch.</figcaption>
    </figure>
  </div>

  <div class="ref-note">
    <strong>My role.</strong>
    <span>Designed the structure-aware temporal vector world model (STAR-AE + STRIDENet) and built the sensor-level closed loop on a MagicDrive-V2-based mask-guided DiT editor. Wording is high-level to protect enterprise confidentiality.</span>
  </div>

</div>
