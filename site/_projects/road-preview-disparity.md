---
title: "Road Preview: Surface-Element Segmentation"
subtitle: "Robust segmentation of small road elements — manhole covers and speed bumps — for the road-preview / 'magic-carpet' suspension feature, hardened against hard cases and quantized for TDA4 edge deployment."
description: "Robust segmentation of manhole covers and speed bumps for a road-preview suspension feature, hardened against hard cases and INT8-quantized for TDA4 edge deployment."
date_range: "2023.05–2023.11"
partners: "BYD"
role: "Perception Model Optimization Engineer"
category: "Production Project"
stage: "Deployment-oriented · near-SOP"
tags: ["production", "perception", "deployment"]
cover: "/assets/media/projects/magic-carpet/badcase_vis_waterstains.mp4"
cover_type: "video"
featured: false
order: 60
rich_body: true
summary: "Road-surface perception for a road-preview ('magic-carpet') suspension feature: segment manhole covers and speed bumps reliably in the wild, then compress and quantize the model to INT8 for TDA4 edge inference."
problem: "A preview-controlled suspension has to know about a speed bump before the wheel reaches it. The targets are small, low-contrast and easily imitated — water stains, oil marks and textureless asphalt all look like the thing you are trying to find — and the whole model has to fit an automotive edge SoC."
built: "A segmentation model targeted at safety-critical small road elements, hardened against the specific false positives that dominate in the field, then compressed and quantized to INT8 for the TDA4 toolchain."
result: "Reached the initial mass-production quality bar for the feature while running inside the TDA4 inference budget — accuracy and latency taken to release together rather than in sequence."
my_role: "Perception model optimisation engineer: model architecture and training for the small-target segmentation, and the compression and INT8 quantization path to TDA4."
privacy_note: "Only high-level model and deployment information is shown. Internal datasets, exact metrics, customer-specific calibration data, and vehicle-integration details are omitted."
---
<div class="lawn-modules">

  <!-- ===================== CHALLENGE ===================== -->
  <div class="module-head">
    <p class="eyebrow">The Challenge</p>
    <h2>Why small road-element segmentation is hard</h2>
    <p class="module-oneliner">
      The road-preview feature looks ahead and segments small surface elements so the suspension can
      pre-adjust. The targets are tiny and the visual conditions are adversarial — three failure modes
      dominate.
    </p>
  </div>

  <div class="challenge-row">
    <figure>
      <img src="{{ '/assets/media/projects/magic-carpet/seg_challenge_1_1.png' | relative_url }}" alt="Tiny road element in a full driving scene" loading="lazy">
      <figcaption>Full-scene context — the target is a small fraction of the frame.</figcaption>
    </figure>
    <figure>
      <img src="{{ '/assets/media/projects/magic-carpet/seg_challenge_1.png' | relative_url }}" alt="Close-up of a manhole cover" loading="lazy">
      <figcaption>Manhole cover — often textureless or road-colored.</figcaption>
    </figure>
    <figure>
      <img src="{{ '/assets/media/projects/magic-carpet/seg_challenge_2.png' | relative_url }}" alt="Water-stain patch on the road" loading="lazy">
      <figcaption>Water / oil stain — texture mimics a real cover.</figcaption>
    </figure>
    <figure>
      <img src="{{ '/assets/media/projects/magic-carpet/seg_challenge_3.png' | relative_url }}" alt="Low-contrast road element" loading="lazy">
      <figcaption>Low contrast — element blends into the asphalt.</figcaption>
    </figure>
  </div>

  <div class="info-table">
    <table>
      <thead>
        <tr><th>#</th><th>Challenge</th><th>Why it breaks naive models</th></tr>
      </thead>
      <tbody>
        <tr>
          <td>01</td>
          <td>Extremely small targets</td>
          <td>Manhole covers and speed bumps can occupy <strong>less than 1% of the image pixels</strong>, so the signal is easily lost to pooling and down-sampling.</td>
        </tr>
        <tr>
          <td>02</td>
          <td>Stain / texture confusion</td>
          <td>Water and oil stains on the road produce textures <strong>highly similar to a real manhole cover</strong>, driving false positives.</td>
        </tr>
        <tr>
          <td>03</td>
          <td>Textureless / color-matched</td>
          <td>Many covers are <strong>textureless or nearly the same color as the asphalt</strong>, driving missed detections.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ===================== TRAINING PIPELINE ===================== -->
  <div class="module-head" style="margin-top:2.4rem">
    <p class="eyebrow">Stage 1 · Train (FP32)</p>
    <h2>Segmentation training pipeline</h2>
    <p class="module-oneliner">
      A classic <strong>Encoder–Decoder</strong> design, tuned end-to-end for TDA4 edge deployment.
      The flow runs data → features → decoding → loss → optimization → evaluation, looped each epoch.
    </p>
    <div class="tool-chips">
      <span class="chip">RegNet backbone</span>
      <span class="chip">FPN EdgeAI-Lite decoder</span>
      <span class="chip">OHEM · Lovász · Tversky · Focal</span>
      <span class="chip">AdamW · mIoU</span>
    </div>
  </div>

  <div class="proj-figure on-white is-narrow" style="margin-top:1.1rem">
    <img src="{{ '/assets/media/projects/magic-carpet/seg_model_arch.png' | relative_url }}" alt="Segmentation training pipeline architecture" loading="lazy">
    <figcaption><strong>Training pipeline.</strong> Data loading → augmentation → RegNet backbone → FPN EdgeAI-Lite decoder → combined losses; AdamW optimizes and mIoU evaluates. The blue arcs are the per-epoch training loop. This stage produces a high-accuracy floating-point model.</figcaption>
  </div>

  <div class="sub-head"><span class="ver">Left</span><h4>Data → feature extraction</h4></div>
  <div class="info-table">
    <table>
      <thead><tr><th>Module</th><th>Role</th></tr></thead>
      <tbody>
        <tr><td>Data Loading</td><td>Reads images and their pixel-level annotation masks; supports multiple segmentation dataset formats.</td></tr>
        <tr><td>Data Augmentation</td><td>The <strong>train</strong> pipeline applies strong augmentation (random crop / flip / color jitter); the <strong>test</strong> pipeline only normalizes. The two are strictly separated to avoid data leakage.</td></tr>
        <tr><td>Backbone · RegNet</td><td>A regularized network found by design-space search — high compute efficiency and accuracy, ideal for edge deployment (low MAC, low memory). Emits multi-scale feature maps (C2–C5, ResNet-style).</td></tr>
      </tbody>
    </table>
  </div>

  <div class="sub-head"><span class="ver v2">Center</span><h4>Decoding → losses</h4></div>
  <div class="info-table">
    <table>
      <thead><tr><th>Module</th><th>Role</th></tr></thead>
      <tbody>
        <tr><td>Decoder · FPNEdgeAILiteDecoder</td><td>A lightweight FPN-based decoder built for EdgeAI (TI EdgeAI Toolbox): fuses multi-scale features, upsamples back to full resolution, and outputs a per-pixel class-probability map.</td></tr>
        <tr><td>Loss · OHEM</td><td>Online Hard Example Mining — dynamically selects high-loss hard samples for back-propagation to mitigate class imbalance.</td></tr>
        <tr><td>Loss · Lovász</td><td>A differentiable surrogate that directly optimizes IoU, aligned with the mIoU metric; outperforms pure cross-entropy on segmentation.</td></tr>
        <tr><td>Loss · Tversky</td><td>A generalization of Dice loss; α/β control the false-positive / false-negative trade-off — well suited to small and rare targets.</td></tr>
        <tr><td>Loss · Focal</td><td>Down-weights easy samples and focuses on hard pixels; effective under extreme class imbalance.</td></tr>
      </tbody>
    </table>
  </div>
  <p class="flow-note">The four losses are combined with weights so they complementarily cover the different failure modes above.</p>

  <div class="sub-head"><span class="ver">Right</span><h4>Optimization → evaluation</h4></div>
  <div class="info-table">
    <table>
      <thead><tr><th>Module</th><th>Role</th></tr></thead>
      <tbody>
        <tr><td>Optimizer · AdamW</td><td>Adam with decoupled weight decay — fast convergence and good generalization, robust for CNN/Transformer-style architectures.</td></tr>
        <tr><td>Evaluation · mIoU</td><td>Mean Intersection-over-Union — the standard segmentation metric, averaged over all classes for a fair view of long-tail performance.</td></tr>
        <tr><td>Training loop (blue arcs)</td><td>The left arc re-enters Data Loading each epoch to stream new batches; the right arc feeds evaluation back to drive hyper-parameter tuning (LR scheduler) and early stopping.</td></tr>
      </tbody>
    </table>
  </div>

  <!-- ===================== QUANTIZATION / COMPILE ===================== -->
  <div class="module-head" style="margin-top:2.4rem">
    <p class="eyebrow">Stage 2 · Quantize &amp; Compile (INT8)</p>
    <h2>From FP32 ONNX to a TDA4 TIDL binary</h2>
    <p class="module-oneliner">
      The trained floating-point model is compiled and quantized into a TDA4-runnable TIDL binary using
      TI's <strong>TIDL Model Import</strong> toolchain — three inputs feed a containerized import step.
    </p>
  </div>

  <div class="proj-figure on-white is-narrow" style="margin-top:1.1rem">
    <img src="{{ '/assets/media/projects/magic-carpet/TDA4_QAT_flow.png' | relative_url }}" alt="TDA4 TIDL model import and quantization flow" loading="lazy">
    <figcaption><strong>Quantization &amp; compile flow.</strong> Float ONNX + import config + calibration set → TIDL model-import Docker container → quantized TIDL binary. This stage compresses the model to an edge-efficient form.</figcaption>
  </div>

  <div class="sub-head"><span class="ver">Inputs</span><h4>Three inputs to the import step</h4></div>
  <div class="info-table">
    <table>
      <thead><tr><th>Input</th><th>Role</th></tr></thead>
      <tbody>
        <tr><td>float onnx</td><td>The exported FP32 ONNX model — full network structure and FP32 weights.</td></tr>
        <tr><td>model import cfg</td><td>TIDL compile config: quantization bit-width (INT8/INT16), input size, target core (MMA / C7x DSP), and operator-mapping strategy.</td></tr>
        <tr><td>calibration set</td><td>A small set of real images (~100–500) for <strong>Post-Training Quantization (PTQ)</strong> calibration — collects each layer's activation range (min/max or histogram) to set the quantization scale / zero-point.</td></tr>
      </tbody>
    </table>
  </div>

  <div class="sub-head"><span class="ver v2">Container</span><h4>Inside the model-import Docker container</h4></div>
  <p class="module-oneliner" style="margin-top:.4rem">
    <strong>Why Docker?</strong> The TIDL toolchain depends on a specific TI SDK environment; the container
    guarantees consistency and avoids dependency conflicts. The dashed arrow means the Docker image is the
    container's source — provided by TI and pulled on demand.
  </p>
  <div class="info-table">
    <table>
      <thead><tr><th>Step</th><th>What happens</th></tr></thead>
      <tbody>
        <tr><td>1 · Operator fusion</td><td>Merges <span class="mono">Conv + BN + ReLU</span> to cut memory traffic.</td></tr>
        <tr><td>2 · Quant calibration</td><td>Uses the calibration set to estimate activation distributions and derive INT8 quantization parameters.</td></tr>
        <tr><td>3 · Hardware-aware compile</td><td>Maps operators onto the TDA4 <strong>MMA</strong> (matrix accelerator) or <strong>C7x</strong> DSP; unsupported ops fall back to ARM.</td></tr>
      </tbody>
    </table>
  </div>

  <div class="sub-head"><span class="ver">Output</span><h4>TIDL Model Bin</h4></div>
  <div class="info-table">
    <table>
      <thead><tr><th>Property</th><th>Detail</th></tr></thead>
      <tbody>
        <tr><td>Contents</td><td>INT8 quantized weights, network topology, and hardware scheduling info.</td></tr>
        <tr><td>Runtime</td><td>Loaded and executed directly by the TDA4 <strong>TIDL Runtime</strong>.</td></tr>
        <tr><td>Efficiency</td><td>About <strong>4× smaller</strong> than the FP32 ONNX, with much faster inference and significantly lower power.</td></tr>
      </tbody>
    </table>
  </div>

  <!-- ===================== TRAIN → QUANTIZE → DEPLOY LOOP ===================== -->
  <div class="module-head" style="margin-top:2.4rem">
    <p class="eyebrow">The full loop</p>
    <h2>Train → Quantize → Deploy</h2>
    <p class="module-oneliner">
      Stage 1 produces a high-accuracy FP32 model; Stage 2 compresses it into an edge-efficient quantized
      binary. Together they form a complete closed loop from training to on-vehicle inference.
    </p>
  </div>

  <div class="pipeline-loop">
    <div class="stage">
      <span class="step-tag">Train</span>
      <span class="k">seg_model_arch</span>
      <span class="v">FP32 segmentation training — RegNet + FPN decoder, combined losses, mIoU.</span>
    </div>
    <div class="arrow" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
    </div>
    <div class="stage">
      <span class="step-tag">Quantize</span>
      <span class="k">TDA4 QAT flow</span>
      <span class="v">Export ONNX → PTQ INT8 import &amp; compile → TIDL binary (~4× smaller).</span>
    </div>
    <div class="arrow" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
    </div>
    <div class="stage">
      <span class="step-tag">Deploy</span>
      <span class="k">TDA4 on-board</span>
      <span class="v">TIDL Runtime inference on the vehicle — efficient, low-power edge execution.</span>
    </div>
  </div>

  <!-- ===================== EVALUATION ===================== -->
  <div class="module-head" style="margin-top:2.4rem">
    <p class="eyebrow">Evaluation</p>
    <h2>Quantized model on bad cases</h2>
    <p class="module-oneliner">
      Per-scene evaluation of the quantized model on representative hard cases — water stains, far-range
      targets, and complex multi-bump / night scenes.
    </p>
  </div>

  <div class="proj-figstack">
    <figure class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/magic-carpet/Example_indicator1.png' | relative_url }}" alt="Water-stain bad-case evaluation" loading="lazy">
      <figcaption><strong>Water-stain scene.</strong> Evaluation on a water-stain bad case — the prime source of false positives.</figcaption>
    </figure>
    <figure class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/magic-carpet/Example_indicator2.png' | relative_url }}" alt="Far-range target evaluation" loading="lazy">
      <figcaption><strong>Far-range targets.</strong> Evaluation on distant, small targets — the prime source of missed detections.</figcaption>
    </figure>
    <figure class="proj-figure on-white">
      <img src="{{ '/assets/media/projects/magic-carpet/Example_indicator3.png' | relative_url }}" alt="Multi-bump and night-scene evaluation" loading="lazy">
      <figcaption><strong>Complex scenes.</strong> Evaluation on multi-speed-bump and night scenes — combined difficulty.</figcaption>
    </figure>
  </div>

  <div class="eval-note">
    Across both hard and easy scenes, the quantized model reaches an <strong>initial mass-production quality bar</strong>.
  </div>

  <!-- ===================== VISUALIZATIONS ===================== -->
  <div class="module-head" style="margin-top:2.4rem">
    <p class="eyebrow">Visualizations</p>
    <h2>On-road inference replays</h2>
    <p class="module-oneliner">Selected replay clips — all play automatically and loop.</p>
  </div>

  <div class="proj-figrow two">
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback>
        <source src="{{ '/assets/media/projects/magic-carpet/pred_4.7.17_vis.mp4' | relative_url }}" type="video/mp4">
      </video>
      <figcaption><strong>Hard-failure replay.</strong> Re-injection test on complex failure scenes — resolving most false and missed detections.</figcaption>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback>
        <source src="{{ '/assets/media/projects/magic-carpet/pred_1280_case.mp4' | relative_url }}" type="video/mp4">
      </video>
      <figcaption><strong>High-resolution stress test.</strong> Generalization under large 1280-input signals on complex, difficult scenes.</figcaption>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback>
        <source src="{{ '/assets/media/projects/magic-carpet/vis_seg2.mp4' | relative_url }}" type="video/mp4">
      </video>
      <figcaption><strong>Joint post-processing.</strong> Combined post-processing that also outputs the target's elevation / height information.</figcaption>
    </figure>
    <figure class="proj-figure">
      <video autoplay muted loop playsinline preload="metadata" disablepictureinpicture disableremoteplayback>
        <source src="{{ '/assets/media/projects/magic-carpet/badcase_vis_waterstains.mp4' | relative_url }}" type="video/mp4">
      </video>
      <figcaption><strong>Night &amp; garage generalization.</strong> Generalization test on night and underground-garage scenes with heavy water stains.</figcaption>
    </figure>
  </div>

</div>
