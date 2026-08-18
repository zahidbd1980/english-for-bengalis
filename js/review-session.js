/**
 * Review due + Mistake Bank session builders (Master Plan §141 / Phase 4 start)
 * Builds quiz-shaped questions from progress IDs + content banks.
 */
(function (global) {
  function shuffle(arr) {
    const a = (arr || []).slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function asList(data) {
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.words)) return data.words;
    return [];
  }

  function indexById(lists) {
    const map = {};
    (lists || []).forEach((list) => {
      asList(list).forEach((item) => {
        if (item && item.id) map[item.id] = item;
      });
    });
    return map;
  }

  function quizByItemId(quizzes) {
    const map = {};
    (quizzes || []).forEach((q) => {
      if (q.item_id && !map[q.item_id]) map[q.item_id] = q;
    });
    return map;
  }

  function distractors(pool, correct, pickKey, n) {
    const correctN = String(correct || "").toLowerCase();
    const others = shuffle(
      pool
        .map((x) => (typeof pickKey === "function" ? pickKey(x) : x[pickKey]))
        .filter((v) => v && String(v).toLowerCase() !== correctN)
    );
    return others.slice(0, n);
  }

  function fromVocab(item, bank) {
    const meaning = item.meaning_en || item.meaning_bn || "";
    const opts = shuffle([meaning].concat(distractors(bank, meaning, "meaning_en", 3))).slice(0, 4);
    while (opts.length < 4) opts.push("—");
    return {
      id: "gen:" + item.id,
      type: "mcq",
      skill: "vocabulary",
      item_id: item.id,
      question: 'What does "' + item.word + '" mean?',
      question_bn: '"' + item.word + '" শব্দের অর্থ কী?',
      options: opts,
      answer: meaning,
      explanation: (item.meaning_bn || "") + (item.example ? " · " + item.example : ""),
    };
  }

  function fromPhrasal(item, bank) {
    const meaning = item.meaning_en || item.meaning_bn || "";
    const opts = shuffle([meaning].concat(distractors(bank, meaning, "meaning_en", 3))).slice(0, 4);
    while (opts.length < 4) opts.push("—");
    return {
      id: "gen:" + item.id,
      type: "mcq",
      skill: "phrasal",
      item_id: item.id,
      question: '"' + item.phrase + '" means:',
      question_bn: '"' + item.phrase + '" মানে?',
      options: opts,
      answer: meaning,
      explanation: item.meaning_bn || "",
    };
  }

  function fromSpelling(item) {
    return {
      id: "gen:" + item.id,
      type: "type",
      skill: "spelling",
      item_id: item.id,
      question: "Type the correct spelling" + (item.meaning_bn ? " (" + item.meaning_bn + ")" : "") + ":",
      question_bn: "সঠিক বানান লিখুন",
      answer: item.correct_word,
      answers: [item.correct_word],
      explanation: item.memory_tip || ("Correct: " + item.correct_word),
    };
  }

  function fromMistake(item) {
    const wrong = item.incorrect;
    const right = item.correct;
    const opts = shuffle([right, wrong]).concat(["Both are fine.", "Neither is correct."]).slice(0, 4);
    // keep exactly 4 unique-ish
    const uniq = [];
    opts.forEach((o) => {
      if (uniq.indexOf(o) === -1) uniq.push(o);
    });
    while (uniq.length < 4) uniq.push("I am not sure.");
    return {
      id: "gen:" + item.id,
      type: "mcq",
      skill: "mistakes",
      item_id: item.id,
      question: "Choose the correct English:",
      question_bn: "সঠিক বাক্য বেছে নিন:" + (item.bangla_tip ? " (" + item.bangla_tip + ")" : ""),
      options: uniq.slice(0, 4),
      answer: right,
      explanation: item.explanation || item.bangla_tip || "",
    };
  }

  function fromGrammar(item) {
    const errs = item.common_errors || [];
    const raw = String(errs[0] || "");
    const pair = raw.split(/\s*→\s*/);
    if (pair.length >= 2) {
      const wrong = pair[0].replace(/^.*?:\s*/, "").trim();
      const right = pair[1].trim();
      const opts = [];
      [right, wrong, "Both are fine.", "I am not sure."].forEach(function (o) {
        if (o && opts.indexOf(o) === -1) opts.push(o);
      });
      while (opts.length < 4) opts.push("—");
      return {
        id: "gen:" + item.id,
        type: "mcq",
        skill: "grammar",
        item_id: item.id,
        question: "Choose the correct sentence (" + (item.topic || "grammar") + "):",
        question_bn: "সঠিক বাক্য বেছে নিন",
        options: shuffle(opts).slice(0, 4),
        answer: right,
        explanation: item.explanation || item.bangla_explanation || raw,
      };
    }
    const tip = errs[0] || item.topic;
    return {
      id: "gen:" + item.id,
      type: "type",
      skill: "grammar",
      item_id: item.id,
      question: "Type the grammar topic name (English): " + (item.bangla_explanation || "").slice(0, 80),
      question_bn: "টপিকের ইংরেজি নাম লিখুন",
      answer: item.topic,
      answers: [item.topic],
      explanation: item.explanation || tip || "",
    };
  }

  function generateFromItem(item, banks) {
    if (!item || !item.id) return null;
    const id = item.id;
    if (id.indexOf("vocab:") === 0) return fromVocab(item, banks.vocab || []);
    if (id.indexOf("pv:") === 0) return fromPhrasal(item, banks.phrasal || []);
    if (id.indexOf("spell:") === 0 || item.correct_word) return fromSpelling(item);
    if (id.indexOf("mistake:") === 0) return fromMistake(item);
    if (id.indexOf("grammar:") === 0) return fromGrammar(item);
    return null;
  }

  function resolveQuestion(itemId, banks, quizMap) {
    if (quizMap[itemId]) return Object.assign({}, quizMap[itemId]);
    const item = banks.byId[itemId];
    if (!item) return null;
    return generateFromItem(item, banks);
  }

  /**
   * @param {object} opts
   * @param {"review"|"mistakes"} opts.mode
   * @param {array} opts.quizzes
   * @param {object} opts.banks raw JSON loads
   * @param {number} [opts.limit]
   */
  function buildSession(opts) {
    opts = opts || {};
    const vocab = asList(opts.banks && opts.banks.vocab);
    const phrasal = asList(opts.banks && opts.banks.phrasal);
    const spelling = asList(opts.banks && opts.banks.spelling);
    const grammar = asList(opts.banks && opts.banks.grammar);
    const mistakesBank = asList(opts.banks && opts.banks.mistakes);
    const byId = indexById([vocab, phrasal, spelling, grammar, mistakesBank]);
    const quizMap = quizByItemId(opts.quizzes || []);
    const pack = { byId: byId, vocab: vocab, phrasal: phrasal };

    let ids = [];
    if (opts.mode === "mistakes") {
      const state = global.EFBStorage ? EFBStorage.load() : { mistakes: [] };
      ids = (state.mistakes || []).slice();
    } else if (opts.mode === "weak") {
      ids = weakAreas(opts.limit || 10).map((w) => w.id);
    } else {
      const due = global.EFBProgress ? EFBProgress.dueItems() : [];
      ids = due.map((d) => d.id);
      // also include NEEDS_REVIEW without next_review
      if (global.EFBStorage) {
        const state = EFBStorage.load();
        Object.keys(state.items || {}).forEach((id) => {
          const it = state.items[id];
          if (it && it.status === 6 && ids.indexOf(id) === -1) ids.push(id);
        });
      }
    }

    const questions = [];
    const seen = {};
    shuffle(ids).forEach((id) => {
      if (seen[id]) return;
      const q = resolveQuestion(id, pack, quizMap);
      if (q) {
        seen[id] = true;
        questions.push(q);
      }
    });

    // Fallback: if review empty, offer mixed weak/low-mastery items
    if (!questions.length && (opts.mode === "review" || opts.mode === "weak") && global.EFBStorage) {
      const state = EFBStorage.load();
      const weak = Object.entries(state.items || {})
        .filter(([, it]) => it.attempts > 0 && it.mastery_score < 60)
        .sort((a, b) => a[1].mastery_score - b[1].mastery_score)
        .map(([id]) => id);
      weak.forEach((id) => {
        if (questions.length >= (opts.limit || 10)) return;
        const q = resolveQuestion(id, pack, quizMap);
        if (q) questions.push(q);
      });
    }

    const titles = {
      mistakes: { title: "Mistake Bank practice", title_bn: "Mistake Bank অনুশীলন" },
      weak: { title: "Weak areas practice", title_bn: "দুর্বল অংশ অনুশীলন" },
      review: { title: "Review due", title_bn: "রিভিউ সেশন" },
    };
    const t = titles[opts.mode] || titles.review;

    return {
      ids: ids,
      questions: questions.slice(0, opts.limit || 10),
      title: t.title,
      title_bn: t.title_bn,
    };
  }

  function weakAreas(limit) {
    if (!global.EFBStorage) return [];
    const state = EFBStorage.load();
    const rows = Object.entries(state.items || {})
      .filter(([, it]) => (it.wrong_count || 0) > 0 || it.status === 6 || (it.mastery_score > 0 && it.mastery_score < 50))
      .map(([id, it]) => ({
        id: id,
        wrong_count: it.wrong_count || 0,
        mastery_score: it.mastery_score || 0,
        status: it.status,
      }))
      .sort((a, b) => b.wrong_count - a.wrong_count || a.mastery_score - b.mastery_score);
    return rows.slice(0, limit || 5);
  }

  global.EFBReview = {
    buildSession: buildSession,
    weakAreas: weakAreas,
    generateFromItem: generateFromItem,
    questionsFromItems: questionsFromItems,
    asList: asList,
  };

  function questionsFromItems(items, banks, quizzes, limit) {
    const quizMap = quizByItemId(quizzes || []);
    const pack = {
      byId: (banks && banks.byId) || {},
      vocab: asList(banks && banks.vocab),
      phrasal: asList(banks && banks.phrasal),
    };
    const out = [];
    const cap = limit || 10;
    shuffle(items || []).forEach((item) => {
      if (out.length >= cap) return;
      if (!item) return;
      const id = item.id;
      let q = id && quizMap[id] ? Object.assign({}, quizMap[id]) : generateFromItem(item, pack);
      if (q) out.push(q);
    });
    return out;
  }
})(window);
