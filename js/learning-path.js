/**
 * Learning Path — 14-day daily plan (localStorage via EFBStorage)
 */
(function (global) {
  function todayStr() {
    return window.EFBProgress ? EFBProgress.todayStr() : new Date().toISOString().slice(0, 10);
  }

  function defaultPath() {
    return {
      plan_id: null,
      day: 1,
      started_on: null,
      tasks_done: {},
      last_active_on: null,
    };
  }

  function getState() {
    const s = EFBStorage.load();
    if (!s.path) s.path = defaultPath();
    return s;
  }

  function ensurePath(planId) {
    return EFBStorage.update((state) => {
      if (!state.path) state.path = defaultPath();
      if (!state.path.plan_id) {
        state.path.plan_id = planId || "foundation-14";
        state.path.day = 1;
        state.path.started_on = todayStr();
        state.path.tasks_done = state.path.tasks_done || {};
      }
      state.path.last_active_on = todayStr();
    });
  }

  function resetPath(planId) {
    return EFBStorage.update((state) => {
      state.path = {
        plan_id: planId || "foundation-14",
        day: 1,
        started_on: todayStr(),
        tasks_done: {},
        last_active_on: todayStr(),
      };
    });
  }

  function findPlan(data, planId) {
    const plans = (data && data.plans) || [];
    return (
      plans.find((p) => p.id === planId) ||
      plans.find((p) => p.id === (data && data.default_plan_id)) ||
      plans[0] ||
      null
    );
  }

  function daySpec(plan, dayNum) {
    if (!plan) return null;
    return (plan.days || []).find((d) => Number(d.day) === Number(dayNum)) || null;
  }

  function doneSet(path, dayNum) {
    const key = String(dayNum);
    const arr = (path.tasks_done && path.tasks_done[key]) || [];
    return new Set(arr);
  }

  function markTask(dayNum, taskId, done) {
    return EFBStorage.update((state) => {
      if (!state.path) state.path = defaultPath();
      if (!state.path.tasks_done) state.path.tasks_done = {};
      const key = String(dayNum);
      const set = new Set(state.path.tasks_done[key] || []);
      if (done === false) set.delete(taskId);
      else set.add(taskId);
      state.path.tasks_done[key] = Array.from(set);
      state.path.last_active_on = todayStr();
      if (window.EFBProgress) {
        state.profile.last_skill = "path";
        state.profile.last_lesson_id = "day-" + dayNum;
      }
    });
  }

  function dayComplete(path, plan, dayNum) {
    const spec = daySpec(plan, dayNum);
    if (!spec || !spec.tasks || !spec.tasks.length) return false;
    const done = doneSet(path, dayNum);
    return spec.tasks.every((t) => done.has(t.id));
  }

  function advanceDay(plan) {
    return EFBStorage.update((state) => {
      if (!state.path) return;
      const max = (plan && plan.days && plan.days.length) || 14;
      if (!dayComplete(state.path, plan, state.path.day)) return;
      if (state.path.day < max) state.path.day = Number(state.path.day) + 1;
      state.path.last_active_on = todayStr();
    });
  }

  function snapshot(data) {
    const state = getState();
    const path = state.path || defaultPath();
    const plan = findPlan(data, path.plan_id || (data && data.default_plan_id));
    const day = Math.max(1, Number(path.day) || 1);
    const spec = daySpec(plan, day);
    const done = doneSet(path, day);
    const tasks = ((spec && spec.tasks) || []).map((t) =>
      Object.assign({}, t, { done: done.has(t.id) })
    );
    const doneCount = tasks.filter((t) => t.done).length;
    const total = tasks.length;
    const complete = total > 0 && doneCount === total;
    const maxDay = (plan && plan.days && plan.days.length) || 14;
    return {
      state: path,
      plan: plan,
      day: day,
      spec: spec,
      tasks: tasks,
      doneCount: doneCount,
      total: total,
      complete: complete,
      maxDay: maxDay,
      started: !!path.plan_id,
      finishedPlan: complete && day >= maxDay,
    };
  }

  function continueHint(data, pagesPrefix) {
    const snap = snapshot(data);
    const p = pagesPrefix || "";
    if (!snap.started) {
      return {
        href: p + "learning-path.html",
        label: "Learning Path শুরু করুন →",
        pending: true,
      };
    }
    if (snap.finishedPlan) {
      return {
        href: p + "learning-path.html",
        label: "১৪ দিন শেষ · আবার দেখুন →",
        pending: false,
      };
    }
    if (!snap.complete) {
      return {
        href: p + "learning-path.html",
        label: "আজকের প্ল্যান · Day " + snap.day + " · " + snap.doneCount + "/" + snap.total + " →",
        pending: true,
      };
    }
    return {
      href: p + "learning-path.html",
      label: "Day " + snap.day + " শেষ · পরের দিন আনলক →",
      pending: true,
    };
  }

  global.EFBPath = {
    todayStr,
    ensurePath,
    resetPath,
    findPlan,
    markTask,
    dayComplete,
    advanceDay,
    snapshot,
    continueHint,
  };
})(window);
