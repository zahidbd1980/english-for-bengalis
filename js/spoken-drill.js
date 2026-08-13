/**
 * Spoken drill — hide English, show Bangla, listen + type line
 */
(function (global) {
  function normalize(s) {
    return String(s || "")
      .trim()
      .toLowerCase()
      .replace(/[’']/g, "'")
      .replace(/[.?!…,;:]+$/g, "")
      .replace(/^["'“”]+|["'“”]+$/g, "")
      .replace(/\s+/g, " ");
  }

  function lineOk(user, expected) {
    const u = normalize(user);
    const e = normalize(expected);
    if (!u) return false;
    if (u === e) return true;
    // allow missing final punctuation / minor article slip already normalized
    return u.replace(/\s+/g, "") === e.replace(/\s+/g, "");
  }

  function speak(text, lang) {
    return new Promise((resolve) => {
      if (!global.speechSynthesis) {
        resolve(false);
        return;
      }
      global.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = lang || "en-GB";
      u.rate = 0.95;
      u.onend = () => resolve(true);
      u.onerror = () => resolve(false);
      const voices = global.speechSynthesis.getVoices() || [];
      const pref = voices.find((v) => v.lang && v.lang.toLowerCase().startsWith(u.lang.slice(0, 2)));
      if (pref) u.voice = pref;
      global.speechSynthesis.speak(u);
    });
  }

  function flattenLines(dialogue) {
    return (dialogue.lines || []).map((l, i) => ({
      i: i,
      en: l.en,
      bn: l.bn || "",
      speaker: l.speaker || "",
      item_id: dialogue.id + ":L" + i,
    }));
  }

  global.EFBSpokenDrill = {
    normalize: normalize,
    lineOk: lineOk,
    speak: speak,
    flattenLines: flattenLines,
  };
})(window);
