# AGENTS.md — Build and Maintenance Guide

## Project Type

This is a static Jekyll site deployed through GitHub Pages.

The site is intentionally lightweight:

- No Node.js build step for content (one optional zero-dependency Node
  *post-build* step encrypts protected project pages — see "Protected projects").
- No remote fonts.
- No required CDN.
- No required third-party runtime JavaScript (the passcode gate uses the
  browser-native Web Crypto API only).
- One global CSS file.
- One global JS file.
- Data-driven publications and news.
- One markdown file per project.

## Commands

The Jekyll source lives in `site/`. Run all commands from there.

Install dependencies:

```bash
cd site && bundle install
```

Run locally:

```bash
cd site && bundle exec jekyll serve --host 127.0.0.1 --port 4000 --incremental
```

Build:

```bash
cd site && bundle exec jekyll build --trace
```

Clean regenerable artifacts and junk (run from repo root):

```bash
bash site/tools/clean.sh
```

## Deployment

Pushing to `main` triggers `.github/workflows/pages.yml`, which builds `site/`
and publishes it. One-time repo setting: **Settings → Pages → Source: "GitHub Actions"**.

## Content Rules

### Publications

Edit:

```text
_data/publications.yml
```

Media should be placed in:

```text
assets/media/papers/
```

Do not add unverified links.

### News

Edit:

```text
_data/news.yml
```

Use reverse chronological order manually.

### Projects

Each project is one markdown file under:

```text
_projects/
```

Project media should be placed under:

```text
assets/media/projects/
```

Company-sensitive content must remain high-level and sanitized.

### Protected projects (passcode-encrypted)

A project can be gated behind a passcode by adding `protected: true` to its front
matter. The listing, nav and search still show the sanitized title/cover/summary,
but the full detail page is **encrypted at build time** and only decrypts in the
browser with the correct passcode.

How it works:

- `protected: true` makes `_layouts/default.html` emit `<meta name="x-protected">`
  plus `<meta name="robots" content="noindex,nofollow">`.
- After `jekyll build`, run the post-build encryptor (CI does this automatically):

  ```bash
  cd site && node tools/encrypt-projects.js
  ```

  It finds every page carrying that meta tag and replaces the whole file with a
  self-contained lock page: AES-256-GCM ciphertext + a passcode form. On the
  correct passcode the browser (Web Crypto: PBKDF2-SHA256 → AES-GCM) decrypts and
  re-renders the original page. Zero dependencies, zero third-party runtime JS.

- The passcode comes from `SITE_PROTECT_PASSWORD` (defaults to `5896`). In CI set
  it as the `SITE_PROTECT_PASSWORD` Actions secret.

Security reality: the ciphertext is public, so a short numeric passcode can be
brute-forced offline. This stops crawlers and casual/accidental access — it is
**not** protection against a determined attacker. For genuinely sensitive material
use a long random passphrase, or do not publish the page at all. Never commit the
plaintext `_site/` output of a protected page.

### Blog

Blog posts live in:

```text
_posts/
```

Use filename format:

```text
YYYY-MM-DD-title.md
```

Most new posts are the **"talk" format**: one recorded video walkthrough per
post, embedded from Bilibili. That format is fully templated — **follow
`TALK_POST_GUIDE.md`** (repo root of `site/`) to add one; it has the complete
front-matter schema, a copy-paste template, and a ready-to-use AI prompt.
Don't hand-roll a new talk post's HTML — `_includes/talk-post.html` already
renders every field.

A different, free-form "note" layout (rich custom HTML, no single video) is
used for text/diagram reading notes — see e.g.
`_posts/2026-06-26-from-3dgrut-to-artifixer3d.md` for that pattern. There is
no template for it; it is intentionally bespoke per post.

Videos in general: prefer uploading to Bilibili and embedding (per
`TALK_POST_GUIDE.md`) over committing new local `.mp4` files — this repo has
already paid the cost of a bloated media history once. If a local `.mp4` is
unavoidable, keep it as small as reasonably possible and confirm it is
actually referenced somewhere before committing (an unreferenced file under
`assets/media/` is pure waste — nothing automatically checks for this, so it
is worth a quick `grep` for the filename before and after any content rework).

## Design Rules

Follow `DESIGN.md`.

Use local assets. Do not introduce external CSS/JS/CDN dependencies unless explicitly required and locally vendored.

## Quality Checklist

Before publishing:

- Run `cd site && bundle exec jekyll build --trace`.
- Run `cd site && python3 tools/check-css.py`.
- Open Home, Publications, Projects, Blog, Contact.
- Check mobile layout.
- Check all media paths.
- Check external paper links.
- Confirm enterprise descriptions are sanitized.

### Why the CSS check matters

Jekyll copies `assets/css/main.css` verbatim and never parses it. A single
unclosed brace therefore produces a **completely clean build** and a **destroyed
site**: browsers discard every rule after the parse error, so the page silently
loses hundreds of rules and the layout collapses. This has happened once, from an
in-place string edit that ate a closing brace. `tools/check-css.py` catches
unbalanced braces and declarations missing a semicolon before the next rule.
Always run it after editing CSS — the build passing tells you nothing.
