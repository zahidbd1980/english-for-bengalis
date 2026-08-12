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
        if (item.status < STATUS.PRACTICED) item.status = STATUS.PRACTICED;
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
    setLevel,
    setGoal,
    todayStr,
    ensureItem,
  };
})(window);
