/**
 * Homepage v2 — streak, word of the day, quiz teaser, countdown
 * Prefix: EFBHomeV2  |  CSS: .efb-v2-*
 */
(function (global) {
  var WOTD_FALLBACK = [
    {
      word: "improve",
      meaning_bn: "উন্নত করা",
      meaning_en: "to make better",
      example: "I want to improve my English.",
      example_bn: "আমি আমার ইংরেজি উন্নত করতে চাই।"
    },
    {
      word: "confident",
      meaning_bn: "আত্মবিশ্বাসী",
      meaning_en: "sure of yourself",
      example: "She feels confident in interviews.",
      example_bn: "সে ইন্টারভিউতে আত্মবিশ্বাসী বোধ করে।"
    },
    {
      word: "deadline",
      meaning_bn: "শেষ সময়সীমা",
      meaning_en: "the latest time to finish something",
      example: "The project deadline is Friday.",
      example_bn: "প্রজেক্টের ডেডলাইন শুক্রবার।"
    },
    {
      word: "polite",
      meaning_bn: "বিনয়ী / ভদ্র",
      meaning_en: "having good manners",
      example: "Please be polite to customers.",
      example_bn: "কাস্টমারদের সাথে ভদ্র থাকুন।"
    },
    {
      word: "available",
      meaning_bn: "উপলব্ধ; (সময়) ফাঁকা",
      meaning_en: "free to use or meet",
      example: "Are you available tomorrow?",
      example_bn: "আপনি কি কাল খালি আছেন?"
    },
    {
      word: "recommend",
      meaning_bn: "সুপারিশ করা",
      meaning_en: "to suggest as good",
      example: "Can you recommend a good book?",
      example_bn: "একটি ভালো বই সুপারিশ করতে পারেন?"
    },
    {
      word: "colleague",
      meaning_bn: "সহকর্মী",
      meaning_en: "a person you work with",
      example: "My colleague helped me.",
      example_bn: "আমার সহকর্মী আমাকে সাহায্য করেছে।"
    }
  ];

  var TEASER = [
    {
      q: "Choose the correct sentence:",
      qbn: "সঠিক বাক্যটি বেছে নিন:",
      options: ["He goes to school.", "He go to school.", "He going to school."],
      answer: 0,
      explain: "he/she/it + verb-s → He goes."
    },
    {
      q: "\"Don't give up\" means:",
      qbn: "Don't give up মানে?",
      options: ["Don't stop trying", "Don't wake up", "Don't sit down"],
      answer: 0,
      explain: "give up = stop trying / চেষ্টা ছেড়ে দেওয়া।"
    },
    {
      q: "I am ___ student.",
      qbn: "সঠিক article:",
      options: ["a", "an", "the"],
      answer: 0,
      explain: "I am a student. (singular countable → a)"
    }
  ];

  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function dayIndex(len) {
    var now = new Date();
    var start = new Date(now.getFullYear(), 0, 0);
    var day = Math.floor((now - start) / 86400000);
    return day % Math.max(len, 1);
  }

  function pagesPrefix() {
    if (/blogspot\.com/i.test(location.hostname)) return "/p/";
    if (global.EFBApp && typeof EFBApp.rootPrefix === "function") {
      return EFBApp.rootPrefix() === "." ? "pages/" : "";
    }
    return "pages/";
  }

  function speak(word) {
    if (!global.speechSynthesis) return;
    global.speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(word);
    u.lang = "en-GB";
    u.rate = 0.92;
    var voices = global.speechSynthesis.getVoices() || [];
    var pref = voices.find(function (v) {
      return v.lang && v.lang.toLowerCase().indexOf("en") === 0;
    });
    if (pref) u.voice = pref;
    global.speechSynthesis.speak(u);
  }

  function renderStreak() {
    var el = document.getElementById("efb-v2-streak");
    if (!el) return;
    var streak = 0;
    var longest = 0;
    if (global.EFBStorage) {
      var state = EFBStorage.load();
      streak = (state.streak && state.streak.current) || 0;
      longest = (state.streak && state.streak.longest) || 0;
    }
    var msg =
      streak > 0
        ? "🔥 " + streak + "-Day Streak! · " + streak + " দিনের লার্নিং স্ট্রাইক"
        : "🔥 আজ শুরু করুন · Start your streak today";
    el.innerHTML =
      '<div class="efb-v2-streak-inner">' +
      '<p class="efb-v2-streak-msg bn">' +
      esc(msg) +
      "</p>" +
      (longest
        ? '<span class="efb-v2-streak-best">Best: ' + longest + "</span>"
        : "") +
      "</div>";
  }

  function renderWotd(item) {
    var el = document.getElementById("efb-v2-wotd");
    if (!el || !item) return;
    el.innerHTML =
      '<div class="efb-v2-wotd-card">' +
      '<p class="efb-v2-kicker">Word of the Day · আজকের শব্দ</p>' +
      '<div class="efb-v2-wotd-row">' +
      '<strong class="efb-v2-wotd-word">' +
      esc(item.word) +
      "</strong>" +
      '<button type="button" class="efb-v2-speak" data-word="' +
      esc(item.word) +
      '" aria-label="Pronounce ' +
      esc(item.word) +
      '">🔊</button>' +
      "</div>" +
      '<p class="efb-v2-wotd-en">' +
      esc(item.meaning_en || "") +
      "</p>" +
      '<p class="efb-v2-wotd-bn bn">' +
      esc(item.meaning_bn || "") +
      "</p>" +
      (item.example
        ? '<p class="efb-v2-wotd-ex">“' +
          esc(item.example) +
          '”<br><span class="bn">' +
          esc(item.example_bn || "") +
          "</span></p>"
        : "") +
      '<a class="efb-v2-link" href="' +
      pagesPrefix() +
      'vocabulary.html">আরও শব্দ শিখুন →</a>' +
      "</div>";
    var btn = el.querySelector(".efb-v2-speak");
    if (btn) {
      btn.addEventListener("click", function () {
        speak(btn.getAttribute("data-word"));
      });
    }
  }

  function loadWotd() {
    var fallback = WOTD_FALLBACK[dayIndex(WOTD_FALLBACK.length)];
    renderWotd(fallback);
    if (!global.EFBApp || !EFBApp.loadJSON) return;
    EFBApp.loadJSON("vocabulary.json")
      .then(function (data) {
        var list = Array.isArray(data) ? data : data.words || [];
        if (!list.length) return;
        var item = list[dayIndex(list.length)];
        renderWotd({
          word: item.word,
          meaning_en: item.meaning_en,
          meaning_bn: item.meaning_bn,
          example: item.example,
          example_bn: item.example_bn
        });
      })
      .catch(function () {});
  }

  function renderQuiz() {
    var root = document.getElementById("efb-v2-quiz");
    if (!root) return;
    var i = 0;
    var score = 0;
    var locked = false;

    function paint() {
      if (i >= TEASER.length) {
        root.innerHTML =
          '<div class="efb-v2-quiz-done">' +
          "<p><strong>স্কোর: " +
          score +
          "/" +
          TEASER.length +
          "</strong></p>" +
          '<p class="bn">পুরো কুইজ করুন — আরও প্রশ্ন অপেক্ষা করছে।</p>' +
          '<a class="btn btn-primary" href="' +
          pagesPrefix() +
          'quizzes.html">Quizzes খুলুন</a>' +
          "</div>";
        return;
      }
      var q = TEASER[i];
      locked = false;
      root.innerHTML =
        '<p class="efb-v2-quiz-meta">' +
        (i + 1) +
        " / " +
        TEASER.length +
        "</p>" +
        '<p class="efb-v2-quiz-q">' +
        esc(q.q) +
        "</p>" +
        '<p class="bn efb-v2-quiz-bn">' +
        esc(q.qbn) +
        "</p>" +
        '<div class="efb-v2-quiz-opts">' +
        q.options
          .map(function (opt, idx) {
            return (
              '<button type="button" class="efb-v2-opt" data-i="' +
              idx +
              '">' +
              esc(opt) +
              "</button>"
            );
          })
          .join("") +
        "</div>" +
        '<p class="efb-v2-quiz-fb" id="efb-v2-fb" hidden></p>';
      root.querySelectorAll(".efb-v2-opt").forEach(function (btn) {
        btn.addEventListener("click", function () {
          if (locked) return;
          locked = true;
          var pick = Number(btn.getAttribute("data-i"));
          var ok = pick === q.answer;
          if (ok) score += 1;
          root.querySelectorAll(".efb-v2-opt").forEach(function (b, idx) {
            b.disabled = true;
            if (idx === q.answer) b.classList.add("is-right");
            else if (idx === pick) b.classList.add("is-wrong");
          });
          var fb = document.getElementById("efb-v2-fb");
          fb.hidden = false;
          fb.className = "efb-v2-quiz-fb " + (ok ? "ok" : "bad");
          fb.textContent = (ok ? "সঠিক! " : "ভুল। ") + q.explain;
          setTimeout(function () {
            i += 1;
            paint();
          }, 900);
        });
      });
    }
    paint();
  }

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function msUntilMidnight() {
    var now = new Date();
    var next = new Date(now);
    next.setHours(24, 0, 0, 0);
    return next - now;
  }

  function tickCountdown() {
    var el = document.getElementById("efb-v2-countdown");
    if (!el) return;
    var ms = msUntilMidnight();
    var h = Math.floor(ms / 3600000);
    var m = Math.floor((ms % 3600000) / 60000);
    var s = Math.floor((ms % 60000) / 1000);
    el.textContent = pad(h) + ":" + pad(m) + ":" + pad(s);
  }

  function mount() {
    if (!document.getElementById("efb-v2-home")) return;
    renderStreak();
    loadWotd();
    renderQuiz();
    tickCountdown();
    setInterval(tickCountdown, 1000);
    if (global.speechSynthesis) {
      speechSynthesis.getVoices();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }

  global.EFBHomeV2 = { mount: mount, speak: speak };
})(window);
