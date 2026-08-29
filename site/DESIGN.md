# DESIGN.md — Jiang Chaokang Personal Brand System

## 1. Visual Theme & Atmosphere

The site is an academic + engineering personal brand system for a world-models and 3D/4D autonomous-driving researcher-engineer.

The visual language should feel:

- Precise, credible, and research-grade.
- Engineering-forward, not decorative.
- Calm, minimal, structured, and fast.
- Motion-rich only where it improves comprehension.
- Suitable for publications, production projects, long-term notes, and invited talks.

Primary references:

- Vercel / Linear: precision, monochrome surfaces, sharp hierarchy.
- Apple / IBM Carbon: trust, whitespace, system clarity.
- Anime.js: smooth micro-interactions, scroll reveal, timeline-like motion.
- Automotive design language: dark premium cards, technical badges, controlled contrast.

Do not make the site look like a generic student homepage.

## 2. Color Palette & Roles

Core colors:

- Ink: `#101114`
- Muted ink: `#5F6570`
- Soft ink: `#8A9099`
- Page background: `#F7F7F3`
- Surface: `#FFFFFF`
- Surface soft: `#F1F2EE`
- Hairline: `#E3E3DC`
- Primary accent: `#2457FF`
- Cyan accent: `#00A7B5`
- Green accent: `#16A05D`
- Purple accent: `#7657FF`
- Warning accent: `#E8A000`

Dark mode:

- Background: `#08090B`
- Surface: `#111319`
- Surface soft: `#171A22`
- Ink: `#F3F5F7`
- Muted ink: `#AAB0BA`
- Hairline: `#292D36`

Use accent colors for semantic badges, publication venues, links, and state, not for large decorative areas.

## 3. Typography Rules

Use system fonts only for performance and offline robustness.

Font stack:

```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

Hierarchy:

| Role | Size | Weight | Notes |
|---|---:|---:|---|
| Hero title | clamp(48px, 8vw, 104px) | 760 | Tight tracking |
| Page title | clamp(38px, 6vw, 76px) | 740 | Strong but readable |
| Section title | 28px–42px | 700 | Clear structure |
| Card title | 20px–28px | 700 | Compact |
| Body | 16px–18px | 400 | Comfortable reading |
| Metadata | 12px–14px | 650 | Uppercase optional |
| Badge | 11px–13px | 720 | Letter spaced |

## 4. Components

### Navigation

- Sticky top header.
- Translucent blur surface.
- Compact brand on the left.
- Page links on the right.
- Mobile collapses into a panel.

### Cards

- Rounded corners.
- One-pixel hairline border.
- Subtle shadow.
- Spotlight hover using radial gradient.
- Media left, text right for publications/projects.
- Stack vertically on mobile.

### Publication Cards

Each publication should include:

- Media preview.
- Venue badge.
- Year.
- Status.
- Title.
- Authors.
- Conservative institution / collaboration tags.
- One-sentence summary.
- One-sentence contribution.
- Links: PDF, arXiv, DOI, Code, Project Page, BibTeX when available.

### Project Cards

Each project should include:

- Production / Research / POC / Internal R&D tag.
- Timeline.
- Partner or company context.
- Role.
- Sanitized summary.
- Main contributions.
- Media gallery.
- Confidentiality note when needed.

### News Rail

- Collapsible side rail.
- Shows latest 6–8 news items.
- Sticky on desktop.
- Becomes normal section on mobile.

## 5. Layout Principles

- Max content width: 1280px.
- Main grid: content + news rail.
- Prefer two-column layouts for high-level cards.
- Avoid dense walls of text on the home page.
- Home page is for positioning, highlights, and navigation.
- Detailed content belongs to Publications, Projects, Blog, and Contact (which also covers academic service).

## 6. Motion Principles

Use motion to clarify hierarchy:

- Scroll reveal for major sections.
- Slight lift on card hover.
- Spotlight card gradient on pointer movement.
- Filter transitions for publications/projects.
- Media hover should feel responsive but not distracting.

Respect `prefers-reduced-motion`.

Avoid:

- Infinite large animations that distract reading.
- Heavy canvas or WebGL in v1.
- Remote animation libraries unless locally vendored.

## 7. Do's and Don'ts

Do:

- Keep enterprise projects sanitized.
- Prefer local assets.
- Prefer data-driven content.
- Keep pages fast and readable.
- Use precise, verifiable wording.

Don't:

- Overuse gradients.
- Add fake metrics.
- Use remote icons as required assets.
- Expose confidential company details.
- Make every project look equally important.

## 8. Responsive Behavior

Breakpoints:

- Desktop: 1100px+
- Tablet: 720px–1099px
- Mobile: below 720px

Rules:

- Two-column cards collapse into one column.
- News rail moves below content.
- Touch targets at least 44px.
- Media remains visible but does not dominate on mobile.

## 9. Agent Prompt Guide

When adding a new publication:

> Add a publication card using the existing publication schema. Keep the summary to one sentence and the contribution to one sentence. Use only verified links. If a link is unknown, omit it.

When adding a new project:

> Add one project markdown file in `_projects`. Keep company-sensitive details high-level and sanitized. Use local media only. Add timeline, role, category, tags, summary, contributions, and gallery.

When adding animation:

> Use CSS or local JS first. Respect reduced motion. Do not add external CDN dependencies.
