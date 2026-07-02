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
    const edgeObjs = edges
      .map((e, i) => {
        const from = e.from || e[0];
        const to = e.to || e[1];
        const kind = e.kind || e[2] || "flow";
        if (!adj[from] || !adj[to]) return null;
        adj[from].edges.push(i);
        adj[to].edges.push(i);
        adj[from].down.push(to);
        adj[to].up.push(from);
        return { from, to, kind, path: null, head: null };
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
    });

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
        if (e.kind === "loop") {
          const x1 = a.left, y1 = a.cy, x2 = b.left, y2 = b.cy;
          const cx = Math.min(x1, x2) - Math.max(46, (a.bottom - a.top) * 0.7);
          e.path.setAttribute("d", `M ${x1} ${y1} C ${cx} ${y1} ${cx} ${y2} ${x2} ${y2}`);
          e.head.setAttribute("d", arrow(x2, y2, Math.atan2(0, x2 - cx)));
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
      });
    };

    // panel
    const panel = qs("[data-atlas-panel]", atlas);
    const accentVar = { cyan: "--at-cyan", blue: "--at-blue", purple: "--at-purple", green: "--at-green", warn: "--at-warn", ink: "--at-ink" };
    const setPanel = (n) => {
      if (!panel) return;
      const set = (sel, val) => { const el = qs(sel, panel); if (el) el.textContent = val || "—"; };
      const css = "var(" + (accentVar[n.accent] || "--at-cyan") + ")";
      const dot = qs("[data-ap-dot]", panel);
      if (dot) { dot.style.background = css; dot.style.boxShadow = "0 0 10px " + css; }
      set("[data-ap-tag]", (n.tag || "Module").toUpperCase());
      set("[data-ap-title]", n.title);
      set("[data-ap-receives]", n.receives);
      set("[data-ap-logic]", n.logic);
      set("[data-ap-sends]", n.sends);
      set("[data-ap-gives]", n.gives);

      const rel = qs("[data-ap-rel]", panel);
      const up = qs("[data-ap-up]", panel), down = qs("[data-ap-down]", panel);
      const names = (ids) => ids.map((id) => (nodeById[id] || {}).title || id).join(", ");
      let any = false;
      if (up) { const u = adj[n.id].up; up.hidden = !u.length; if (u.length) { qs("span", up).textContent = names(u); any = true; } }
      if (down) { const d = adj[n.id].down; down.hidden = !d.length; if (d.length) { qs("span", down).textContent = names(d); any = true; } }
      if (rel) rel.hidden = !any;

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

    const focusNode = (id) => {
      const n = nodeById[id];
      if (!n) return;
      grid.classList.add("has-dim");
      svg.classList.add("has-dim");
      const lit = new Set([id]);
      // light connected edges + neighbours
      edgeObjs.forEach((e) => {
        const on = e.from === id || e.to === id;
        e.path.classList.toggle("is-lit", on);
        e.head.classList.toggle("is-lit", on);
        if (on) { lit.add(e.from); lit.add(e.to); }
      });
      qsa(".atlas-node", grid).forEach((el) => {
        const on = lit.has(el.dataset.node);
        el.classList.toggle("is-lit", on);
        el.classList.toggle("is-active", el.dataset.node === id);
      });
      setPanel(n);
    };

    const clearFocus = () => {
      grid.classList.remove("has-dim");
      svg.classList.remove("has-dim");
      edgeObjs.forEach((e) => { e.path.classList.remove("is-lit"); e.head.classList.remove("is-lit"); });
      qsa(".atlas-node", grid).forEach((el) => el.classList.remove("is-lit", "is-active"));
    };

    // tour
    const tourWrap = qs("[data-atlas-tour]", atlas);
    const tourBtn = qs("[data-atlas-toggle]", atlas);
    const statusEl = qs("[data-atlas-status]", atlas);
    let touring = false, tourIdx = -1, tourTimer = null, started = false;

    const tourStep = () => { tourIdx = (tourIdx + 1) % nodes.length; focusNode(nodes[tourIdx].id); };
    const startTour = () => {
      if (touring || reduceMotion) return;
      touring = true; atlas.classList.add("is-touring");
      if (statusEl) statusEl.textContent = "Touring";
      tourStep();
      tourTimer = window.setInterval(tourStep, 2300);
    };
    const stopTour = () => {
      touring = false; atlas.classList.remove("is-touring");
      if (statusEl) statusEl.innerHTML = "Auto&nbsp;Tour";
      window.clearInterval(tourTimer);
    };

    if (tourWrap && !reduceMotion) {
      tourWrap.hidden = false;
      if (tourBtn) tourBtn.addEventListener("click", () => { if (touring) { stopTour(); clearFocus(); } else startTour(); });
    }

    // interactions pause the tour
    const userInterrupt = () => { if (touring) { stopTour(); } };

    qsa(".atlas-node", grid).forEach((el) => {
      el.addEventListener("pointerenter", () => { userInterrupt(); focusNode(el.dataset.node); });
      el.addEventListener("focus", () => { userInterrupt(); focusNode(el.dataset.node); });
      el.addEventListener("click", () => { userInterrupt(); focusNode(el.dataset.node); });
    });
    stage.addEventListener("pointerleave", () => { if (!touring) clearFocus(); });

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

    // auto-start the tour once, shortly after the atlas enters the viewport
    if (!reduceMotion && "IntersectionObserver" in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !started) {
            started = true;
            window.setTimeout(() => { if (!touring) startTour(); }, 2600);
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
    const heads = qsa("h2, h3[data-toc]", main).filter((h) => !h.closest(".atlas"));
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
  const zoomables = qsa(".proj-figure img, .viz-media img, .gallery-item img");
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
