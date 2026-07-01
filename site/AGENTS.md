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

Blog posts live in:

```text
_posts/
```

Use filename format:

```text
YYYY-MM-DD-title.md
```

## Design Rules

Follow `DESIGN.md`.

Use local assets. Do not introduce external CSS/JS/CDN dependencies unless explicitly required and locally vendored.

## Quality Checklist

Before publishing:

- Run `cd site && bundle exec jekyll build --trace`.
- Open Home, Publications, Projects, Blog, Contact.
- Check mobile layout.
- Check all media paths.
- Check external paper links.
- Confirm enterprise descriptions are sanitized.
