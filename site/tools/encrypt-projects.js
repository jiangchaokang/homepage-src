#!/usr/bin/env node
/*
 * encrypt-projects.js — build-time content encryption for protected pages.
 *
 * WHY THIS EXISTS
 *   The site is served from a *public* repo (Free-plan user sites must be
 *   public). A JavaScript "password gate" is therefore useless: the real HTML
 *   would sit in plain sight in the public repo. To actually keep company
 *   material private we must ship *ciphertext* and decrypt it in the browser
 *   with the passcode. This script does the encryption at build time.
 *
 * WHAT IT DOES
 *   After `jekyll build`, it scans `_site` for pages that carry
 *   `<meta name="x-protected">` (emitted when a project has `protected: true`),
 *   encrypts the *entire* rendered page with AES-256-GCM (key = PBKDF2-SHA256
 *   over the passcode), and replaces the file with a small self-contained lock
 *   page. On the correct passcode the browser decrypts and re-renders the
 *   original page (a full re-parse so every script/animation initialises
 *   exactly as on a normal load).
 *
 * SECURITY NOTE (read me)
 *   Client-side encryption only hides content as well as the passcode is
 *   strong. The ciphertext is public, so a short numeric code (e.g. 5896) can
 *   be brute-forced offline. This defeats crawlers, casual visitors and
 *   accidental exposure — it is NOT protection against a determined attacker.
 *   For truly sensitive material use a long random passphrase
 *   (SITE_PROTECT_PASSWORD) or do not publish the page at all.
 *
 * Zero dependencies: uses Node's built-in WebCrypto (node:crypto), which is the
 * same API the browser uses, so encrypt (Node) and decrypt (browser) match.
 */
"use strict";

const fs = require("fs");
const path = require("path");
const { webcrypto } = require("node:crypto");
const { subtle } = webcrypto;

const PASSWORD = process.env.SITE_PROTECT_PASSWORD || "5896";
const ITERATIONS = Number(process.env.SITE_PROTECT_ITERATIONS || 310000);
const SITE_DIR = process.env.SITE_DIR || "_site";

const b64 = (buf) => Buffer.from(buf).toString("base64");

async function deriveKey(password, salt, iterations, usage) {
  const base = await subtle.importKey(
    "raw",
    new TextEncoder().encode(password),
    "PBKDF2",
    false,
    ["deriveKey"]
  );
  return subtle.deriveKey(
    { name: "PBKDF2", salt, iterations, hash: "SHA-256" },
    base,
    { name: "AES-GCM", length: 256 },
    false,
    [usage]
  );
}

async function encrypt(plaintext, password) {
  const salt = webcrypto.getRandomValues(new Uint8Array(16));
  const iv = webcrypto.getRandomValues(new Uint8Array(12));
  const key = await deriveKey(password, salt, ITERATIONS, "encrypt");
  const ct = await subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    new TextEncoder().encode(plaintext)
  );
  return {
    v: 1,
    kdf: "PBKDF2-SHA256",
    cipher: "AES-GCM",
    iter: ITERATIONS,
    salt: b64(salt),
    iv: b64(iv),
    ct: b64(new Uint8Array(ct)),
  };
}

// Pull the stylesheet + icon links out of the original <head> so the lock
// screen inherits the exact (baseurl-correct) asset paths and styling.
function extractHeadAssets(html) {
  const head = (html.match(/<head[^>]*>([\s\S]*?)<\/head>/i) || [, ""])[1];
  const grab = (re) => head.match(re) || [];
  const links = [
    ...grab(/<link[^>]*rel=["']stylesheet["'][^>]*>/gi),
    ...grab(/<link[^>]*rel=["'](?:icon|apple-touch-icon)["'][^>]*>/gi),
  ];
  return links.join("\n  ");
}

function lang(html) {
  const m = html.match(/<html[^>]*\blang=["']([^"']+)["']/i);
  return m ? m[1] : "en";
}

// Inline, dependency-free browser script. Decrypts with WebCrypto, then does a
// full document rewrite so the real page initialises normally.
const DECRYPT_SCRIPT = `
(function () {
  var el = document.getElementById("lock-payload");
  if (!el) return;
  var p = JSON.parse(el.textContent);
  var form = document.querySelector("[data-lock-form]");
  var input = document.querySelector("[data-lock-input]");
  var err = document.querySelector("[data-lock-error]");
  var busy = document.querySelector("[data-lock-busy]");
  var KEY = "ck-unlock:" + location.pathname;
  function bytes(b64) {
    var bin = atob(b64), u = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
    return u;
  }
  function key(pw) {
    var enc = new TextEncoder();
    return crypto.subtle
      .importKey("raw", enc.encode(pw), "PBKDF2", false, ["deriveKey"])
      .then(function (base) {
        return crypto.subtle.deriveKey(
          { name: "PBKDF2", salt: bytes(p.salt), iterations: p.iter, hash: "SHA-256" },
          base,
          { name: "AES-GCM", length: 256 },
          false,
          ["decrypt"]
        );
      });
  }
  function unlock(pw, silent) {
    if (busy) busy.hidden = false;
    return key(pw)
      .then(function (k) {
        return crypto.subtle.decrypt({ name: "AES-GCM", iv: bytes(p.iv) }, k, bytes(p.ct));
      })
      .then(function (buf) {
        var html = new TextDecoder().decode(buf);
        try { sessionStorage.setItem(KEY, pw); } catch (e) {}
        document.open();
        document.write(html);
        document.close();
      })
      .catch(function () {
        try { sessionStorage.removeItem(KEY); } catch (e) {}
        if (busy) busy.hidden = true;
        if (!silent && err) {
          err.hidden = false;
          input.value = "";
          input.focus();
        }
      });
  }
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (err) err.hidden = true;
      unlock(input.value.trim(), false);
    });
  }
  try {
    var saved = sessionStorage.getItem(KEY);
    if (saved) unlock(saved, true);
  } catch (e) {}
  if (input) input.focus();
})();
`;

function lockPage(html, payload) {
  const assets = extractHeadAssets(html);
  const json = JSON.stringify(payload);
  return `<!doctype html>
<html lang="${lang(html)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>Protected · Chaokang Jiang</title>
  <script>
    (function () {
      try {
        var s = localStorage.getItem("theme");
        var d = s === "dark" || s === "light" ? s === "dark"
          : window.matchMedia("(prefers-color-scheme: dark)").matches;
        document.documentElement.setAttribute("data-theme", d ? "dark" : "light");
      } catch (e) {}
    })();
  </script>
  ${assets}
</head>
<body class="lock-body">
  <main class="lock-screen" id="main" tabindex="-1">
    <section class="lock-card">
      <span class="lock-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4.5" y="10.5" width="15" height="10" rx="2.2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><circle cx="12" cy="15.5" r="1.3"/></svg>
      </span>
      <p class="eyebrow">Protected project</p>
      <h1>Passcode required</h1>
      <p class="lock-desc">This project contains sanitized company-internal material and is intentionally not public. Enter the passcode to view the full page.</p>
      <form class="lock-form" data-lock-form novalidate>
        <input type="password" inputmode="numeric" autocomplete="off" spellcheck="false" data-lock-input aria-label="Passcode" placeholder="Passcode">
        <button type="submit">Unlock</button>
      </form>
      <p class="lock-busy" data-lock-busy hidden>Decrypting…</p>
      <p class="lock-error" data-lock-error hidden>Incorrect passcode — please try again.</p>
      <p class="lock-note">Access is limited to authorized reviewers. Request the passcode from Chaokang (<a href="mailto:jck98@foxmail.com">jck98@foxmail.com</a>).</p>
      <a class="lock-back" href="../">← Back to all projects</a>
    </section>
  </main>
  <script type="application/json" id="lock-payload">${json}</script>
  <script>${DECRYPT_SCRIPT}</script>
</body>
</html>
`;
}

function findProtected(dir, out = []) {
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) findProtected(full, out);
    else if (name.endsWith(".html")) {
      const html = fs.readFileSync(full, "utf8");
      if (/<meta[^>]*name=["']x-protected["']/i.test(html)) out.push(full);
    }
  }
  return out;
}

async function main() {
  if (!fs.existsSync(SITE_DIR)) {
    console.error(`[encrypt] build dir "${SITE_DIR}" not found — run jekyll build first.`);
    process.exit(1);
  }
  const files = findProtected(SITE_DIR);
  if (files.length === 0) {
    console.log("[encrypt] no protected pages found (nothing to do).");
    return;
  }
  for (const file of files) {
    const original = fs.readFileSync(file, "utf8");
    const payload = await encrypt(original, PASSWORD);

    // Self-check: decrypt round-trip must reproduce the original exactly.
    const key = await deriveKey(PASSWORD, Buffer.from(payload.salt, "base64"), payload.iter, "decrypt");
    const back = await subtle.decrypt(
      { name: "AES-GCM", iv: Buffer.from(payload.iv, "base64") },
      key,
      Buffer.from(payload.ct, "base64")
    );
    if (new TextDecoder().decode(back) !== original) {
      console.error(`[encrypt] round-trip mismatch for ${file} — aborting.`);
      process.exit(1);
    }

    fs.writeFileSync(file, lockPage(original, payload));
    console.log(`[encrypt] locked ${path.relative(SITE_DIR, file)} (${payload.iter} PBKDF2 iters, ${original.length}B → ciphertext).`);
  }
  console.log(`[encrypt] done — ${files.length} page(s) protected.`);
}

main().catch((e) => {
  console.error("[encrypt] failed:", e);
  process.exit(1);
});
