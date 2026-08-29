---
layout: default
title: "One-step generative models: the MeanFlow line, paper by paper"
description: "A four-paper walkthrough of He Kaiming's group compressing diffusion's hundreds of steps down to one — MeanFlow, improved iMF, drift-based modeling, and FID-as-a-loss."
date: 2026-06-28
hide_news: true
tags: ["generative", "talk"]
category: generative-models
talk: true
duration: "20:54"
slides: 15
cover: "/assets/media/blog/one_steps_gen_model/poster.jpg"
bilibili: "BV19gTq61EBV"
poster: "/assets/media/blog/one_steps_gen_model/poster.jpg"
takeaways:
  - "MeanFlow — an average-velocity field plus an identity and a JVP turn many-step sampling into a single step (FID 3.43)."
  - "iMF fixes the target bias of MeanFlow and pushes quality much further (FID 1.72)."
  - "Drift-based generation drops the ODE and trades inference iterations for training iterations (FID 1.54)."
  - "FD-Loss trains FID itself as the objective, closing the loop between metric and loss (FID 0.72)."
---
{% include talk-post.html %}
