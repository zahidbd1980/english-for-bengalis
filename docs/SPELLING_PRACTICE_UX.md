# Spelling Practice — Product & UX Spec

## Core loop (confirmed)

1. Target word list (deduped, shuffled once)
2. Play pronunciation (do not show spelling)
3. User types spelling
4. Correct → Correct list; Wrong → Wrong list
5. Main list never repeats a word in the same pass
6. After main queue empty → drain Wrong queue until all Correct

## Research-backed features to include

| Feature | Why |
|---|---|
| Listen → type → instant feedback | Standard dictation UX (7ESL, UD5, classroom tests) |
| Replay audio + slow rate | Hard words need multiple listens |
| Retry-missed-only phase | Focused mastery, not random restudy |
| Preset packs + custom lists | Activation + teacher/self use |
| Deduplicate lists | Avoid wasted reps |
| Keyboard-first | Faster practice, accessibility, no mouse required |
| US/UK voice toggle | Accent preference |
| Session summary | Motivation + export of remaining wrongs |
| Letter-count hint (optional) | Soft help without full reveal |
| Reveal after wrong | Learning moment, then continue |
| Practice vs Test mode (later) | Practice = instant; Test = score at end |

## MVP feature set (this build)

- Preset lists: Common misspellings, IELTS-style, Everyday hard
- Custom list: paste / upload `.txt`
- Full mastery loop + no main-list repeats
- TTS play / replay / slow
- Keyboard shortcuts + visible cheat-sheet
- Progress: remaining / correct / wrong
- End screen with restart / practice wrongs export

## Keyboard map

| Key | Action |
|---|---|
| `Enter` | Check answer; after feedback → Next |
| `L` | Listen / replay (when not typing letter... use when Ctrl/Meta+L OR when input empty) |
| `Ctrl+L` / `Cmd+L` | Always replay |
| `Shift+L` | Slow replay |
| `N` | Next (after feedback) |
| `Esc` | Clear input / close help |
| `?` | Toggle shortcuts help |
| `S` | Toggle slow mode |
| `H` | Toggle letter-count hint |
| `1`–`3` | Quick-select preset on setup (when not in input focus conflict) |

While focus is in the text box, letter keys type normally; use `Ctrl+L` for listen.

## UI composition

1. **Setup screen**: pick list / paste custom → Start (primary CTA)
2. **Practice screen**: progress chips, big Listen button, answer input, Check, Correct/Wrong columns
3. **Complete screen**: score, time, buttons Restart / New list

One job per view. No ad near Check button.
