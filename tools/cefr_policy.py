# -*- coding: utf-8 -*-
"""Site policy: lists target intermediate–advanced learners (B1+). Never collect A1/A2."""
from __future__ import annotations

import re

BEGINNER_LEVELS = {"a1", "a2"}
MIN_LIST_CEFR = "B1"
# Dedicated beginner packs — drop from the public catalogue (do not refill).
BEGINNER_ONLY_LIST_IDS = frozenset(
    {
        "path-week-1-survival",
        "target-a1-core",
        "target-a2-bridge",
    }
)


def normalize_cefr(level: str | None) -> str:
    return (level or "").strip().lower().replace("–", "-").replace("—", "-")


def is_beginner_cefr(level: str | None) -> bool:
    """True if the primary CEFR tag is A1 or A2."""
    s = normalize_cefr(level)
    if not s:
        return False
    first = re.split(r"[-/, ]+", s)[0]
    return first in BEGINNER_LEVELS


def word_cefr(entry: dict | None) -> str:
    if not entry:
        return ""
    return str(entry.get("cefr_level") or entry.get("cefr") or "")


def keep_word(entry: dict | None) -> bool:
    return not is_beginner_cefr(word_cefr(entry))


def filter_list_ids(ids: list | None, lookup: dict) -> list[str]:
    """Keep B1+ ids only. Drop missing vocab:/verb: ids."""
    out: list[str] = []
    seen: set[str] = set()
    for wid in ids or []:
        if not wid or wid in seen:
            continue
        entry = lookup.get(wid)
        if entry is None:
            if str(wid).startswith(("vocab:", "verb:")):
                continue
            out.append(wid)
            seen.add(wid)
            continue
        if keep_word(entry):
            out.append(wid)
            seen.add(wid)
    return out


def list_cefr_label(existing: str | None = None) -> str:
    s = normalize_cefr(existing)
    if not s or is_beginner_cefr(s):
        return "B1–C1"
    # already B1+ range
    if s.startswith("b") or s.startswith("c"):
        raw = (existing or "B1–C1").replace("A1–", "").replace("A2–", "")
        raw = raw.replace("A1-", "").replace("A2-", "")
        return raw or "B1–C1"
    return "B1–C1"
