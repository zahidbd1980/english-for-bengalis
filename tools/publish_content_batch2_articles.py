# -*- coding: utf-8 -*-
"""Build + publish multiple SEO articles from vocab lists (Bangla learners)."""
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

VOCAB = ROOT / "data" / "vocabulary.json"
VLISTS = ROOT / "data" / "vocabulary-lists.json"
OUT_DIR = ROOT / "content" / "posts"

BRAND = "#217a66"
WASH = "#dceee6"
BORDER = "#cfe0d7"
INK = "#1e2b26"


def esc(s: object) -> str:
    return html_lib.escape(str(s or ""), quote=True)


def tip(title: str, body: str) -> str:
    return (
        f'<div style="padding:14px 16px;margin:16px 0;background:{WASH};'
        f'border-left:4px solid {BRAND};border-radius:8px">'
        f"<strong>{title}</strong><br>{body}</div>"
    )


def table(items: list[dict], cols: str = "full") -> str:
    parts = [
        '<div class="efb-table-wrap">',
        f'<table style="width:100%;border-collapse:collapse;margin:0;font-size:15px;min-width:460px">',
        "<thead><tr>"
        f'<th style="text-align:left;border-bottom:2px solid {BRAND};padding:8px">Word</th>'
        f'<th style="text-align:left;border-bottom:2px solid {BRAND};padding:8px">বাংলা</th>'
        f'<th style="text-align:left;border-bottom:2px solid {BRAND};padding:8px">Example</th>'
        "</tr></thead><tbody>",
    ]
    for i, w in enumerate(items):
        bg = "#f2faf6" if i % 2 == 0 else "#ffffff"
        parts.append(
            f'<tr style="background:{bg}">'
            f'<td style="padding:8px;border-bottom:1px solid {BORDER};font-weight:700">{esc(w.get("word"))}</td>'
            f'<td style="padding:8px;border-bottom:1px solid {BORDER}">{esc(w.get("meaning_bn"))}</td>'
            f'<td style="padding:8px;border-bottom:1px solid {BORDER}"><em>{esc(w.get("example"))}</em></td>'
            "</tr>"
        )
    parts.append("</tbody></table></div>")
    return "\n".join(parts)


def load_list(list_id: str) -> list[dict]:
    vmeta = json.loads(VLISTS.read_text(encoding="utf-8"))
    bank = {w["id"]: w for w in json.loads(VOCAB.read_text(encoding="utf-8"))}
    ids = []
    for L in vmeta.get("lists") or []:
        if L.get("id") == list_id:
            ids = list(L.get("word_ids") or [])
            break
    return [bank[i] for i in ids if i in bank]


def find_post_by_title(service, blog_id: str, title: str):
    title_l = title.strip().lower()
    for status in ("LIVE", "DRAFT"):
        token = None
        while True:
            kwargs = {"blogId": blog_id, "maxResults": 50, "status": status}
            if token:
                kwargs["pageToken"] = token
            resp = service.posts().list(**kwargs).execute()
            for item in resp.get("items") or []:
                if item.get("title", "").strip().lower() == title_l:
                    return item
            token = resp.get("nextPageToken")
            if not token or status == "DRAFT":
                break
        if status == "DRAFT":
            break
    return None


def safe_print(*args):
    msg = " ".join(str(a) for a in args)
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", "replace").decode("ascii"))


def upsert_post(service, blog_id: str, title: str, content: str, labels: list[str], draft: bool):
    existing = find_post_by_title(service, blog_id, title)
    body = {"title": title, "content": content, "labels": labels}
    if existing:
        safe_print("Updating:", title)
        return service.posts().update(blogId=blog_id, postId=existing["id"], body={**existing, **body}).execute()
    safe_print("Creating:", title, "[DRAFT]" if draft else "[LIVE]")
    return service.posts().insert(blogId=blog_id, body=body, isDraft=draft).execute()


def article_task1(items: list[dict]) -> tuple[str, str, list[str]]:
    title = "IELTS Writing Task 1 Graph Language — বাংলায় Cheat-sheet"
    labels = ["IELTS", "Writing", "Task 1", "Vocabulary", "বাংলা"]
    html = f"""
<div class="efb-seo-article" style="color:{INK};line-height:1.65">
<p>IELTS Academic Writing Task 1-এ নম্বর বাড়ে যদি আপনি শুধু <em>increase/decrease</em> না বলে <strong>trend language</strong> বৈচিত্র্যময়ভাবে ব্যবহার করেন।
নিচে <strong>{len(items)}</strong>টি high-value word/phrase আছে বাংলা অর্থসহ (unofficial practice)।</p>
{tip("Band tip", "Overview-এ overall trend লিখুন (rose / fell / fluctuated)। Detail paragraph-এ numbers দিন। Personal opinion Task 1-এ নয়।")}
<h2 style="color:{BRAND}">Word bank</h2>
{table(items)}
<h2 style="color:{BRAND}">Ready sentence frames</h2>
<ul>
<li>Overall, X <strong>rose steadily</strong>, while Y <strong>declined slightly</strong>.</li>
<li>X <strong>peaked</strong> in 2018, then <strong>fell dramatically</strong>.</li>
<li><strong>Compared with</strong> 2005, the 2015 figure was <strong>twice as high</strong>.</li>
<li>Group A <strong>accounted for</strong> roughly one third of the total.</li>
</ul>
<h2 style="color:{BRAND}">সাইটে প্র্যাকটিস</h2>
<ol>
<li><a href="/p/vocabulary.html">Vocabulary</a> → <strong>IELTS Writing Task 1 · Graphs</strong></li>
<li><a href="/p/spelling-practice.html">Spelling</a> → <strong>IELTS Task 1 Spellings</strong></li>
<li>সম্পর্কিত: Writing Linkers, Exam Collocations Core</li>
</ol>
<p>
<a href="/p/vocabulary.html" style="display:inline-block;margin:6px 6px 6px 0;background:{BRAND};color:#fff;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700">Vocabulary →</a>
</p>
<p style="font-size:0.95rem;color:#5c6b64"><em>Unofficial</em> — IELTS® bodies-এর সাথে affiliated নয়।</p>
</div>
""".strip()
    return title, html + "\n", labels


def article_colloc(items: list[dict]) -> tuple[str, str, list[str]]:
    title = "IELTS TOEFL PTE Collocations — make/do/take ভুল এড়ান (বাংলা)"
    labels = ["IELTS", "TOEFL", "PTE", "Collocations", "Vocabulary", "বাংলা"]
    html = f"""
<div class="efb-seo-article" style="color:{INK};line-height:1.65">
<p>Exam writing-এ <strong>collocation</strong> (শব্দের স্বাভাবিক জোড়া) ভুল হলে band/score কাটে —
যেমন <em>do a decision</em> ❌, সঠিক <em>make a decision</em> ✅।
নিচে <strong>{len(items)}</strong>টি exam-friendly collocation (unofficial)।</p>
{tip("Memory tip", "make → decision/effort/progress/mistake · do → research/homework/business · take → part/responsibility/advantage")}
{table(items)}
<h2 style="color:{BRAND}">প্র্যাকটিস লিংক</h2>
<ol>
<li><a href="/p/vocabulary.html">Vocabulary</a> → <strong>Exam Collocations Core</strong></li>
<li>Essay লিখার সময় প্রতি paragraph-এ ১টি collocation ইচ্ছাকৃত ব্যবহার করুন</li>
</ol>
<p><a href="/p/vocabulary.html" style="display:inline-block;background:{BRAND};color:#fff;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700">Collocation list খুলুন →</a></p>
<p style="font-size:0.95rem;color:#5c6b64">Unofficial practice for IELTS / TOEFL / PTE learners from Bangladesh.</p>
</div>
""".strip()
    return title, html + "\n", labels


def article_listening_traps(items: list[dict]) -> tuple[str, str, list[str]]:
    title = "IELTS Listening Part 1 Spelling Traps — ফর্ম ফিলিংয়ে নম্বর বাঁচান"
    labels = ["IELTS", "Listening", "Spelling", "Vocabulary", "বাংলা"]
    html = f"""
<div class="efb-seo-article" style="color:{INK};line-height:1.65">
<p>Listening Part 1-এ উত্তর ঠিক শুনেও <strong>বানান ভুলে</strong> নম্বর কাটে।
নিচে <strong>{len(items)}</strong>টি common trap — accommodation, necessary, Wednesday… (unofficial)।</p>
{tip("Drill", "Spelling Practice-এ শুনে লিখুন। British spelling (centre/organise) পরীক্ষা অনুযায়ী মেনে চলুন।")}
{table(items)}
<h2 style="color:{BRAND}">কীভাবে অনুশীলন করবেন</h2>
<ol>
<li><a href="/p/spelling-practice.html">Spelling Practice</a> → <strong>IELTS Listening Form Traps</strong></li>
<li><a href="/p/vocabulary.html">Vocabulary</a> → একই list</li>
<li>বড় list: <strong>IELTS Listening · 1600</strong></li>
</ol>
<p>
<a href="/p/spelling-practice.html" style="display:inline-block;margin:6px 6px 6px 0;background:{BRAND};color:#fff;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700">এখনই Spelling →</a>
</p>
<p style="font-size:0.95rem;color:#5c6b64">Unofficial — official IELTS bodies-এর সাথে সম্পর্ক নেই।</p>
</div>
""".strip()
    return title, html + "\n", labels


def article_speaking(items: list[dict]) -> tuple[str, str, list[str]]:
    title = "IELTS Speaking Part 1 Vocabulary — Hometown, Hobby, Study (বাংলা)"
    labels = ["IELTS", "Speaking", "Vocabulary", "বাংলা"]
    html = f"""
<div class="efb-seo-article" style="color:{INK};line-height:1.65">
<p>Speaking Part 1 ছোট প্রশ্ন — কিন্তু vocabulary পুনরাবৃত্তি হলে score থেমে যায়।
নিচে <strong>{len(items)}</strong>টি micro-topic word/phrase: hometown, leisure, study/work (unofficial)।</p>
{tip("Fluency tip", "১ বাক্যে থামবেন না। Reason + example দিন: I prefer tea because… For example…")}
{table(items)}
<h2 style="color:{BRAND}">প্র্যাকটিস</h2>
<ol>
<li><a href="/p/vocabulary.html">Vocabulary</a> → <strong>IELTS Speaking Part 1</strong></li>
<li><a href="/p/spoken-drill.html">Spoken Drill</a> দিয়ে জোরে অনুশীলন</li>
</ol>
<p><a href="/p/vocabulary.html" style="display:inline-block;background:{BRAND};color:#fff;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700">Speaking list →</a></p>
</div>
""".strip()
    return title, html + "\n", labels


ARTICLES = [
    ("ielts-task1-graphs", "ielts-writing-task1-graphs-bn.html", article_task1),
    ("exam-collocations-core", "ielts-toefl-pte-collocations-bn.html", article_colloc),
    ("ielts-listening-spelling-traps", "ielts-listening-spelling-traps-bn.html", article_listening_traps),
    ("ielts-speaking-part1", "ielts-speaking-part1-vocab-bn.html", article_speaking),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    built = []
    for list_id, filename, builder in ARTICLES:
        items = load_list(list_id)
        if len(items) < 8:
            print("SKIP (too few):", list_id)
            continue
        title, html, labels = builder(items)
        path = OUT_DIR / filename
        path.write_text(html, encoding="utf-8")
        meta = {"title": title, "labels": labels, "file": str(path.relative_to(ROOT)), "count": len(items)}
        path.with_suffix(".meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        built.append((title, html, labels, path))
        safe_print("Wrote", path.name, "items=", len(items))

    if args.build_only:
        return

    cfg = load_config()
    service = build_service()
    blog = get_blog(service, cfg["blog_url"])
    for title, html, labels, path in built:
        last = None
        for attempt in range(1, 4):
            try:
                result = upsert_post(service, blog["id"], title, html, labels, draft=args.draft)
                safe_print("URL:", result.get("url") or result.get("id"))
                break
            except Exception as e:
                last = e
                safe_print("fail", attempt, e)
                time.sleep(10 * attempt)
        else:
            raise last


if __name__ == "__main__":
    main()
