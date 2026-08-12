/**
 * Vocabulary helpers — filter, TTS, custom lists, bank normalize
 */
(function (global) {
  const SAVED_KEY = "efb_vocab_my_lists_v1";

  function asWords(data) {
    const list = Array.isArray(data) ? data : data && Array.isArray(data.words) ? data.words : [];
    return list.map((w) => {
      if (!w || typeof w !== "object") return w;
      const out = Object.assign({}, w);
      if (!out.cefr_level && out.cefr) out.cefr_level = out.cefr;
      if (!out.part_of_speech && out.pos) out.part_of_speech = out.pos;
      if (!out.category) {
        const tags = out.tags || [];
        out.category = tags[0] || "general";
      }
      if (out.id && !String(out.id).startsWith("vocab:") && out.word) {
        out.id = "vocab:" + normalizeWord(out.word).replace(/\s+/g, "-");
      }
      out.synonyms = out.synonyms || [];
      out.antonyms = out.antonyms || [];
      out.word_family = out.word_family || [];
      return out;
    });
  }

  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function normalizeWord(s) {
    return String(s || "")
      .trim()
      .toLowerCase()
      .replace(/[’']/g, "'");
  }

  function speak(text, opts) {
    return new Promise((resolve) => {
      if (!global.speechSynthesis) {
        resolve(false);
        return;
      }
      global.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(String(text || ""));
      u.lang = (opts && opts.lang) || "en-GB";
      u.rate = opts && opts.slow ? 0.72 : 0.95;
      u.onend = () => resolve(true);
      u.onerror = () => resolve(false);
      const voices = global.speechSynthesis.getVoices() || [];
      const pref =
        voices.find((v) => v.lang && v.lang.toLowerCase().startsWith(u.lang.slice(0, 2).toLowerCase())) ||
        voices.find((v) => /en/i.test(v.lang || ""));
      if (pref) u.voice = pref;
      global.speechSynthesis.speak(u);
    });
  }

  function loadSavedLists() {
    try {
      return JSON.parse(localStorage.getItem(SAVED_KEY) || "[]");
    } catch (e) {
      return [];
    }
  }

  function saveSavedLists(lists) {
    localStorage.setItem(SAVED_KEY, JSON.stringify(lists || []));
  }

  function parseCustomText(text) {
    const lines = String(text || "")
      .split(/[\n,;]+/)
      .map((x) => x.trim())
      .filter(Boolean);
    const seen = new Set();
    const out = [];
    lines.forEach((line) => {
      // accept "word — meaning" or plain word
      const word = line.split(/[—\-–|:]/)[0].trim();
      const n = normalizeWord(word);
      if (!n || seen.has(n)) return;
      seen.add(n);
      out.push(word);
    });
    return out;
  }

  function indexByWord(bank) {
    const map = {};
    (bank || []).forEach((w) => {
      map[normalizeWord(w.word)] = w;
    });
    return map;
  }

  function resolveCustomWords(wordStrings, bank) {
    const map = indexByWord(bank);
    return wordStrings.map((raw) => {
      const hit = map[normalizeWord(raw)];
      if (hit) return Object.assign({}, hit);
      return {
        id: "custom:" + normalizeWord(raw),
        word: raw,
        meaning_en: "(custom word — add your own meaning while studying)",
        meaning_bn: "(কাস্টম শব্দ — নিজে অর্থ নোট করুন)",
        part_of_speech: "—",
        cefr_level: "—",
        category: "custom",
        example: "",
        example_bn: "",
        synonyms: [],
        antonyms: [],
        word_family: [],
        custom: true,
      };
    });
  }

  function filterWords(bank, opts) {
    opts = opts || {};
    let list = (bank || []).slice();

    if (opts.wordIds && opts.wordIds.length) {
      const set = new Set(opts.wordIds);
      list = list.filter((w) => set.has(w.id));
    }
    if (opts.category && opts.category !== "all") {
      list = list.filter((w) => w.category === opts.category);
    }
    if (opts.pos && opts.pos !== "all") {
      list = list.filter((w) => String(w.part_of_speech || "").toLowerCase().indexOf(opts.pos) !== -1);
    }
    if (opts.level && opts.level !== "all") {
      list = list.filter((w) => w.cefr_level === opts.level);
    }
    if (opts.q) {
      const q = normalizeWord(opts.q);
      list = list.filter((w) => {
        const fam = (w.word_family || []).map((f) => [f.word, f.meaning_bn, f.pos].join(" ")).join(" ");
        const blob = [w.word, w.meaning_en, w.meaning_bn, w.example, (w.synonyms || []).join(" "), (w.antonyms || []).join(" "), fam]
          .join(" ")
          .toLowerCase();
        return blob.indexOf(q) !== -1;
      });
    }
    if (opts.onlyWithAntonyms) {
      list = list.filter((w) => (w.antonyms || []).length);
    }
    return list;
  }

  function cardHTML(w) {
    const syn = (w.synonyms || []).filter(Boolean);
    const ant = (w.antonyms || []).filter(Boolean);
    const head = normalizeWord(w.word);
    const family = (w.word_family || []).filter((f) => f && f.word && normalizeWord(f.word) !== head);
    const familyBlock = family.length
      ? `<div class="vocab-family" aria-label="Word family">
          <p class="vocab-family-title"><span class="rel-label">Word family</span> <span class="bn muted">শব্দ পরিবার</span></p>
          <ul class="vocab-family-list">
            ${family
              .map((f) => {
                const pos = f.pos ? ` <span class="vocab-family-pos">(${esc(f.pos)})</span>` : "";
                const bn = f.meaning_bn ? ` <span class="bn muted">— ${esc(f.meaning_bn)}</span>` : "";
                return `<li><strong class="vocab-family-word">${esc(f.word)}</strong>${pos}${bn}
                  <button type="button" class="btn-speak-inline btn-speak" data-speak="${esc(f.word)}" aria-label="Pronounce ${esc(f.word)}">🔊</button>
                </li>`;
              })
              .join("")}
          </ul>
        </div>`
      : "";
    return `
      <article class="panel vocab-card vocab-card-focus" data-id="${esc(w.id)}" data-word="${esc(w.word)}">
        <div class="quiz-meta">
          <strong class="vocab-word">${esc(w.word)}</strong>
          <span class="chip">${esc(w.cefr_level)}</span>
          <span class="chip">${esc(w.part_of_speech)}</span>
          <span class="chip chip-accent">${esc(w.category)}</span>
        </div>
        <div class="stack-actions vocab-actions">
          <button type="button" class="btn btn-secondary btn-speak" data-speak="${esc(w.word)}" aria-label="Pronounce ${esc(w.word)}">🔊 উচ্চারণ</button>
          <button type="button" class="btn btn-ghost btn-speak-slow" data-speak="${esc(w.word)}" data-slow="1">ধীরে</button>
        </div>
        <p class="vocab-meaning"><strong>${esc(w.meaning_en)}</strong></p>
        <p class="bn muted vocab-meaning-bn">${esc(w.meaning_bn)}</p>
        ${
          w.example
            ? `<div class="example">${esc(w.example)}${w.example_bn ? `<br><span class="bn muted">${esc(w.example_bn)}</span>` : ""}</div>`
            : ""
        }
        ${familyBlock}
        <div class="vocab-relations">
          ${
            syn.length
              ? `<p class="vocab-rel"><span class="rel-label">Similar</span> ${syn.map((s) => `<span class="chip">${esc(s)}</span>`).join(" ")}</p>`
              : ""
          }
          ${
            ant.length
              ? `<p class="vocab-rel"><span class="rel-label">Opposite</span> ${ant.map((s) => `<span class="chip">${esc(s)}</span>`).join(" ")}</p>`
              : ""
          }
        </div>
      </article>`;
  }

  global.EFBVocab = {
    asWords,
    esc,
    speak,
    loadSavedLists,
    saveSavedLists,
    parseCustomText,
    resolveCustomWords,
    filterWords,
    cardHTML,
    normalizeWord,
  };
})(window);
