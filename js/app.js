/**
 * Shared chrome + data helpers for English for Bengalis MVP
 */
(function () {
  function rootPrefix() {
    if (window.EFB_ASSET_BASE) {
      return String(window.EFB_ASSET_BASE).replace(/\/$/, "");
    }
    const body = document.body;
    return (body && body.getAttribute("data-root")) || ".";
  }

  function asset(path) {
    const root = rootPrefix().replace(/\/$/, "");
    const clean = path.replace(/^\//, "");
    // On Blogger, EFB_ASSET_BASE is absolute CDN/GitHub Pages root
    if (/^https?:\/\//i.test(root)) {
      return root + "/" + clean;
    }
    return root + "/" + clean;
  }

  async function loadJSON(name) {
    const url = asset("data/" + name);
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to load " + name);
    return res.json();
  }

  function navHTML(root) {
    const p = root === "." ? "pages/" : "";
    const home = root === "." ? "index.html" : "../index.html";
    return `
      <a class="brand" href="${home}">
        <span class="brand-name">English for Bengalis</span>
        <span class="brand-tag bn">শিখুন · অনুশীলন · মাস্টারি</span>
      </a>
      <nav class="nav-desktop" aria-label="Primary">
        <details class="nav-drop">
          <summary>শিখুন · Learn</summary>
          <div class="nav-panel">
            <a href="${p}learn.html">Learn hub</a>
            <a href="${p}vocabulary.html">Vocabulary</a>
            <a href="${p}grammar.html">Grammar</a>
            <a href="${p}phrasal-verbs.html">Phrasal Verbs</a>
            <a href="${p}spelling.html">Spelling</a>
            <a href="${p}spoken-english.html">Spoken English</a>
            <a href="${p}common-mistakes.html">Common Mistakes</a>
          </div>
        </details>
        <details class="nav-drop">
          <summary>অনুশীলন · Practice</summary>
          <div class="nav-panel">
            <a href="${p}daily-challenge.html">Daily Challenge</a>
            <a href="${p}quizzes.html">Quizzes</a>
            <a href="${p}flashcards.html">Flashcards</a>
            <a href="${p}translation-lab.html">Translation Lab</a>
            <a href="${p}spelling-practice.html">Spelling Practice</a>
            <a href="${p}practice.html">Practice hub</a>
          </div>
        </details>
        <a href="${p}my-progress.html">প্রোগ্রেস</a>
        <a href="${p}level-test.html">লেভেল টেস্ট</a>
        <a href="${p}ielts.html">IELTS</a>
        <details class="nav-drop">
          <summary>আরও · More</summary>
          <div class="nav-panel">
            <a href="${p}settings.html">Settings</a>
            <a href="${p}about.html">About</a>
            <a href="${p}contact.html">Contact</a>
            <a href="${p}privacy.html">Privacy</a>
            <a href="${p}terms.html">Terms</a>
            <a href="${p}disclaimer.html">Disclaimer</a>
          </div>
        </details>
      </nav>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-drawer" id="nav-toggle">
        <span></span><span class="sr-only">Menu</span>
      </button>
    `;
  }

  function drawerHTML(root) {
    const p = root === "." ? "pages/" : "";
    const home = root === "." ? "index.html" : "../index.html";
    return `
      <div class="pin-actions">
        <a class="btn btn-accent" href="${p}daily-challenge.html">ডেইলি চ্যালেঞ্জ</a>
        <a class="btn btn-primary" href="${p}my-progress.html" id="continue-link">Continue / প্রোগ্রেস</a>
      </div>
      <a href="${home}">Home · হোম</a>
      <a href="${p}learn.html">শিখুন · Learn</a>
      <a class="sub" href="${p}vocabulary.html">Vocabulary</a>
      <a class="sub" href="${p}grammar.html">Grammar</a>
      <a class="sub" href="${p}phrasal-verbs.html">Phrasal Verbs</a>
      <a class="sub" href="${p}spelling.html">Spelling</a>
      <a class="sub" href="${p}spoken-english.html">Spoken</a>
      <a class="sub" href="${p}common-mistakes.html">Common Mistakes</a>
      <a href="${p}practice.html">অনুশীলন · Practice</a>
      <a class="sub" href="${p}daily-challenge.html">Daily Challenge</a>
      <a class="sub" href="${p}quizzes.html">Quizzes</a>
      <a class="sub" href="${p}flashcards.html">Flashcards</a>
      <a class="sub" href="${p}translation-lab.html">Translation Lab</a>
      <a class="sub" href="${p}spelling-practice.html">Spelling Practice</a>
      <a href="${p}my-progress.html">My Progress</a>
      <a href="${p}level-test.html">Level Test</a>
      <a href="${p}ielts.html">IELTS</a>
      <a href="${p}settings.html">Settings</a>
      <a href="${p}about.html">About</a>
      <a href="${p}contact.html">Contact</a>
      <a href="${p}privacy.html">Privacy</a>
    `;
  }

  function footerHTML(root) {
    const p = root === "." ? "pages/" : "";
    return `
      <div class="footer-inner">
        <div>
          <div class="brand-name" style="font-family:var(--font-display);color:var(--color-brand-dark)">English for Bengalis</div>
          <p class="muted bn" style="margin:0.5rem 0 0">বাংলাভাষীদের জন্য মাপযোগ্য ইংরেজি শেখা।</p>
        </div>
        <div>
          <h3>শিখুন</h3>
          <a href="${p}vocabulary.html">Vocabulary</a>
          <a href="${p}grammar.html">Grammar</a>
          <a href="${p}phrasal-verbs.html">Phrasal Verbs</a>
          <a href="${p}common-mistakes.html">Common Mistakes</a>
        </div>
        <div>
          <h3>অনুশীলন</h3>
          <a href="${p}daily-challenge.html">Daily Challenge</a>
          <a href="${p}quizzes.html">Quizzes</a>
          <a href="${p}flashcards.html">Flashcards</a>
          <a href="${p}translation-lab.html">Translation Lab</a>
          <a href="${p}spelling-practice.html">Spelling Practice</a>
        </div>
        <div>
          <h3>Trust</h3>
          <a href="${p}about.html">About</a>
          <a href="${p}contact.html">Contact</a>
          <a href="${p}privacy.html">Privacy</a>
          <a href="${p}disclaimer.html">Disclaimer</a>
          <a href="${p}settings.html">Settings / Export</a>
        </div>
      </div>
      <p class="footer-note">IELTS® is a registered trademark of its owners. This site offers unofficial IELTS-style practice only — not affiliated with British Council, IDP, or Cambridge.</p>
    `;
  }

  function mountChrome() {
    const root = rootPrefix();
    const header = document.getElementById("site-header");
    const drawer = document.getElementById("nav-drawer");
    const footer = document.getElementById("site-footer");
    if (header) {
      header.innerHTML = `<div class="header-inner">${navHTML(root)}</div>`;
    }
    if (drawer) drawer.innerHTML = drawerHTML(root);
    if (footer) footer.innerHTML = footerHTML(root);

    const toggle = document.getElementById("nav-toggle");
    if (toggle && drawer) {
      toggle.addEventListener("click", () => {
        const open = drawer.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      });
    }

    // Close desktop details when clicking outside
    document.addEventListener("click", (e) => {
      document.querySelectorAll("details.nav-drop[open]").forEach((d) => {
        if (!d.contains(e.target)) d.removeAttribute("open");
      });
    });
  }

  function renderHomeProgress() {
    const el = document.getElementById("home-progress");
    if (!el || !window.EFBStorage) return;
    const state = EFBStorage.load();
    const streak = state.streak.current || 0;
    const level = state.profile.estimated_level || "—";
    const tracked = Object.keys(state.items).length;
    el.innerHTML = `
      <div class="panel highlight">
        <p class="chip">Your journey</p>
        <h2 style="font-family:var(--font-display);margin:0.4rem 0 0.75rem">প্রোগ্রেস এক নজরে</h2>
        <p class="muted bn">Streak: <strong>${streak}</strong> day(s) · Estimated level: <strong>${level}</strong> · Items tracked: <strong>${tracked}</strong></p>
        <div class="stack-actions">
          <a class="btn btn-primary" href="${rootPrefix() === "." ? "pages/" : ""}my-progress.html">পুরো প্রোগ্রেস</a>
          <a class="btn btn-secondary" href="${rootPrefix() === "." ? "pages/" : ""}daily-challenge.html">ডেইলি চ্যালেঞ্জ</a>
        </div>
      </div>
    `;
  }

  function animateBars() {
    document.querySelectorAll(".bar[data-pct]").forEach((bar) => {
      const pct = Number(bar.getAttribute("data-pct") || 0);
      const i = bar.querySelector("i");
      if (i) requestAnimationFrame(() => (i.style.width = clamp(pct, 0, 100) + "%"));
    });
  }

  function clamp(n, a, b) {
    return Math.max(a, Math.min(b, n));
  }

  document.addEventListener("DOMContentLoaded", () => {
    mountChrome();
    renderHomeProgress();
    animateBars();
  });

  window.EFBApp = {
    rootPrefix,
    asset,
    loadJSON,
    mountChrome,
    animateBars,
  };
})();
