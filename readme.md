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

# GitHub Pages 私有源码 → 公开部署 快速教程

---

## 前提
- 私有仓：存放源码（含 `.github/workflows/deploy.yml`）
- 公开仓：`jiangchaokang/jiangchaokang.github.io`（只存编译结果）

---

## 二、生成 SSH 密钥对（5分钟）

```bash
# 生成密钥
ssh-keygen -t ed25519 -f pages_deploy -N ""

# 查看公钥（待会儿填入 GitHub）
cat pages_deploy.pub

# 查看私钥（待会儿填入 GitHub）
cat pages_deploy
```

---

## 三、配置 GitHub（网页端）

**3.1 公开仓 → 添加公钥**
> Settings → Deploy keys → Add deploy key
> - Title：`pages_deploy`
> - Key：粘贴 `pages_deploy.pub` 内容
> - ✅ 勾选 Allow write access

**3.2 私有仓 → 添加私钥和密码**
> Settings → Secrets and variables → Actions → New repository secret

| Name | Value |
|---|---|
| `PAGES_DEPLOY_KEY` | `pages_deploy` 私钥全文（含 BEGIN/END 行）|
| `SITE_PROTECT_PASSWORD` | `5896` |

**3.3 公开仓 → 配置 Pages 来源**
> Settings → Pages → Source:
> `Deploy from a branch` → `main` → `/(root)` → Save

**3.4 公开仓 → 修改默认分支为 main**
> Settings → Branches → Default branch → 切换为 `main`

---

## 四、触发部署

```bash
# 在私有仓目录下，push 即可自动触发 deploy.yml
git add .
git commit -m "deploy"
git push origin main
```

> 或手动触发：私有仓 → Actions → `Build and publish to public Pages repo` → Run workflow

---

## 五、验证

- 私有仓 → Actions → 查看 `Build and publish to public Pages repo` 是否 ✅
- 打开 https://jiangchaokang.github.io 确认网站上线

---

## 六、重新生成密钥（丢失时）

```bash
# 重新生成
ssh-keygen -t ed25519 -f pages_deploy -N ""

# 公开仓：删除旧 Deploy Key → 添加新 pages_deploy.pub
# 私有仓：更新 Secret PAGES_DEPLOY_KEY 为新私钥内容
```

See [`site/AGENTS.md`](site/AGENTS.md) for maintenance rules and [`site/DESIGN.md`](site/DESIGN.md) for the visual system.
