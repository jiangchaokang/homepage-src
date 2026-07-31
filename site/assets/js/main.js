(function () {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const qs = (selector, scope = document) => scope.querySelector(selector);
  const qsa = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));

  const navToggle = qs("[data-nav-toggle]");
  const siteNav = qs("[data-site-nav]");

  if (navToggle && siteNav) {
    navToggle.addEventListener("click", () => {
      const isOpen = siteNav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });
  }

  /* ---- Liquid Glass nav: hover-intent on desktop, tap-toggle on mobile ---- */
  const navItems = qsa("[data-nav-item]");
  if (navItems.length) {
    const hoverable = window.matchMedia("(hover: hover) and (pointer: fine)");
    const mobile = window.matchMedia("(max-width: 720px)");
    let closeTimer = null;

    const setOpen = (item, open) => {
      item.classList.toggle("is-open", open);
      const trigger = qs("[data-nav-trigger]", item);
      if (trigger) trigger.setAttribute("aria-expanded", String(open));
    };
    const closeAll = (except) =>
      navItems.forEach((it) => { if (it !== except) setOpen(it, false); });

    navItems.forEach((item) => {
      const trigger = qs("[data-nav-trigger]", item);
      const dropdown = qs("[data-nav-menu]", item);
      const glass = dropdown ? qs(".liquid-glass", dropdown) : null;

      item.addEventListener("mouseenter", () => {
        if (!hoverable.matches || mobile.matches) return;
        window.clearTimeout(closeTimer);
        closeAll(item);
        setOpen(item, true);
      });
      item.addEventListener("mouseleave", () => {
        if (!hoverable.matches || mobile.matches) return;
        window.clearTimeout(closeTimer);
        closeTimer = window.setTimeout(() => setOpen(item, false), 160);
      });
      item.addEventListener("focusin", () => { if (!mobile.matches) { closeAll(item); setOpen(item, true); } });
      item.addEventListener("focusout", (event) => {
        if (mobile.matches) return;
        if (!item.contains(event.relatedTarget)) setOpen(item, false);
      });

      if (trigger) {
        trigger.addEventListener("click", (event) => {
          if (!mobile.matches) return;
          event.preventDefault();
          setOpen(item, !item.classList.contains("is-open"));
        });
      }

      // Pointer-tracked specular highlight on the glass panel
      if (dropdown && glass) {
        dropdown.addEventListener("pointermove", (event) => {
          const rect = dropdown.getBoundingClientRect();
          glass.style.setProperty("--mx", `${((event.clientX - rect.left) / rect.width) * 100}%`);
          glass.style.setProperty("--my", `${((event.clientY - rect.top) / rect.height) * 100}%`);
        });
      }
    });

    document.addEventListener("keydown", (event) => { if (event.key === "Escape") closeAll(null); });
    document.addEventListener("click", (event) => {
      if (!event.target.closest("[data-nav-item]")) closeAll(null);
    });
  }

  const newsToggle = qs("[data-news-toggle]");
  const newsRail = qs("[data-news-rail]");

  if (newsToggle && newsRail) {
    newsToggle.addEventListener("click", () => {
      const isCollapsed = document.body.classList.toggle("news-collapsed");
      newsRail.classList.toggle("is-collapsed", isCollapsed);
      newsToggle.setAttribute("aria-expanded", String(!isCollapsed));
    });
  }

  /* ---- News rail: seamless auto-scrolling ticker (desktop only) ---- */
  const newsScroll = qs("[data-news-scroll]");
  const newsTrack = newsScroll ? qs("[data-news-track]", newsScroll) : null;

  if (newsScroll && newsTrack && !reduceMotion) {
    const desktop = window.matchMedia("(min-width: 1101px)");
    const SPEED = 30; // px per second — calm but clearly visible
    let baseHeight = 0; // seamless wrap distance (offset of first clone)
    let offset = 0;
    let rafId = null;
    let lastTs = 0;
    let paused = false;

    const stop = () => {
      if (rafId) cancelAnimationFrame(rafId);
      rafId = null;
      lastTs = 0;
      newsTrack.style.transform = "";
      qsa("[data-news-clone]", newsTrack).forEach((node) => node.remove());
    };

    const tick = (ts) => {
      if (!lastTs) lastTs = ts;
      const dt = Math.min((ts - lastTs) / 1000, 0.05);
      lastTs = ts;
      if (!paused) {
        offset += SPEED * dt;
        if (offset >= baseHeight) offset -= baseHeight;
        newsTrack.style.transform = "translateY(" + -offset + "px)";
      }
      rafId = requestAnimationFrame(tick);
    };

    const start = () => {
      stop();
      offset = 0;
      if (!desktop.matches) return;
      // Only animate when the content actually overflows its container.
      if (newsTrack.scrollHeight <= newsScroll.clientHeight + 8) return;

      Array.from(newsTrack.children).forEach((node) => {
        const clone = node.cloneNode(true);
        clone.setAttribute("aria-hidden", "true");
        clone.setAttribute("data-news-clone", "");
        clone.tabIndex = -1;
        newsTrack.appendChild(clone);
      });

      const firstClone = qs("[data-news-clone]", newsTrack);
      baseHeight = firstClone ? firstClone.offsetTop : 0;
      if (baseHeight <= 0) {
        stop();
        return;
      }
      rafId = requestAnimationFrame(tick);
    };

    newsScroll.addEventListener("pointerenter", () => { paused = true; });
    newsScroll.addEventListener("pointerleave", () => { paused = false; });
    newsScroll.addEventListener("focusin", () => { paused = true; });
    newsScroll.addEventListener("focusout", () => { paused = false; });

    let resizeTimer = null;
    window.addEventListener("resize", () => {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(start, 200);
    });
    desktop.addEventListener("change", start);

    window.requestAnimationFrame(() => window.requestAnimationFrame(start));
  }

  /* ---- Scroll-aware video: play in view, pause off-screen, lazy preload ----
     One engine, two kinds of clip:
       • Cover clips  (video[autoplay], no controls): silent looping motion-posters
         that autoplay even under reduced-motion — a quiet looping cover is content.
       • Player clips (have [controls], e.g. talks and project demos): muted autoplay
         when scrolled into view, but the visitor stays in charge — pause / seek /
         speed / fullscreen via the native controls, and a deliberate pause is never
         overridden when the clip scrolls back into view. */
  const scrollVideos = qsa("video[autoplay], video.talk-video");
  if (scrollVideos.length) {
    const isPlayer = (v) => v.hasAttribute("controls");

    scrollVideos.forEach((v) => {
      // Hard-guarantee every attribute browsers require for silent inline autoplay.
      v.muted = true;
      v.defaultMuted = true;
      v.setAttribute("muted", "");
      v.setAttribute("playsinline", "");
      v.setAttribute("webkit-playsinline", "");
      if (!isPlayer(v) && !v.hasAttribute("loop")) v.loop = true;

      // Remember a deliberate pause so the observer never fights the visitor.
      v.addEventListener("pause", () => {
        if (!v._byObserver && !v.ended) v._userPaused = true;
      });
      v.addEventListener("play", () => { v._userPaused = false; });
    });

    const tryPlay = (v) => {
      const p = v.play();
      if (p && typeof p.catch === "function") {
        p.catch(() => {
          // Blocked or not yet decodable — retry once a frame is ready, then stop listening.
          const retry = () => {
            v.removeEventListener("canplay", retry);
            v.removeEventListener("loadeddata", retry);
            const r = v.play();
            if (r && typeof r.catch === "function") r.catch(() => {});
          };
          v.addEventListener("canplay", retry);
          v.addEventListener("loadeddata", retry);
        });
      }
    };

    const enter = (v) => {
      // Upgrade buffering only as the clip nears the viewport, so a page full of
      // videos never downloads everything at once — keeps decode smooth and jank-free.
      if (v.preload === "none" || v.preload === "metadata") v.preload = "auto";
      if (!v._userPaused && !v.ended) tryPlay(v);
    };
    const leave = (v) => {
      if (v.paused) return;
      v._byObserver = true;
      v.pause();
      v._byObserver = false;
    };

    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver(
        (entries) => entries.forEach((e) => (e.isIntersecting ? enter(e.target) : leave(e.target))),
        { threshold: 0.2, rootMargin: "200px 0px" }
      );
      scrollVideos.forEach((v) => io.observe(v));
    } else {
      scrollVideos.forEach(enter);
    }
  }

  /* ---- Talk stage: click-to-load Bilibili facade ----
     The poster + play button is a real <a href="https://www.bilibili.com/..."> ,
     so it already works with JavaScript disabled. With JS, a click swaps the
     facade for a real <iframe> instead of following the link — the official
     player embed only ever loads after the visitor asks for it. */
  qsa("[data-talk-facade]").forEach((facade) => {
    facade.addEventListener("click", (event) => {
      const bvid = facade.getAttribute("data-bvid");
      if (!bvid) return; // no id to embed — let the real link open Bilibili
      event.preventDefault();

      const page = facade.getAttribute("data-bvid-page");
      const params = new URLSearchParams({ bvid: bvid, autoplay: "1", high_quality: "1", danmaku: "0" });
      if (page) params.set("page", page);

      const iframe = document.createElement("iframe");
      iframe.src = "https://player.bilibili.com/player.html?" + params.toString();
      iframe.className = "talk-bilibili-frame";
      iframe.title = facade.getAttribute("aria-label") || "Bilibili video player";
      iframe.setAttribute("allow", "autoplay; fullscreen; picture-in-picture; encrypted-media");
      iframe.setAttribute("allowfullscreen", "");
      iframe.setAttribute("scrolling", "no");
      facade.replaceWith(iframe);
    });
  });

  const themeToggle = qs("[data-theme-toggle]");

  if (themeToggle) {
    const root = document.documentElement;
    const systemDark = window.matchMedia("(prefers-color-scheme: dark)");

    const currentTheme = () => {
      const explicit = root.getAttribute("data-theme");
      if (explicit === "dark" || explicit === "light") return explicit;
      return systemDark.matches ? "dark" : "light";
    };

    themeToggle.addEventListener("click", () => {
      const next = currentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try {
        localStorage.setItem("theme", next);
      } catch (e) {}
    });

    // Follow the OS theme live while the visitor has not made an explicit choice.
    systemDark.addEventListener("change", (event) => {
      let stored = null;
      try {
        stored = localStorage.getItem("theme");
      } catch (e) {}
      if (stored === "dark" || stored === "light") return;
      root.setAttribute("data-theme", event.matches ? "dark" : "light");
    });
  }

  qsa(".spotlight-card, .feature-card, .pub-card, .project-card, .news-card, .mini-card, .gallery-item, .post-card").forEach((card) => {
    card.addEventListener("pointermove", (event) => {
      const rect = card.getBoundingClientRect();
      card.style.setProperty("--px", `${event.clientX - rect.left}px`);
      card.style.setProperty("--py", `${event.clientY - rect.top}px`);
    });
  });

  qsa("[data-filter-group]").forEach((group) => {
    const listName = group.getAttribute("data-filter-group");
    const list = qs(`[data-filter-list="${listName}"]`);
    if (!list) return;

    const buttons = qsa("[data-filter]", group);
    const items = qsa("[data-tags]", list);

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const filter = button.getAttribute("data-filter");

        buttons.forEach((btn) => btn.classList.toggle("is-active", btn === button));

        items.forEach((item) => {
          const tags = item.getAttribute("data-tags") || "";
          const shouldShow = filter === "all" || tags.split(/\s+/).includes(filter);
          item.classList.toggle("is-hidden", !shouldShow);
        });
      });
    });
  });

  qsa("[data-tabs]").forEach((group) => {
    const tabs = qsa("[data-tab]", group);
    const panels = qsa("[data-panel]", group);

    const activate = (tab) => {
      const target = tab.getAttribute("data-tab");
      tabs.forEach((btn) => {
        const isActive = btn === tab;
        btn.classList.toggle("is-active", isActive);
        btn.setAttribute("aria-selected", String(isActive));
        btn.tabIndex = isActive ? 0 : -1;
      });
      panels.forEach((panel) => {
        panel.classList.toggle("is-active", panel.getAttribute("data-panel") === target);
      });
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener("click", () => activate(tab));
      tab.addEventListener("keydown", (event) => {
        if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") return;
        event.preventDefault();
        const dir = event.key === "ArrowRight" ? 1 : -1;
        const next = tabs[(index + dir + tabs.length) % tabs.length];
        activate(next);
        next.focus();
      });
    });
  });

  qsa(".reveal-stagger").forEach((group) => {
    Array.from(group.children).forEach((child, i) => child.style.setProperty("--i", i));
  });

  if (!reduceMotion && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
    );

    qsa(".reveal, .reveal-stagger").forEach((item) => observer.observe(item));
  } else {
    qsa(".reveal, .reveal-stagger").forEach((item) => item.classList.add("is-visible"));
  }

  /* ---- Logic Atlas: interactive 2.5D logic map ---- */
  qsa("[data-atlas]").forEach((atlas) => {
    const stage = qs("[data-atlas-stage]", atlas);
    const grid = qs("[data-atlas-grid]", atlas);
    const svg = qs("[data-atlas-edges]", atlas);
    const dataEl = qs("[data-atlas-data]", atlas);
    if (!stage || !grid || !svg || !dataEl) return;

    let data;
    try { data = JSON.parse(dataEl.textContent); } catch (e) { return; }
    const nodes = data.nodes || [];
    const edges = data.edges || [];
    if (!nodes.length) return;

    const NS = "http://www.w3.org/2000/svg";
    const nodeById = {};
    nodes.forEach((n) => { nodeById[n.id] = n; });
    const elById = {};
    qsa(".atlas-node", grid).forEach((el) => { elById[el.dataset.node] = el; });

    // adjacency: id -> { edges:[idx], up:[id], down:[id] }
    const adj = {};
    nodes.forEach((n) => { adj[n.id] = { edges: [], up: [], down: [] }; });
    // One vocabulary for every map: flow = inference data flow, cond = conditioning /
    // structural link, train = train-time only, grad = gradient, loop = closed loop.
    // `solid` / `dashed` are kept as legacy aliases so older maps keep rendering.
    const KIND_ALIAS = { solid: "cond", dashed: "train" };
    const edgeObjs = edges
      .map((e, i) => {
        const from = e.from || e[0];
        const to = e.to || e[1];
        const raw = e.kind || e[2] || "flow";
        const kind = KIND_ALIAS[raw] || raw;
        if (!adj[from] || !adj[to]) return null;
        adj[from].edges.push(i);
        adj[to].edges.push(i);
        adj[from].down.push(to);
        adj[to].up.push(from);
        return { from, to, kind, label: e.label || "", path: null, head: null, text: null };
      })
      .filter(Boolean);

    edgeObjs.forEach((e) => {
      const p = document.createElementNS(NS, "path");
      p.setAttribute("class", "kind-" + e.kind);
      p.setAttribute("data-from", e.from);
      p.setAttribute("data-to", e.to);
      const h = document.createElementNS(NS, "path");
      h.setAttribute("class", "edge-head kind-" + e.kind);
      svg.appendChild(p);
      svg.appendChild(h);
      e.path = p;
      e.head = h;
      if (e.label) {
        const t = document.createElementNS(NS, "text");
        t.setAttribute("class", "edge-label kind-" + e.kind);
        t.setAttribute("text-anchor", "middle");
        t.setAttribute("dominant-baseline", "middle");
        t.setAttribute("paint-order", "stroke");
        t.textContent = e.label;
        svg.appendChild(t);
        e.text = t;
      }
    });

    // Reserve a left rail whenever the map draws a loop / gradient edge, so the
    // bow has somewhere to go instead of cutting through the first column.
    if (edgeObjs.some((e) => e.kind === "loop" || e.kind === "grad")) atlas.classList.add("has-rail");

    const measure = (el) => ({
      cx: el.offsetLeft + el.offsetWidth / 2, cy: el.offsetTop + el.offsetHeight / 2,
      left: el.offsetLeft, right: el.offsetLeft + el.offsetWidth,
      top: el.offsetTop, bottom: el.offsetTop + el.offsetHeight
    });

    const arrow = (x, y, ang) => {
      const s = 6.5, a1 = ang + Math.PI - 0.4, a2 = ang + Math.PI + 0.4;
      return `M ${x} ${y} L ${x + s * Math.cos(a1)} ${y + s * Math.sin(a1)} L ${x + s * Math.cos(a2)} ${y + s * Math.sin(a2)} Z`;
    };

    // Pick the connection coordinate on the shared (perpendicular) axis so an edge
    // leaves and enters each box at the point nearest the other box — the shortest
    // path that never cuts across a node's content. Overlapping spans give a clean
    // straight line through the shared band; disjoint spans use the facing edges.
    const along = (loA, hiA, loB, hiB) => {
      const pad = 11;
      const fit = (lo, hi, v) => {
        const a = lo + pad, b = hi - pad;
        return a > b ? (lo + hi) / 2 : Math.min(b, Math.max(a, v));
      };
      const lo = Math.max(loA, loB), hi = Math.min(hiA, hiB);
      if (lo <= hi) {
        const m = (lo + hi) / 2;
        return [fit(loA, hiA, m), fit(loB, hiB, m)];
      }
      return hiA < loB ? [hiA - pad, loB + pad] : [loA + pad, hiB - pad];
    };

    const draw = () => {
      const w = grid.offsetWidth, h = grid.offsetHeight;
      if (!w || !h) return;
      svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
      edgeObjs.forEach((e) => {
        const ae = elById[e.from], be = elById[e.to];
        if (!ae || !be) return;
        const a = measure(ae), b = measure(be);
        // Loop-back edge: bow out to the left margin so the closed loop reads clearly,
        // kept clear of the training-weight line that rises on the right.
        // Loop / gradient edge: bow out into the left rail so the closed loop reads
        // clearly and never cuts across a node. The rail is reserved by `has-rail`.
        if (e.kind === "loop" || e.kind === "grad") {
          const x1 = a.left, y1 = a.cy, x2 = b.left, y2 = b.cy;
          const near = Math.min(x1, x2);
          const cx = near - Math.min(Math.max(near - 6, 8), Math.max(30, (a.bottom - a.top) * 0.55));
          e.path.setAttribute("d", `M ${x1} ${y1} C ${cx} ${y1} ${cx} ${y2} ${x2} ${y2}`);
          e.head.setAttribute("d", arrow(x2, y2, Math.atan2(0, x2 - cx)));
          if (e.text) {
            e.text.setAttribute("x", ((x1 + 3 * cx + 3 * cx + x2) / 8).toFixed(1));
            e.text.setAttribute("y", ((y1 + y2) / 2).toFixed(1));
          }
          return;
        }
        const dx = b.cx - a.cx, dy = b.cy - a.cy;
        let x1, y1, x2, y2, c1x, c1y, c2x, c2y;
        if (Math.abs(dy) >= Math.abs(dx)) {
          const [ax, bx] = along(a.left, a.right, b.left, b.right);
          x1 = ax; x2 = bx;
          y1 = dy >= 0 ? a.bottom : a.top;
          y2 = dy >= 0 ? b.top : b.bottom;
          const my = (y1 + y2) / 2;
          c1x = x1; c1y = my; c2x = x2; c2y = my;
        } else {
          const [ay, by] = along(a.top, a.bottom, b.top, b.bottom);
          y1 = ay; y2 = by;
          x1 = dx >= 0 ? a.right : a.left;
          x2 = dx >= 0 ? b.left : b.right;
          const mx = (x1 + x2) / 2;
          c1x = mx; c1y = y1; c2x = mx; c2y = y2;
        }
        e.path.setAttribute("d", `M ${x1} ${y1} C ${c1x} ${c1y} ${c2x} ${c2y} ${x2} ${y2}`);
        e.head.setAttribute("d", arrow(x2, y2, Math.atan2(y2 - c2y, x2 - c2x)));
        if (e.text) {
          e.text.setAttribute("x", ((x1 + 3 * c1x + 3 * c2x + x2) / 8).toFixed(1));
          e.text.setAttribute("y", ((y1 + 3 * c1y + 3 * c2y + y2) / 8).toFixed(1));
        }
      });
    };

    // panel
    const panel = qs("[data-atlas-panel]", atlas);
    const accentVar = { cyan: "--at-cyan", blue: "--at-blue", purple: "--at-purple", green: "--at-green", warn: "--at-warn", ink: "--at-ink" };
    const setPanel = (n) => {
      if (!panel) return;
      const set = (sel, val) => { const el = qs(sel, panel); if (el) el.textContent = val || "—"; };
      const row = (sel, val) => {
        const el = qs(sel, panel);
        if (el) el.hidden = !val;
        return val;
      };
      const css = "var(" + (accentVar[n.accent] || "--at-cyan") + ")";
      const dot = qs("[data-ap-dot]", panel);
      if (dot) { dot.style.background = css; dot.style.boxShadow = "0 0 10px " + css; }

      const lane = n.lane || "main";
      const laneSuffix = lane === "aux" ? " · TRAIN-ONLY" : lane === "prior" ? " · FROZEN" : "";
      set("[data-ap-tag]", (n.tag || "Module").toUpperCase() + laneSuffix);
      set("[data-ap-title]", n.title);
      set("[data-ap-receives]", n.receives);
      set("[data-ap-logic]", n.logic);
      set("[data-ap-sends]", n.sends);

      // "Why this design" carries the judgement; `gives` is the legacy field name.
      const why = n.why || n.gives;
      if (row("[data-ap-why-row]", why)) set("[data-ap-why]", why);
      if (row("[data-ap-trade-row]", n.tradeoff)) set("[data-ap-tradeoff]", n.tradeoff);
      if (row("[data-ap-role-row]", n.role)) set("[data-ap-role]", n.role);

      const hint = qs("[data-ap-hint]", panel);
      if (hint) hint.hidden = true;
      const io = qs("[data-ap-io]", panel);
      if (io) io.hidden = false;
      const copy = qs("[data-ap-copy]", panel);
      if (copy) { copy.hidden = false; copy.dataset.nodeId = n.id; }

      const note = qs("[data-ap-note]", panel);
      if (note) {
        if (n.note) { note.hidden = false; note.textContent = n.note; }
        else { note.hidden = true; note.textContent = ""; }
      }

      const media = qs("[data-ap-media]", panel);
      if (media) {
        if (n.media) {
          media.hidden = false;
          if (n.media_type === "video") {
            media.innerHTML = '<video autoplay muted loop playsinline preload="metadata"><source src="' + n.media + '" type="video/mp4"></video>';
            const v = qs("video", media); if (v) { v.muted = true; const pr = v.play(); if (pr && pr.catch) pr.catch(() => {}); }
          } else {
            media.innerHTML = '<img src="' + n.media + '" alt="">';
          }
        } else { media.hidden = true; media.innerHTML = ""; }
      }
    };

    const nodeEls = qsa(".atlas-node", grid);
    let pinnedId = null;

    const paint = (id) => {
      const lit = new Set([id]);
      edgeObjs.forEach((e) => {
        const on = e.from === id || e.to === id;
        e.path.classList.toggle("is-lit", on);
        e.head.classList.toggle("is-lit", on);
        if (e.text) e.text.classList.toggle("is-lit", on);
        if (on) { lit.add(e.from); lit.add(e.to); }
      });
      grid.classList.add("has-dim");
      svg.classList.add("has-dim");
      nodeEls.forEach((el) => {
        const on = lit.has(el.dataset.node);
        el.classList.toggle("is-lit", on);
        el.classList.toggle("is-active", el.dataset.node === id);
        el.setAttribute("aria-expanded", String(el.dataset.node === id));
      });
    };

    const focusNode = (id) => {
      const n = nodeById[id];
      if (!n) return;
      atlas.classList.remove("is-idle");
      paint(id);
      setPanel(n);
    };

    const clearFocus = () => {
      grid.classList.remove("has-dim");
      svg.classList.remove("has-dim");
      edgeObjs.forEach((e) => {
        e.path.classList.remove("is-lit");
        e.head.classList.remove("is-lit");
        if (e.text) e.text.classList.remove("is-lit");
      });
      nodeEls.forEach((el) => {
        el.classList.remove("is-lit", "is-active");
        el.setAttribute("aria-expanded", "false");
      });
    };

    // Hover previews; a click (or Enter/Space on the button) pins the node so the
    // panel survives pointer-out — which is the only workable model on touch.
    const preview = (id) => { if (!pinnedId) focusNode(id); };
    const restore = () => { if (pinnedId) focusNode(pinnedId); else clearFocus(); };
    const pin = (id) => {
      pinnedId = pinnedId === id ? null : id;
      atlas.classList.toggle("is-pinned", !!pinnedId);
      if (pinnedId) focusNode(pinnedId); else clearFocus();
    };

    // tour — two steps on first view, then it gets out of the way
    const tourWrap = qs("[data-atlas-tour]", atlas);
    const tourBtn = qs("[data-atlas-toggle]", atlas);
    const statusEl = qs("[data-atlas-status]", atlas);
    let touring = false, tourIdx = -1, tourTimer = null, started = false, tourBudget = Infinity;

    const stopTour = () => {
      touring = false; atlas.classList.remove("is-touring");
      if (statusEl) statusEl.innerHTML = "Auto&nbsp;tour";
      window.clearInterval(tourTimer);
    };
    const tourStep = () => {
      if (tourBudget <= 0) { stopTour(); return; }
      tourBudget -= 1;
      tourIdx = (tourIdx + 1) % nodes.length;
      focusNode(nodes[tourIdx].id);
    };
    const startTour = (steps) => {
      if (touring || reduceMotion) return;
      pinnedId = null;
      atlas.classList.remove("is-pinned");
      tourBudget = steps || Infinity;
      touring = true; atlas.classList.add("is-touring");
      if (statusEl) statusEl.textContent = "Touring";
      tourStep();
      tourTimer = window.setInterval(tourStep, 2300);
    };

    if (tourWrap && !reduceMotion) {
      tourWrap.hidden = false;
      if (tourBtn) tourBtn.addEventListener("click", () => { if (touring) { stopTour(); clearFocus(); } else startTour(); });
    }

    const userInterrupt = () => { if (touring) stopTour(); };

    nodeEls.forEach((el) => {
      el.addEventListener("pointerenter", () => { userInterrupt(); preview(el.dataset.node); });
      el.addEventListener("focus", () => { userInterrupt(); preview(el.dataset.node); });
      el.addEventListener("blur", restore);
      el.addEventListener("click", () => { userInterrupt(); pin(el.dataset.node); });
    });
    stage.addEventListener("pointerleave", () => { if (!touring) restore(); });
    atlas.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && pinnedId) { pinnedId = null; atlas.classList.remove("is-pinned"); clearFocus(); }
    });

    // Copy a deep link to the focused node — the cheapest way for someone else to
    // reference one specific stage of the map.
    const copyBtn = qs("[data-ap-copy]", atlas);
    if (copyBtn) {
      copyBtn.addEventListener("click", () => {
        const id = copyBtn.dataset.nodeId;
        if (!id) return;
        const href = location.origin + location.pathname + "#" + atlas.id + "--" + id;
        const done = () => { copyBtn.classList.add("is-done"); window.setTimeout(() => copyBtn.classList.remove("is-done"), 1400); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(href).then(done, () => {});
      });
    }

    // subtle parallax
    const scene = qs("[data-atlas-scene]", atlas) || grid;
    if (!reduceMotion) {
      let raf = null;
      stage.addEventListener("pointermove", (event) => {
        userInterrupt();
        const r = stage.getBoundingClientRect();
        const nx = (event.clientX - r.left) / r.width - 0.5;
        const ny = (event.clientY - r.top) / r.height - 0.5;
        if (raf) return;
        raf = requestAnimationFrame(() => {
          raf = null;
          scene.style.transform = `rotateX(${(-ny * 4).toFixed(2)}deg) rotateY(${(nx * 5).toFixed(2)}deg) translate3d(${(nx * 7).toFixed(1)}px, ${(ny * 5).toFixed(1)}px, 0)`;
        });
      });
      stage.addEventListener("pointerleave", () => { scene.style.transform = ""; });
    }

    // draw + keep in sync
    const redraw = () => requestAnimationFrame(draw);
    redraw();
    window.addEventListener("load", redraw);
    [120, 400, 900].forEach((t) => window.setTimeout(redraw, t));
    if ("ResizeObserver" in window) {
      new ResizeObserver(redraw).observe(stage);
    } else {
      window.addEventListener("resize", redraw);
    }

    /* ---- Export the map as a standalone SVG (no dependencies) ---- */
    const exportBtn = qs("[data-atlas-export]", atlas);
    if (exportBtn && "Blob" in window && "URL" in window) {
      exportBtn.hidden = false;
      const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      const wrap = (text, perLine) => {
        const words = String(text).split(/\s+/);
        const lines = []; let line = "";
        words.forEach((w) => {
          if (!line.length) line = w;
          else if ((line + " " + w).length <= perLine) line += " " + w;
          else { lines.push(line); line = w; }
        });
        if (line) lines.push(line);
        return lines;
      };
      exportBtn.addEventListener("click", () => {
        const W = grid.offsetWidth, H = grid.offsetHeight;
        if (!W || !H) return;
        const pad = 28, footer = 34;
        const parts = [];
        parts.push(`<rect x="0" y="0" width="${W + pad * 2}" height="${H + pad * 2 + footer}" fill="#07090f"/>`);
        parts.push(`<g transform="translate(${pad},${pad})">`);
        edgeObjs.forEach((e) => {
          const d = e.path.getAttribute("d");
          if (!d) return;
          const dash = e.kind === "train" ? ' stroke-dasharray="2 6"' : e.kind === "flow" ? ' stroke-dasharray="5 9"' : "";
          const col = e.kind === "grad" || e.kind === "loop" ? "#38e1ef" : "rgba(150,180,255,0.45)";
          parts.push(`<path d="${d}" fill="none" stroke="${col}" stroke-width="1.6"${dash}/>`);
          parts.push(`<path d="${e.head.getAttribute("d") || ""}" fill="${col}"/>`);
          if (e.text) parts.push(`<text x="${e.text.getAttribute("x")}" y="${e.text.getAttribute("y")}" fill="#9aa6bd" font-size="10" font-family="ui-sans-serif,system-ui,sans-serif" text-anchor="middle">${esc(e.label)}</text>`);
        });
        nodeEls.forEach((el) => {
          const n = nodeById[el.dataset.node] || {};
          const x = el.offsetLeft, y = el.offsetTop, w = el.offsetWidth, h = el.offsetHeight;
          const accent = (getComputedStyle(el).getPropertyValue("--nc") || "#38e1ef").trim();
          const lane = n.lane || "main";
          const dash = lane === "main" ? "" : ' stroke-dasharray="4 4"';
          parts.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="rgba(255,255,255,0.05)" stroke="${accent}" stroke-opacity="0.55" stroke-width="1.2"${dash}/>`);
          let ty = y + 20;
          if (n.tag) { parts.push(`<text x="${x + 14}" y="${ty}" fill="${accent}" font-size="9" letter-spacing="1.2" font-family="ui-sans-serif,system-ui,sans-serif" font-weight="700">${esc(String(n.tag).toUpperCase())}</text>`); ty += 16; }
          wrap(n.title || "", Math.max(12, Math.floor(w / 8))).forEach((ln) => {
            parts.push(`<text x="${x + 14}" y="${ty}" fill="#ffffff" font-size="13" font-family="ui-sans-serif,system-ui,sans-serif" font-weight="700">${esc(ln)}</text>`);
            ty += 16;
          });
          if (n.desc) wrap(n.desc, Math.max(16, Math.floor(w / 6))).forEach((ln) => {
            parts.push(`<text x="${x + 14}" y="${ty}" fill="#9aa6bd" font-size="10.5" font-family="ui-sans-serif,system-ui,sans-serif">${esc(ln)}</text>`);
            ty += 13;
          });
        });
        parts.push("</g>");
        parts.push(`<text x="${pad}" y="${H + pad + 24}" fill="#6c7791" font-size="11" font-family="ui-sans-serif,system-ui,sans-serif">${esc((data.title || "Logic map") + " — jiangchaokang.github.io")}</text>`);
        const svgText = `<svg xmlns="http://www.w3.org/2000/svg" width="${W + pad * 2}" height="${H + pad * 2 + footer}" viewBox="0 0 ${W + pad * 2} ${H + pad * 2 + footer}">${parts.join("")}</svg>`;
        const url = URL.createObjectURL(new Blob([svgText], { type: "image/svg+xml" }));
        const a = document.createElement("a");
        a.href = url;
        a.download = (data.title || "logic-map").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") + ".svg";
        document.body.appendChild(a); a.click(); a.remove();
        window.setTimeout(() => URL.revokeObjectURL(url), 1000);
      });
    }

    // Deep link: /projects/x/#<atlas-id>--<node-id> opens straight onto that node.
    const openFromHash = () => {
      const hash = decodeURIComponent(location.hash || "").slice(1);
      const prefix = atlas.id + "--";
      if (!hash.startsWith(prefix)) return false;
      const id = hash.slice(prefix.length);
      if (!nodeById[id]) return false;
      stopTour();
      pinnedId = id;
      atlas.classList.add("is-pinned");
      focusNode(id);
      return true;
    };
    window.addEventListener("hashchange", openFromHash);

    // First view: play two tour steps so it is obvious the map is interactive,
    // then hand control back to the reader.
    if (!openFromHash() && "IntersectionObserver" in window) {
      atlas.classList.add("is-idle");
      const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !started) {
            started = true;
            if (!reduceMotion) window.setTimeout(() => { if (!touring && !pinnedId) startTour(2); }, 1400);
            io.disconnect();
          }
        });
      }, { threshold: 0.4 });
      io.observe(atlas);
    }
  });

  /* ---- Blog: contribution cards highlight their source atlas nodes + links ---- */
  qsa("[data-atlas-link]").forEach((card) => {
    const atlas = qs("[data-atlas]");
    if (!atlas) return;
    const grid = qs("[data-atlas-grid]", atlas);
    const edges = qs("[data-atlas-edges]", atlas);
    if (!grid) return;
    const ids = card.getAttribute("data-atlas-link").split(",").map((s) => s.trim());
    const nodes = qsa(".atlas-node", grid);
    const paths = qsa("path[data-from]", edges);
    const on = () => {
      grid.classList.add("has-dim");
      if (edges) edges.classList.add("has-dim");
      nodes.forEach((n) => n.classList.toggle("is-lit", ids.indexOf(n.dataset.node) !== -1));
      paths.forEach((p) => p.classList.toggle("is-lit", ids.indexOf(p.dataset.from) !== -1 && ids.indexOf(p.dataset.to) !== -1));
    };
    const off = () => {
      grid.classList.remove("has-dim");
      if (edges) edges.classList.remove("has-dim");
      nodes.forEach((n) => n.classList.remove("is-lit"));
      paths.forEach((p) => p.classList.remove("is-lit"));
    };
    card.addEventListener("pointerenter", on);
    card.addEventListener("pointerleave", off);
    card.addEventListener("focusin", on);
    card.addEventListener("focusout", off);
  });

  const tocShell = qs("[data-proj-shell]");
  const tocList = qs("[data-toc-list]");
  if (tocShell && tocList) {
    const main = qs(".project-body-main", tocShell) || tocShell;
    // The contents list is for sections of *this* page. Site navigation ("Jump
    // to another project") is a different mental model and belongs at the foot.
    const heads = qsa("h2, h3[data-toc]", main).filter(
      (h) => !h.closest(".atlas") && !h.closest(".project-nav")
    );
    const toc = qs("[data-proj-toc]", tocShell);

    if (heads.length < 2) {
      if (toc) toc.hidden = true;
    } else {
      const used = {};
      const slug = (s) =>
        s.toLowerCase().trim().replace(/[^\w\s-]/g, "").replace(/\s+/g, "-").replace(/-+/g, "-") || "section";
      const links = {};
      heads.forEach((h) => {
        if (!h.id) {
          let base = slug(h.textContent);
          let id = base, i = 2;
          while (used[id]) { id = base + "-" + i; i += 1; }
          used[id] = true;
          h.id = id;
        } else { used[h.id] = true; }
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = "#" + h.id;
        a.textContent = h.textContent;
        if (h.tagName === "H3") a.className = "lvl-3";
        li.appendChild(a);
        tocList.appendChild(li);
        links[h.id] = a;
      });

      let currentId = null;
      const toc = qs("[data-proj-toc]", tocShell);
      const nav = qs(".proj-toc-nav", tocShell);
      const setCurrent = (id) => {
        if (id === currentId) return;
        if (currentId && links[currentId]) links[currentId].classList.remove("is-current");
        currentId = id;
        const a = links[id];
        if (!a) return;
        a.classList.add("is-current");
        if (nav && toc && !toc.classList.contains("is-collapsed")) {
          const target = a.offsetLeft - nav.clientWidth / 2 + a.clientWidth / 2;
          nav.scrollTo({ left: Math.max(0, target), behavior: reduceMotion ? "auto" : "smooth" });
        }
      };

      if ("IntersectionObserver" in window) {
        const spy = new IntersectionObserver(
          (entries) => {
            entries
              .filter((e) => e.isIntersecting)
              .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)
              .forEach((e) => setCurrent(e.target.id));
          },
          { rootMargin: "-12% 0px -72% 0px", threshold: 0 }
        );
        heads.forEach((h) => spy.observe(h));
      }

      const toggle = qs("[data-toc-toggle]", tocShell);
      const setCollapsed = (collapsed) => {
        if (toc) toc.classList.toggle("is-collapsed", collapsed);
        if (toggle) toggle.setAttribute("aria-expanded", String(!collapsed));
      };
      if (toggle) toggle.addEventListener("click", () => setCollapsed(!(toc && toc.classList.contains("is-collapsed"))));
      if (window.matchMedia("(max-width: 720px)").matches) setCollapsed(true);
    }
  }

  /* ---- Copy to clipboard (WeChat ID and similar) ---- */
  qsa("[data-copy]").forEach((el) => {
    el.addEventListener("click", () => {
      const value = el.getAttribute("data-copy");
      const done = el.getAttribute("data-copy-done") || "Copied";
      const label = el.querySelector("span") || el.querySelector("h3");
      const original = label ? label.textContent : "";

      const finish = () => {
        el.classList.add("is-copied");
        if (label) label.textContent = done;
        window.setTimeout(() => {
          el.classList.remove("is-copied");
          if (label) label.textContent = original;
        }, 1600);
      };

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(value).then(finish).catch(finish);
      } else {
        const ta = document.createElement("textarea");
        ta.value = value;
        ta.setAttribute("readonly", "");
        ta.style.position = "absolute";
        ta.style.left = "-9999px";
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta);
        finish();
      }
    });
  });

  /* ---- Image lightbox: click any figure image to zoom ---- */
  const zoomables = qsa(".proj-figure img, .viz-media img, .gallery-item img, .bx-fig img");
  if (zoomables.length) {
    let lightbox = null;
    let lightboxImg = null;

    const closeLightbox = () => {
      if (!lightbox) return;
      lightbox.classList.remove("is-open");
      document.body.classList.remove("lightbox-open");
      window.setTimeout(() => { lightbox.hidden = true; }, reduceMotion ? 0 : 220);
    };

    const openLightbox = (src, alt) => {
      if (!lightbox) {
        lightbox = document.createElement("div");
        lightbox.className = "lightbox";
        lightbox.hidden = true;
        lightbox.innerHTML =
          '<button class="lightbox-close" type="button" aria-label="Close image">' +
          '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="m6 6 12 12M18 6 6 18"/></svg>' +
          '</button><img alt="">';
        document.body.appendChild(lightbox);
        lightboxImg = qs("img", lightbox);
        lightbox.addEventListener("click", (event) => {
          if (event.target !== lightboxImg) closeLightbox();
        });
      }
      lightboxImg.src = src;
      lightboxImg.alt = alt || "";
      lightbox.hidden = false;
      document.body.classList.add("lightbox-open");
      window.requestAnimationFrame(() => lightbox.classList.add("is-open"));
    };

    zoomables.forEach((img) => {
      img.addEventListener("click", () => openLightbox(img.currentSrc || img.src, img.alt));
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && lightbox && !lightbox.hidden) closeLightbox();
    });
  }

  /* ---- Command-palette site search ---- */
  const searchModal = qs("[data-search-modal]");
  if (searchModal) {
    const input = qs("[data-search-input]", searchModal);
    const resultsList = qs("[data-search-results]", searchModal);
    const hint = qs("[data-search-hint]", searchModal);
    const openers = qsa("[data-search-open]");
    const closers = qsa("[data-search-close]", searchModal);
    const indexUrl = searchModal.getAttribute("data-search-url") || "/search.json";
    const baseHint = hint ? hint.textContent : "";
    let index = null;
    let activeIndex = -1;
    let matches = [];

    const escapeHtml = (str) =>
      String(str).replace(/[&<>"']/g, (c) =>
        ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
      );

    const loadIndex = () => {
      if (index !== null) return Promise.resolve(index);
      return fetch(indexUrl)
        .then((res) => (res.ok ? res.json() : []))
        .then((data) => {
          index = Array.isArray(data) ? data : [];
          return index;
        })
        .catch(() => {
          index = [];
          return index;
        });
    };

    const go = (url) => {
      if (url) window.location.href = url;
    };

    const setActive = (i) => {
      const items = qsa(".search-result", resultsList);
      if (!items.length) {
        activeIndex = -1;
        return;
      }
      activeIndex = (i + items.length) % items.length;
      items.forEach((el, idx) => el.classList.toggle("is-active", idx === activeIndex));
      items[activeIndex].scrollIntoView({ block: "nearest" });
    };

    const render = () => {
      resultsList.innerHTML = "";
      matches.forEach((item, i) => {
        const li = document.createElement("li");
        li.className = "search-result" + (i === 0 ? " is-active" : "");
        li.setAttribute("role", "option");
        li.dataset.url = item.url;
        li.innerHTML =
          '<span class="res-type">' + escapeHtml(item.type) + "</span>" +
          '<span class="res-body"><span class="res-title">' + escapeHtml(item.title) + "</span>" +
          '<span class="res-meta">' + escapeHtml(item.meta || item.summary || "") + "</span></span>";
        li.addEventListener("click", () => go(item.url));
        li.addEventListener("mousemove", () => setActive(i));
        resultsList.appendChild(li);
      });
      activeIndex = matches.length ? 0 : -1;
    };

    const search = (query) => {
      const q = query.trim().toLowerCase();
      if (!q) {
        matches = [];
        resultsList.innerHTML = "";
        hint.hidden = false;
        hint.textContent = baseHint;
        hint.classList.remove("is-empty");
        return;
      }
      const terms = q.split(/\s+/);
      matches = (index || [])
        .map((item) => {
          const hay = (
            item.title + " " + (item.summary || "") + " " + (item.tags || "") + " " + (item.type || "")
          ).toLowerCase();
          let score = 0;
          for (let t = 0; t < terms.length; t += 1) {
            if (hay.indexOf(terms[t]) === -1) return null;
            score += item.title.toLowerCase().indexOf(terms[t]) !== -1 ? 2 : 1;
          }
          return { item: item, score: score };
        })
        .filter(Boolean)
        .sort((a, b) => b.score - a.score)
        .slice(0, 8)
        .map((r) => r.item);

      if (matches.length) {
        hint.hidden = true;
        render();
      } else {
        resultsList.innerHTML = "";
        hint.hidden = false;
        hint.textContent = "No matches for \u201C" + query.trim() + "\u201D.";
        hint.classList.add("is-empty");
      }
    };

    const open = () => {
      searchModal.hidden = false;
      document.body.classList.add("search-open");
      loadIndex().then(() => {
        if (input.value) search(input.value);
      });
      window.requestAnimationFrame(() => input.focus());
    };

    const close = () => {
      searchModal.hidden = true;
      document.body.classList.remove("search-open");
    };

    openers.forEach((btn) => btn.addEventListener("click", open));
    closers.forEach((el) => el.addEventListener("click", close));
    input.addEventListener("input", () => search(input.value));

    input.addEventListener("keydown", (event) => {
      if (event.key === "ArrowDown") {
        event.preventDefault();
        setActive(activeIndex + 1);
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        setActive(activeIndex - 1);
      } else if (event.key === "Enter") {
        event.preventDefault();
        const items = qsa(".search-result", resultsList);
        if (items[activeIndex]) go(items[activeIndex].dataset.url);
      }
    });

    document.addEventListener("keydown", (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        if (searchModal.hidden) open();
        else close();
      } else if (event.key === "Escape" && !searchModal.hidden) {
        close();
      }
    });
  }
})();
