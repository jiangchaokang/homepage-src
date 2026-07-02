# TALK_POST_GUIDE.md — adding a new "one Blog = one video" post

## 0. Why this file exists

Most new Blog entries from now on are one recorded talk built around one
video. That is a narrow, repeatable shape — which means it should be a
**fill-in-the-blanks operation**, not a from-scratch design/engineering task
every time. This file is that fill-in-the-blanks form.

Design principle: **content and mechanics are separated.** You (or an AI
assistant) only ever supply the *content* — title, description, takeaways,
the Bilibili link, a poster image, a category. The *mechanics* — HTML
structure, CSS, responsive layout, the click-to-play embed, dark/light theme,
accessibility — already live in `_includes/talk-post.html` and
`assets/css/main.css` and never need to change per post. Follow this guide
and every new talk post automatically looks, behaves, and performs exactly
like the existing ones.

**If you don't have a video** (a text/diagram "reading note" post instead,
like `_posts/2026-06-26-from-3dgrut-to-artifixer3d.md`), this guide does not
apply — that is a different, free-form post layout. This guide is
specifically for the video-driven "talk" format.

---

## 1. TL;DR — the fastest path

1. Upload the video to Bilibili (outside this repo).
2. Copy the share link, e.g. `https://www.bilibili.com/video/BV1dKTq6EEnP/`.
3. Grab one clean screenshot from the video (title slide or a key diagram
   works best) and save it as `assets/media/blog/<slug>/poster.jpg`.
4. Copy the template in [§4](#4-the-canonical-template) to
   `_posts/YYYY-MM-DD-<slug>.md` and fill in the blanks.
5. Run `bundle exec jekyll build --trace` from `site/` to confirm it builds.
6. Commit and push — `.github/workflows/pages.yml` builds and deploys.

Or — even faster — skip straight to [§9](#9-ready-to-paste-ai-prompt) and
hand an AI assistant this file, the video's Bilibili link, and a poster
screenshot.

---

## 2. Mental model: how a talk post actually renders

```
_posts/YYYY-MM-DD-slug.md  (front matter)
        │
        │  layout: default, then {% include talk-post.html %}
        ▼
_includes/talk-post.html   (fixed structure, reads front matter fields)
        │
        ▼
assets/css/main.css  (.talk-* classes)     assets/js/main.js  (click-to-load)
```

`talk-post.html` picks **one of three video sources**, in this priority
order, so the same template works whether or not a Bilibili id exists yet:

| Priority | Front matter | What renders | When to use |
|---|---|---|---|
| 1 | `bilibili: "BVxxxxxxxxxx"` | Poster image + play button ("facade"). Clicking swaps in the real Bilibili `<iframe>` player. | **Default — always prefer this.** |
| 2 | `video: "/assets/media/...mp4"` | A native `<video controls>` player, local file. | Only if the video is not on Bilibili yet (temporary; costs repo size). |
| 3 | neither | Static poster image labelled "Video coming soon". Never a play button that leads nowhere. | Placeholder while a video is being prepared. |

Why the facade (poster + play button) instead of just embedding the iframe
directly: an `<iframe>` for a third-party player loads that third party's
JS/cookies/network requests **the instant the page loads**, for every
visitor, whether or not they ever watch the video. The facade defers all of
that until the visitor actually clicks play — faster page loads, no
unnecessary third-party requests, and it matches this repo's existing rule
of "no required third-party runtime JS" (`AGENTS.md`). It degrades
gracefully too: the facade is a real `<a href="https://www.bilibili.com/...">`
link, so clicking it still takes you to the video even with JavaScript
disabled.

---

## 3. Before you start: three things to have ready

1. **The Bilibili BV id.** Take it from the video's URL:
   `https://www.bilibili.com/video/`**`BV1dKTq6EEnP`**`/?spm_id_from=...`
   → you want exactly `BV1dKTq6EEnP` (drop everything from the `?` on,
   and don't paste a `i0/i1/i2.hdslb.com/.../*.jpg` cover-image URL by
   mistake — that is an image link, not a video link; if that's all you
   have, use it as `poster:` and leave `bilibili:` out for now — see the
   `one_steps_gen_model` post for a worked example of this exact fallback).

2. **A poster image**, ~1280×720 (16:9), JPG, ideally a real frame from the
   video — a title slide or a key diagram reads best as a static thumbnail.
   Take a screenshot (Snipaste, macOS `Cmd+Shift+4`, or pause the Bilibili
   player and screenshot it) and save it as
   `assets/media/blog/<slug>/poster.jpg`. Keep it under ~200KB
   (`.jpg`, quality ~85 is plenty — these are thumbnails, not the video).

3. **A category slug** from `_data/blog_categories.yml` (or a new one — see
   [§7](#7-categories)):

   | slug | label | used for |
   |---|---|---|
   | `world-models` | World Models | world/video models, simulators |
   | `embodied-ai` | Embodied AI | robots, VLA, manipulation |
   | `autonomous-driving` | Autonomous Driving | AD stacks, planning, control |
   | `scene-reconstruction` | Scene Reconstruction | 3D/4D reconstruction, NeRF/GS |
   | `generative-models` | Generative Models | diffusion, flow, image/video gen |
   | `ai-tools` | AI Tools | agents, LLM engineering, tooling |

---

## 4. The canonical template

Create `_posts/YYYY-MM-DD-<slug>.md` (Jekyll requires this exact
`YYYY-MM-DD-` filename prefix — see [§8](#8-filenames--dates)) with:

```markdown
---
layout: default
title: "<Talk title — plain, specific, no clickbait>"
description: "<One or two sentences: what the talk covers and why it matters. This is also the meta/OG/Twitter description, so keep it under ~200 characters and make it stand on its own.>"
date: YYYY-MM-DD
hide_news: true
tags: ["<free-text keyword>", "<free-text keyword>", "talk"]
category: <one slug from the table in §3 — no quotes needed>
talk: true
duration: "MM:SS"
slides: <number, omit the whole line if the talk is not slide-based>
cover: "/assets/media/blog/<slug>/poster.jpg"
bilibili: "BVxxxxxxxxxx"
poster: "/assets/media/blog/<slug>/poster.jpg"
takeaways:
  - "<One-sentence takeaway #1 — the single most important idea.>"
  - "<One-sentence takeaway #2.>"
  - "<One-sentence takeaway #3.>"
  - "<One-sentence takeaway #4 — optional, 3-6 total reads best.>"
---
{% include talk-post.html %}
```

That's the whole file — the last line is not a placeholder, it is the
literal, complete body. All rendering happens inside `talk-post.html`.

### Field reference

| Field | Required | Notes |
|---|---|---|
| `layout` | yes | Always `default`. |
| `title` | yes | Plain-language, specific. Shown as the page `<h1>` and in `<title>`, nav dropdown, search, and the blog grid. |
| `description` | yes | 1-2 sentences. Falls back to being the on-page byline too (unless `byline` is set — rare, see below). Also becomes `<meta name="description">`, `og:description`, `twitter:description` — this is the copy people see when the link is shared, so make it self-contained. |
| `date` | yes | `YYYY-MM-DD`. Controls sort order and the permalink. Future dates are fine — `future: true` is set in `_config.yml`, so nothing is held back. |
| `hide_news` | yes | Always `true` for posts — keeps the news rail off talk pages (matches every existing post). |
| `tags` | yes | Free-text keywords for the **search index** only (`search.json`) — not shown as UI badges. Always include `"talk"` as one of them by convention, so a future full-text search for "talk" surfaces every talk post. |
| `category` | yes | Must exactly match a `slug` in `_data/blog_categories.yml` (§3). Drives the filter buttons on `/blog/` and the accent color of the card. This is **not** the same thing as `tags` — don't confuse the two. |
| `talk` | yes | Always `true`. Flags the post as a "Talk" (vs a written "Note") in the blog grid — shows the play-icon overlay and `Talk` badge, and switches the layout include. |
| `duration` | yes | `"MM:SS"` string, shown as a chip. This is metadata about the talk's length — keep it accurate even for the Bilibili-embed path, since the visitor sees it before pressing play. |
| `slides` | no | Integer. Omit the line entirely if the talk has no slide deck. |
| `cover` | yes | Used by the **blog listing grid** (`/blog/`) and nav dropdown thumbnails. Always a **local** file path — never hotlink here, this image loads on every visit to `/blog/`. |
| `bilibili` | recommended | The bare `BVxxxxxxxxxx` id, no URL wrapper, no query string. See [§2](#2-mental-model-how-a-talk-post-actually-renders) for what happens if omitted. |
| `bilibili_page` | no | Only for a multi-part Bilibili upload (a "collection" with parts 1/2/3...). Integer part number. Omit for a normal single-part video. |
| `poster` | yes | The big hero image on the **talk's own page** (`.talk-stage`). Usually the same local file as `cover`. May be a remote URL as a documented fallback (see the `one_steps_gen_model` post) — if so, also set `poster_fallback` to a local file. |
| `poster_fallback` | no | Local path used as an `onerror` fallback if `poster` is a remote URL that fails to load. Only needed when `poster` is remote. |
| `video` | no | Legacy/local-file fallback — see the priority table in §2. Prefer `bilibili` instead; only use this for a talk that genuinely isn't uploaded to Bilibili yet. |
| `takeaways` | yes | 3-6 bullet strings, one full sentence each. Rendered as the "What the talk covers" list below the video. This is usually the highest-value content on the page — write it like you are briefing a colleague who has 30 seconds, not a summary of every slide. |
| `eyebrow` | no | Overrides the small label above the title (defaults to `"Video walkthrough · Talk"`). Not used by any existing post — leave it out unless you have a specific reason. |
| `byline` | no | Overrides the on-page subtitle (defaults to reusing `description`). Not used by any existing post — leave it out unless `description` alone can't do both jobs (meta tag *and* on-page byline). |

---

## 5. Poster image guidance

- **Format:** JPG, ~1280×720 (16:9 — matches `.talk-stage`'s fixed aspect
  ratio; other ratios still work because the image is cropped with
  `object-fit: cover`, but 16:9 crops the least).
- **Content:** a frame that reads well as a still — a title slide, a clean
  diagram, or a strong visual moment. Avoid a random mid-motion frame
  (motion blur, a half-finished camera pan, a transition).
  All five existing talk posts use a manually chosen screenshot for exactly
  this reason — it looks noticeably more intentional than an auto-picked
  frame.
- **Size:** keep it under ~200KB. These posters are downloaded on the blog
  grid, the nav dropdown, and the post page — they should be light.
- **Location:** `assets/media/blog/<slug>/poster.jpg`, one folder per post,
  matching every existing post's layout.

---

## 6. Writing good takeaways

`takeaways` is the part of the page most likely to actually be read.
Guidelines, taken from the five existing posts:

- One sentence each. No sub-clauses stacked with semicolons.
- Lead with the mechanism or the number, not a vague claim — "Causal
  autoregressive DiT with a KV cache makes generation real-time" beats
  "The model is very fast."
- Order them the way the talk actually unfolds, ending on the takeaway that
  matters most (often a result, a comparison, or an implication).
- 3-6 items. Fewer than 3 feels thin; more than 6 stops being a summary.

---

## 7. Categories

If none of the six existing categories in
[§3](#3-before-you-start-three-things-to-have-ready) fit, add a new one to
`_data/blog_categories.yml`:

```yaml
- slug: your-new-slug
  label: Human-Readable Label
  accent: cyan   # one of: cyan, green, accent, warn, purple (reuse an existing accent — don't invent a new color)
```

Don't add a new category for a single one-off post — reuse the closest
existing one. Categories exist to make the `/blog/` filter bar useful; too
many thin categories defeats that.

---

## 8. Filenames & dates

- File: `_posts/YYYY-MM-DD-<slug>.md`. Jekyll **requires** this exact
  date-prefixed pattern to recognize a post at all — a file without it is
  silently ignored.
- `<slug>` becomes part of the URL
  (`/blog/YYYY/MM/DD/<slug>/` per the `permalink` in `_config.yml`) — keep
  it short, lowercase, hyphenated, matching the front matter `title` in
  spirit (e.g. title "OmniDreams: a real-time generative world model for
  driving" → filename slug `omnidreams-realtime-world-model`).
- The media folder name doesn't have to match the post filename slug exactly
  (existing posts mix conventions, e.g. `GE_Sim/` for
  `ge-sim-2-closed-loop-simulator.md`) — but keep it short and recognizable.
- `date:` can be anything, including "future" dates relative to today —
  `future: true` in `_config.yml` means every post always builds and
  publishes immediately, regardless of its `date:` value. Date only controls
  sort order and the permalink.

---

## 9. Ready-to-paste AI prompt

Copy this, fill in the bracketed parts, attach the poster screenshot, and
send it together with this file to an AI assistant working in this repo:

```text
Follow site/TALK_POST_GUIDE.md exactly to add one new "talk" blog post.

- Title: <TITLE>
- Bilibili link: <PASTE THE FULL https://www.bilibili.com/video/BV.../ LINK HERE>
- Description (1-2 sentences, also used as the meta description): <DESCRIPTION>
- Category: <pick one slug from _data/blog_categories.yml, or tell me to propose a new one>
- Duration: <MM:SS>
- Slides: <N, or "none">
- Takeaways (3-6, one sentence each):
  1. <...>
  2. <...>
  3. <...>
- Poster: <attached screenshot — save it as the post's poster.jpg> (or: "use the Bilibili auto-cover instead, no screenshot available")
- Date: <YYYY-MM-DD, or "today">

Create the _posts/ file and the media folder, wire up every front-matter
field per the guide, then run `bundle exec jekyll build --trace` from site/
to confirm it builds clean before you're done.
```

An AI assistant with repo access can execute this end to end: extract the BV
id, place the poster, create the dated post file from the template in §4,
and verify the build — no manual HTML/CSS work required, because none of
that changes per post.

---

## 10. Worked example

This is the actual front matter used for the `ad_arch` post — copy its shape
directly:

```markdown
---
layout: default
title: "Full-stack autonomous driving: from sensors to control"
description: "A talk through a complete AD stack — dual-brain domain control, multi-view + LiDAR perception, BEV and occupancy, online mapping, tracking, planning, control, parking, and the data flywheel."
date: 2026-06-29
hide_news: true
tags: ["autonomous-driving", "talk"]
category: autonomous-driving
talk: true
duration: "27:39"
slides: 20
cover: "/assets/media/blog/ad_arch/poster.jpg"
bilibili: "BV1dKTq6EEnP"
poster: "/assets/media/blog/ad_arch/poster.jpg"
takeaways:
  - "Dual-brain domain control: an AI compute domain (APU) paired with a safety execution domain (RPU)."
  - "Perception: multi-view cameras and LiDAR, BEV transformation, occupancy networks, and online vectorized mapping."
  - "Decision: multi-object tracking fusion, high-precision localization, behavior prediction, motion planning, control, and parking."
  - "A data-closed-loop flywheel, with an outlook from modular pipelines toward end-to-end and VLA / world-model architectures."
---
{% include talk-post.html %}
```

---

## 11. Troubleshooting

- **Post doesn't show up on `/blog/` at all.** Filename doesn't match
  `YYYY-MM-DD-slug.md`, or it's missing the leading `---` front matter
  fences, or `date:` is malformed.
- **Play button click does nothing.** `bilibili:` value includes a stray
  `?spm_id_from=...` query string, a leading/trailing slash mismatch, or
  quotes were dropped — it must be the bare id, e.g. `"BV1dKTq6EEnP"`.
- **Filter buttons on `/blog/` never show the new post.** `category:` does
  not exactly match a `slug` in `_data/blog_categories.yml` (case-sensitive,
  no quotes needed on the value but the text must match exactly).
- **Poster image looks stretched or oddly cropped.** Source image isn't
  close to 16:9 — re-crop nearer to 1280×720.
- **Link preview (iMessage/Slack/X) shows the wrong text.** That's the
  `description` field — it drives `og:description`/`twitter:description`.
- **Always finish with:** `cd site && bundle exec jekyll build --trace` — a
  clean build with no `Liquid Exception` / `Error:` lines means the front
  matter is well-formed.
