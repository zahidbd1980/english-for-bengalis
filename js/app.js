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
            <a href="${p}learning-path.html">Learning Path · আজ কী করব</a>
            <a href="${p}vocabulary.html">Vocabulary</a>
            <a href="${p}grammar.html">Grammar</a>
            <a href="${p}verb-forms.html">Verb Forms · V1 V2 V3</a>
            <a href="${p}phrasal-verbs.html">Phrasal Verbs</a>
            <a href="${p}spelling.html">Spelling</a>
            <a href="${p}spoken-english.html">Spoken English</a>
            <a href="${p}spoken-drill.html">Spoken Drill</a>
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
            <a href="${p}sentence-builder.html">Sentence Builder</a>
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
      <a class="sub" href="${p}learning-path.html">Learning Path</a>
      <a class="sub" href="${p}vocabulary.html">Vocabulary</a>
      <a class="sub" href="${p}grammar.html">Grammar</a>
      <a class="sub" href="${p}verb-forms.html">Verb Forms</a>
      <a class="sub" href="${p}phrasal-verbs.html">Phrasal Verbs</a>
      <a class="sub" href="${p}spelling.html">Spelling</a>
      <a class="sub" href="${p}spoken-english.html">Spoken</a>
      <a class="sub" href="${p}spoken-drill.html">Spoken Drill</a>
      <a class="sub" href="${p}common-mistakes.html">Common Mistakes</a>
      <a href="${p}practice.html">অনুশীলন · Practice</a>
      <a class="sub" href="${p}daily-challenge.html">Daily Challenge</a>
      <a class="sub" href="${p}quizzes.html">Quizzes</a>
      <a class="sub" href="${p}flashcards.html">Flashcards</a>
      <a class="sub" href="${p}translation-lab.html">Translation Lab</a>
      <a class="sub" href="${p}sentence-builder.html">Sentence Builder</a>
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
          <a href="${p}learning-path.html">Learning Path</a>
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
          <a href="${p}sentence-builder.html">Sentence Builder</a>
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
      const setDrawer = (open) => {
        drawer.classList.toggle("open", open);
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        if (!open) toggle.focus();
      };
      toggle.addEventListener("click", () => {
        setDrawer(!drawer.classList.contains("open"));
      });
      document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && drawer.classList.contains("open")) {
          e.preventDefault();
          setDrawer(false);
        }
      });
    }

    // Close desktop details when clicking outside
    document.addEventListener("click", (e) => {
      document.querySelectorAll("details.nav-drop[open]").forEach((d) => {
        if (!d.contains(e.target)) d.removeAttribute("open");
      });
    });
    bindSpeakHotkey();
  }

  function isTypingTarget(el) {
    if (!el) return false;
    const tag = (el.tagName || "").toUpperCase();
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return true;
    if (el.isContentEditable) return true;
    return false;
  }

  function clickSpeakControl(slow) {
    const scope =
      document.getElementById("app") ||
      document.getElementById("root") ||
      document.getElementById("main") ||
      document.body;
    const slowBtn = scope.querySelector(".btn-speak-slow, [data-speak][data-slow='1'], #btn-slow");
    const normalBtn = scope.querySelector(
      ".btn-speak:not(.btn-speak-slow), .verb-speak-btn, #btn-listen, [data-speak]:not([data-slow])"
    );
    const btn = slow && slowBtn ? slowBtn : normalBtn;
    if (!btn) return false;
    btn.click();
    return true;
  }

  function bindSpeakHotkey() {
    if (window._efbSpeakHotkeyBound) return;
    window._efbSpeakHotkeyBound = true;
    document.addEventListener("keydown", (e) => {
      if (e.defaultPrevented) return;
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (isTypingTarget(e.target)) return;
      if (e.key !== "p" && e.key !== "P") return;
      if (clickSpeakControl(!!e.shiftKey)) e.preventDefault();
    });
  }

  function clamp(n, a, b) {
    return Math.max(a, Math.min(b, n));
  }

  const SKILL_PAGE = {
    vocabulary: "vocabulary.html",
    grammar: "grammar.html",
    verbforms: "verb-forms.html",
    spelling: "spelling-practice.html",
    phrasal: "phrasal-verbs.html?resume=1",
    mistakes: "common-mistakes.html",
    sentence: "sentence-builder.html",
    translate: "translation-lab.html",
    spoken: "spoken-drill.html",
    quizzes: "quizzes.html",
    flashcards: "flashcards.html",
    daily: "daily-challenge.html",
    review: "quizzes.html?mode=review",
    path: "learning-path.html",
  };

  function pagesPrefix() {
    if (/blogspot\.com/i.test(location.hostname)) return "/p/";
    return rootPrefix() === "." ? "pages/" : "";
  }

  function skillHref(skill) {
    return pagesPrefix() + (SKILL_PAGE[skill] || "my-progress.html");
  }

  /** Mark lesson items only when mostly on screen — not all on page load. */
  function watchLessonSeen(container) {
    if (!container || !window.EFBProgress) return;
    const marked = new Set();
    const mark = (id) => {
      if (!id || marked.has(id)) return;
      marked.add(id);
      EFBProgress.markSeen(id);
    };
    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((en) => {
            if (!en.isIntersecting) return;
            mark(en.target.getAttribute("data-item-id"));
          });
        },
        { threshold: 0.65 }
      );
      container.querySelectorAll("[data-item-id]").forEach((el) => io.observe(el));
    } else {
      container.addEventListener("click", (e) => {
        const art = e.target.closest("[data-item-id]");
        if (art) mark(art.getAttribute("data-item-id"));
      });
    }
  }

  function resolveContinue(state) {
    state = state || (window.EFBStorage ? EFBStorage.load() : null);
    const p = pagesPrefix();
    if (!state) return { href: p + "my-progress.html", label: "প্রোগ্রেস দেখুন →" };
    const due = window.EFBProgress ? EFBProgress.dueItems() : [];
    const today = window.EFBProgress ? EFBProgress.todayStr() : "";
    const challengeDone =
      state.challenge && state.challenge.date === today && state.challenge.completed;
    const dailyResume =
      window.EFBProgress && state.resume && EFBProgress.isResumeActive(state.resume.daily)
        ? state.resume.daily
        : null;

    if (due.length) {
      return {
        href: p + "quizzes.html?mode=review&resume=1",
        label: "Review due (" + due.length + ") · আজকের রিভিউ →",
      };
    }

    // Learning Path when started and today's tasks still open
    if (window.EFBPath && state.path && state.path.plan_id) {
      try {
        const cached = window.__EFB_PATH_DATA__;
        if (cached) {
          const hint = EFBPath.continueHint(cached, p);
          if (hint && hint.pending) return hint;
        } else {
          return {
            href: p + "learning-path.html",
            label: "আজকের প্ল্যান · Day " + (state.path.day || 1) + " →",
          };
        }
      } catch (e) {}
    }

    if (!challengeDone) {
      return {
        href: p + "daily-challenge.html?resume=1",
        label: dailyResume
          ? "Daily Challenge চালিয়ে যান · " +
            ((Number(dailyResume.index) || 0) + 1) +
            "/" +
            (dailyResume.total || "?") +
            " →"
          : "Daily Challenge শুরু করুন →",
      };
    }

    if (window.EFBProgress) {
      const best = EFBProgress.getBestResume();
      if (best) {
        const cont = EFBProgress.resumeContinue(best, p);
        if (cont) return cont;
      }
    }

    if (state.profile && state.profile.last_skill) {
      const skill = state.profile.last_skill;
      return { href: skillHref(skill), label: "Continue · " + skill + " →" };
    }
    if (state.mistakes && state.mistakes.length) {
      return { href: p + "quizzes.html?mode=mistakes&resume=1", label: "Mistake Bank practice →" };
    }
    if (!state.path || !state.path.plan_id) {
      return { href: p + "learning-path.html", label: "Learning Path শুরু করুন →" };
    }
    return { href: p + "my-progress.html", label: "Continue where you left off →" };
  }

  function nextRoundActions(opts) {
    opts = opts || {};
    const p = pagesPrefix();
    const skill = opts.skill || "";
    const dueN = window.EFBProgress ? EFBProgress.dueItems().length : 0;
    const bits = [];
    bits.push('<button type="button" class="btn btn-primary" data-next="retry">আরেক রাউন্ড · Again</button>');
    if (dueN) bits.push(`<a class="btn btn-accent" href="${p}quizzes.html?mode=review">রিভিউ (${dueN})</a>`);
    if (skill && SKILL_PAGE[skill]) {
      bits.push(`<a class="btn btn-secondary" href="${skillHref(skill)}">এই স্কিল চালিয়ে যান</a>`);
    }
    bits.push(`<a class="btn btn-ghost" href="${p}daily-challenge.html">Daily Challenge</a>`);
    bits.push(`<a class="btn btn-ghost" href="${p}my-progress.html">প্রোগ্রেস</a>`);
    return `<div class="stack-actions">${bits.join("")}</div>`;
  }

  function renderHomeProgress() {
    const el = document.getElementById("home-progress");
    if (!el || !window.EFBStorage) return;
    const state = EFBStorage.load();
    const streak = state.streak.current || 0;
    const level = state.profile.estimated_level || null;
    const tracked = Object.keys(state.items).length;
    const pages = pagesPrefix();
    const cont = resolveContinue(state);

    const continueLink = document.getElementById("home-continue-link");
    if (continueLink) {
      continueLink.href = cont.href;
      continueLink.textContent = cont.label;
      if (continueLink.parentElement) continueLink.parentElement.style.display = "";
    }

    el.innerHTML = `
      <article class="home-progress panel highlight">
        <div class="home-progress-head">
          <span class="chip">Your journey</span>
          <h2 class="home-h2 bn" style="margin:0.45rem 0 0">প্রোগ্রেস এক নজরে</h2>
        </div>
        <div class="home-stats">
          <div class="home-stat">
            <strong class="home-stat-num">${streak}</strong>
            <span class="bn">দিন streak</span>
          </div>
          <div class="home-stat">
            <strong class="home-stat-num">${level || "—"}</strong>
            <span class="bn">লেভেল</span>
          </div>
          <div class="home-stat">
            <strong class="home-stat-num">${tracked}</strong>
            <span class="bn">আইটেম</span>
          </div>
        </div>
        <div class="stack-actions">
          <a class="btn btn-primary" href="${cont.href}">${cont.label}</a>
          <a class="btn btn-secondary" href="${pages}my-progress.html">পুরো প্রোগ্রেস</a>
          <a class="btn btn-ghost" href="${pages}daily-challenge.html">ডেইলি চ্যালেঞ্জ</a>
        </div>
      </article>
    `;
  }

  function animateBars() {
    document.querySelectorAll(".bar[data-pct]").forEach((bar) => {
      const pct = Number(bar.getAttribute("data-pct") || 0);
      const i = bar.querySelector("i");
      if (i) requestAnimationFrame(() => (i.style.width = clamp(pct, 0, 100) + "%"));
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.add("app-body");
    mountChrome();
    if (window.EFBStorage && EFBStorage.applyIdMap) {
      loadJSON("progress_id_migrate.json")
        .then((map) => EFBStorage.applyIdMap(map || {}))
        .catch(() => {})
        .finally(() => {
          renderHomeProgress();
          animateBars();
        });
    } else {
      renderHomeProgress();
      animateBars();
    }
  });

  function decodeHtml(s) {
    s = String(s == null ? "" : s);
    if (s.indexOf("&") === -1) return s;
    const t = document.createElement("textarea");
    t.innerHTML = s;
    return t.value;
  }

  function escHtml(s) {
    return decodeHtml(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function setText(el, s) {
    if (typeof el === "string") el = document.getElementById(el);
    if (el) el.textContent = decodeHtml(s);
  }

  window.EFBApp = {
    rootPrefix,
    asset,
    loadJSON,
    mountChrome,
    animateBars,
    watchLessonSeen,
    resolveContinue,
    nextRoundActions,
    skillHref,
    bindSpeakHotkey,
    decodeHtml,
    escHtml,
    setText,
    SKILL_PAGE,
  };
})();
