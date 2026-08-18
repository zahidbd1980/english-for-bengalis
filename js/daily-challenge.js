/**
 * Daily challenge + flashcards helpers (with mid-session resume)
 */
(function (global) {
  function flattenPools(pools) {
    const out = [];
    Object.keys(pools || {}).forEach((k) => {
      (pools[k] || []).forEach((q) => out.push(q));
    });
    return out;
  }

  function buildChallenge(pools) {
    const state = EFBStorage.load();
    const today = EFBProgress.todayStr();
    const all = flattenPools(pools);
    const byId = {};
    all.forEach((q) => {
      const id = q.item_id || q.id;
      if (id) byId[id] = q;
    });

    if (state.challenge.date === today && state.challenge.item_ids && state.challenge.item_ids.length) {
      const questions = state.challenge.item_ids.map((id) => byId[id]).filter(Boolean);
      return {
        date: state.challenge.date,
        completed: !!state.challenge.completed,
        item_ids: state.challenge.item_ids.slice(),
        questions: questions,
        score: state.challenge.score || 0,
        total: state.challenge.total || questions.length,
      };
    }

    const picked = [];
    const take = (arr, n) => EFBQuiz.shuffle(arr).slice(0, n);

    take(pools.vocabulary || [], 5).forEach((x) => picked.push(x));
    take(pools.phrasal || [], 2).forEach((x) => picked.push(x));
    take(pools.spelling || [], 3).forEach((x) => picked.push(x));
    take(pools.grammar || [], 3).forEach((x) => picked.push(x));
    take(pools.mistakes || [], 2).forEach((x) => picked.push(x));

    const challenge = {
      date: today,
      completed: false,
      item_ids: picked.map((p) => p.item_id || p.id),
      questions: picked,
      score: 0,
      total: picked.length,
    };

    EFBStorage.update((s) => {
      s.challenge = {
        date: challenge.date,
        completed: false,
        item_ids: challenge.item_ids,
        score: 0,
        total: challenge.total,
      };
    });

    return challenge;
  }

  function markChallengeComplete(score, total) {
    EFBStorage.update((s) => {
      s.challenge.completed = true;
      s.challenge.score = score;
      s.challenge.total = total;
    });
    if (window.EFBProgress) {
      EFBProgress.clearResume("daily");
      EFBProgress.setLastLesson("daily", "daily-challenge");
    }
  }

  function wantsFresh() {
    try {
      return new URLSearchParams(location.search || "").get("restart") === "1";
    } catch (e) {
      return false;
    }
  }

    function mountFlashcards(root, cards, opts) {
    opts = opts || {};
    cards = (cards || []).slice();
    if (!cards.length) {
      root.innerHTML = '<div class="empty-state bn">কোনো কার্ড নেই।</div>';
      return;
    }

    const skill = opts.skill || "vocabulary";
    let i = 0;
    let showBack = false;
    let knows = 0;
    let hards = 0;
    let showResumeHint = false;
    let deck = cards;

    function shuffleDeck(arr) {
      const a = arr.slice();
      for (let x = a.length - 1; x > 0; x--) {
        const j = Math.floor(Math.random() * (x + 1));
        const t = a[x];
        a[x] = a[j];
        a[j] = t;
      }
      return a;
    }

    const saved =
      !opts.fresh &&
      !wantsFresh() &&
      window.EFBProgress &&
      EFBProgress.getResume("flashcards");

    let restored = false;
    if (
      saved &&
      saved.skill === skill &&
      Array.isArray(saved.item_ids) &&
      saved.item_ids.length &&
      EFBProgress.isResumeActive(saved)
    ) {
      const byId = {};
      cards.forEach((c) => {
        if (c.item_id) byId[c.item_id] = c;
      });
      let ordered = saved.item_ids.map((id) => byId[id]).filter(Boolean);
      if (saved.cards_lite && saved.cards_lite.length && ordered.length < saved.item_ids.length) {
        const liteById = {};
        saved.cards_lite.forEach((c) => {
          if (c.item_id) liteById[c.item_id] = c;
        });
        ordered = saved.item_ids.map((id) => byId[id] || liteById[id]).filter(Boolean);
      }
      if (ordered.length) {
        const seen = new Set(ordered.map((c) => c.item_id));
        cards.forEach((c) => {
          if (c.item_id && !seen.has(c.item_id)) ordered.push(c);
        });
        deck = ordered;
        i = Math.max(0, Math.min(deck.length - 1, Number(saved.index) || 0));
        knows = Number(saved.knows) || 0;
        hards = Number(saved.hards) || 0;
        showResumeHint = i > 0;
        restored = true;
      }
    }

    // Fresh session (no resume): randomize card order for better practice
    if (!restored && opts.shuffle !== false) {
      deck = shuffleDeck(deck);
    }

    if (window.EFBProgress) EFBProgress.setLastLesson("flashcards", "flash-session");

    function persist() {
      if (!window.EFBProgress || i >= deck.length) return;
      const itemIds = deck.map((c) => c.item_id).filter(Boolean);
      const payload = {
        skill: skill,
        from_filter: !!opts.fromFilter,
        item_ids: itemIds,
        index: i,
        knows: knows,
        hards: hards,
        total: deck.length,
        label: opts.label || "Flashcards · " + skill,
        href: "flashcards.html?resume=1&skill=" + encodeURIComponent(skill) + (opts.fromFilter ? "&from=filter" : ""),
        profile_skill: "flashcards",
        lesson_id: "flash-session",
        active: true,
      };
      if (opts.fromFilter) {
        payload.cards_lite = deck.map((c) => ({
          item_id: c.item_id,
          front: c.front,
          back: c.back,
          back_bn: c.back_bn,
          example: c.example,
        }));
      }
      EFBProgress.saveResume("flashcards", payload);
    }

    function paint() {
      if (i >= deck.length) {
        if (root._efbFlashKey) {
          document.removeEventListener("keydown", root._efbFlashKey);
          root._efbFlashKey = null;
        }
        if (window.EFBProgress) EFBProgress.clearResume("flashcards");
        const skillGuess = (deck[0] && String(deck[0].item_id || "").split(":")[0]) || skill;
        const skillOut =
          skillGuess === "pv" ? "phrasal" : skillGuess === "vocab" ? "vocabulary" : skillGuess;
        const actions =
          window.EFBApp && EFBApp.nextRoundActions
            ? EFBApp.nextRoundActions({ skill: skillOut })
            : '<div class="stack-actions"><button type="button" class="btn btn-primary" data-next="retry">আবার</button></div>';
        root.innerHTML = `
          <div class="panel highlight">
            <p class="chip">Deck complete</p>
            <h2 class="page-title" style="font-size:1.6rem">জানি ${knows} · কঠিন ${hards}</h2>
            <p class="muted bn">প্রোগ্রেস সেভ হয়েছে। পরের রাউন্ড বেছে নিন।</p>
            ${actions}
          </div>`;
        const retry = root.querySelector('[data-next="retry"]');
        if (retry) {
          retry.addEventListener("click", () => {
            mountFlashcards(root, cards, Object.assign({}, opts, { fresh: true }));
          });
        }
        return;
      }

      persist();
      const c = deck[i];
      if (c.item_id && window.EFBProgress) EFBProgress.markSeen(c.item_id);

      const resumeBanner =
        showResumeHint
          ? `<div class="vocab-resume-banner bn" role="status">
              যেখানে থেমেছিলেন · <strong>${i + 1}</strong> / ${deck.length}
              <button type="button" class="btn btn-ghost" id="btn-flash-restart">১ নম্বর থেকে শুরু</button>
            </div>`
          : "";

      root.innerHTML = `
        <div class="panel flash-shell">
          <div class="quiz-meta">
            <span class="chip">${i + 1}/${deck.length}</span>
            <button type="button" class="verb-speak-btn" data-speak="${escape(c.front)}" id="btn-flash-speak" aria-label="Pronounce">🔊 Pronounce · P</button>
          </div>
          ${resumeBanner}
          <div class="flash-card" id="card" role="button" tabindex="0" aria-label="Flip card">
            ${
              showBack
                ? `<div><div class="back-mean">${escape(c.back)}</div>
                   ${c.back_bn ? `<p class="bn muted">${escape(c.back_bn)}</p>` : ""}
                   ${c.example ? `<p class="example">${escape(c.example)}</p>` : ""}</div>`
                : `<div class="front-word">${escape(c.front)}</div>`
            }
          </div>
          <div class="flash-actions-sticky">
            <div class="stack-actions">
              <button type="button" class="btn btn-secondary" id="prev">‹ আগে</button>
              <button type="button" class="btn btn-primary" id="flip">উল্টান</button>
              <button type="button" class="btn btn-secondary" id="next">পরে ›</button>
            </div>
            <div class="stack-actions">
              <button type="button" class="btn btn-accent" id="know">জানি · K</button>
              <button type="button" class="btn btn-secondary" id="hard">কঠিন · H</button>
              <button type="button" class="btn btn-ghost" id="btn-flash-shuffle">Shuffle</button>
            </div>
          </div>
          <p class="session-kbd-hint bn"><kbd>Space</kbd>/<kbd>Enter</kbd> flip · <kbd>P</kbd> pronounce · <kbd>←</kbd><kbd>→</kbd> · <kbd>K</kbd> know · <kbd>H</kbd> hard</p>
        </div>
      `;

      const restartBtn = root.querySelector("#btn-flash-restart");
      if (restartBtn) {
        restartBtn.addEventListener("click", () => {
          if (window.EFBProgress) EFBProgress.clearResume("flashcards");
          mountFlashcards(root, cards, Object.assign({}, opts, { fresh: true }));
        });
      }
      const shuffleBtn = root.querySelector("#btn-flash-shuffle");
      if (shuffleBtn) {
        shuffleBtn.addEventListener("click", () => {
          if (window.EFBProgress) EFBProgress.clearResume("flashcards");
          mountFlashcards(root, shuffleDeck(deck), Object.assign({}, opts, { fresh: true, shuffle: false }));
        });
      }

      const flip = () => {
        showBack = !showBack;
        paint();
      };
      const goPrev = () => {
        i = Math.max(0, i - 1);
        showBack = false;
        showResumeHint = false;
        paint();
      };
      const goNext = () => {
        i = i + 1;
        showBack = false;
        showResumeHint = false;
        paint();
      };
      const markKnow = () => {
        if (c.item_id) EFBProgress.recordResult(c.item_id, true, "mcq");
        knows += 1;
        i = i + 1;
        showBack = false;
        showResumeHint = false;
        paint();
      };
      const markHard = () => {
        if (c.item_id) EFBProgress.recordResult(c.item_id, false, "mcq");
        hards += 1;
        showBack = true;
        showResumeHint = false;
        paint();
      };

      const cardEl = root.querySelector("#card");
      cardEl.addEventListener("click", flip);
      root.querySelector("#flip").addEventListener("click", flip);
      root.querySelector("#prev").addEventListener("click", goPrev);
      root.querySelector("#next").addEventListener("click", goNext);
      root.querySelector("#know").addEventListener("click", markKnow);
      root.querySelector("#hard").addEventListener("click", markHard);
      const speakBtn = root.querySelector("#btn-flash-speak");
      if (speakBtn) {
        speakBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          const text = speakBtn.getAttribute("data-speak");
          if (!window.speechSynthesis || !text) return;
          try {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(text);
            u.lang = "en-GB";
            u.rate = 0.95;
            window.speechSynthesis.speak(u);
          } catch (err) {}
        });
      }

      if (root._efbFlashKey) document.removeEventListener("keydown", root._efbFlashKey);
      root._efbFlashKey = function (e) {
        if (!document.body.contains(root)) {
          document.removeEventListener("keydown", root._efbFlashKey);
          return;
        }
        const tag = (e.target && e.target.tagName) || "";
        if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
        if (tag === "BUTTON" || tag === "A") return;
        if (e.key === " " || e.key === "Enter") {
          e.preventDefault();
          flip();
        } else if (e.key === "ArrowLeft") {
          e.preventDefault();
          goPrev();
        } else if (e.key === "ArrowRight") {
          e.preventDefault();
          goNext();
        } else if (e.key === "k" || e.key === "K") {
          e.preventDefault();
          markKnow();
        } else if (e.key === "h" || e.key === "H") {
          e.preventDefault();
          markHard();
        }
      };
      document.addEventListener("keydown", root._efbFlashKey);
    }

    function escape(s) {
      return String(s || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
    }

    paint();
  }

  global.EFBChallenge = { buildChallenge, markChallengeComplete };
  global.EFBFlashcards = { mount: mountFlashcards };
})(window);
