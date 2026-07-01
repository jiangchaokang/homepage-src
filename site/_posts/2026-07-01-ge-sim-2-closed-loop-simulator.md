---
layout: default
title: "GE-Sim 2.0: a closed-loop video world simulator for manipulation"
description: "A talk on AgiBot Genie's GE-Sim 2.0 — turning a video generator into an environment robots can actually train and test in, via a state expert, a VLM world judge, and pixel-aligned action conditioning."
date: 2026-07-01
hide_news: true
tags: ["world-model", "robotics", "talk"]
category: world-models
talk: true
duration: "12:52"
slides: 11
cover: "/assets/media/blog/GE_Sim/poster.jpg"
video: "/assets/media/blog/GE_Sim/GE-Sim.mp4"
poster: "/assets/media/blog/GE_Sim/poster.jpg"
takeaways:
  - "Body-state expert — reads joint angles and gripper state straight out of the video latent space."
  - "World judge — a VLM that automatically scores task success as reward."
  - "Pixel-aligned action conditioning — draws end-effector trajectories into the image for cross-robot control."
  - "Together they form a policy-act → world-sim → reward-score flywheel, so policies are evaluated and improved at scale before touching real hardware."
---
{% include talk-post.html %}
