# English Learning Platform for Bengali Speakers
## Complete Product, Content, SEO, AdSense & Development Master Plan

**Document version:** 1.2 (IA + Navigation + UI/UX complete)  
**Date:** 11 August 2026  
**Last enriched:** 11 August 2026  
**Primary platform:** Blogger.com (V1 content + SEO layer)  
**Working URL:** https://englishforbengalis.blogspot.com  
**Target custom domain (recommended ASAP):** to be decided (e.g. englishforbengalis.com)  
**Primary audience:** Bengali-speaking English learners (Bangladesh + West Bengal diaspora)  
**Core concept:** Learn → Practice → Test → Master → Track Progress  
**Product thesis:** Measurable English mastery for Bengali speakers — not another grammar blog.

### Changelog (v1.1)

- Fixed SRS schedule inconsistency and defined a concrete review algorithm
- Clarified MVP vs soft-launch vs public-launch priorities (especially placement test)
- Added Blogger technical constraints, bilingual UX, Bangla SEO, legal/trademark, risks
- Added mastery scoring formula, progress export/import, audio strategy, growth channels
- Added Definition of Done, content calendar, competitive positioning, and editor suggestions

### Changelog (v1.2)

- Fixed nav duplication (`Challenges` vs Daily Challenge) and clarified full IA tree
- Added Blogger Page / Post / Label mapping and URL slug rules
- Added Primary / Mobile / Footer menu specs (Bangla + English)
- Added MVP nav vs Full nav, breadcrumbs, screen inventory
- Added Design system, wireframe notes, quiz/progress UX, empty/error/loading states
- Added remaining planning gaps: search UX, settings, 404, publish workflow UI, component list

---

# 1. Executive Summary

The original plan had a strong foundation, especially the idea of measurable learning progress. A critical review identified many gaps (Sections 2–3). **Version 1.1** keeps that foundation, closes remaining product/tech/business gaps, and turns vague ideas into buildable specs.

**What this product is**

The final product should not be treated as a normal Blogger English-learning blog.

It should be designed as:

> **A Bengali-speaker-focused English Learning Web Platform built around Blogger content, JavaScript interactive tools, structured learning data, quizzes, mastery tracking and personalized practice.**

Blogger should primarily handle:

- SEO content
- lessons
- articles
- landing pages
- static learning resources
- category/topic navigation

A JavaScript learning layer should handle:

- quizzes
- flashcards
- progress tracking
- mastery
- streaks
- daily challenges
- games
- sentence building
- spelling tests
- revision
- learning goals

A future backend can handle:

- user accounts
- cloud progress
- cross-device synchronization
- advanced analytics
- personalized recommendations
- certificates
- leaderboards

---

# 2. Critical Review of the Previous Plan

## What was already strong

The previous plan correctly identified:

1. Vocabulary Academy
2. Grammar Academy
3. Spoken English Academy
4. Phrasal Verb Academy
5. Pronunciation Academy
6. Spelling Academy
7. IELTS Academy
8. Quiz & Games
9. My Progress
10. Daily Challenge
11. Streaks
12. Mastery
13. Weak-area detection
14. SEO topic clusters
15. AdSense considerations
16. Blogger + JavaScript architecture

These should remain.

---

# 3. Gaps Found in the Previous Plan

## Gap 1 — No formal learner-level system

The platform needs CEFR-style levels:

- Pre-A1
- A1
- A2
- B1
- B2
- C1

The learner should receive an estimated level through a placement test.

---

## Gap 2 — "Learned" was not defined rigorously enough

A user clicking "I learned this" is not proof of mastery.

The final system should distinguish:

- Seen
- Learning
- Practiced
- Familiar
- Mastered
- Needs Review

Mastery should be based on performance, not only self-declaration.

---

## Gap 3 — No spaced-repetition engine

Learning without revision produces poor long-term retention.

The system should automatically schedule revision using a consistent interval ladder (see Section 25 for the canonical schedule):

- Day 1 → Day 3 → Day 7 → Day 14 → Day 30 → Day 60+
- Intervals expand on success and shrink (or reset) on failure

---

## Gap 4 — No mistake history

The system should remember what the learner gets wrong.

Example:

> Learner repeatedly confuses "affect" and "effect."

The system should place these into:

### My Weak Words

and automatically generate revision.

---

## Gap 5 — No diagnostic assessment

The platform needs an initial assessment.

The test should measure:

- vocabulary
- grammar
- spelling
- reading
- sentence construction
- listening, where possible

Speaking assessment can initially be self-practice and later use speech recognition.

---

## Gap 6 — No explicit Bengali-to-English bridge methodology

Because the target audience is Bengali speakers, the teaching system should deliberately exploit:

- Bangla → English translation
- English → Bangla comprehension
- Bengali-speaker common errors
- pronunciation differences
- article/preposition problems
- tense confusion
- subject-verb agreement
- word-order problems
- false friends
- direct translation mistakes

This should become a major USP.

---

## Gap 7 — Pronunciation technology was under-specified

The platform should distinguish:

- British pronunciation
- American pronunciation
- syllables
- stress
- common pronunciation mistakes
- audio
- listen-and-repeat
- optional speech-recognition practice

Do not rely only on Bangla phonetic spelling because that can teach inaccurate pronunciation.

---

## Gap 8 — No listening curriculum

English learning requires listening.

Add:

- short audio
- word recognition
- sentence recognition
- dictation
- listening MCQ
- listening spelling
- IELTS-style listening practice

---

## Gap 9 — No reading curriculum

Add:

- graded reading
- short stories
- dialogues
- news-style simplified passages
- comprehension questions
- vocabulary extraction
- reading speed practice

---

## Gap 10 — No writing curriculum

Add:

- sentence writing
- paragraph writing
- email writing
- everyday writing
- IELTS Task 1
- IELTS Task 2
- error correction
- model answers

Automated writing scoring should not be promised in V1 unless a reliable evaluation service is integrated.

---

## Gap 11 — No conversation simulator

A future feature should allow scenario-based practice:

- restaurant
- airport
- interview
- classroom
- office
- customer service
- shopping
- doctor visit
- travel
- meeting
- introduction

V1 can use branching dialogue. AI conversation can be added later.

---

## Gap 12 — No content quality framework

Large quantities of AI-generated content could make the site thin or repetitive.

Every lesson should follow editorial standards:

- correct English
- natural examples
- learner-appropriate difficulty
- original explanation
- practical usage
- quiz
- revision
- internal linking
- human review

---

## Gap 13 — No technical data architecture

The original plan mentioned localStorage but did not define the data model.

A reusable content schema is required so that vocabulary, grammar, spelling, phrasal verbs and quizzes can share the same learning engine.

---

## Gap 14 — No migration strategy from localStorage to cloud

The project needs a future-safe architecture.

V1:

> Browser localStorage

V2:

> User account + cloud database

Migration should be possible without redesigning the entire application.

---

## Gap 15 — No accessibility plan

The site should support:

- keyboard navigation
- readable font sizes
- sufficient contrast
- visible focus states
- alt text
- accessible buttons
- captions/transcripts for audio
- screen-reader-friendly labels

---

## Gap 16 — No mobile-first learning strategy

Most learners may use mobile devices.

The learning engine must work properly on:

- Android phones
- iPhones
- tablets
- desktop

Do not design desktop first and "make it responsive" later.

---

## Gap 17 — No PWA/offline strategy

A future Progressive Web App layer could allow learners to:

- install the site
- continue basic lessons offline
- practice flashcards offline
- preserve local progress

This should be a future phase, not a V1 requirement.

---

## Gap 18 — No measurement/KPI framework

The business and learning system needs measurable KPIs.

Examples:

- daily active learners
- returning learners
- lesson completion rate
- quiz accuracy
- mastery rate
- 7-day retention
- 30-day retention
- average session duration
- daily challenge completion
- organic search traffic
- CTR
- AdSense RPM
- page experience metrics

---

## Gap 19 — No anti-cheat/mastery protection

If mastery is based only on clicking answers repeatedly, progress becomes meaningless.

Use:

- randomized questions
- question pools
- delayed reviews
- minimum mastery score
- repeated testing
- different question formats

---

## Gap 20 — No content production workflow

A large educational site needs a repeatable pipeline:

Research → Draft → Teacher Review → Quiz Creation → SEO → Publish → Update → Performance Review

---

# 4. Final Product Vision

## Product Statement

> Learn practical English through Bengali-friendly explanations, structured practice and measurable progress.

## Core Promise

> **Don't just study English. Know exactly what you have mastered.**

---

# 5. Target Users

## Primary

### A. Beginner learner

Knows a few English words but cannot make sentences confidently.

### B. School/college student

Needs vocabulary, grammar and spelling.

### C. Job seeker

Needs spoken English, interview English and workplace English.

### D. General spoken-English learner

Wants practical daily English.

### E. IELTS learner

Needs vocabulary, spelling, grammar, reading, listening, speaking and writing.

### F. Returning learner

Has studied English before but needs structured revision.

---

# 6. Learning Philosophy

The platform should follow:

> **Understand → See → Hear → Practice → Produce → Test → Review → Master**

For a vocabulary item:

1. See the word
2. Understand meaning
3. Hear pronunciation
4. See examples
5. Use it in a sentence
6. Answer a quiz
7. Produce the word
8. Review later
9. Achieve mastery

---

# 7. Main Academies

## Academy 1 — Vocabulary

Content:

- Core vocabulary
- Daily-use vocabulary
- Academic vocabulary
- IELTS vocabulary
- Workplace vocabulary
- Travel vocabulary
- Topic-based vocabulary
- Synonyms
- Antonyms
- Collocations
- Word families

Initial target:

> 2,000 core words

Long-term:

> 5,000+ structured words

---

# 8. Academy 2 — Phrasal Verbs

Initial target:

> 250 essential phrasal verbs

Each item:

- phrasal verb
- meaning
- Bangla explanation
- pronunciation
- examples
- common patterns
- synonyms
- common mistakes
- quiz
- sentence production
- mastery status

Example:

> give up

Meaning:

> stop trying

Example:

> Don't give up on your dream.

---

# 9. Academy 3 — Spelling

Initial target:

> 1,000 commonly misspelled words

Each word:

- correct spelling
- common wrong spellings
- meaning
- pronunciation
- example
- memory tip
- typing challenge
- listening spelling
- quiz
- mastery

Categories:

- everyday spelling
- difficult spelling
- silent letters
- double letters
- suffix/prefix problems
- IELTS spelling

---

# 10. Academy 4 — Grammar

Initial target:

> 30 core grammar topics

Suggested curriculum:

1. Parts of Speech
2. Sentence Structure
3. Subject and Predicate
4. Be Verbs
5. Present Simple
6. Present Continuous
7. Past Simple
8. Past Continuous
9. Present Perfect
10. Past Perfect
11. Future Forms
12. Modal Verbs
13. Articles
14. Prepositions
15. Conjunctions
16. Conditionals
17. Passive Voice
18. Reported Speech
19. Relative Clauses
20. Gerunds
21. Infinitives
22. Comparatives
23. Questions
24. Negatives
25. Subject-Verb Agreement
26. Countable/Uncountable Nouns
27. Determiners
28. Punctuation
29. Common Errors
30. Advanced Sentence Structure

Each topic should contain:

Concept → Examples → Bengali explanation → Practice → Error correction → Quiz → Mastery

---

# 11. Academy 5 — Spoken English

Categories:

### Daily life

- greeting
- introduction
- shopping
- food
- transport
- travel
- phone calls
- asking for directions

### Workplace

- meetings
- requests
- updates
- explanations
- disagreement
- presentations
- interviews

### Social

- small talk
- invitations
- apologies
- opinions
- agreement/disagreement

---

# 12. Academy 6 — Pronunciation

Features:

- audio
- syllables
- stress
- British/US variants
- minimal pairs
- difficult sounds
- common Bengali-speaker pronunciation mistakes
- listen-and-repeat
- optional speech recognition

Important:

Avoid teaching English pronunciation solely through Bengali phonetic spellings.

---

# 13. Academy 7 — Listening

Curriculum:

### Level 1

Single words

### Level 2

Short sentences

### Level 3

Short conversations

### Level 4

Short passages

### Level 5

Natural-speed English

### IELTS

IELTS-style listening practice

Activities:

- listen and choose
- listen and type
- dictation
- identify the word
- identify the meaning
- spelling from audio

---

# 14. Academy 8 — Reading

Levels:

- Beginner
- Elementary
- Intermediate
- Upper Intermediate
- Advanced

Content:

- short stories
- dialogues
- practical articles
- simplified news
- IELTS passages

Activities:

- comprehension
- vocabulary extraction
- true/false
- matching
- inference
- main idea

---

# 15. Academy 9 — Writing

Levels:

- word
- sentence
- paragraph
- email
- application
- professional message
- IELTS writing

Practice:

- arrange sentence
- correct sentence
- translate
- write from prompt
- improve sentence

---

# 16. Academy 10 — Common Mistakes

Create a major content library:

> 500 Common English Mistakes Bengali Speakers Make

Examples:

Incorrect:

> I am agree.

Correct:

> I agree.

Incorrect:

> Discuss about the issue.

Correct:

> Discuss the issue.

Categories:

- grammar
- prepositions
- articles
- word choice
- pronunciation
- spelling
- direct translation
- sentence structure

---

# 17. Academy 11 — IELTS

Sections:

- IELTS vocabulary
- IELTS spelling
- IELTS grammar
- IELTS speaking
- IELTS listening
- IELTS reading
- IELTS writing
- IELTS practice tests

Do not present the site as an official IELTS provider.

---

# 18. Academy 12 — Quizzes & Games

Quiz types:

1. MCQ
2. True/False
3. Fill in the blank
4. Match meaning
5. Match word
6. Arrange sentence
7. Correct the mistake
8. Type the answer
9. Spelling test
10. Listening test
11. Translation test
12. Flashcard recall

Games:

- Word Match
- Sentence Builder
- Spelling Race
- Phrasal Verb Challenge
- Grammar Fix
- Vocabulary Memory
- Missing Word
- Speed Quiz
- Word Scramble
- Daily Challenge

---

# 19. CEFR Level System

Use:

- Pre-A1
- A1
- A2
- B1
- B2
- C1

Do not claim a quiz provides an official CEFR certification.

Use wording such as:

> Estimated learning level

---

# 20. Placement Test

New users should be invited to:

> Take a 10-minute English Level Test

Measure:

- vocabulary
- grammar
- spelling
- sentence construction
- reading

Future:

- listening
- speaking

Output:

> Estimated Level: A2

Then:

> Recommended Learning Path

---

# 21. Goal System

Users choose:

- Speak English
- IELTS
- Grammar
- Vocabulary
- Spelling
- Workplace English
- General English

The dashboard recommends content based on the selected goal.

---

# 22. Progress Tracking

## Main dashboard

Example:

Vocabulary:

> 734 / 2,000

Phrasal Verbs:

> 87 / 250

Spelling:

> 426 / 1,000

Grammar:

> 12 / 30

Pronunciation:

> 180 / 500

Common Mistakes:

> 132 / 500

---

# 23. Mastery Model

Recommended statuses:

### 0 — Not Started

### 1 — Seen

### 2 — Learning

### 3 — Practiced

### 4 — Familiar

### 5 — Mastered

### 6 — Needs Review

A word should only become "Mastered" after successful testing.

---

# 24. Mastery Rules

### Canonical V1 mastery formula

Each item has `mastery_score` from 0–100.

| Event | Score change |
|---|---|
| First open / Seen | set floor to 10 |
| Correct easy recognition (MCQ) | +8 |
| Correct productive recall (type / speak / translate) | +12 |
| Wrong answer | −15 (min 0) |
| Successful scheduled review (Good/Easy) | +10 |
| Failed scheduled review | −20 + status → Needs Review |
| Unused for 45+ days while Familiar/Mastered | −10 / week until reviewed |

**Mastered** only if ALL are true:

1. `mastery_score >= 80`
2. At least **2 productive** correct answers (not only MCQ)
3. At least **3 successful delayed reviews** (R1–R3 or later)
4. Last 5 attempts accuracy ≥ 80%
5. No fail in the last 48 hours

**Anti-cheat:**

- Randomize option order and question pool
- Require mixed formats before Mastered
- Ignore rapid-fire identical correct answers under ~1.5s (mark as suspicious; do not award full mastery points)
- Cap same-item attempts per hour (e.g. 8)

Thresholds may be tuned after 50–100 real learner sessions — document changes in content governance.

---

# 25. Spaced Repetition

**Canonical schedule (use everywhere — do not invent alternate day lists):**

| Stage | Interval after previous success |
|---|---|
| Learn (Day 0) | immediate first check optional |
| R1 | +1 day |
| R2 | +3 days |
| R3 | +7 days |
| R4 | +14 days |
| R5 | +30 days |
| R6+ | +60 days (then +90 if still strong) |

### Simple V1 algorithm (custom, SM-2 inspired — no external library required)

For each `LearningItem`:

```text
ease = 2.3          // default; clamp 1.3–3.0
interval_days = 0
reps = 0
next_review = today
```

On review result:

- **Again (fail):** `reps = 0`, `interval_days = 1`, `ease -= 0.2`, status → Needs Review
- **Hard:** `interval_days = max(1, round(interval_days * 1.2))`, `ease -= 0.05`
- **Good:** `reps += 1`; if reps==1 → 1 day; if reps==2 → 3 days; else `interval_days = round(interval_days * ease)`; `ease += 0.05`
- **Easy:** same as Good but `interval_days = round(interval_days * ease * 1.3)`, `ease += 0.1`

Persist: `ease`, `interval_days`, `reps`, `next_review`, `last_reviewed`, `lapses`.

Daily Challenge / Review queue = all items where `next_review <= today`.

Cap daily new items (e.g. 10–20) so review load stays sustainable.

---

# 26. Mistake Bank

Every wrong answer should optionally create a mistake record.

Example:

> Mistake Bank

- affect/effect
- advice/advise
- their/there/they're
- much/many
- since/for

The system generates:

> Review Your Mistakes

---

# 27. Daily Challenge

Target:

> 10 minutes/day

Example:

- 5 vocabulary
- 3 phrasal verbs
- 5 spellings
- 3 grammar questions
- 5 sentences
- 1 listening task

Total:

> 20+ activities

---

# 28. Streak System

Track:

- daily activity
- current streak
- longest streak
- weekly activity

Example:

> 🔥 12-day streak

Do not make streaks punitive. Offer recovery/revision options.

---

# 29. Achievement System

Examples:

- First 100 Words
- 100 Spelling Master
- 50 Phrasal Verbs
- Grammar Beginner
- 7-Day Streak
- 30-Day Streak
- Vocabulary Master
- IELTS Starter
- English Champion

---

# 30. Weekly Report

Show:

- words learned
- words mastered
- spelling mastered
- grammar completed
- quiz accuracy
- speaking practice time
- listening practice
- weak areas
- recommended next lessons

---

# 31. Weak-Area Engine

Example:

> Your Weak Areas

Prepositions — 52%

Articles — 64%

Phrasal Verbs — 71%

Vocabulary — 86%

Then:

> Recommended next lesson:
> Articles: A, An and The

---

# 32. Personalized Learning

Future engine:

Input:

- level
- goal
- performance
- mistakes
- completed lessons
- review schedule

Output:

> What should I study today?

This can become one of the platform's strongest long-term features.

---

# 33. Bengali-Speaker-Specific Teaching

This is a major differentiator.

Build special modules around:

### Grammar transfer errors

- article omission
- preposition misuse
- tense confusion
- subject-verb agreement
- plural errors

### Translation errors

- literal Bengali-to-English translation
- unnatural sentence structure

### Pronunciation

- problematic English sounds
- syllable stress
- word endings
- consonant clusters

### Vocabulary

- false friends
- confusing words

---

# 34. Bengali → English Practice Lab

Example:

Bangla:

> আমি ইংরেজি শিখছি।

Answer:

> I am learning English.

Then explain:

> am + learning = Present Continuous

Practice modes:

- translation
- multiple choice
- sentence builder
- typing
- speaking

---

# 35. English → Bengali Comprehension

Example:

> I have already finished my work.

Ask:

> What does this sentence mean?

This prevents the learner from relying only on translation in one direction.

---

# 36. Sentence Builder

Give:

> I / want / to / improve / my / English

User arranges:

> I want to improve my English.

Then:

- grammar explanation
- pronunciation
- alternative sentences

---

# 37. Conversation Simulator

V1:

> Branching scenario

Example:

### At the Airport

System:

> Good morning. May I see your passport?

Learner chooses:

A. Here you are.
B. I am passport.
C. Give passport.

Correct:

> Here you are.

Future:

> AI conversation practice

---

# 38. Content Data Architecture

Do not build thousands of pages manually without structured data.

## Vocabulary schema

```text
id
word
meaning_en
meaning_bn
pronunciation
audio
part_of_speech
difficulty
cefr_level
category
example
example_bn
synonyms
antonyms
collocations
common_mistake
quiz_ids
```

## Phrasal verb schema

```text
id
phrase
meaning_en
meaning_bn
pronunciation
example
example_bn
usage_pattern
synonyms
common_mistake
difficulty
quiz_ids
```

## Spelling schema

```text
id
correct_word
wrong_spellings
meaning
pronunciation
example
memory_tip
difficulty
quiz_ids
```

## Grammar schema

```text
id
topic
level
cefr
explanation
bangla_explanation
examples
common_errors
practice_questions
quiz_ids
```

## Quiz schema

```text
id
type
question
options
correct_answer
explanation
difficulty
skill
content_id
```

---

# 39. Generic Learning Item Model

The learning engine should eventually treat different content types as learning items.

```text
LearningItem
├── item_id
├── item_type
├── skill
├── difficulty
├── level
├── status
├── mastery_score
├── attempts
├── correct_count
├── wrong_count
├── last_reviewed
├── next_review
└── streak
```

This allows one progress engine to handle:

- words
- spelling
- grammar
- phrasal verbs
- sentences
- pronunciation

---

# 40. Blogger + JavaScript Architecture

## Layer 1 — Blogger

Responsible for:

- SEO pages
- articles
- lessons
- navigation
- landing pages

## Layer 2 — JavaScript

Responsible for:

- quizzes
- progress
- games
- flashcards
- scoring
- localStorage
- UI state

## Layer 3 — Future backend

Responsible for:

- accounts
- cloud sync
- analytics
- personalized learning
- multi-device progress

---

# 41. V1 Storage

Use:

> localStorage

Store:

- completed lessons
- mastered items
- quiz attempts
- streak
- goals
- daily activity
- review schedule
- `progress_version`
- settings (accent preference, UI language, daily new-item cap)

### Mandatory V1 protections (gap fix)

1. **Export progress** → download JSON file  
2. **Import progress** → restore from JSON  
3. **Schema versioning** → migrate on load if `progress_version` changes  
4. **Quota warning** → if storage nearly full, prompt export  
5. **Clear progress** → explicit confirm; never silent wipe  

Do not store passwords or unnecessary PII.

---

# 42. V2 Storage

Potential options:

- Firebase
- Supabase
- custom REST API

Core entities:

- users
- learning_items
- progress
- attempts
- mistakes
- reviews
- goals
- achievements
- sessions

---

# 43. Data Migration

Design a stable local progress format.

Example:

```text
progress_version: 1
user_id: local
items: [...]
settings: {...}
```

Future versions can migrate V1 local data into the cloud account.

---

# 44. Site Architecture

**Canonical tree (v1.2).** Do not add a separate top-level “Challenges” item — Daily Challenge lives under Practice.

```text
HOME

├── Learn                         (hub page)
│   ├── Vocabulary
│   ├── Grammar
│   ├── Phrasal Verbs
│   ├── Spelling
│   ├── Spoken English
│   ├── Common Mistakes           (USP — early)
│   ├── Pronunciation             (post-MVP expand)
│   ├── Listening                 (later)
│   ├── Reading                   (later)
│   └── Writing                   (later)
│
├── Practice                      (hub page)
│   ├── Daily Challenge           (ONLY challenge entry — no duplicate nav)
│   ├── Quizzes
│   ├── Flashcards
│   ├── Spelling Test
│   ├── Sentence Builder
│   ├── Translation Lab           (USP — early)
│   └── Games
│
├── IELTS                         (hub; unofficial disclaimer on page)
│   ├── Overview
│   ├── Vocabulary
│   ├── Grammar / Spelling
│   └── Skills (Speaking / Listening / Reading / Writing)  [expand later]
│
├── My Progress                   (dashboard page)
│   ├── Overview
│   ├── Review Due
│   ├── Mistake Bank
│   ├── Achievements
│   └── Export / Import
│
├── Level Test                    (page)
│
├── Blog / Tips                   (label index of SEO posts)
│
├── Settings                      (page: language, accent, caps, reset)
│
└── Trust
    ├── About
    ├── Contact
    ├── Privacy
    ├── Terms
    ├── Disclaimer
    └── Learning Methodology (optional)
```

**Full menu / Page–Post mapping / UI specs:** see Sections 124–135.

---

# 45. Homepage Structure

**One composition, brand-first, mobile-first.** First viewport = brand + one headline + one support line + CTA group only. No stats strip, no card grid in the hero.

## Hero (first viewport)

Brand:

> English for Bengalis *(final name TBD)*

Headline:

> Learn English. Practice Daily. Track Your Progress.

Subtitle:

> Practical English for Bengali speakers — with proof of what you have mastered.

Buttons:

- Start Learning → `/p/learn.html` or first vocab path
- Take Level Test → `/p/level-test.html`

Secondary text link (not a third competing CTA):

> Continue where I left off *(if local progress exists)*

---

## Below the fold (order)

1. **Daily Challenge** — 10 minutes — primary retention hook  
2. **Skills** — Vocabulary, Grammar, Phrasal Verbs, Spelling, Spoken, Common Mistakes  
3. **Progress teaser** — “Your English Journey, Measured” → My Progress  
4. **Learning tools** — Flashcards, Quiz, Translation Lab, Sentence Builder  
5. **IELTS-style hub** (with unofficial note)  
6. **Latest blog / tips** (3 links max)  
7. Footer  

Do not put Listening/Reading/Writing in the homepage skill row until those academies have real content.

---

# 46. SEO Architecture

Do not publish random articles.

Build topic clusters.

## Pillar

> English Grammar Complete Guide

Supporting articles:

- Present Simple
- Present Continuous
- Present Perfect
- Articles
- Prepositions
- Modals
- Conditionals
- Passive Voice

Internal linking should connect:

Pillar → supporting content → practice → quiz → related lessons

---

# 47. SEO Content Clusters

## Vocabulary cluster

- common English words
- daily-use English words
- English words with Bangla meaning
- vocabulary for beginners
- workplace vocabulary
- IELTS vocabulary

## Phrasal verb cluster

- common phrasal verbs
- phrasal verbs with Bangla meaning
- phrasal verbs for speaking
- IELTS phrasal verbs

## Spelling cluster

- commonly misspelled words
- difficult English spelling
- IELTS spelling
- spelling practice

## Spoken English cluster

- daily English sentences
- English conversation
- spoken English for beginners
- workplace English

## Grammar cluster

- English grammar for beginners
- tenses
- articles
- prepositions
- subject-verb agreement

---

# 48. SEO Page Template

Each educational page should have:

1. Clear title
2. Short introduction
3. Learning objective
4. Explanation
5. Examples
6. Bengali explanation where useful
7. Common mistakes
8. Interactive practice
9. Quiz
10. Related lessons
11. FAQ where genuinely useful
12. Next lesson CTA

Avoid making pages artificially long.

---

# 49. Internal Linking Strategy

Every lesson should have:

### Previous lesson

### Current lesson

### Next lesson

And:

> Practice this topic

> Take the quiz

> Learn related vocabulary

This creates a learning journey and improves discoverability.

---

# 50. Search Strategy

Site search should support:

- word
- grammar topic
- phrasal verb
- spelling
- category
- IELTS topic

Future:

> Search: "look after"

Results:

- meaning
- lesson
- quiz
- examples
- pronunciation
- progress status

---

# 51. Technical SEO Checklist

Implement:

- responsive design
- clean URLs
- proper titles
- meta descriptions
- canonical URLs
- structured headings
- internal links
- image alt text
- sitemap
- robots configuration
- Search Console
- analytics
- breadcrumbs where appropriate
- fast loading
- minimal JavaScript blocking
- optimized images

Do not create duplicate or near-duplicate pages just to target keywords.

---

# 52. Structured Data

Where appropriate, investigate structured data for:

- Article
- Breadcrumb
- FAQ where eligible and genuinely useful
- Educational content

Do not add schema that misrepresents the page.

---

# 53. Content Quality Standards

Every content item should pass:

### English accuracy

Is the English correct?

### Naturalness

Would a native speaker naturally say it?

### Learner value

Does the learner gain something practical?

### Difficulty

Is it appropriate for the intended level?

### Example quality

Is the example realistic?

### Practice

Can the learner actually use the knowledge?

### Originality

Is the explanation genuinely useful and not copied?

---

# 54. AI Content Policy

AI can assist with:

- drafts
- examples
- quiz generation
- categorization
- metadata
- brainstorming

But AI output must be reviewed.

Never mass-publish thousands of unreviewed AI pages.

Educational content should be:

> AI-assisted + human reviewed + learner tested

---

# 55. AdSense Strategy

Primary priority:

> Learning value

Secondary priority:

> Organic traffic

Third priority:

> Monetization

Avoid:

- excessive ads
- deceptive ad placement
- ads that look like navigation
- ads inside critical quiz controls
- intrusive popups
- misleading click prompts

Keep learning interactions clean.

---

# 56. Recommended Ad Placement

Potential areas:

- header/upper content area where appropriate
- between major article sections
- sidebar on desktop
- end of article
- related-content area

For interactive tools:

> Minimize distraction.

Never encourage users to click ads.

Always follow the current AdSense policies and requirements before monetization.

---

# 57. Trust Pages

Required core pages:

- About
- Contact
- Privacy Policy
- Terms
- Disclaimer

Recommended:

- Editorial Policy
- Corrections Policy
- Learning Methodology
- Accessibility Statement

---

# 58. Analytics

Track:

### Content

- page views
- organic landing pages
- search queries
- scroll depth

### Learning

- lesson starts
- lesson completions
- quiz attempts
- accuracy
- mastery
- review completion

### Retention

- 1-day return
- 7-day return
- 30-day return

### Business

- traffic source
- conversion to account
- ad performance
- premium conversion later

Use privacy-conscious analytics practices.

---

# 59. Learning KPIs

Important metrics:

### Learning completion rate

How many learners finish lessons?

### Mastery rate

How many learners master an item?

### Retention

How many return after 7/30 days?

### Accuracy improvement

Does repeated practice improve scores?

### Weak-area recovery

Do weak topics improve?

---

# 60. Product KPIs

Initial targets should be measured rather than guessed.

Track:

- new users
- returning users
- daily active users
- weekly active users
- lessons/session
- quiz/session
- average learning session
- challenge completion
- streak continuation
- organic traffic
- search impressions
- CTR
- indexed pages

---

# 61. Accessibility

Minimum:

- semantic HTML
- keyboard support
- visible focus
- accessible buttons
- readable font
- good contrast
- descriptive labels
- alt text
- captions/transcripts
- no color-only indicators

---

# 62. Mobile-first Requirements

Interactive tools must work on:

- small Android phones
- iPhones
- tablets
- desktop

Buttons should be touch-friendly.

Do not make drag-and-drop the only interaction for important exercises.

Provide alternative controls.

---

# 63. Performance Requirements

Prioritize:

- fast first render
- compressed images
- minimal external scripts
- lazy loading
- efficient JavaScript
- no unnecessary animation
- no autoplay media
- cached/static assets where possible

---

# 64. Security

For V1 localStorage:

- do not store passwords
- do not store sensitive personal information
- validate user input
- sanitize dynamic HTML
- avoid unsafe eval-like techniques

For V2:

- secure authentication
- HTTPS
- server-side validation
- rate limiting
- database rules
- secure API design

---

# 65. Offline/PWA Future

Future features:

- installable app
- offline flashcards
- offline basic quizzes
- offline progress
- synchronization when online

Do not make this a launch blocker.

---

# 66. Content Production Pipeline

Use:

```text
Topic Research
      ↓
Learning Objective
      ↓
Draft
      ↓
Teacher Review
      ↓
Examples
      ↓
Quiz
      ↓
Practice
      ↓
SEO
      ↓
Publish
      ↓
Analytics
      ↓
Update
```

---

# 67. Content Inventory — Initial Target

| Content | Initial Target |
|---|---:|
| Core Vocabulary | 2,000 |
| Common Sentences | 1,000 |
| Phrasal Verbs | 250 |
| Spelling | 1,000 |
| Grammar Topics | 30 |
| Common Mistakes | 500 |
| Pronunciation Words | 500 |
| IELTS Vocabulary | 1,000 |
| Quiz Questions | 2,000+ |
| Games | 10–15 |

Do not attempt to publish all of these before launch.

Launch with a smaller, high-quality core and expand systematically.

---

# 68. Recommended MVP

The first release should contain:

## Content

- 300 vocabulary items
- 50 phrasal verbs
- 100 spelling words
- 10 grammar topics
- 100 daily sentences
- 50 common mistakes

## Tools

- quiz engine
- flashcards
- progress dashboard
- localStorage + **export/import JSON backup**
- daily challenge
- basic streak
- basic site search (labels / in-page index)
- **soft placement test** (short; can be refined post-launch)

## Pages

- Home
- Vocabulary
- Grammar
- Phrasal Verbs
- Spelling
- Spoken English
- Quiz
- My Progress
- Blog
- About
- Contact
- Policies (Privacy, Terms, Disclaimer — IELTS trademark disclaimer included)

### Launch tiers (clarifies earlier ambiguity)

| Tier | When | Placement test | Listening/Reading/Writing | SRS + Mistake Bank |
|---|---|---|---|---|
| Soft launch | Friends/family / limited traffic | Optional short test | Skip or 1–2 demos | Basic review queue OK |
| Public launch | AdSense-ready + Search Console | Recommended in hero CTA | Landing pages only | Should-have live |
| Growth | Months 3–6 | Full diagnostic | Real curricula | Full learning intelligence |

**Rule:** Do not block public launch on cloud accounts, AI tutor, speech recognition, or full IELTS suite.

---

# 69. Phase Roadmap

## Phase 0 — Research & Architecture

Duration:

> 1–2 weeks

Tasks:

- brand
- domain
- audience definition
- information architecture
- content schema
- learning model
- design system

---

## Phase 1 — Blogger Foundation

Duration:

> 1–2 weeks

Tasks:

- Blogger setup
- custom domain
- theme
- navigation
- SEO foundation
- policy pages
- analytics
- Search Console

---

## Phase 2 — Content MVP

Duration:

> 3–6 weeks

Tasks:

- vocabulary
- grammar
- spelling
- phrasal verbs
- spoken English
- common mistakes

---

## Phase 3 — Interactive Engine

Duration:

> 2–4 weeks

Tasks:

- quiz engine
- progress engine
- localStorage
- mastery
- streak
- daily challenge
- flashcards

---

## Phase 4 — Learning Intelligence

Tasks:

- spaced repetition
- mistake bank
- weak-area analysis
- personalized recommendations
- placement test

---

## Phase 5 — IELTS

Tasks:

- IELTS vocabulary
- grammar
- listening
- reading
- writing
- speaking

---

## Phase 6 — Cloud Platform

Tasks:

- accounts
- cloud progress
- synchronization
- profile
- advanced analytics

---

## Phase 7 — Advanced Product

Tasks:

- speech recognition
- conversation simulator
- AI tutor
- PWA
- certificates
- leaderboards
- premium learning

---

# 70. Recommended Tech Stack

## V1

- Blogger
- HTML
- CSS
- Vanilla JavaScript
- localStorage

Optional:

- lightweight icon library
- audio assets
- analytics

Avoid heavy frameworks initially.

---

## V2

Possible:

- Firebase or Supabase
- authentication
- database
- cloud storage
- serverless functions

---

## V3

Possible:

- React/Next.js or dedicated SPA
- API backend
- PostgreSQL
- AI services
- speech services

At that stage Blogger can remain as the SEO/content layer while the application becomes a separate subdomain.

---

# 71. Suggested Domain Architecture

**V1 interim:**

> https://englishforbengalis.blogspot.com

**Recommended ASAP:**

> custom domain → e.g. `englishforbengalis.com` (or shorter brandable name)

Reasons to move off raw blogspot early:

- trust & AdSense perception
- brandability for social growth
- cleaner URLs for SEO
- easier future split of content vs app

Future split:

> example.com — SEO lessons / blog (may stay on Blogger or migrate)  
> app.example.com — learning application (JS SPA / Next.js)

Plan the subdomain split **before** the JS engine becomes tightly coupled to Blogger HTML widgets.

---

# 72. User Journey

## New visitor

Home

↓

Level Test

↓

Estimated Level

↓

Choose Goal

↓

Recommended Path

↓

First Lesson

↓

Practice

↓

Quiz

↓

Progress Updated

↓

Daily Challenge

↓

Return Tomorrow

---

# 73. Returning User Journey

Home

↓

Continue Learning

↓

Review Due Items

↓

Daily Challenge

↓

Weak Area Practice

↓

New Lesson

↓

Progress Update

---

# 74. Example Full Learning Cycle

Target:

> 250 Phrasal Verbs

User starts:

> 0 / 250

Learns:

> 1. look after

Practice:

> MCQ

Practice:

> Fill in the blank

Practice:

> Sentence production

Review:

> Day 2

Review:

> Day 7

Mastery:

> 1 / 250

Dashboard:

> 0.4% complete

Repeat until:

> 250 / 250

Then:

> Phrasal Verb Master 🏆

---

# 75. Example Spelling Cycle

Target:

> 1,000 words

Word:

> definitely

Step 1:

See

Step 2:

Hear

Step 3:

Understand

Step 4:

Identify wrong spelling

Step 5:

Type spelling

Step 6:

Use in sentence

Step 7:

Delayed review

Step 8:

Master

Dashboard:

> 426 / 1,000 mastered

---

# 76. Example Grammar Cycle

Target:

> 30 topics

Topic:

> Present Perfect

Learn

↓

Examples

↓

Bangla explanation

↓

Error correction

↓

Translation

↓

Sentence builder

↓

Quiz

↓

Delayed test

↓

Mastery

Dashboard:

> 13 / 30

---

# 77. Gamification Rules

Reward:

- learning
- correct answers
- revision
- consistency

Do not reward meaningless clicking.

Example:

- Lesson complete: +20 XP
- Correct quiz: +10 XP
- Mastery: +30 XP
- Daily challenge: +50 XP
- Review completion: +20 XP

---

# 78. Leaderboard Considerations

A public leaderboard can motivate some learners but discourage others.

If implemented:

- weekly leaderboard
- optional participation
- XP-based
- no personal sensitive information
- allow nickname

Avoid making competition the core learning experience.

---

# 79. Certificates

Future certificates can recognize:

- 30-day challenge
- vocabulary milestone
- spelling milestone
- grammar course completion

Important:

Do not present internal certificates as official academic or IELTS certification.

---

# 80. Future AI Tutor

Potential capabilities:

> Explain this grammar.

> Give me 5 examples.

> Correct my sentence.

> Practice an interview with me.

> Talk to me in English.

> Explain my mistakes in Bangla.

> Give me easier examples.

AI should supplement structured learning rather than replace it.

---

# 81. AI-Powered Personal Tutor — Future Architecture

```text
Learner Profile
      ↓
Progress
      ↓
Mistake History
      ↓
Current Goal
      ↓
AI Tutor
      ↓
Personalized Lesson
      ↓
Practice
      ↓
Assessment
      ↓
Progress Update
```

---

# 82. Content Governance

Create versioning for educational content.

Each item should have:

- created date
- updated date
- reviewed status
- reviewer
- source/reference where relevant
- content version

This matters because English examples and educational recommendations may need correction.

---

# 83. Editorial Review Checklist

Before publishing:

- Is the English correct?
- Is the Bangla explanation clear?
- Is pronunciation accurate?
- Are examples natural?
- Are quiz answers unambiguous?
- Is the difficulty appropriate?
- Are distractor options reasonable?
- Is the content original?
- Are internal links present?
- Is the page mobile-friendly?

---

# 84. Testing Strategy

## Functional testing

Test:

- quiz scoring
- progress
- mastery
- localStorage
- streak
- reset
- review schedule

## Browser testing

- Chrome
- Edge
- Firefox
- Safari where possible

## Device testing

- Android
- iPhone
- tablet
- desktop

## Content testing

- spelling
- grammar
- answer keys
- pronunciation

---

# 85. Backup Strategy

Keep:

- Blogger XML backup
- content database backup
- JavaScript source
- CSS source
- images
- audio files
- quiz data
- progress schema
- documentation

Do not keep the only copy inside Blogger's editor.

Use Git for source code and structured content where practical.

---

# 86. Recommended Project Folder

```text
english-learning-platform/
│
├── docs/
│   ├── product-plan.md
│   ├── content-guidelines.md
│   ├── seo-plan.md
│   └── data-model.md
│
├── data/
│   ├── vocabulary.json
│   ├── phrasal-verbs.json
│   ├── spelling.json
│   ├── grammar.json
│   └── quizzes.json
│
├── js/
│   ├── quiz-engine.js
│   ├── progress.js
│   ├── mastery.js
│   ├── review.js
│   ├── streak.js
│   └── storage.js
│
├── css/
│   └── learning.css
│
└── assets/
    ├── audio/
    └── images/
```

---

# 87. Monetization Roadmap

## Stage 1

Free content

↓

Organic traffic

↓

AdSense

---

## Stage 2

Free + premium learning

Potential:

- advanced IELTS
- unlimited practice
- detailed analytics
- premium courses

---

## Stage 3

Potential:

- subscription
- certificates
- live classes
- teacher dashboard
- institutional plans

---

# 88. Business Opportunities

Long term:

### B2C

Individual learners

### B2B

Schools

### Coaching centers

### Universities

### Corporate English training

### Teacher dashboard

A teacher could eventually assign:

> Learn 50 vocabulary words by Friday.

The system tracks students.

---

# 89. Teacher Dashboard — Future

Teacher can:

- create class
- assign lessons
- assign vocabulary
- assign quizzes
- see completion
- see weak areas
- see scores
- send practice tasks

This could turn the platform into an LMS.

---

# 90. Parent Dashboard — Future

For younger learners:

- learning time
- lessons completed
- vocabulary learned
- quiz scores
- streak
- areas needing attention

Privacy and child-safety considerations must be addressed before targeting minors extensively.

---

# 91. Final Product Modules

The final product should contain:

```text
1. English Level Test
2. Goal Selection
3. Vocabulary Academy
4. Grammar Academy
5. Phrasal Verb Academy
6. Spelling Academy
7. Pronunciation Academy
8. Spoken English Academy
9. Listening Academy
10. Reading Academy
11. Writing Academy
12. IELTS Academy
13. Common Mistakes
14. Translation Lab
15. Sentence Builder
16. Quiz Engine
17. Game Engine
18. Flashcards
19. Daily Challenge
20. Spaced Repetition
21. Mistake Bank
22. Progress Dashboard
23. Streak
24. Achievements
25. Weak-Area Engine
26. Personalized Learning
27. User Account
28. Cloud Sync
29. Teacher Dashboard
30. Future AI Tutor
```

---

# 92. MVP vs Future Feature Priority

## Must Have (public launch)

- content structure + JSON schemas
- vocabulary / grammar / spelling / phrasal verbs (MVP volumes)
- quizzes + flashcards
- progress + mastery (formula in Section 24)
- mobile-first UI
- SEO foundation + trust pages
- progress export/import
- AdSense-safe layout

## Should Have (soon after launch / Phase 4)

- daily challenge + streak polish
- mistake bank
- full placement / diagnostic test
- spaced repetition engine (Section 25)
- weak-area recommendations
- Bangla ↔ English Translation Lab (core USP — prioritize early)

## Later

- cloud accounts
- speech recognition
- AI tutor
- conversation simulator
- PWA
- teacher / parent dashboard
- certificates
- premium subscriptions
- full Listening / Reading / Writing academies
- IELTS full skill suite

---

# 93. The Most Important Design Principle

Never build:

> Article → Article → Article

Build:

> Lesson → Practice → Test → Mastery → Review → Progress → Next Lesson

The website should feel like a learning application even though Blogger is powering the content.

---

# 94. Final Information Architecture

Conceptual flow (product logic). For **menus / Page–Post mapping**, use §44 + §124–127.

```text
                        HOME
                          │
             ┌────────────┴────────────┐
             │                         │
         LEVEL TEST                 GOAL
             │                         │
             └────────────┬────────────┘
                          │
                   LEARNING PATH
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
     LEARN              PRACTICE            TEST
       │                  │                  │
 Vocabulary            Daily Challenge     Level / Review
 Grammar               Quiz                Assessment
 Spelling              Flashcards
 Spoken English        Translation Lab
 Phrasal Verbs         Sentence Builder
 Common Mistakes       Spelling Test
 (+ later: Pronunciation / Listening / Reading / Writing / Games)
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                       MASTERY
                          │
                  PROGRESS DASHBOARD
                          │
             ┌────────────┼────────────┐
             │            │            │
          Strengths     Weaknesses    Reviews
             │            │            │
             └────────────┼────────────┘
                          │
                  PERSONALIZED NEXT STEP
```

---

# 95. Recommended Launch Strategy

Do not wait until 10,000 content items are ready.

Launch when the following are polished:

### Core content

- 300 vocabulary
- 50 phrasal verbs
- 100 spelling
- 10 grammar topics
- 100 sentences
- 50 common mistakes

### Core tools

- level test
- quiz
- progress
- mastery
- daily challenge
- flashcards

Then publish new content continuously.

---

# 96. 12-Month Growth Direction

## Months 1–2

Foundation + MVP

## Months 3–4

Content expansion + SEO

## Months 5–6

Spaced repetition + weak areas + placement

## Months 7–8

IELTS + listening + reading

## Months 9–10

Accounts + cloud sync

## Months 11–12

AI tutor + speaking/conversation experiments

The exact timeline depends on available development and content resources.

---

# 97. Final Strategic Positioning

The site should not try to become:

> "Another English grammar blog."

Instead it should become:

> **"A measurable English learning journey for Bengali speakers."**

Core differentiators:

1. Bengali-speaker-specific teaching
2. Structured learning paths
3. Practical English
4. Large vocabulary/spelling targets
5. Phrasal verb mastery
6. Interactive practice
7. Progress tracking
8. Spaced repetition
9. Weak-area detection
10. IELTS preparation
11. Gamification
12. Future AI tutor

---

# 98. Final Product Definition

## Short version

> **Learn English**
> 
> Understand the lesson.

> **Practice English**
>
> Use quizzes, games and exercises.

> **Master English**
>
> Prove that you can recall and use it.

> **Track English**
>
> See exactly how much you have learned.

> **Improve English**
>
> Let the system identify your weak areas and recommend what to study next.

---

# 99. The Ultimate Learning Loop

```text
          DISCOVER
              ↓
            LEARN
              ↓
            HEAR
              ↓
           PRACTICE
              ↓
            TEST
              ↓
           REVIEW
              ↓
          MASTER
              ↓
           TRACK
              ↓
      FIND WEAK AREAS
              ↓
      PERSONALIZE NEXT STEP
              ↓
            LEARN
              ↺
```

This loop should be the foundation of the entire platform.

---

# 100. Final Recommendation

The best development order is:

## Step 1
Define brand, domain and visual identity.

## Step 2
Create the complete Blogger information architecture.

## Step 3
Create the structured learning data model.

## Step 4
Create the content production templates.

## Step 5
Build the reusable JavaScript learning engine.

## Step 6
Build the progress/mastery engine.

## Step 7
Build quiz and practice engines.

## Step 8
Create the MVP content.

## Step 9
Launch.

## Step 10
Measure learner behavior.

## Step 11
Improve content and UX.

## Step 12
Add spaced repetition, weak-area detection and personalization.

## Step 13
Add accounts/cloud sync.

## Step 14
Add advanced IELTS, speaking and listening.

## Step 15
Add AI tutor and advanced platform capabilities.

---

# 101. One-Sentence Vision

> **Build a fast, SEO-friendly Blogger-based English learning platform where Bengali speakers can learn practical English, practice through interactive exercises, and see measurable proof of their progress from beginner to advanced level.**

---

# 102. Critical Analysis Summary (v1.1)

## Overall verdict

The v1.0 plan is **strategically strong**: clear USP (Bengali-speaker bridge + measurable mastery), sensible Blogger+JS hybrid, and a realistic MVP mindset. Weaknesses were mostly **underspecification** (algorithms, platform limits, legal, growth, bilingual UX) and a few **priority contradictions**. Those are addressed below and in updated Sections 24–25, 41, 68, 71, 92.

## What was already excellent

- Learn → Practice → Test → Master loop
- Academy breadth with MVP discipline
- Content quality / anti–thin-content stance
- AdSense subordinated to learning value
- Future-safe local → cloud migration thinking

## What still needed enrichment (now added)

| Gap | Risk if ignored | Fix location |
|---|---|---|
| Blogger JS/hosting limits | Engine breaks or becomes unmaintainable | §103 |
| Bilingual UI strategy | Confused UX for beginners | §104 |
| Bangla keyword SEO | Miss primary search market | §105 |
| Audio production plan | Pronunciation academy stalls | §106 |
| Trademark / legal disclaimers | IELTS / AdSense / trust issues | §107 |
| Progress data loss | Angry churn when cache clears | §41, §108 |
| Concrete SRS + mastery math | Inconsistent implementation | §24, §25 |
| Competitive positioning | Feature bloat vs Duolingo etc. | §109 |
| BD/WB market growth channels | SEO-only growth too slow | §110 |
| Risk register | Surprises at monetization | §111 |
| Definition of Done | Endless “almost launch” | §112 |
| Content calendar / ops | Irregular publishing | §113 |
| Onboarding first session | Drop-off before habit forms | §114 |
| Regional Bengali nuances | BD vs WB friction | §115 |
| Page/Post/Menu mapping | Confused Blogger setup | §124–127 *(v1.2)* |
| Navigation + UI/UX specs | Inconsistent build | §126–133 *(v1.2)* |
| Publish runbook | Irregular ops | §137 *(v1.2)* |

---

# 103. Blogger Platform Constraints & Workarounds

Blogger is good for SEO pages; it is **not** a full app host. Plan around these limits:

### Constraints

- Theme HTML/JS can get fragile; gadget/widget limits apply
- Large inline JSON in every post is unmaintainable
- Cross-post shared JS must be loaded from a stable URL
- No real server-side logic in V1
- localStorage is origin-bound (`blogspot.com` ≠ custom domain — **migration warning**)
- Limited control vs Cloudflare/custom hosting for caching headers

### Recommended workarounds

1. Keep **canonical content JSON** in Git (`/data/*.json`), not only inside Blogger posts  
2. Host built JS/CSS on a stable place Blogger can load:
   - GitHub Pages / Cloudflare Pages / jsDelivr from a public repo  
   - or Blogger Theme “Layout” + external `<script src="...">`  
3. Each lesson page embeds only a **small bootstrap**: `data-item-id`, academy type, and script include  
4. Build a tiny **content publish checklist**: validate JSON → generate post HTML snippet → paste/publish  
5. Before connecting a custom domain, warn users to **export progress** (origin change can orphan localStorage)

### Decision rule

If the learning engine needs routing, auth, or large asset pipelines, move the app to `app.` subdomain earlier rather than forcing Blogger to pretend it is Next.js.

---

# 104. Bilingual UX Strategy (Bangla + English)

### Principle

> UI teaches in the learner’s comfort language; English is the *object of study*, not a barrier to navigation.

### V1 UI language modes

| Mode | Who | Behavior |
|---|---|---|
| Bangla-first | Absolute beginners | Labels, instructions, errors in Bangla; examples in English |
| Mixed (default) | Most learners | Nav in Bangla+English; explanations bilingual |
| English-first | Intermediate+ | Bangla available via toggle on explanations |

### Rules

- Settings: `ui_language = bn | mixed | en`
- Never force long English-only onboarding for Pre-A1 / A1
- Quiz stems for beginners may be bilingual; answers remain English where testing English
- Pronunciation tips: IPA + audio primary; Bangla phonetic **optional footnote only** (never sole teaching method)
- Error messages and empty states must be Bangla-capable

### Microcopy examples

- “আজকের চ্যালেঞ্জ শুরু করুন” / Start today’s challenge  
- “আপনার লেভেল: Estimated A2”  
- “প্রোগ্রেস এক্সপোর্ট করুন” / Export progress

---

# 105. Bangla SEO & Keyword Strategy

English keywords alone miss how many learners actually search.

### Query types to cover

1. **Bangla script:** `ইংরেজি শেখার উপায়`, `ইংরেজি গ্রামার`, `ইংলিশ স্পিকিং প্র্যাকটিস`  
2. **Banglish / Romanized Bangla:** `english grammar bangla`, `spoken english bangla meaning`  
3. **English + Bangla intent:** `present perfect bangla`, `phrasal verbs with bangla meaning`  
4. **Problem-led:** `I am agree correct`, `discuss about wrong`, `affect vs effect bangla`

### On-page approach

- Titles can be bilingual when natural: `Present Perfect Tense — বাংলা ব্যাখ্যা সহ`  
- One primary intent per URL — do not duplicate the same lesson for BN and EN keywords  
- FAQ blocks in Bangla where they answer real learner questions  
- Internal links between Bangla-intent posts and practice tools

### Content cluster additions

- “বাংলা থেকে ইংরেজি অনুবাদ প্র্যাকটিস”
- “বাংলাভাষীদের সাধারণ ইংরেজি ভুল”
- “ইংরেজি উচ্চারণ — বাংলাভাষীদের সমস্যা”

---

# 106. Audio & Pronunciation Production Plan

Without audio, Pronunciation / Listening academies are weak.

### V1 (ship)

- High-quality **TTS** (e.g. browser Speech Synthesis for practice + curated recorded set for core 300 words)
- Prefer a consistent voice; document British vs American toggle (`accent = uk | us`)
- Store `audio_url` or `tts_text` in schema; do not hardcode only Bangla phonetics

### V1.5

- Record human audio for minimal pairs and high-frequency words
- Host MP3/OGG on CDN / Drive-alternative with stable URLs (prefer Git LFS / Cloudflare R2 / similar)

### Rules

- No autoplay  
- Always provide transcript / text fallback  
- Lazy-load audio  
- License check: only use audio you own or have rights to

---

# 107. Legal, Trademark & Trust Gaps

### IELTS / exam brands

- IELTS is a registered trademark of its owners  
- Always use: “IELTS-style practice” / “unofficial preparation materials”  
- Footer + IELTS hub disclaimer: *Not affiliated with British Council, IDP, or Cambridge*  
- Do not imply score guarantees

### Content rights

- Original explanations preferred  
- Cite sources for definitions when needed; do not scrape copyrighted exam papers  
- Keep a corrections policy and update dates on lessons

### Privacy (V1)

- Privacy Policy must mention localStorage, analytics cookies, AdSense if used  
- Prefer privacy-conscious analytics (e.g. cookieless or minimal GA4 configuration)  
- If targeting under-13 heavily, pause and design parental consent — default audience: teens/adults

### AdSense readiness extras

- Enough original articles (not doorway pages)  
- Clear navigation, About, Contact  
- No encouraging ad clicks  
- Stable custom domain recommended before aggressive monetization

---

# 108. Progress Schema Enrichment (V1)

Extend Section 43 with exportable shape:

```json
{
  "progress_version": 1,
  "exported_at": "2026-08-11T12:00:00Z",
  "user_id": "local",
  "settings": {
    "ui_language": "mixed",
    "accent": "us",
    "daily_new_cap": 15,
    "goal": "spoken_english"
  },
  "profile": {
    "estimated_level": "A2",
    "placement_taken_at": null
  },
  "streak": { "current": 0, "longest": 0, "last_active_date": null },
  "items": {
    "vocab:look-after": {
      "status": 2,
      "mastery_score": 42,
      "attempts": 6,
      "correct_count": 4,
      "wrong_count": 2,
      "ease": 2.3,
      "interval_days": 3,
      "reps": 1,
      "last_reviewed": "2026-08-10",
      "next_review": "2026-08-13",
      "lapses": 0
    }
  },
  "mistakes": [],
  "achievements": [],
  "daily": {}
}
```

**Import rule:** merge by item key; never silently delete cloud-worthy history without confirm.

---

# 109. Competitive Positioning

| Competitor type | Examples | They win on | We win on |
|---|---|---|---|
| Global apps | Duolingo, Babbel | Habit loops, polish, brand | Bengali explanations, common BD/WB mistakes, SEO lessons |
| Exam platforms | Official IELTS partners, big prep sites | Authority, mocks | Free structured bridge + Bangla support (unofficial) |
| Bangla YouTube / Facebook pages | Local teachers | Reach, personality | Measurable mastery, reusable drills, searchable evergreen pages |
| Grammar blogs | Generic SEO blogs | Traffic | Practice engine + progress proof |

### Positioning statement

> We are the place where a Bengali speaker can learn a point in Bangla, practice it immediately, and **prove** it is mastered — then find us again from Google when they need the next topic.

### Anti-goals (do not chase in V1)

- Becoming a social network  
- Guaranteeing IELTS band scores  
- Replacing a human teacher for speaking fluency overnight  
- Cloning Duolingo’s full game economy

---

# 110. Growth & Distribution (Bangladesh / West Bengal)

SEO is necessary but slow. Add a **distribution layer**:

### Channels

1. **Facebook** — short “common mistake” posts + link to practice  
2. **YouTube** — 3–6 min grammar/mistake videos → lesson URL in description  
3. **Shorts/Reels/TikTok** — one mistake / one phrasal verb per clip  
4. **WhatsApp / Telegram channel** — daily 5-word challenge  
5. **Pinterest** — vocabulary graphics (evergreen)  
6. **Student/job Facebook groups** — value-first sharing (no spam)

### Content→channel rule

Every major lesson should have a **share card**: mistake → correct → one-line Bangla tip → CTA to quiz.

### North-star early metric

> Weekly returning learners who complete Daily Challenge ≥ 1×

Not vanity pageviews alone.

---

# 111. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| AdSense rejection / thin content flag | Medium | High | Quality bar, original lessons, trust pages, slow publish |
| localStorage progress loss | High | High | Export/import, versioning, later cloud |
| Custom domain breaks progress origin | Medium | High | Pre-migration export banner |
| Blogger JS maintenance hell | Medium | High | External script host + Git source of truth |
| AI mass-content quality drop | High | High | Human review gate; publish caps/week |
| Trademark complaints (IELTS) | Low–Med | High | Disclaimers; “IELTS-style” wording |
| Scope creep (12 academies) | High | High | MVP volumes + MoSCoW |
| Audio licensing issues | Medium | Medium | TTS + owned recordings only |
| Solo-founder burnout | High | High | Content calendar + templates; batch production |
| Competitor copy of USP | Medium | Medium | Speed + community + progress data moat |

---

# 112. MVP Definition of Done (Go / No-Go)

Launch only when **all** are true:

### Product

- [ ] Home, Learn hubs, Quiz, Progress, trust pages live on mobile  
- [ ] ≥ 300 vocab / 50 PV / 100 spelling / 10 grammar / 50 mistakes published & reviewed  
- [ ] Quiz engine scores correctly across MCQ + type-answer  
- [ ] Mastery statuses update per Section 24  
- [ ] Progress export + import works  
- [ ] Daily Challenge runs without breaking on empty queues  
- [ ] No critical ad/quiz overlap  

### Quality

- [ ] Editorial checklist passed on all MVP lessons  
- [ ] 5 real learners complete a first session without assistance  
- [ ] Lighthouse / mobile usability: no blocking issues on key templates  

### Ops

- [ ] Analytics + Search Console connected  
- [ ] Blogger XML + Git backup of data/JS  
- [ ] Privacy / Terms / Disclaimer (incl. IELTS) published  

If any Product checkbox fails → **do not** announce publicly.

---

# 113. Content Operations & Calendar

### Weekly cadence (solo-friendly)

| Day focus | Output |
|---|---|
| Mon | 1 grammar OR mistake lesson |
| Tue | 10–20 vocabulary items + quizzes |
| Wed | 5 phrasal verbs OR 10 spelling |
| Thu | Spoken English dialogue / sentences |
| Fri | SEO polish + internal links + FAQ |
| Sat | Quiz/game pack + Daily Challenge refresh |
| Sun | Analytics review + fix top bounce pages |

### Batching

- Draft 2 weeks ahead in JSON  
- Review day separate from publish day  
- Max AI-draft publish without human review: **zero**

### Definition of a “finished” lesson

Learning objective + explanation + Bangla help + examples + common mistake + practice + quiz + prev/next links + mobile check.

---

# 114. First-Session Onboarding (Critical Path)

Target: **value in under 5 minutes**.

```text
Land on Home
  → optional Level Test (≤ 10 questions) OR skip
  → pick Goal (1 tap)
  → “Your first 5 words” guided lesson
  → 5-question quiz
  → show Progress: 5 Seen / 1 Practiced
  → invite Daily Challenge tomorrow
  → prompt: Export progress tip (once)
```

### Drop-off killers to avoid

- Long forms  
- Forced account (V1)  
- Desktop-only interactions  
- Autoplaying audio  
- Ads before first success moment  

---

# 115. Bangladesh vs West Bengal Considerations

Most content is shared Standard English, but be careful with:

- **Examples:** mix contexts (Dhaka, Kolkata, campus, remittance, job interview) so neither audience feels foreign  
- **Bangla explanations:** prefer clear, widely understood Bangla; avoid overly region-locked slang in teaching text  
- **Spelling preference:** teach **both** British/American where it matters (organise/organize); let `accent` setting drive audio + preferred spelling notes  
- **Job English:** include Gulf/Malaysia migration interview English (high BD relevance) and IT/office English (both markets)

---

# 116. AdSense & Page Experience Checklist (Practical)

Before applying / enabling ads:

1. 30–50+ solid original articles/lessons (not thin stubs)  
2. Custom domain preferred  
3. About, Contact, Privacy live  
4. Navigation clear; no cloaking  
5. Ads not near quiz answer buttons  
6. Mobile readable fonts; CLS stable when ads load  
7. No “click the ad” language anywhere  
8. Learning tools usable if ad blockers remove ads  

**RPM optimization comes after retention.** Fix bounce and session quality first.

---

# 117. Technical Module Build Order (Engineering)

Build in this order to avoid rework:

```text
1. content schemas + sample JSON (vocab, quiz)
2. storage.js (load/save/migrate/export/import)
3. progress.js + mastery.js
4. quiz-engine.js (MCQ, type, shuffle, explain)
5. flashcards.js
6. review.js (SRS queue)
7. streak.js + daily-challenge.js
8. dashboard UI
9. placement-test.js
10. mistake-bank.js
11. weak-area.js
12. search index
```

Do **not** start with games or AI. Games consume time; AI needs clean learner data first.

---

# 118. Sample Lesson Template (Publish-ready)

```text
Title: Present Perfect — Have/Has + Past Participle (বাংলা ব্যাখ্যা)
Level: A2
Objective: Use present perfect for life experience and recent unfinished time.

1. Warm-up question
2. Form table
3. 6 natural examples (+ 2 Bangla meaning lines)
4. Bengali-speaker traps (e.g. overusing Past Simple)
5. Mini dialogue
6. Practice: 5 items (MCQ + type)
7. Quiz CTA
8. Related: Past Simple vs Present Perfect; Already/Yet/Just
9. FAQ (2–4 real questions)
10. Next lesson CTA
```

Embed:

```html
<div class="efb-lesson" data-skill="grammar" data-id="grammar-present-perfect"></div>
<script src="https://cdn.example.com/efb/learning-engine.js" defer></script>
```

---

# 119. Analytics Event Map (Implement Early)

Minimum custom events (names stable):

| Event | Props |
|---|---|
| `lesson_start` | skill, id, level |
| `lesson_complete` | skill, id, duration_ms |
| `quiz_start` / `quiz_complete` | skill, score, max, id |
| `item_result` | item_id, correct, format |
| `review_complete` | count, accuracy |
| `challenge_complete` | day_key |
| `progress_export` | — |
| `placement_complete` | estimated_level |

Without these, “personalized learning” later is guesswork.

---

# 120. Editor Suggestions & Priority Recommendations

These are product recommendations from the v1.1 enrichment review — adopt unless you consciously reject them.

### P0 — Do before public launch

1. **Treat Translation Lab + Common Mistakes as USP pillars**, not side pages — schedule them in Phase 2 content, not “later nice-to-have.”  
2. **Ship export/import with localStorage** on day one.  
3. **Freeze one SRS + mastery formula** (Sections 24–25) so every feature uses the same truth.  
4. **Externalize JS/JSON from Blogger posts** into Git + CDN.  
5. **Write IELTS/unofficial disclaimers** into hub + footer templates now.

### P1 — Do in first 60 days after launch

6. Soft placement test in hero, full diagnostic in Phase 4.  
7. Bangla SEO cluster for mistakes + “with Bangla meaning” pages.  
8. Facebook + YouTube distribution paired to each pillar lesson.  
9. Human audio for top 100 words; TTS elsewhere.  
10. Weekly content calendar with a hard publish cap (quality > volume).

### P2 — Strategic bets

11. Move interactive app to `app.` subdomain once quiz/progress is stable.  
12. WhatsApp “5-minute daily” channel as retention wedge for BD users.  
13. Teacher dashboard only after cloud accounts exist (do not fake multi-student on localStorage).  
14. AI tutor only after mistake bank + structured items are rich — otherwise AI will ramble without curriculum grounding.

### Suggestions to *cut* or delay

- Public leaderboards at MVP (can demotivate beginners)  
- Certificates before cloud identity  
- Full Listening/Reading/Writing academies before Vocabulary/Grammar/Spelling loops feel excellent  
- Heavy gamification cosmetics (avatars, complex XP shops)

### One product bet worth making

> **“বাংলাভাষীদের ভুল” + instant practice** should be the shareable growth engine;  
> **mastery dashboard** should be the retention engine;  
> **SEO lesson library** should be the acquisition engine.

If those three reinforce each other, the platform compounds. If you only publish articles, it becomes another blog.

---

# 121. Updated 90-Day Execution Plan (Practical)

### Days 1–14 — Architecture

- Brand name lock + visual tokens  
- Schemas + folder structure in Git  
- Blogger theme skeleton + nav + trust pages  
- `storage` / `progress` / `quiz` spikes with 20 sample items  

### Days 15–45 — MVP content + engine

- Produce MVP volumes  
- Wire lesson bootstrap + dashboard  
- Daily Challenge v1  
- Export/import  
- Soft level test  

### Days 46–60 — Harden & soft launch

- 5–10 learner tests  
- Fix mobile UX  
- Search Console / analytics events  
- Soft launch to community  

### Days 61–90 — Public launch + distribution

- Custom domain if ready (with progress migration warning)  
- Bangla SEO posts + social clips  
- SRS + mistake bank polish  
- AdSense application only if DoD + content depth met  

---

# 122. Open Decisions Log (Resolve Explicitly)

Track these decisions in writing when made:

| Decision | Options | Recommendation |
|---|---|---|
| Final brand/domain | keep blogspot name vs shorter .com | Shorter .com ASAP |
| Default accent | US vs UK | US audio default + UK toggle (or reverse if IELTS-heavy) |
| Default UI language | bn / mixed / en | `mixed` |
| Primary goal for marketing | Spoken vs Grammar vs IELTS | Spoken + Common Mistakes for growth; Grammar for SEO |
| Backend later | Firebase vs Supabase | Supabase if SQL comfort; Firebase if speed-to-auth |
| When to leave Blogger for lessons | never / hybrid / full migrate | Hybrid: Blogger SEO + `app.` for engine |

---

# 123. Final v1.1 Recommendation

Keep the vision of a **measurable English learning journey for Bengali speakers**.

Build in this spirit:

1. **Acquisition** = SEO lessons + Bangla-intent content + social mistake clips  
2. **Activation** = 5-minute first win  
3. **Retention** = Daily Challenge + SRS + visible mastery  
4. **Monetization** = AdSense only after learning quality is obvious  
5. **Expansion** = cloud sync → IELTS-style → AI tutor  

Do not expand academies horizontally until the vertical loop  
`Lesson → Practice → Test → Review → Master → Next`  
is unmistakably better than a normal blog.

---

# 124. Blogger Content Model — Page vs Post vs Label

This section closes the gap: what is a **Page**, what is a **Post**, and how **Labels** work.

## Rule of thumb

| Type | Use for | Indexed as | Examples |
|---|---|---|---|
| **Page** | Stable destinations, tools, hubs, legal | Site nav / utility | Home sections via theme; Learn hub; Progress; Level Test; About |
| **Post** | SEO lessons, tip articles, dated updates | Blog / search / labels | “Present Perfect — বাংলা ব্যাখ্যা”, mistake posts |
| **Label** | Taxonomy / filters / hub lists | Label archive URLs | `grammar`, `a2`, `phrasal-verbs`, `common-mistakes` |

## A. Blogger Pages (create once, put in menu)

| Page title (EN) | Bangla label | Suggested path/slug | MVP? |
|---|---|---|---|
| Home | হোম | `/` (blog home) | Yes |
| Learn | শিখুন | `/p/learn.html` | Yes |
| Practice | অনুশীলন | `/p/practice.html` | Yes |
| Vocabulary | শব্দভাণ্ডার | `/p/vocabulary.html` | Yes |
| Grammar | গ্রামার | `/p/grammar.html` | Yes |
| Phrasal Verbs | ফ্রেজাল ভার্ব | `/p/phrasal-verbs.html` | Yes |
| Spelling | বানান | `/p/spelling.html` | Yes |
| Spoken English | স্পোকেন ইংলিশ | `/p/spoken-english.html` | Yes |
| Common Mistakes | সাধারণ ভুল | `/p/common-mistakes.html` | Yes |
| Translation Lab | অনুবাদ ল্যাব | `/p/translation-lab.html` | Yes |
| Quizzes | কুইজ | `/p/quizzes.html` | Yes |
| Flashcards | ফ্ল্যাশকার্ড | `/p/flashcards.html` | Yes |
| Daily Challenge | ডেইলি চ্যালেঞ্জ | `/p/daily-challenge.html` | Yes |
| Sentence Builder | বাক্য গঠন | `/p/sentence-builder.html` | Should |
| My Progress | আমার প্রোগ্রেস | `/p/my-progress.html` | Yes |
| Level Test | লেভেল টেস্ট | `/p/level-test.html` | Soft Yes |
| IELTS Hub | আইইএলটিএস | `/p/ielts.html` | Landing only at MVP |
| Settings | সেটিংস | `/p/settings.html` | Yes |
| About | আমাদের সম্পর্কে | `/p/about.html` | Yes |
| Contact | যোগাযোগ | `/p/contact.html` | Yes |
| Privacy Policy | গোপনীয়তা | `/p/privacy.html` | Yes |
| Terms | শর্তাবলি | `/p/terms.html` | Yes |
| Disclaimer | ডিসক্লেইমার | `/p/disclaimer.html` | Yes |
| Search | খুঁজুন | `/p/search.html` | Should |
| Games | গেমস | `/p/games.html` | Later |
| Pronunciation | উচ্চারণ | `/p/pronunciation.html` | Later hub |
| Listening / Reading / Writing hubs | … | `/p/...` | Later |

**Do not** create separate Pages for every vocabulary word — those are **Posts** or data-driven tool views.

## B. Blogger Posts (evergreen lessons + tips)

Each lesson/article = one Post.

Required labels on every lesson post:

1. Skill label — e.g. `grammar`, `vocabulary`, `spelling`, `phrasal-verbs`, `spoken`, `common-mistakes`  
2. Level label — `pre-a1` | `a1` | `a2` | `b1` | `b2` | `c1`  
3. Format label — `lesson` | `list` | `dialogue` | `quiz-pack`  
4. Optional cluster — `tenses`, `articles`, `prepositions`, `ielts-style`

### Post types

| Post type | Purpose | Template |
|---|---|---|
| Skill lesson | Teach one topic | §48 + §118 |
| Word/list post | Batch of words with practice embed | Vocabulary list template |
| Mistake post | Incorrect → Correct → Bangla tip → quiz | USP growth format |
| Pillar post | Cluster hub (long guide) | Pillar + child links |
| Tip / motivation | Light SEO / social | Short; link into practice |

## C. What is NOT a separate nav item

- Individual quiz results  
- Individual word IDs  
- “Challenges” (removed — use Daily Challenge only)  
- Duplicate IELTS skill pages before content exists  

---

# 125. URL & Slug Conventions

```text
Pages:   /p/{kebab-case}.html
Posts:   /{yyyy}/{mm}/{kebab-case-english-slug}.html
Labels:  /search/label/{kebab-case}
```

### Slug rules

- English kebab-case primary: `present-perfect-tense-bangla`  
- Include `bangla` in slug when Bangla-intent SEO is the target  
- No Bangla script in URLs (encoding pain on Blogger)  
- Stable slugs — do not rename after indexing  
- One intent per URL  

### Canonical examples

- `/p/my-progress.html`  
- `/2026/08/present-perfect-tense-bangla.html`  
- `/2026/08/i-am-agree-common-mistake.html`  
- `/search/label/common-mistakes`  

---

# 126. Navigation Specification

## A. Primary desktop nav (max 7 top items)

Keep top bar scannable. Overflow goes under Learn / Practice / More.

| Order | EN | BN | Destination | MVP visible? |
|---|---|---|---|---|
| 1 | Learn | শিখুন | `/p/learn.html` | Yes (dropdown) |
| 2 | Practice | অনুশীলন | `/p/practice.html` | Yes (dropdown) |
| 3 | Progress | প্রোগ্রেস | `/p/my-progress.html` | Yes |
| 4 | Level Test | লেভেল টেস্ট | `/p/level-test.html` | Yes |
| 5 | IELTS | আইইএলটিএস | `/p/ielts.html` | Yes (hub only) |
| 6 | Blog | ব্লগ | `/search/label/lesson` or home posts | Yes |
| 7 | More | আরও | About, Contact, Settings, Privacy… | Yes |

### Learn dropdown (MVP)

- Vocabulary  
- Grammar  
- Phrasal Verbs  
- Spelling  
- Spoken English  
- Common Mistakes  
- *(Pronunciation / Listening / Reading / Writing — hide until ready; show “Soon” only on Learn hub, not in nav)*

### Practice dropdown (MVP)

- Daily Challenge  ★ primary  
- Quizzes  
- Flashcards  
- Translation Lab  
- Spelling Test  
- Sentence Builder  
- *(Games — later)*

## B. Mobile nav

- Hamburger → full-screen or drawer panel  
- Top pinned actions inside drawer: **Daily Challenge**, **Continue**, **Progress**  
- Then Learn / Practice accordion  
- Then Level Test, IELTS, Blog, Settings, Trust links  
- Touch targets ≥ 44×44 px  
- No hover-only menus  

## C. Footer nav (every page)

**Column 1 — Learn:** Vocabulary, Grammar, Phrasal Verbs, Spelling, Mistakes  
**Column 2 — Practice:** Daily Challenge, Quizzes, Flashcards, Translation Lab  
**Column 3 — Account-lite:** Progress, Settings, Export tip link  
**Column 4 — Trust:** About, Contact, Privacy, Terms, Disclaimer  

Footer also: short brand line + “Unofficial IELTS-style materials” one-liner.

## D. Utility / in-lesson chrome

Sticky or top-of-lesson bar:

`Home › Learn › Grammar › Present Perfect`  
Actions: Practice | Quiz | Next lesson  

Floating (optional, non-intrusive): **Continue learning** only when progress exists — never cover quiz answers.

## E. Nav anti-patterns (forbidden)

- Two entries for the same Daily Challenge  
- Putting all 12 academies in the top bar  
- Ads styled like menu items  
- English-only menu for default `mixed` UI mode  

---

# 127. MVP Navigation vs Full Navigation

| Area | MVP (launch) | Full (later) |
|---|---|---|
| Learn dropdown | 6 skills | + Pronunciation, Listening, Reading, Writing |
| Practice | Challenge, Quiz, Flashcards, Translation, Spelling, Sentence | + Games, Conversation |
| IELTS | 1 hub page + disclaimer | Full skill subnav |
| Progress | Overview + review + export | Achievements detail, cloud sync |
| Blog | Label “lesson” / tips | Multi-cluster hubs |
| Settings | Language, accent, reset, export/import | Account, notifications |

**Learn hub page** may list future academies as “Coming soon” cards/text — but **do not** add dead top-nav links.

---

# 128. Breadcrumbs, Search & 404

## Breadcrumbs

```text
Home › Learn › Grammar › Present Perfect
Home › Practice › Daily Challenge
Home › My Progress › Mistake Bank
```

- Last crumb = current page (not a link)  
- Hub pages always linkable  
- Implement with visible HTML + optional BreadcrumbList schema  

## Search UX (`/p/search.html` + Blogger search)

V1:

- Native Blogger search box in header  
- Results page template: title, skill label, level, short snippet  
- Empty: “কিছু পাওয়া যায়নি — Grammar বা Common Mistakes দেখুন” + 3 suggested links  

V1.5:

- Client-side index over JSON for words / phrasal verbs (“look after”)  

## 404 / missing page

Custom theme message:

> এই পেজটি পাওয়া যায়নি।  
> Home · Learn · Daily Challenge · Progress  

Never show a bare Blogger default if theme allows override.

---

# 129. Screen Inventory (UI must design for these)

| ID | Screen | Type | Priority |
|---|---|---|---|
| S01 | Home | Page | P0 |
| S02 | Learn hub | Page | P0 |
| S03 | Skill hub (e.g. Grammar) | Page | P0 |
| S04 | Lesson post | Post | P0 |
| S05 | Practice hub | Page | P0 |
| S06 | Quiz session | Tool UI | P0 |
| S07 | Quiz result | Tool UI | P0 |
| S08 | Flashcard session | Tool UI | P0 |
| S09 | Daily Challenge | Tool UI | P0 |
| S10 | My Progress dashboard | Page | P0 |
| S11 | Review due list | Page section | P0 |
| S12 | Level Test + result | Page | P0/P1 |
| S13 | Translation Lab | Page | P1 |
| S14 | Sentence Builder | Page | P1 |
| S15 | Mistake Bank | Progress section | P1 |
| S16 | Settings | Page | P0 |
| S17 | IELTS hub | Page | P1 |
| S18 | About / Contact / Legal | Pages | P0 |
| S19 | Search results | System | P1 |
| S20 | 404 | System | P1 |
| S21 | Onboarding first-run overlay/path | Flow | P0 |
| S22 | Export / Import progress | Settings | P0 |
| S23 | Games hub | Later | P2 |
| S24 | Conversation simulator | Later | P2 |

---

# 130. Design System (UI foundation)

Phase 0 deliverable — lock before theming Blogger.

## Brand direction (avoid generic AI look)

- **Not:** purple-on-white gradients, cream+terracotta cliché, dark neon glow, emoji-heavy UI  
- **Yes:** clean academic-practical learning product; calm confidence; Bangla-friendly typography  

### Suggested tokens (adjust when brand name locks)

```text
--color-bg:        #F7F4EF        /* warm paper, not flat pure white only */
--color-surface:   #FFFFFF
--color-ink:       #1C2430        /* primary text */
--color-muted:     #5B6573
--color-brand:     #0F6B5C        /* deep teal — trust/learning */
--color-brand-2:   #C45C26        /* clay accent for CTAs — sparingly */
--color-success:   #1F7A4C
--color-danger:    #B42318
--color-border:    #E4DED5
--font-display:    "Fraunces" or "Source Serif 4"   /* headlines */
--font-body:       "Source Sans 3" or "IBM Plex Sans"
--font-bangla:     "Noto Sans Bengali" (always load)
--radius:          10px           /* soft, not pill-everything */
--space:           4/8/12/16/24/32/48
```

### Background atmosphere

Subtle paper grain or soft diagonal wash behind home hero — not a flat single fill only. Lesson pages stay calmer for reading.

### Motion (2–3 intentional)

1. Hero brand/headline fade-up once on load  
2. Progress ring / bar animate on dashboard enter  
3. Quiz correct/incorrect gentle feedback (no confetti spam)

### Components (build once, reuse)

- Primary button / secondary button / text button  
- Skill chip (not rounded-full candy pills everywhere)  
- Lesson content block  
- Quiz option button  
- Mastery status badge (Seen → Mastered)  
- Streak indicator (simple; emoji optional, not required)  
- Empty state block  
- Banner: “Export your progress”  
- Disclaimer callout (IELTS)

### Ads vs UI

Reserve ad slots **outside** quiz option lists and primary CTAs. Mark `.efb-ad-slot` in theme; never inside `.efb-quiz`.

---

# 131. Key Screen Wireframe Notes

## S01 Home

```text
[ Brand ]
[ Headline ]
[ Subtitle ]
[ Start Learning ] [ Level Test ]
— fold —
[ Daily Challenge CTA ]
[ Skill links row/list ]
[ Progress teaser ]
[ Tools ]
[ IELTS hub teaser ]
[ Latest 3 posts ]
[ Footer ]
```

## S04 Lesson

```text
Breadcrumb
Title + level chip
Objective (1 line)
Explanation
Examples
Bangla help
Common mistakes
[ Embedded practice widget ]
[ Take quiz ]
Prev | Next | Related
FAQ
```

## S06–S07 Quiz

```text
Progress n/N
Question (BN instruction ok)
Options / input
[ Check ]
Feedback + short explanation
[ Next ]
— end —
Score
Mastery deltas
[ Review mistakes ] [ Continue learning ] [ Home ]
```

Rules:

- One question per screen on mobile  
- Large tap targets  
- Don’t rely on drag-only  
- Disable double-submit  
- Keep explanation collapsed until answered  

## S10 Progress

```text
Greeting + estimated level
Streak | Today’s challenge status
Bars: Vocab / Grammar / PV / Spelling / Mistakes
Due reviews (count + Start)
Weak areas (top 3)
[ Export ] [ Settings ]
```

No fake precision (don’t show “73.482%”).

## S21 First run

Follow §114. Prefer inline guided path over modal walls. Max one dismissible tip.

---

# 132. Interaction, Empty, Error & Loading States

| State | Behavior |
|---|---|
| Loading quiz/data | Skeleton or “লোড হচ্ছে…” — no blank white flash |
| Empty progress | “এখনো শুরু হয়নি — ৫টা শব্দ শিখুন” + CTA |
| Empty review queue | “আজ রিভিউ নেই — নতুন লেসন করুন” |
| Quiz no data | “এই টপিকে এখনো কুইজ নেই” + related lesson |
| Wrong answer | Explain + show correct; don’t shame |
| Storage full / blocked | Prompt export; explain private mode limits |
| Import fail | “ফাইল পড়া যায়নি — version চেক করুন” |
| Offline (V1) | Soft message; no fake sync |
| Ad blocked | Learning still fully usable |

### Accessibility UX (binds §61)

- Focus visible on all controls  
- Quiz options as real buttons/radios, not clickable divs only  
- Bangla+English labels announce meaningfully  
- Don’t use color alone for correct/incorrect (icon + text)

---

# 133. Settings, Continue Learning & Session UX

## Settings page fields

- UI language: বাংলা / Mixed / English  
- Accent: US / UK  
- Daily new-item cap: 10 / 15 / 20  
- Export progress (download JSON)  
- Import progress (file picker)  
- Reset progress (double confirm)  
- Soft note about custom-domain localStorage move  

## “Continue learning” logic

Priority order:

1. Due reviews > 0 → Review  
2. Incomplete Daily Challenge → Challenge  
3. Last open lesson → Resume  
4. Else → Goal-based recommended lesson  

Show Continue on Home + mobile drawer.

## Session length targets

- Micro: 3–5 min (flashcards / 5 quiz Qs)  
- Standard: ~10 min Daily Challenge  
- Deep: full lesson + quiz (15–20 min)  

Default CTAs optimize for micro/standard on mobile.

---

# 134. Internal Page Templates (Blogger)

| Template | Used by | Must include |
|---|---|---|
| Hub | Learn, Practice, skill hubs | Intro, links to children, progress snapshot, CTA |
| Lesson post | Teaching posts | §48 structure + embed hook |
| Tool | Quiz, Challenge, Lab | Full-width tool canvas; minimal chrome |
| Dashboard | My Progress | Numbers, due list, weak areas |
| Legal | Privacy/Terms/Disclaimer | Readable long-form; updated date |
| Hub-IELTS | IELTS | Disclaimer banner above content |

### Lesson embed hook (every lesson)

```html
<div
  class="efb-widget"
  data-type="lesson-practice"
  data-skill="grammar"
  data-id="grammar-present-perfect">
</div>
```

Theme loads one `learning-engine.js` globally.

---

# 135. Information Architecture QA Checklist

Before calling structure “done”:

- [ ] Every primary nav item has a live destination  
- [ ] No duplicate Challenge entry  
- [ ] MVP hides empty academies from top nav  
- [ ] Every lesson has Prev/Next + Practice/Quiz links  
- [ ] Trust pages linked in footer  
- [ ] Progress + Export reachable in ≤ 2 taps from Home  
- [ ] Level Test linked from Home hero  
- [ ] IELTS disclaimer visible on IELTS hub  
- [ ] Mobile drawer usable with one thumb  
- [ ] Bangla labels present in default mixed mode  
- [ ] Page vs Post rules followed (no 2,000 Pages for words)  
- [ ] Label taxonomy documented and used consistently  

---

# 136. Remaining Planning Pack (still maintain as living docs)

These should exist as separate files under `/docs` when build starts (see §86). Until then, this Master Plan is source of truth.

| Doc | Purpose | Status in Master Plan |
|---|---|---|
| `product-plan.md` | Vision, MVP, roadmap | Covered (§1, 68–69, 121) |
| `ia-navigation.md` | Menus, pages, URLs | **Added §124–128** |
| `ui-ux-spec.md` | Design system + screens | **Added §129–133** |
| `data-model.md` | JSON schemas | Covered (§38–39, 108) |
| `content-guidelines.md` | Editorial rules | Covered (§53–54, 82–83) |
| `seo-plan.md` | Clusters + Bangla SEO | Covered (§46–52, 105) |
| `adsense-checklist.md` | Monetization safety | Covered (§55–56, 116) |
| `analytics-events.md` | Event map | Covered (§119) |
| `qa-test-plan.md` | Functional/device tests | Covered (§84) + expand when coding |
| `brand-kit.md` | Logo, name lock, voice | **Tokens started §130 — logo/name still open decision** |
| `publish-runbook.md` | How to ship a lesson to Blogger | **§137 below** |
| `support-macros.md` | Contact reply templates | Optional later |

### Still open product decisions (track in §122)

- Final brand name + domain  
- Logo mark  
- Exact font pairing after license check  
- Whether Blog is top-nav or only footer on mobile  

---

# 137. Publish Runbook (Page / Post operations)

### New lesson post

1. Add/update JSON item(s) in Git `data/`  
2. Draft post in Blogger using lesson template  
3. Apply labels (skill + level + format)  
4. Paste embed hook with correct `data-id`  
5. Set search description  
6. Preview mobile  
7. Publish  
8. Add to Prev/Next of neighbors  
9. Share card for Facebook/YouTube if USP mistake post  

### New static page

1. Create Blogger Page  
2. Add to menu only if MVP-visible (§127)  
3. Add footer link if trust/utility  
4. Verify canonical slug  

### Menu change

1. Update Blogger Pages menu  
2. Update this doc §126 if structure changes  
3. Check mobile drawer parity  

---

# 138. Content Type Matrix (quick reference)

| User need | Content type | Where |
|---|---|---|
| Understand a topic | Lesson Post | Blog + skill label |
| Drill skills | Tool Page | Practice/* |
| See mastery | Dashboard Page | My Progress |
| Fix Bangla-speaker error | Mistake Post + Lab | Common Mistakes / Translation |
| Daily habit | Tool Page | Daily Challenge |
| SEO discovery | Pillar + cluster Posts | Blog |
| Trust / legal | Pages | Footer |
| Configure | Settings Page | More / footer |

---

# 139. UX Writing Rules (microcopy)

- Mixed mode default: Bangla first for instructions, English for language examples  
- Buttons = verbs: শুরু করুন, যাচাই করুন, পরবর্তী, প্রোগ্রেস দেখুন  
- Avoid jargon in UI: say “লেভেল অনুমান” not “CEFR certification”  
- Errors = calm + next step  
- Success = short; don’t block with long celebration  
- IELTS wording = “IELTS-style / অনুশীলন” never “official”  

---

# 140. Final v1.2 Structure Verdict

| Area | Before v1.2 | After v1.2 |
|---|---|---|
| Site tree | Rough + duplicate Challenges | Canonical §44 |
| Page/Post/Label | Missing | §124 |
| Menus | Missing | §126–127 |
| URLs | Missing | §125 |
| Screen list | Missing | §129 |
| UI design system | Named only | §130–131 |
| Empty/error UX | Missing | §132–133 |
| Publish ops | Pipeline only | §137 |

**Planning completeness for IA + Navigation + UI/UX:** previously ~35–40% → **target ~90%** for V1 build readiness. Remaining ~10% = final brand lock, visual mockups in Figma (optional), and QA scripts during implementation.

---

## End of Master Plan (v1.2)

*This document supersedes v1.0 and v1.1 where they conflict. Canonical schedules/formulas: §24–25, 41, 68, 92. Canonical IA/nav/UI: §44–45, 124–140.*
