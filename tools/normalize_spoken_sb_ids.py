# -*- coding: utf-8 -*-
"""Normalize spoken + sentence-builder ids for progress dashboard."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIG = ROOT / "data" / "progress_id_migrate.json"


def slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower().strip())
    return s.strip("-") or "item"


def main():
    migrate = {}
    if MIG.exists():
        migrate = json.loads(MIG.read_text(encoding="utf-8"))

    sp_path = ROOT / "data" / "spoken.json"
    spoken = json.loads(sp_path.read_text(encoding="utf-8"))
    for d in spoken:
        old = str(d.get("id") or "")
        if old.startswith("spoken:"):
            continue
        title = d.get("title") or d.get("title_bn") or old
        new = f"spoken:{slug(title)}"
        if old and old != new:
            migrate[old] = new
        d["id"] = new
        # unify level field used by page
        if not d.get("level") and d.get("cefr"):
            d["level"] = d["cefr"]
        if not d.get("cefr") and d.get("level"):
            d["cefr"] = d["level"]
    sp_path.write_text(json.dumps(spoken, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sb_path = ROOT / "data" / "sentence-builder.json"
    sb = json.loads(sb_path.read_text(encoding="utf-8"))
    for item in sb:
        old = str(item.get("id") or "")
        if old.startswith("sb:"):
            continue
        # sb1 -> sb:1 keep stable numeric suffix
        m = re.match(r"^sb(\d+)$", old)
        new = f"sb:{m.group(1)}" if m else f"sb:{slug(old)}"
        if old and old != new:
            migrate[old] = new
        item["id"] = new
    sb_path.write_text(json.dumps(sb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    MIG.write_text(json.dumps(migrate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("spoken", len(spoken), "all spoken:", all(x["id"].startswith("spoken:") for x in spoken))
    print("sb", len(sb), "all sb:", all(x["id"].startswith("sb:") for x in sb))
    print("migrate keys", len(migrate))


if __name__ == "__main__":
    main()
