/**
 * Quiz engine — MCQ + type answer + mid-session resume
 */
(function (global) {
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function normalize(s) {
    return String(s || "")
      .trim()
      .toLowerCase()
      .replace(/[’']/g, "'")
      .replace(/[.?!…,;:]+$/g, "")
      .replace(/^["'“”]+|["'“”]+$/g, "")
      .replace(/\s+/g, " ");
  }

  function isCorrect(userAnswer, question) {
    const user = normalize(userAnswer);
    const accepted = [];
    if (question.answer != null) accepted.push(question.answer);
    if (Array.isArray(question.answers)) accepted.push(...question.answers);
    return accepted.some((a) => normalize(a) === user);
  }

  function qId(q) {
    return q.item_id || q.id || "q:" + normalize(q.question || "").slice(0, 80);
  }

  function wantsFresh() {
    try {
      const p = new URLSearchParams(location.search || "");
      return p.get("restart") === "1";
    } catch (e) {
      return false;
    }
  }

  function mount(root, config) {
    config = config || {};
    const resumeSkill = config.resumeSkill || config.skill || "quiz";
    const sessionTag =
      config.sessionTag ||
      [config.mode || "", config.skill || "", config.itemId || "", config.topic || ""].join("|");
    const pool = (config.questions || []).slice();
    const limit = config.limit || 10;

    let questions = [];
    let index = 0;
    let score = 0;
    let answered = false;
    let showResumeHint = false;
    let restored = false;

    const saved =
      !config.fresh &&
      !wantsFresh() &&
      window.EFBProgress &&
      EFBProgress.getResume(resumeSkill);

    if (
      saved &&
      Array.isArray(saved.q_ids) &&
      saved.q_ids.length &&
      saved.session_tag === sessionTag &&
      EFBProgress.isResumeActive(saved)
    ) {
      const byKey = {};
      pool.forEach((q) => {
        byKey[qId(q)] = q;
      });
      const ordered = saved.q_ids.map((id) => byKey[id]).filter(Boolean);
      if (ordered.length >= Math.max(1, Math.floor(saved.q_ids.length * 0.5))) {
        questions = ordered;
        index = Math.max(0, Math.min(questions.length - 1, Number(saved.index) || 0));
        score = Number(saved.score) || 0;
        showResumeHint = index > 0 || score > 0;
        restored = true;
      }
    }

    if (!questions.length) {
      questions = shuffle(pool).slice(0, limit);
      index = 0;
      score = 0;
    }

    if (!questions.length) {
      root.innerHTML =
        '<div class="empty-state bn">এই টপিকে এখনো কুইজ নেই। <a href="../pages/learn.html">শিখুন</a> থেকে অন্য লেসন দেখুন।</div>';
      return;
    }

    function persist() {
      if (!window.EFBProgress || index >= questions.length) return;
      EFBProgress.saveResume(resumeSkill, {
        q_ids: questions.map(qId),
        index: index,
        score: score,
        total: questions.length,
        session_tag: sessionTag,
        mode: config.mode || null,
        skill: config.skill || null,
        item_id: config.itemId || null,
        topic: config.topic || null,
        label: config.label || config.skill || resumeSkill,
        href: config.resumeHref || null,
        profile_skill: config.profileSkill || config.skill || resumeSkill,
        lesson_id: config.lessonId || "quiz-session",
        active: true,
      });
    }

    function restartFresh() {
      if (window.EFBProgress) EFBProgress.clearResume(resumeSkill);
      mount(root, Object.assign({}, config, { fresh: true }));
    }

    function render() {
      if (index >= questions.length) {
        renderResult();
        return;
      }
      persist();
      const q = questions[index];
      answered = false;
      const options =
        q.type === "type"
          ? ""
          : shuffle(q.options || [])
              .map(
                (opt, i) =>
                  `<button type="button" class="option" data-opt="${escapeAttr(opt)}" id="opt-${i}">${escapeHtml(opt)}</button>`
              )
              .join("");

      const resumeBanner =
        showResumeHint && restored
          ? `<div class="vocab-resume-banner bn" role="status">
              যেখানে থেমেছিলেন সেখান থেকে · <strong>${index + 1}</strong> / ${questions.length}
              <button type="button" class="btn btn-ghost" id="btn-quiz-restart">১ নম্বর থেকে শুরু</button>
            </div>`
          : "";

      root.innerHTML = `
        <div class="quiz-shell panel">
          <div class="quiz-meta">
            <span class="chip">${index + 1} / ${questions.length}</span>
            <span class="muted">Score: ${score}</span>
          </div>
          ${resumeBanner}
          <p class="quiz-question">${escapeHtml(q.question)}</p>
          ${q.question_bn ? `<p class="quiz-hint bn">${escapeHtml(q.question_bn)}</p>` : ""}
          ${
            q.type === "type"
              ? `<input class="type-input" id="type-answer" autocomplete="off" placeholder="Type your answer" />`
              : `<div class="options">${options}</div>`
          }
          <div class="stack-actions">
            <button type="button" class="btn btn-primary" id="check-btn">যাচাই করুন · Check</button>
          </div>
          <div class="feedback" id="feedback"></div>
        </div>
      `;

      const restartBtn = root.querySelector("#btn-quiz-restart");
      if (restartBtn) {
        restartBtn.addEventListener("click", () => {
          showResumeHint = false;
          restored = false;
          restartFresh();
        });
      }

      const checkBtn = root.querySelector("#check-btn");
      const optionBtns = [...root.querySelectorAll(".option")];
      let selected = null;

      optionBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
          if (answered) return;
          optionBtns.forEach((b) => b.classList.remove("selected"));
          btn.classList.add("selected");
          selected = btn.getAttribute("data-opt");
        });
      });

      checkBtn.addEventListener("click", () => {
        if (answered) {
          showResumeHint = false;
          index += 1;
          render();
          return;
        }
        let userAnswer = selected;
        if (q.type === "type") {
          userAnswer = root.querySelector("#type-answer").value;
        }
        if (userAnswer == null || String(userAnswer).trim() === "") {
          const fb = root.querySelector("#feedback");
          fb.className = "feedback show bad bn";
          fb.textContent = "আগে উত্তর দিন।";
          return;
        }

        const ok = isCorrect(userAnswer, q);

        answered = true;
        if (ok) score += 1;

        if (q.item_id && window.EFBProgress) {
          EFBProgress.recordResult(q.item_id, ok, q.type === "type" ? "type" : "mcq");
        }

        optionBtns.forEach((btn) => {
          btn.disabled = true;
          const val = btn.getAttribute("data-opt");
          if (normalize(val) === normalize(q.answer)) btn.classList.add("correct");
          else if (btn.classList.contains("selected") && !ok) btn.classList.add("wrong");
        });

        const fb = root.querySelector("#feedback");
        fb.className = "feedback show " + (ok ? "ok" : "bad");
        fb.innerHTML = ok
          ? `<strong>সঠিক!</strong> ${escapeHtml(q.explanation || "")}`
          : `<strong>ভুল।</strong> সঠিক উত্তর: <em>${escapeHtml(q.answer)}</em><br>${escapeHtml(q.explanation || "")}`;

        checkBtn.textContent = index + 1 >= questions.length ? "ফলাফল দেখুন · Results" : "পরবর্তী · Next";
        persist();
      });
    }

    function renderResult() {
      const pct = Math.round((score / questions.length) * 100);
      const skill = config.skill || (questions[0] && questions[0].skill) || "quizzes";
      if (window.EFBProgress) {
        EFBProgress.clearResume(resumeSkill);
        EFBProgress.setLastLesson(skill, "quiz-session");
      }
      const actions =
        window.EFBApp && EFBApp.nextRoundActions
          ? EFBApp.nextRoundActions({ skill: skill })
          : `<div class="stack-actions">
            <button type="button" class="btn btn-primary" data-next="retry">আবার করুন</button>
            <a class="btn btn-secondary" href="../pages/my-progress.html">প্রোগ্রেস</a>
          </div>`;
      root.innerHTML = `
        <div class="panel highlight quiz-shell">
          <p class="chip">Quiz complete</p>
          <h2 class="page-title" style="font-size:1.8rem">স্কোর: ${score}/${questions.length} (${pct}%)</h2>
          <p class="muted bn">প্রোগ্রেস সেভ হয়েছে। নিচ থেকে পরের ধাপ বেছে নিন।</p>
          ${actions}
        </div>
      `;
      const retry = root.querySelector('[data-next="retry"]');
      if (retry) {
        retry.addEventListener("click", () => {
          mount(root, Object.assign({}, config, { fresh: true }));
        });
      }
      if (typeof config.onComplete === "function") config.onComplete({ score, total: questions.length });
    }

    render();
  }

  function escapeHtml(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function escapeAttr(str) {
    return escapeHtml(str).replace(/'/g, "&#39;");
  }

  global.EFBQuiz = { mount, shuffle, normalize, isCorrect, qId };
})(window);
