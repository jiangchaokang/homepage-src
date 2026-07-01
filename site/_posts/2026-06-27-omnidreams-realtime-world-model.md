---
layout: default
title: "OmniDreams: a real-time generative world model for driving"
description: "A talk walkthrough of NVIDIA's OmniDreams — a causal autoregressive DiT world model that closes the loop between policy and simulation, with three-stage training to kill error accumulation."
date: 2026-06-27
hide_news: true
tags: ["world-model", "talk"]
category: world-models
talk: true
duration: "18:29"
slides: 18
cover: "/assets/media/blog/OmniDreams/poster.jpg"
video: "/assets/media/blog/OmniDreams/OmniDreams.mp4"
poster: "/assets/media/blog/OmniDreams/poster.jpg"
takeaways:
  - "Closed-loop core: the policy outputs actions, the world model renders the matching frames, and those frames feed back to the policy — round after round."
  - "Causal autoregressive DiT with a KV cache makes generation real-time instead of re-denoising from scratch each step."
  - "Three-stage training (diffusion forcing → self-forcing → DMD distillation) suppresses the error accumulation that breaks long rollouts."
  - "Supports scene editing and out-of-distribution object insertion, and reliably replaces reconstruction-based simulators for policy evaluation."
---
{% include talk-post.html %}
