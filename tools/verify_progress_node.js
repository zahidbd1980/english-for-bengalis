/**
 * Real JS runtime check: load storage.js + progress.js with mock localStorage.
 * Simulates: see word -> wrong quiz -> mistake bank -> correct -> progress counts.
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const store = {};

const localStorage = {
  getItem(k) {
    return Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null;
  },
  setItem(k, v) {
    store[k] = String(v);
  },
  removeItem(k) {
    delete store[k];
  },
};

const window = { localStorage };
const sandbox = { window, localStorage, console, Date, Math, Object, Array, String, Number, JSON };
sandbox.global = sandbox;
sandbox.self = sandbox;

function load(rel) {
  const code = fs.readFileSync(path.join(root, rel), "utf8");
  vm.runInNewContext(code, sandbox, { filename: rel });
  // Mirror window exports onto sandbox globals (browser script order)
  if (sandbox.window.EFBStorage) sandbox.EFBStorage = sandbox.window.EFBStorage;
  if (sandbox.window.EFBProgress) sandbox.EFBProgress = sandbox.window.EFBProgress;
}

load("js/storage.js");
load("js/progress.js");

const EFBStorage = sandbox.window.EFBStorage;
const EFBProgress = sandbox.window.EFBProgress;

function assert(cond, msg) {
  if (!cond) throw new Error("ASSERT: " + msg);
}

// Fresh
EFBStorage.reset();

const vocabId = "vocab:improve";
const grammarId = "grammar:present-simple";
const sbId = "sb:1";

EFBProgress.markSeen(vocabId);
let st = EFBStorage.load();
assert(st.items[vocabId].status === 1, "seen status");
assert(st.items[vocabId].mastery_score >= 10, "seen mastery");

EFBProgress.recordResult(vocabId, false, "mcq");
st = EFBStorage.load();
assert(st.mistakes.includes(vocabId), "in mistake bank");
assert(st.items[vocabId].status === 6, "needs review");

EFBProgress.recordResult(vocabId, true, "mcq");
st = EFBStorage.load();
assert(!st.mistakes.includes(vocabId), "cleared mistake");
assert(st.items[vocabId].status !== 6, "not stuck in NEEDS_REVIEW after correct");
assert(st.items[vocabId].attempts === 2, "attempts=2");
assert(st.items[vocabId].status >= 2, "at least LEARNING after correct");

EFBProgress.markSeen(grammarId);
EFBProgress.setLastLesson("grammar", "grammar-list");
EFBProgress.recordResult(sbId, true, "type");
st = EFBStorage.load();
assert(st.profile.last_skill === "grammar", "last skill");
assert(st.items[sbId].attempts >= 1, "sentence has attempts");
assert(st.items[sbId].productive_correct >= 1, "productive type");
assert(st.items[sbId].status > 0, "sentence tracked");

// Persist across "reload"
const raw = localStorage.getItem("efb_progress_v1");
assert(raw && raw.includes(vocabId), "persisted in localStorage");
const reloaded = JSON.parse(raw);
assert(reloaded.items[vocabId].correct_count >= 1, "reload keeps progress");

// Simulate My Progress practiced count rule (attempts > 0)
function countPracticed(ids) {
  return ids.filter((id) => (st.items[id] && st.items[id].attempts > 0)).length;
}
assert(countPracticed([vocabId, sbId]) === 2, "practiced count by attempts");

console.log("NODE RUNTIME CHECK: PASS");
console.log(
  JSON.stringify(
    {
      tracked_items: Object.keys(st.items).length,
      mistakes: st.mistakes.length,
      last_skill: st.profile.last_skill,
      vocab_status: st.items[vocabId].status,
      vocab_mastery: st.items[vocabId].mastery_score,
      vocab_attempts: st.items[vocabId].attempts,
      sb_attempts: st.items[sbId].attempts,
      persisted_bytes: raw.length,
    },
    null,
    2
  )
);
