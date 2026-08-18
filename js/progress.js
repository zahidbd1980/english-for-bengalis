/**
 * Progress + mastery (Master Plan §24) + light SRS (§25)
 */
(function (global) {
  const STATUS = {
    NOT_STARTED: 0,
    SEEN: 1,
    LEARNING: 2,
    PRACTICED: 3,
    FAMILIAR: 4,
    MASTERED: 5,
    NEEDS_REVIEW: 6,
  };

  function todayStr() {
    return new Date().toISOString().slice(0, 10);
  }

  function addDays(dateStr, days) {
    const d = new Date(dateStr + "T12:00:00");
    d.setDate(d.getDate() + days);
    return d.toISOString().slice(0, 10);
  }

  function ensureItem(state, itemId) {
    if (!state.items[itemId]) {
      state.items[itemId] = {
        status: STATUS.NOT_STARTED,
        mastery_score: 0,
        attempts: 0,
        correct_count: 0,
        wrong_count: 0,
        productive_correct: 0,
        ease: 2.3,
        interval_days: 0,
        reps: 0,
        last_reviewed: null,
        next_review: null,
        lapses: 0,
        recent: [],
      };
    }
    return state.items[itemId];
  }

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function markSeen(itemId) {
    return EFBStorage.update((state) => {
      const item = ensureItem(state, itemId);
      if (item.mastery_score < 10) item.mastery_score = 10;
      if (item.status === STATUS.NOT_STARTED) item.status = STATUS.SEEN;
    });
  }

  function recordResult(itemId, correct, format) {
    return EFBStorage.update((state) => {
      const item = ensureItem(state, itemId);
      const now = Date.now();
      item.attempts += 1;
      item.recent.push({ correct: !!correct, t: now, format: format || "mcq" });
      if (item.recent.length > 5) item.recent.shift();

      if (correct) {
        item.correct_count += 1;
        const productive = format === "type" || format === "translate" || format === "speak";
        const gain = productive ? 12 : 8;
        if (productive) item.productive_correct += 1;
        item.mastery_score = clamp(item.mastery_score + gain, 0, 100);
        // Clear review flag on success; then recomputeStatus may raise to FAMILIAR/MASTERED
        if (item.status === STATUS.NEEDS_REVIEW || item.status < STATUS.PRACTICED) {
          item.status = STATUS.PRACTICED;
        }
        applySrsSuccess(item, "good");
        // Cleared mistakes drop out of Mistake Bank practice queue
        state.mistakes = (state.mistakes || []).filter((id) => id !== itemId);
      } else {
        item.wrong_count += 1;
        item.mastery_score = clamp(item.mastery_score - 15, 0, 100);
        item.status = STATUS.NEEDS_REVIEW;
        applySrsFail(item);
        pushMistake(state, itemId);
      }

      recomputeStatus(item);
      touchStreak(state);
    });
  }

  function applySrsFail(item) {
    item.reps = 0;
    item.interval_days = 1;
    item.ease = clamp(item.ease - 0.2, 1.3, 3);
    item.lapses += 1;
    item.last_reviewed = todayStr();
    item.next_review = addDays(todayStr(), 1);
  }

  function applySrsSuccess(item, grade) {
    item.reps += 1;
    if (item.reps === 1) item.interval_days = 1;
    else if (item.reps === 2) item.interval_days = 3;
    else {
      const mult = grade === "easy" ? item.ease * 1.3 : item.ease;
      item.interval_days = Math.max(1, Math.round(item.interval_days * mult));
    }
    item.ease = clamp(item.ease + (grade === "easy" ? 0.1 : 0.05), 1.3, 3);
    item.mastery_score = clamp(item.mastery_score + 10, 0, 100);
    item.last_reviewed = todayStr();
    item.next_review = addDays(todayStr(), item.interval_days);
  }

  function recomputeStatus(item) {
    const recentAcc =
      item.recent.length === 0
        ? 0
        : item.recent.filter((r) => r.correct).length / item.recent.length;

    if (
      item.mastery_score >= 80 &&
      item.productive_correct >= 2 &&
      item.reps >= 3 &&
      recentAcc >= 0.8
    ) {
      item.status = STATUS.MASTERED;
    } else if (item.mastery_score >= 60) {
      item.status = STATUS.FAMILIAR;
    } else if (item.mastery_score >= 30) {
      item.status = item.status === STATUS.NEEDS_REVIEW ? STATUS.NEEDS_REVIEW : STATUS.PRACTICED;
    } else if (item.attempts > 0) {
      item.status = item.status === STATUS.NEEDS_REVIEW ? STATUS.NEEDS_REVIEW : STATUS.LEARNING;
    }
  }

  function pushMistake(state, itemId) {
    if (!state.mistakes.includes(itemId)) state.mistakes.unshift(itemId);
    state.mistakes = state.mistakes.slice(0, 200);
  }

  function touchStreak(state) {
    const today = todayStr();
    const last = state.streak.last_active_date;
    if (last === today) return;
    if (!last) {
      state.streak.current = 1;
    } else {
      const yesterday = addDays(today, -1);
      state.streak.current = last === yesterday ? state.streak.current + 1 : 1;
    }
    state.streak.longest = Math.max(state.streak.longest, state.streak.current);
    state.streak.last_active_date = today;
  }

  function dueItems() {
    const state = EFBStorage.load();
    const today = todayStr();
    return Object.entries(state.items)
      .filter(([, item]) => item.next_review && item.next_review <= today)
      .map(([id, item]) => ({ id, ...item }));
  }

  function summarize(prefix) {
    const state = EFBStorage.load();
    const ids = Object.keys(state.items).filter((id) => id.startsWith(prefix));
    const mastered = ids.filter((id) => state.items[id].status === STATUS.MASTERED).length;
    const started = ids.filter((id) => state.items[id].status > STATUS.NOT_STARTED).length;
    return { started, mastered, totalTracked: ids.length };
  }

  function setLastLesson(skill, lessonId) {
    EFBStorage.update((state) => {
      state.profile.last_skill = skill;
      state.profile.last_lesson_id = lessonId;
    });
  }

  /**
   * Save where the learner stopped (vocab card, quiz Q#, flash index, etc.).
   * Survives browser close via localStorage / export-import.
   */
  function saveResume(skill, payload) {
    if (!skill || !payload) return;
    return EFBStorage.update((state) => {
      if (!state.resume) state.resume = {};
      const prev =
        state.resume[skill] && typeof state.resume[skill] === "object" ? state.resume[skill] : {};
      const byKey = Object.assign({}, prev.by_key || {});
      const now = new Date().toISOString();
      if (payload.key) {
        byKey[payload.key] = Object.assign({}, byKey[payload.key] || {}, {
          page_index: Number(payload.page_index) || 0,
          word_id: payload.word_id || null,
          label: payload.label || "",
          total: Number(payload.total) || 0,
          order_ids: payload.order_ids || null,
          shuffled: !!payload.shuffled,
          updated_at: now,
        });
      }
      const merged = Object.assign({}, prev, payload, {
        by_key: payload.by_key ? Object.assign(byKey, payload.by_key) : byKey,
        last_key: payload.key != null ? payload.key : prev.last_key || null,
        updated_at: now,
        active: payload.active !== false,
      });
      state.resume[skill] = merged;
      if (payload.touch_profile !== false) {
        state.profile.last_skill = payload.profile_skill || payload.skill || skill;
        if (payload.lesson_id) state.profile.last_lesson_id = payload.lesson_id;
      }
    });
  }

  function getResume(skill) {
    const state = EFBStorage.load();
    const r = state.resume && state.resume[skill];
    return r || null;
  }

  function clearResume(skill, key) {
    return EFBStorage.update((state) => {
      if (!state.resume || !state.resume[skill]) return;
      if (key && state.resume[skill].by_key) {
        delete state.resume[skill].by_key[key];
        if (state.resume[skill].last_key === key) {
          state.resume[skill].page_index = 0;
          state.resume[skill].word_id = null;
        }
      } else {
        state.resume[skill] = null;
      }
    });
  }

  function isResumeActive(r) {
    if (!r || r.active === false) return false;
    if (Array.isArray(r.q_ids) && r.q_ids.length) {
      return (Number(r.index) || 0) < r.q_ids.length;
    }
    if (Array.isArray(r.item_ids) && r.item_ids.length) {
      return (Number(r.index) || 0) < r.item_ids.length;
    }
    if (Array.isArray(r.queue_ids) && r.queue_ids.length) {
      return (Number(r.idx) || 0) < r.queue_ids.length;
    }
    if (r.phase && r.phase !== "done") {
      return !!(r.current || (r.mainQueue && r.mainQueue.length) || (r.wrongQueue && r.wrongQueue.length));
    }
    if (r.page_index != null && Number(r.total) > 0) {
      return (Number(r.page_index) || 0) < Number(r.total);
    }
    return false;
  }

  /** Newest active mid-session resume across skills. */
  function getBestResume() {
    const state = EFBStorage.load();
    const resume = state.resume || {};
    let best = null;
    Object.keys(resume).forEach((key) => {
      const r = resume[key];
      if (!isResumeActive(r)) return;
      if (!best || String(r.updated_at || "") > String(best.updated_at || "")) {
        best = Object.assign({ resume_skill: key }, r);
      }
    });
    return best;
  }

  function quizResumeHref(r) {
    if (r.mode === "review") return "quizzes.html?mode=review&resume=1";
    if (r.mode === "mistakes") return "quizzes.html?mode=mistakes&resume=1";
    let h = "quizzes.html?resume=1";
    if (r.skill && r.skill !== "quizzes" && r.skill !== "all") {
      h += "&skill=" + encodeURIComponent(r.skill);
    }
    if (r.item_id) h += "&item_id=" + encodeURIComponent(r.item_id);
    return h;
  }

  function resumeContinue(r, pagesPrefix) {
    if (!r) return null;
    const p = pagesPrefix || "";
    const n =
      (Number(
        r.index != null ? r.index : r.page_index != null ? r.page_index : r.idx != null ? r.idx : 0
      ) || 0) + 1;
    const t =
      Number(r.total) ||
      (r.q_ids && r.q_ids.length) ||
      (r.item_ids && r.item_ids.length) ||
      (r.queue_ids && r.queue_ids.length) ||
      (r.totalTarget ? Number(r.totalTarget) : 0) ||
      0;
    const label =
      "Continue · " + (r.label || r.resume_skill || "study") + (t ? " · " + n + "/" + t : "") + " →";
    if (r.href) {
      const path = String(r.href).replace(/^\//, "");
      return { href: p + path, label: label };
    }
    const key = r.resume_skill;
    const map = {
      vocabulary: "vocabulary.html",
      verbforms: "verb-forms.html?resume=1",
      flashcards:
        "flashcards.html?resume=1" +
        (r.skill ? "&skill=" + encodeURIComponent(r.skill) : "") +
        (r.list_id ? "&list=" + encodeURIComponent(r.list_id) : ""),
      spelling: "spelling-practice.html?resume=1",
      sentence: "sentence-builder.html?resume=1",
      daily: "daily-challenge.html?resume=1",
      translate: "translation-lab.html?resume=1",
      quiz: quizResumeHref(r),
      review: "quizzes.html?mode=review&resume=1",
      mistakes: "quizzes.html?mode=mistakes&resume=1",
      "mistakes-study": "common-mistakes.html",
      phrasal: "phrasal-verbs.html?resume=1",
    };
    return { href: p + (map[key] || "my-progress.html"), label: label };
  }

  function setLevel(level) {
    EFBStorage.update((state) => {
      state.profile.estimated_level = level;
      state.profile.placement_taken_at = new Date().toISOString();
    });
  }

  function setGoal(goal) {
    EFBStorage.update((state) => {
      state.settings.goal = goal;
    });
  }

  global.EFBProgress = {
    STATUS,
    markSeen,
    recordResult,
    dueItems,
    summarize,
    setLastLesson,
    saveResume,
    getResume,
    clearResume,
    isResumeActive,
    getBestResume,
    resumeContinue,
    setLevel,
    setGoal,
    todayStr,
    ensureItem,
  };
})(window);
