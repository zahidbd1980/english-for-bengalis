/**
 * Spelling Practice engine — listen → type → correct/wrong mastery loop
 * No main-list repeats; wrong queue until all correct.
 */
(function (global) {
  function dedupe(words) {
    const seen = new Set();
    const out = [];
    words.forEach((w) => {
      const n = normalize(w);
      if (!n || seen.has(n)) return;
      seen.add(n);
      out.push(n);
    });
    return out;
  }

  function normalize(s) {
    return String(s || "")
      .trim()
      .toLowerCase()
      .replace(/[’']/g, "'")
      .replace(/\s+/g, " ");
  }

  // Accept common US/UK pairs so learners are not marked wrong unfairly
  const SPELLING_ALTS = {
    neighbour: ["neighbor"],
    neighbor: ["neighbour"],
    favourite: ["favorite"],
    favorite: ["favourite"],
    recognise: ["recognize"],
    recognize: ["recognise"],
    jewellery: ["jewelry"],
    jewelry: ["jewellery"],
    colour: ["color"],
    color: ["colour"],
    centre: ["center"],
    center: ["centre"],
    judgement: ["judgment"],
    judgment: ["judgement"],
    licence: ["license"],
    license: ["licence"],
    manoeuvre: ["maneuver"],
    maneuver: ["manoeuvre"],
    practise: ["practice"],
    practice: ["practise"],
  };

  function answersMatch(user, target) {
    const u = normalize(user);
    const t = normalize(target);
    if (u === t) return true;
    const alts = SPELLING_ALTS[t] || [];
    return alts.some((a) => normalize(a) === u);
  }

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function speak(word, opts) {
    return new Promise((resolve) => {
      if (!global.speechSynthesis) {
        resolve(false);
        return;
      }
      global.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(word);
      u.lang = (opts && opts.lang) || "en-GB";
      u.rate = opts && opts.slow ? 0.7 : 0.95;
      u.onend = () => resolve(true);
      u.onerror = () => resolve(false);
      // Prefer matching voice
      const voices = global.speechSynthesis.getVoices() || [];
      const pref = voices.find((v) => v.lang && v.lang.toLowerCase().startsWith(u.lang.slice(0, 2)));
      if (pref) u.voice = pref;
      global.speechSynthesis.speak(u);
    });
  }

  function createSession(words) {
    const unique = shuffle(dedupe(words));
    return {
      mainQueue: unique.slice(),
      wrongQueue: [],
      correct: [],
      current: null,
      phase: "main", // main | wrong | done
      attempts: 0,
      startedAt: Date.now(),
      lastResult: null, // correct | wrong
      revealed: null,
      totalTarget: unique.length,
    };
  }

  function nextWord(session) {
    session.lastResult = null;
    session.revealed = null;
    if (session.mainQueue.length) {
      session.phase = "main";
      session.current = session.mainQueue.shift();
      return session.current;
    }
    if (session.wrongQueue.length) {
      session.phase = "wrong";
      session.current = session.wrongQueue.shift();
      return session.current;
    }
    session.phase = "done";
    session.current = null;
    return null;
  }

  function check(session, answer) {
    if (!session.current) return { ok: false, done: true };
    session.attempts += 1;
    const ok = answersMatch(answer, session.current);
    if (ok) {
      if (!session.correct.includes(session.current)) session.correct.push(session.current);
      session.lastResult = "correct";
      session.revealed = session.current;
      if (window.EFBProgress) {
        EFBProgress.recordResult("spell:" + session.current, true, "type");
        EFBProgress.setLastLesson("spelling", "spelling-practice");
      }
    } else {
      session.wrongQueue.push(session.current);
      session.lastResult = "wrong";
      session.revealed = session.current;
      if (window.EFBProgress) {
        EFBProgress.recordResult("spell:" + session.current, false, "type");
      }
    }
    return {
      ok,
      word: session.current,
      remainingMain: session.mainQueue.length,
      remainingWrong: session.wrongQueue.length,
      correctCount: session.correct.length,
    };
  }

  function stats(session) {
    const total = session.correct.length + session.mainQueue.length + session.wrongQueue.length + (session.current && session.lastResult == null ? 1 : 0);
    // better total = initial size stored separately; compute from correct+queues+current if mid
    return {
      correct: session.correct.length,
      wrongQueued: session.wrongQueue.length,
      mainLeft: session.mainQueue.length,
      phase: session.phase,
      attempts: session.attempts,
    };
  }

  function parseCustomText(text) {
    return dedupe(
      String(text || "")
        .split(/[\n,;]+/)
        .map((x) => x.trim())
        .filter(Boolean)
    );
  }

  global.EFBSpelling = {
    dedupe,
    normalize,
    answersMatch,
    shuffle,
    speak,
    createSession,
    nextWord,
    check,
    stats,
    parseCustomText,
  };
})(window);
