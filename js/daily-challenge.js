/**
 * Daily challenge + flashcards helpers
 */
(function (global) {
  function buildChallenge(pools) {
    const state = EFBStorage.load();
    const today = EFBProgress.todayStr();
    if (state.challenge.date === today && state.challenge.item_ids.length) {
      return state.challenge;
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
    if (window.EFBProgress) EFBProgress.setLastLesson("daily", "daily-challenge");
  }

  function mountFlashcards(root, cards) {
    if (!cards.length) {
      root.innerHTML = '<div class="empty-state bn">কোনো কার্ড নেই।</div>';
      return;
    }
    let i = 0;
    let showBack = false;
    let knows = 0;
    let hards = 0;
    if (window.EFBProgress) EFBProgress.setLastLesson("flashcards", "flash-session");

    function paint() {
      if (i >= cards.length) {
        const skillGuess = (cards[0] && String(cards[0].item_id || "").split(":")[0]) || "vocabulary";
        const skill =
          skillGuess === "pv" ? "phrasal" : skillGuess === "vocab" ? "vocabulary" : skillGuess;
        const actions =
          window.EFBApp && EFBApp.nextRoundActions
            ? EFBApp.nextRoundActions({ skill: skill })
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
            i = 0;
            knows = 0;
            hards = 0;
            showBack = false;
            paint();
          });
        }
        return;
      }
      const c = cards[i];
      if (c.item_id) EFBProgress.markSeen(c.item_id);
      root.innerHTML = `
        <div class="panel">
          <div class="quiz-meta">
            <span class="chip">${i + 1}/${cards.length}</span>
            <span class="muted bn">ট্যাপ করে উল্টান</span>
          </div>
          <div class="flash-card" id="card" role="button" tabindex="0">
            ${
              showBack
                ? `<div><div class="back-mean">${escape(c.back)}</div>
                   ${c.back_bn ? `<p class="bn muted">${escape(c.back_bn)}</p>` : ""}
                   ${c.example ? `<p class="example">${escape(c.example)}</p>` : ""}</div>`
                : `<div class="front-word">${escape(c.front)}</div>`
            }
          </div>
          <div class="stack-actions">
            <button type="button" class="btn btn-secondary" id="prev">আগে</button>
            <button type="button" class="btn btn-primary" id="flip">উল্টান</button>
            <button type="button" class="btn btn-secondary" id="next">পরে</button>
          </div>
          <div class="stack-actions">
            <button type="button" class="btn btn-accent" id="know">জানি · Got it</button>
            <button type="button" class="btn btn-secondary" id="hard">কঠিন · Again</button>
          </div>
        </div>
      `;

      const flip = () => {
        showBack = !showBack;
        paint();
      };
      root.querySelector("#card").addEventListener("click", flip);
      root.querySelector("#flip").addEventListener("click", flip);
      root.querySelector("#prev").addEventListener("click", () => {
        i = Math.max(0, i - 1);
        showBack = false;
        paint();
      });
      root.querySelector("#next").addEventListener("click", () => {
        i = i + 1;
        showBack = false;
        paint();
      });
      root.querySelector("#know").addEventListener("click", () => {
        if (c.item_id) EFBProgress.recordResult(c.item_id, true, "mcq");
        knows += 1;
        i = i + 1;
        showBack = false;
        paint();
      });
      root.querySelector("#hard").addEventListener("click", () => {
        if (c.item_id) EFBProgress.recordResult(c.item_id, false, "mcq");
        hards += 1;
        showBack = true;
        paint();
      });
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
