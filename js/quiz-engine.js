/**
 * Quiz engine — MCQ + type answer
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

  function mount(root, config) {
    const questions = shuffle(config.questions || []).slice(0, config.limit || 10);
    if (!questions.length) {
      root.innerHTML =
        '<div class="empty-state bn">এই টপিকে এখনো কুইজ নেই। <a href="../pages/learn.html">শিখুন</a> থেকে অন্য লেসন দেখুন।</div>';
      return;
    }

    let index = 0;
    let score = 0;
    let answered = false;

    function render() {
      if (index >= questions.length) {
        renderResult();
        return;
      }
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

      root.innerHTML = `
        <div class="quiz-shell panel">
          <div class="quiz-meta">
            <span class="chip">${index + 1} / ${questions.length}</span>
            <span class="muted">Score: ${score}</span>
          </div>
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
      });
    }

    function renderResult() {
      const pct = Math.round((score / questions.length) * 100);
      root.innerHTML = `
        <div class="panel highlight quiz-shell">
          <p class="chip">Quiz complete</p>
          <h2 class="page-title" style="font-size:1.8rem">স্কোর: ${score}/${questions.length} (${pct}%)</h2>
          <p class="muted bn">প্রোগ্রেস আপডেট হয়েছে। নিয়মিত রিভিউ করলে mastery বাড়বে।</p>
          <div class="stack-actions">
            <a class="btn btn-primary" href="../pages/my-progress.html">প্রোগ্রেস দেখুন</a>
            <button type="button" class="btn btn-secondary" id="retry">আবার করুন</button>
            <a class="btn btn-ghost" href="../pages/practice.html">Practice hub</a>
          </div>
        </div>
      `;
      root.querySelector("#retry").addEventListener("click", () => {
        index = 0;
        score = 0;
        mount(root, config);
      });
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

  global.EFBQuiz = { mount, shuffle, normalize, isCorrect };
})(window);
