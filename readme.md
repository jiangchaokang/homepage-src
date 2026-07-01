# Jiang Chaokang — Personal Website

A lightweight, fast **academic + engineering** personal brand site, focused on world
models, generative autonomous driving, and 3D/4D perception. Fully static, built with
[Jekyll](https://jekyllrb.com/) and served by GitHub Pages. The stack is deliberately
minimal: one global CSS file, one global JS file, data-driven publications and news, and
one Markdown file per project.

## Repository layout

The repo root is intentionally clean — only this README and `.gitignore`. Everything
else lives in folders:

```text
.
├── readme.md            ← you are here
├── .gitignore
├── site/                ← the entire Jekyll site (source)
│   ├── _config.yml      site config: author, nav, collections
│   ├── index.html · blog.html · projects.html · publications.html · contact.html · news.html
│   ├── _data/           publications.yml · news.yml · blog_categories.yml
│   ├── _posts/          blog posts (YYYY-MM-DD-title.md)
│   ├── _projects/       one Markdown file per project
│   ├── _includes/ · _layouts/
│   ├── assets/          css/main.css · js/main.js · media/ · img/
│   ├── AGENTS.md · DESIGN.md   maintenance & design guides
│   └── tools/           clean.sh · convert_videos.sh (not published)
└── .github/workflows/   pages.yml — GitHub Actions build & deploy
```

## Local development

Requires Ruby 3.x + Bundler. Run everything from `site/`:

```bash
cd site
bundle install                                                       # install dependencies
bundle exec jekyll serve --host 127.0.0.1 --port 4000 --incremental  # preview at http://127.0.0.1:4000
bundle exec jekyll build --trace                                     # production build → site/_site
```

> Note: the web-based VS Code preview proxy can mangle asset/data delivery, so the served
> page may look wrong in the browser tab — use a local VS Code (or any local browser) for an
> accurate preview. The build itself is always correct.

## One-click cleanup

Before committing, remove all regenerable build output, caches, OS noise and disposable
backups so the repo stays lightweight and only intended files reach GitHub:

```bash
bash site/tools/clean.sh
```

This never touches your content, source, or media — it only deletes things Jekyll rebuilds
(`_site/`, caches), Bundler restores (`vendor/`, `.bundle/`), throwaway video backups
(`*_bk.mp4`), and OS/editor junk. Local-only tooling (e.g. `site/assets/media/blog/script`)
is already git-ignored and will not be uploaded.

## Deployment

Push to `main` → `.github/workflows/pages.yml` builds `site/` and publishes it.

**One-time setup:** in the repository, go to **Settings → Pages → Build and deployment**
and set **Source: "GitHub Actions"**. (A user site whose source lives in a subfolder cannot
use the classic branch build, so Actions does the build.) After that, every push deploys
automatically.

## Editing content

- **Publications** — edit `site/_data/publications.yml`; put media in `site/assets/media/papers/`. Set `selected: true` to feature on the home page.
- **Projects** — add `site/_projects/<slug>.md`; media in `site/assets/media/projects/<slug>/`. `order` controls sort (higher = newer/first). Keep enterprise content sanitized.
- **News** — edit `site/_data/news.yml` (reverse-chronological, manual).
- **Blog** — add `site/_posts/YYYY-MM-DD-title.md`. Categories are defined in `site/_data/blog_categories.yml`; set `talk: true` for video talks, add `cover:`/`cover_type:` for a cover image/video/SVG.

The ⌘K search index (`search.json`) is rebuilt automatically on every build.

See [`site/AGENTS.md`](site/AGENTS.md) for maintenance rules and [`site/DESIGN.md`](site/DESIGN.md) for the visual system.
