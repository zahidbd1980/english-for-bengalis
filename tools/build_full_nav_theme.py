#!/usr/bin/env python3
"""Build working theme + full PageList navigation from live Blogger pages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

# Reuse auth from blogger_upload
from blogger_upload import build_service, load_config, get_blog  # type: ignore

SRC = ROOT / "themeCode-MINIMAL.txt"
if not SRC.exists():
    SRC = ROOT / "backup" / "theme-indie-original-backup.xml"

OUT = ROOT / "themeCode-FULLNAV.txt"
OUT2 = ROOT / "themeCode.txt"

# Preferred menu order (titles must match Blogger page titles)
ORDER = [
    "Home",
    "Learn",
    "Practice",
    "Quizzes",
    "Daily Challenge",
    "Vocabulary",
    "Grammar",
    "Common Mistakes",
    "My Progress",
    "Level Test",
    "IELTS",
    "Translation Lab",
    "Flashcards",
    "Phrasal Verbs",
    "Spelling",
    "Spoken English",
    "Settings",
    "About",
    "Contact",
    "Privacy Policy",
    "Terms",
    "Disclaimer",
]


def list_all_pages(service, blog_id: str) -> list[dict]:
    items = []
    token = None
    while True:
        kwargs = {"blogId": blog_id, "view": "ADMIN", "maxResults": 50}
        if token:
            kwargs["pageToken"] = token
        resp = service.pages().list(**kwargs).execute()
        items.extend(resp.get("items") or [])
        token = resp.get("nextPageToken")
        if not token:
            break
    return items


def main() -> None:
    cfg = load_config()
    service = build_service()
    blog = get_blog(service, cfg["blog_url"])
    pages = list_all_pages(service, blog["id"])
    print(f"Found {len(pages)} pages")

    by_title = {p.get("title", "").strip(): p for p in pages}

    page_list: dict = {
        "home": {
            "href": cfg["blog_url"].rstrip("/") + "/",
            "position": 0,
            "title": "Home",
        }
    }

    pos = 1
    missing = []
    for title in ORDER:
        if title == "Home":
            continue
        p = by_title.get(title)
        if not p:
            missing.append(title)
            continue
        page_list[str(p["id"])] = {
            "href": p.get("url"),
            "position": pos,
            "title": title,
        }
        pos += 1
        print(f"  + {title} -> {p.get('url')}")

    if missing:
        print("Missing titles (skipped):", ", ".join(missing))

    json_str = json.dumps(page_list, ensure_ascii=False, separators=(",", ":"))

    theme = SRC.read_text(encoding="utf-8")
    # ensure visible
    theme = theme.replace(
        "id='PageList1' locked='true' title='' type='PageList' visible='false'",
        "id='PageList1' locked='true' title='' type='PageList' visible='true'",
    )
    theme = theme.replace(
        "id='PageList1' locked='true' title='Menu' type='PageList' visible='true'",
        "id='PageList1' locked='true' title='' type='PageList' visible='true'",
    )

    import re

    pat = re.compile(
        r"(<b:widget-setting name='pageListJson'><!\[CDATA\[)(.*?)(\]\]></b:widget-setting>)",
        re.S,
    )
    if not pat.search(theme):
        raise SystemExit("pageListJson setting not found in theme")
    theme = pat.sub(rf"\g<1>{json_str}\g<3>", theme, count=1)

    # tiny safe menu CSS (no @import)
    css = """
/* EFB full nav */
.blog-name .PageList ul.tabs{display:flex;flex-wrap:wrap;justify-content:center;gap:2px}
.blog-name .PageList ul.tabs li a{padding:8px 11px !important;border-radius:8px;font-weight:700}
.blog-name .PageList ul.tabs li.selected a,.blog-name .PageList ul.tabs li a:hover{background:rgba(255,255,255,0.16)}
.sticky .PageList ul.tabs li a{color:#0f6b5c !important}
"""
    if "EFB full nav" not in theme:
        theme = theme.replace("]]></b:skin>", css + "]]></b:skin>", 1)

    if theme.count("<![CDATA[") != theme.count("]]>"):
        raise SystemExit("CDATA imbalance")

    OUT.write_text(theme, encoding="utf-8", newline="\n")
    OUT2.write_text(theme, encoding="utf-8", newline="\n")
    print("Wrote", OUT)
    print("Menu items:", len(page_list))


if __name__ == "__main__":
    main()
