# -*- coding: utf-8 -*-
"""Build + publish SEO article: IELTS Writing Task 2 linkers for Bengali learners."""
from __future__ import annotations

import argparse
import html as html_lib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from blogger_upload import build_service, get_blog, load_config  # noqa: E402

OUT_HTML = ROOT / "content" / "posts" / "ielts-writing-task2-linkers-bn.html"
OUT_META = ROOT / "content" / "posts" / "ielts-writing-task2-linkers-bn.meta.json"
VLISTS = ROOT / "data" / "vocabulary-lists.json"
VOCAB = ROOT / "data" / "vocabulary.json"

TITLE = "IELTS Writing Task 2 Linkers — বাংলায় অর্থ ও উদাহরণ (Band 6→7)"
LABELS = ["IELTS", "Writing", "Vocabulary", "Task 2", "বাংলা"]

BRAND = "#217a66"
WASH = "#dceee6"
BORDER = "#cfe0d7"
INK = "#1e2b26"


def esc(s: object) -> str:
    return html_lib.escape(str(s or ""), quote=True)


def tip_box(title: str, body: str) -> str:
    return (
        f'<div style="padding:14px 16px;margin:16px 0;background:{WASH};'
        f'border-left:4px solid {BRAND};border-radius:8px">'
        f"<strong>{title}</strong><br>{body}</div>"
    )


def rows_html(items: list[dict]) -> str:
    parts = [
        '<div class="efb-table-wrap">',
        f'<table style="width:100%;border-collapse:collapse;margin:0;font-size:15px;min-width:480px">',
        "<thead><tr>"
        f'<th style="text-align:left;border-bottom:2px solid {BRAND};padding:8px">Linker</th>'
        f'<th style="text-align:left;border-bottom:2px solid {BRAND};padding:8px">Use</th>'
        f'<th style="text-align:left;border-bottom:2px solid {BRAND};padding:8px">বাংলা</th>'
        f'<th style="text-align:left;border-bottom:2px solid {BRAND};padding:8px">Example</th>'
        "</tr></thead><tbody>",
    ]
    for i, w in enumerate(items):
        bg = "#f2faf6" if i % 2 == 0 else "#ffffff"
        parts.append(
            f'<tr style="background:{bg}">'
            f'<td style="padding:8px;border-bottom:1px solid {BORDER};font-weight:700;color:{INK}">{esc(w.get("word"))}</td>'
            f'<td style="padding:8px;border-bottom:1px solid {BORDER}">{esc(w.get("meaning_en"))}</td>'
            f'<td style="padding:8px;border-bottom:1px solid {BORDER}">{esc(w.get("meaning_bn"))}</td>'
            f'<td style="padding:8px;border-bottom:1px solid {BORDER}"><em>{esc(w.get("example"))}</em></td>'
            "</tr>"
        )
    parts.append("</tbody></table></div>")
    return "\n".join(parts)


GROUPS = [
    ("add", "যোগ করা (Addition)", {"moreover", "furthermore", "additionally", "in addition", "firstly", "secondly", "thirdly", "finally"}),
    ("contrast", "বিপরীত / Contrast", {"however", "nevertheless", "nonetheless", "although", "whereas", "despite", "instead", "in contrast", "on the other hand", "by contrast", "conversely", "that said"}),
    ("result", "ফলাফল (Result)", {"therefore", "consequently", "hence", "thus", "accordingly", "as a result", "otherwise"}),
    ("example", "উদাহরণ", {"for example", "for instance", "specifically", "particularly", "notably"}),
    ("compare", "তুলনা", {"similarly", "likewise", "meanwhile", "overall"}),
    ("end", "উপসংহার", {"in conclusion", "to summarise", "to summarize", "in summary"}),
]


def build_article(items: list[dict]) -> str:
    by_word = {w["word"].lower(): w for w in items}
    total = len(items)
    sections = []
    for _, title_bn, words in GROUPS:
        group_items = [by_word[w] for w in words if w in by_word]
        if not group_items:
            continue
        sections.append(f'<h2 style="color:{BRAND};margin-top:1.6rem">{esc(title_bn)}</h2>')
        sections.append(rows_html(group_items))

    html = f"""
<div class="efb-seo-article" style="color:{INK};line-height:1.65;max-width:100%">
<p style="font-size:1.05rem">IELTS Writing Task 2-এ <strong>linker / discourse marker</strong> ঠিকমতো ব্যবহার করলে ideaগুলো পরিষ্কার হয় —
Band 6 থেকে 7-এ উঠতে এটা অন্যতম practical উপায়। নিচে <strong>{total}</strong>টি useful linker আছে বাংলা অর্থ ও উদাহরণসহ (unofficial practice)।</p>

{tip_box(
    "Band tip",
    "একই linker বারবার ব্যবহার করবেন না। Addition-এর জন্য <em>moreover</em>, contrast-এর জন্য <em>however / on the other hand</em>, "
    "result-এর জন্য <em>therefore / as a result</em> — এভাবে mix করুন। Forced academic words দিয়ে sentence ভাঙবেন না।"
)}

<h2 style="color:{BRAND};margin-top:1.6rem">কেন linker গুরুত্বপূর্ণ?</h2>
<ul>
  <li><strong>Coherence &amp; Cohesion</strong> স্কোর সরাসরি ওঠে</li>
  <li>Examiner সহজে paragraph flow বোঝেন</li>
  <li>TOEFL Independent / PTE Essay-তেও একই skill কাজে লাগে</li>
</ul>

{''.join(sections)}

{tip_box(
    "Common mistake (BN learners)",
    "<strong>Moreover</strong> sentence-এর মাঝে জোর করে ঢোকাবেন না। সাধারণত নতুন sentence বা semicolon-এর পরে শুরু হয়। "
    "<em>Although</em>-এর সাথে <em>but</em> একসাথে ব্যবহার করবেন না।"
)}

<h2 style="color:{BRAND};margin-top:1.6rem">সাইটে কীভাবে প্র্যাকটিস করবেন</h2>
<ol>
  <li><a href="/p/vocabulary.html">Vocabulary</a> → <strong>IELTS Writing Linkers</strong></li>
  <li>প্রতিদিন ৮–১০টি card: অর্থ + example মুখস্থ নয় — নিজের essay sentence লিখুন</li>
  <li><a href="/p/spelling-practice.html">Spelling Practice</a> → <strong>IELTS Writing Markers</strong></li>
  <li>সম্পর্কিত list: <strong>IELTS Writing Task 2</strong>, <strong>Exam Collocations Core</strong>, <strong>Task 1 · Graphs</strong></li>
</ol>

<p>
  <a href="/p/vocabulary.html" style="display:inline-block;margin:6px 6px 6px 0;background:{BRAND};color:#fff;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700">Vocabulary খুলুন →</a>
  <a href="/p/spelling-practice.html" style="display:inline-block;margin:6px 6px 6px 0;background:#fff;color:{BRAND};padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700;border:2px solid {BRAND}">Spelling Practice →</a>
</p>

<h2 style="color:{BRAND};margin-top:1.6rem">FAQ</h2>
<p><strong>প্রশ্ন: কতগুলো linker মুখস্থ করলেই হবে?</strong><br>
উত্তর: ১৫–২০টি active linker যথেষ্ট — কিন্তু প্রতিটির <em>function</em> বুঝে ব্যবহার করতে হবে।</p>
<p><strong>প্রশ্ন: এটা কি official Cambridge list?</strong><br>
উত্তর: না। এটি Bengali learners-এর জন্য unofficial practice set। IELTS® British Council / IDP / Cambridge-এর সাথে affiliated নয়।</p>

<hr style="border:none;border-top:1px solid {BORDER};margin:24px 0">
<p style="font-size:0.95rem;color:#5c6b64"><em>English for Bengalis</em> — Writing vocabulary + interactive practice.
Don't just study English. Know exactly what you have mastered.</p>
</div>
"""
    return html.strip() + "\n"


def load_linker_entries() -> list[dict]:
    vmeta = json.loads(VLISTS.read_text(encoding="utf-8"))
    bank = {w["id"]: w for w in json.loads(VOCAB.read_text(encoding="utf-8"))}
    ids = []
    for L in vmeta.get("lists") or []:
        if L.get("id") == "ielts-writing-linkers":
            ids = list(L.get("word_ids") or [])
            break
    items = []
    for wid in ids:
        w = bank.get(wid)
        if w:
            items.append(w)
    return items


def find_post_by_title(service, blog_id: str, title: str):
    title_l = title.strip().lower()
    token = None
    while True:
        kwargs = {"blogId": blog_id, "maxResults": 50, "status": "LIVE"}
        if token:
            kwargs["pageToken"] = token
        resp = service.posts().list(**kwargs).execute()
        for item in resp.get("items") or []:
            if item.get("title", "").strip().lower() == title_l:
                return item
        token = resp.get("nextPageToken")
        if not token:
            break
    resp = service.posts().list(blogId=blog_id, maxResults=50, status="DRAFT").execute()
    for item in resp.get("items") or []:
        if item.get("title", "").strip().lower() == title_l:
            return item
    return None


def upsert_post(service, blog_id: str, title: str, content: str, labels: list[str], draft: bool):
    existing = find_post_by_title(service, blog_id, title)
    body = {"title": title, "content": content, "labels": labels}
    if existing:
        print("Updating post id:", existing.get("id"))
        return service.posts().update(blogId=blog_id, postId=existing["id"], body={**existing, **body}).execute()
    print("Creating post...", "[DRAFT]" if draft else "[LIVE]")
    return service.posts().insert(blogId=blog_id, body=body, isDraft=draft).execute()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()

    items = load_linker_entries()
    if len(items) < 10:
        raise SystemExit("Run tools/import_exam_writing_pack.py first")

    html = build_article(items)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html, encoding="utf-8")
    OUT_META.write_text(
        json.dumps(
            {"title": TITLE, "labels": LABELS, "file": str(OUT_HTML.relative_to(ROOT)), "count": len(items)},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("Wrote", OUT_HTML, "items=", len(items))

    if args.build_only:
        return

    cfg = load_config()
    service = build_service()
    blog = get_blog(service, cfg["blog_url"])
    last = None
    for attempt in range(1, 5):
        try:
            result = upsert_post(service, blog["id"], TITLE, html, LABELS, draft=args.draft)
            print("Post URL:", result.get("url") or result.get("id"))
            return
        except Exception as e:
            last = e
            print(f"Upload attempt {attempt} failed:", e)
            time.sleep(15 * attempt)
    raise last


if __name__ == "__main__":
    main()
