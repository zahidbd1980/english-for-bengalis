/**
 * localStorage progress — export/import + schema version
 */
(function (global) {
  const STORAGE_KEY = "efb_progress_v1";
  const VERSION = 1;

  function defaultState() {
    return {
      progress_version: VERSION,
      user_id: "local",
      settings: {
        ui_language: "mixed",
        accent: "us",
        daily_new_cap: 15,
        goal: "spoken_english",
        vocab_target: 2000,
      },
      profile: {
        estimated_level: null,
        placement_taken_at: null,
        last_lesson_id: null,
        last_skill: null,
      },
      streak: {
        current: 0,
        longest: 0,
        last_active_date: null,
      },
      items: {},
      mistakes: [],
      achievements: [],
      daily: {},
      challenge: {
        date: null,
        completed: false,
        item_ids: [],
        score: 0,
        total: 0,
      },
      // Mid-session resume slots (vocabulary, quiz, daily, flashcards, spelling, sentence, translate…)
      resume: {},
      // 14-day Learning Path progress
      path: {
        plan_id: null,
        day: 1,
        started_on: null,
        tasks_done: {},
        last_active_on: null,
      },
    };
  }

  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return defaultState();
      const data = JSON.parse(raw);
      if (!data.progress_version) data.progress_version = VERSION;
      const base = defaultState();
      return Object.assign(base, data, {
        settings: Object.assign(base.settings, data.settings || {}),
        profile: Object.assign(base.profile, data.profile || {}),
        streak: Object.assign(base.streak, data.streak || {}),
        challenge: Object.assign(base.challenge, data.challenge || {}),
        items: data.items || {},
        resume: Object.assign({}, base.resume, data.resume || {}),
        path: Object.assign({}, base.path, data.path || {}),
      });
    } catch (e) {
      console.warn("EFB storage load failed", e);
      return defaultState();
    }
  }

  function save(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    return state;
  }

  function update(mutator) {
    const state = load();
    mutator(state);
    return save(state);
  }

  /** Remap legacy item ids (e.g. v227 → vocab:agree) after schema fixes. */
  function applyIdMap(map) {
    if (!map || typeof map !== "object") return load();
    return update((state) => {
      const version = 2;
      if (state._id_migrate_ver >= version) return;
      const next = {};
      Object.keys(state.items || {}).forEach((id) => {
        const dest = map[id] || id;
        if (!next[dest]) next[dest] = state.items[id];
        else {
          const a = next[dest];
          const b = state.items[id];
          next[dest] =
            (b.mastery_score || 0) > (a.mastery_score || 0) ? Object.assign({}, a, b) : Object.assign({}, b, a);
        }
      });
      state.items = next;
      state.mistakes = (state.mistakes || []).map((id) => map[id] || id);
      state._id_migrate_ver = version;
      state._id_migrate_v1 = true;
    });
  }

  function exportJSON() {
    const state = load();
    state.exported_at = new Date().toISOString();
    return JSON.stringify(state, null, 2);
  }

  function importJSON(text) {
    const incoming = JSON.parse(text);
    if (!incoming || typeof incoming !== "object") {
      throw new Error("Invalid file");
    }
    const base = defaultState();
    const merged = Object.assign(base, incoming, {
      progress_version: VERSION,
      settings: Object.assign(base.settings, incoming.settings || {}),
      profile: Object.assign(base.profile, incoming.profile || {}),
      streak: Object.assign(base.streak, incoming.streak || {}),
      items: Object.assign({}, incoming.items || {}),
      mistakes: incoming.mistakes || [],
      challenge: Object.assign(base.challenge, incoming.challenge || {}),
      resume: Object.assign({}, base.resume, incoming.resume || {}),
      path: Object.assign({}, base.path, incoming.path || {}),
    });
    save(merged);
    return merged;
  }

  function reset() {
    localStorage.removeItem(STORAGE_KEY);
    return defaultState();
  }

  function downloadExport() {
    const blob = new Blob([exportJSON()], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "efb-progress-backup.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  global.EFBStorage = {
    STORAGE_KEY,
    load,
    save,
    update,
    applyIdMap,
    exportJSON,
    importJSON,
    reset,
    downloadExport,
    defaultState,
  };
})(window);
