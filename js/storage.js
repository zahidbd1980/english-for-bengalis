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
    };
  }

  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return defaultState();
      const data = JSON.parse(raw);
      if (!data.progress_version) data.progress_version = VERSION;
      return Object.assign(defaultState(), data, {
        settings: Object.assign(defaultState().settings, data.settings || {}),
        profile: Object.assign(defaultState().profile, data.profile || {}),
        streak: Object.assign(defaultState().streak, data.streak || {}),
        challenge: Object.assign(defaultState().challenge, data.challenge || {}),
        items: data.items || {},
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
    exportJSON,
    importJSON,
    reset,
    downloadExport,
    defaultState,
  };
})(window);
