---
title: "Vector Traffic Generation & Sensor-Level Closed-Loop Simulation"
subtitle: "Two halves of a controllable driving simulator: a structure-aware temporal vector world model that compresses and generates traffic as latents, and a sensor-level closed-loop pipeline that reconstructs, populates, and re-renders photorealistic surround video."
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
summary: "Built a two-level controllable driving simulator: a structure-aware temporal vector VAE (STAR-AE) that compresses sparse, variable agents and lanes into fixed latents, a conditional latent-diffusion generator (STRIDENet) that produces history-consistent future traffic, and a sensor-level closed-loop WorldSim that fuses Gaussian-Splatting reconstruction, traffic-flow generation, and a mask-guided DiT video editor (built on MagicDrive-V2) into photorealistic surround rollouts."
privacy_note: "Bosch (XC-CN) ongoing research. Architecture and method are presented at a portfolio level; internal data, calibration, metrics, and product details are intentionally omitted or sanitized."
atlas:
  eyebrow: "Logic map"
  title: "Two control levels — vectors decide what happens, sensors decide what cameras see"
  caption: "Left lane generates traffic as latents; right lane reconstructs photoreal background; both merge into a mask-guided video editor."
  cols: 4
  nodes:
    - id: scene
      col: 1
      span: 4
      row: 1
      kind: input
      accent: cyan
      tag: "Input"
      title: "Driving Scene"
      desc: "Sparse agents + lanes + sensors"
      receives: "Real logs, HD map, sensors"
      logic: "Split into vector + sensor levels"
      sends: "Scene to both lanes"
      gives: "One source, two simulators"
    - id: starae
      col: 1
      span: 2
      row: 2
      kind: process
      accent: purple
      tag: "VAE"
      title: "STAR-AE VAE"
      desc: "Structure-aware temporal"
      receives: "Variable agents + lanes"
      logic: "Slotify + factorized space/time attention"
      sends: "Per-slot latents"
      gives: "Variable scenes → fixed size"
    - id: gs
      col: 3
      span: 2
      row: 2
      kind: process
      accent: cyan
      tag: "Reconstruct"
      title: "Gaussian Splatting"
      desc: "3D/4D · novel views"
      receives: "Real frames + auto-labels"
      logic: "Optimize Gaussians, render at (R,t)"
      sends: "Background renders"
      gives: "Real backgrounds, any viewpoint"
    - id: latent
      col: 1
      span: 2
      row: 3
      kind: reason
      accent: purple
      tag: "Latent"
      title: "Structured Latent"
      desc: "Fixed · samplable"
      receives: "Encoder posteriors"
      logic: "Reparameterize z = μ + σε"
      sends: "Continuous latent"
      gives: "Smooth space for diffusion"
    - id: bg
      col: 3
      span: 2
      row: 3
      kind: output
      accent: cyan
      tag: "Background"
      title: "Photoreal Background"
      desc: "Any camera pose"
      receives: "GS renders"
      logic: "Free-viewpoint background"
      sends: "Conditioning frames"
      gives: "Kills simulator background fakeness"
    - id: stridenet
      col: 1
      span: 2
      row: 4
      kind: process
      accent: blue
      tag: "Diffusion"
      title: "STRIDENet"
      desc: "Conditional latent diffusion"
      receives: "Noised latent + history τ"
      logic: "Denoise; AdaLN history conditioning"
      sends: "Clean future latent"
      gives: "History-consistent, multimodal"
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
      logic: "AE.decode → agents + lanes"
      sends: "What-happens layer"
      gives: "Controllable vector traffic"
    - id: maskdit
      col: 1
      span: 4
      row: 6
      kind: process
      accent: warn
      tag: "Editor"
      title: "Mask-guided DiT"
      desc: "Edit, don't regenerate"
      receives: "Traffic + background"
      logic: "Freeze bg, generate fg, fix seams"
      sends: "Edited latents"
      gives: "Quality up, wasted compute down"
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
      receives: "Masked flow-field update"
      logic: "Decode to surround frames"
      sends: "Photoreal surround video"
      gives: "Sensor-level closed-loop sim"
  edges:
    - { from: scene, to: starae, kind: flow }
    - { from: scene, to: gs, kind: flow }
    - { from: starae, to: latent, kind: flow }
    - { from: gs, to: bg, kind: flow }
    - { from: latent, to: stridenet, kind: flow }
    - { from: stridenet, to: vtraffic, kind: flow }
    - { from: vtraffic, to: maskdit, kind: flow }
    - { from: bg, to: maskdit, kind: flow }
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
