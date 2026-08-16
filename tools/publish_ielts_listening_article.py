# -*- coding: utf-8 -*-
"""Build + publish SEO article: IELTS Listening 1600 words for Bengali learners.

Includes EVERY word from the source JSON, grouped by category.
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from blogger_upload import (  # noqa: E402
    build_service,
    get_blog,
    load_config,
)

SRC = ROOT / "various words lists" / "ielts-listening-1600-words.json"
OUT_HTML = ROOT / "content" / "posts" / "ielts-listening-1600-words-bn.html"
OUT_META = ROOT / "content" / "posts" / "ielts-listening-1600-words-bn.meta.json"

TITLE = "IELTS Listening Vocabulary 1600 Words — বাংলায় শিখুন (Spelling + Meaning)"
LABELS = ["IELTS", "Listening", "Vocabulary", "Spelling", "বাংলা"]

BRAND = "#217a66"
WASH = "#dceee6"
BORDER = "#cfe0d7"
INK = "#1e2b26"

# Display order + Bangla titles for categories in source JSON
CATEGORY_META = [
    ("education", "Education / Campus / Study", "একাডেমিক ও ক্যাম্পাস"),
    ("travel", "Travel & Transport", "ভ্রমণ ও যাতায়াত"),
    ("health", "Health & Appointments", "স্বাস্থ্য ও অ্যাপয়েন্টমেন্ট"),
    ("shopping", "Shopping & Money", "কেনাকাটা ও টাকা"),
    ("food", "Food & Restaurant", "খাবার ও রেস্তোরাঁ"),
    ("home", "Home & Accommodation", "বাড়ি ও আবাসন"),
    ("office", "Office & Work", "অফিস ও কাজ"),
    ("daily", "Daily Life", "দৈনন্দিন জীবন"),
    ("outdoor", "Outdoor & Places", "বাইরে ও স্থান"),
    ("nature", "Nature & Environment", "প্রকৃতি ও পরিবেশ"),
    ("technology", "Technology", "প্রযুক্তি"),
    ("verbs", "Useful Verbs", "প্রয়োজনীয় ভার্ব"),
    ("ielts", "IELTS High-frequency", "IELTS বহুল ব্যবহৃত"),
]


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
        f'<th style="text-align:left;border-bottom:2px solid {BRAND};padding:8px">Word</th>'
        f'<th style="text-align:left;border-bottom:2px solid {BRAND};padding:8px">Meaning (EN)</th>'
        f'<th style="text-align:left;border-bottom:2px solid {BRAND};padding:8px">বাংলা অর্থ</th>'
        "</tr></thead><tbody>",
    ]
    for i, w in enumerate(items):
        bg = "#f2faf6" if i % 2 == 0 else "#ffffff"
        parts.append(
            f'<tr style="background:{bg}">'
            f'<td style="padding:8px;border-bottom:1px solid {BORDER}"><strong>{esc(w.get("word"))}</strong></td>'
            f'<td style="padding:8px;border-bottom:1px solid {BORDER}">{esc(w.get("meaning_en"))}</td>'
            f'<td style="padding:8px;border-bottom:1px solid {BORDER}">{esc(w.get("meaning_bn"))}</td>'
            "</tr>"
        )
    parts.append("</tbody></table></div>")
    return "\n".join(parts)


def build_article(words: list[dict]) -> str:
    total = len(words)
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for w in words:
        cat = (w.get("category") or "ielts").strip().lower()
        by_cat[cat].append(w)

    for cat in by_cat:
        by_cat[cat].sort(key=lambda x: (x.get("word") or "").lower())

    known = {c for c, _, _ in CATEGORY_META}
    extra_cats = sorted(c for c in by_cat if c not in known)

    toc_items = []
    sections = []
    section_i = 0

    for cat, en_title, bn_title in CATEGORY_META:
        items = by_cat.get(cat) or []
        if not items:
            continue
        section_i += 1
        anchor = f"cat-{cat}"
        toc_items.append(
            f'<li><a href="#{anchor}" style="color:{BRAND};font-weight:600">'
            f"{section_i}) {esc(en_title)}</a> — {esc(bn_title)} "
            f"(<strong>{len(items)}</strong>)</li>"
        )
        sections.append(
            f'<h2 id="{anchor}" style="color:{BRAND};margin-top:1.8rem">'
            f"{section_i}) {esc(en_title)} · {esc(bn_title)} "
            f"<span style=\"font-size:0.85rem;font-weight:600;color:#5c6b64\">({len(items)} words)</span>"
            f"</h2>\n"
            f"<p class=\"bn\">এই গ্রুপের <strong>{len(items)}</strong>টি শব্দ — Word · Meaning · বাংলা অর্থ।</p>\n"
            f"{rows_html(items)}"
        )

    for cat in extra_cats:
        items = by_cat[cat]
        section_i += 1
        anchor = f"cat-{cat}"
        title = cat.replace("_", " ").title()
        toc_items.append(
            f'<li><a href="#{anchor}" style="color:{BRAND};font-weight:600">'
            f"{section_i}) {esc(title)}</a> (<strong>{len(items)}</strong>)</li>"
        )
        sections.append(
            f'<h2 id="{anchor}" style="color:{BRAND};margin-top:1.8rem">'
            f"{section_i}) {esc(title)} "
            f"<span style=\"font-size:0.85rem;font-weight:600;color:#5c6b64\">({len(items)} words)</span>"
            f"</h2>\n"
            f"{rows_html(items)}"
        )

    # Spelling traps highlight (subset still useful as tip, words already in full tables)
    trap_names = {
        "accommodation", "necessary", "environment", "separate", "definitely",
        "committee", "questionnaire", "rhythm", "conscious", "guarantee",
        "colleague", "fascinating", "occurrence", "embarrassed", "recommend",
    }
    traps = [w for w in words if (w.get("word") or "").lower() in trap_names]
    traps.sort(key=lambda x: (x.get("word") or "").lower())

    html = f"""
<div style="font-family:'Source Sans 3','Noto Sans Bengali',Segoe UI,sans-serif;line-height:1.7;color:{INK};max-width:100%;box-sizing:border-box">

<p style="font-size:1.05rem"><strong>IELTS Listening</strong>-এ অনেক শিক্ষার্থী শব্দ বোঝেন, কিন্তু <em>বানান</em> ভুল লেখেন — আর Band score কমে যায়।
এই আর্টিকেলে <strong>IELTS Listening Vocabulary {total} Words</strong> তালিকার <strong>প্রতিটি শব্দ</strong>
ইংরেজি অর্থ + বাংলা অর্থসহ দেওয়া আছে। থিম অনুযায়ী পড়ুন, তারপর সাইটে Spelling Practice করুন।</p>

{tip_box(
    "এই পোস্টে যা আছে",
    f"সম্পূর্ণ <strong>{total}</strong>টি শব্দ (Word · Meaning EN · বাংলা অর্থ), ক্যাটাগরি অনুযায়ী সাজানো। "
    "নিচে Table of Contents থেকে যেকোনো গ্রুপে যান। Practice: Vocabulary + Spelling Practice লিঙ্ক।"
)}

<h2 style="color:{BRAND};margin-top:1.6rem">কেন IELTS Listening-এ Vocabulary এত জরুরি?</h2>
<p>Listening টেস্টে আপনি শুধু “শুনবেন” না — <strong>Form / Note / Table completion</strong>-এ সঠিক বানান লিখতে হবে।
এক অক্ষর ভুল হলেও উত্তর ভুল ধরা হয়। তাই এই তালিকা শুধু মুখস্থ নয় —
<strong>শোনা → বোঝা → সঠিক বানানে লেখা</strong>র প্রশিক্ষণ।</p>

<ul>
  <li><strong>Section 1–2:</strong> daily life — booking, shopping, travel, address</li>
  <li><strong>Section 3–4:</strong> study / academic — lecture, research, campus life</li>
</ul>

<p>ইন্টারঅ্যাকটিভ প্র্যাকটিস (অডিও + quiz + progress):</p>
<p>
  <a href="/p/vocabulary.html" style="color:{BRAND};font-weight:700">Vocabulary → IELTS Listening · 1600 Words</a><br>
  <a href="/p/spelling-practice.html" style="color:{BRAND};font-weight:700">Spelling Practice → IELTS Listening · 1600 Spellings</a>
</p>

<h2 style="color:{BRAND};margin-top:1.6rem">কীভাবে পড়বেন (টিচারের পরামর্শ)</h2>
<ol>
  <li>প্রতিদিন <strong>২০–৩০টি</strong> শব্দ — এক গ্রুপ শেষ করে পরের গ্রুপ।</li>
  <li>শব্দ জোরে বলুন → বানান কল্পনা করুন → কাগজে লিখুন।</li>
  <li>একই দিনে <a href="/p/spelling-practice.html">Spelling Practice</a>-এ শুনে লেখো।</li>
  <li>ভুল হলে Mistake Bank / Review due দিয়ে আবার করুন।</li>
</ol>

<h2 style="color:{BRAND};margin-top:1.6rem">Table of Contents · বিষয়সূচি</h2>
<p class="bn">মোট শব্দ: <strong>{total}</strong> · মোবাইলে টেবিল সাইডে সোয়াইপ করে পড়ুন।</p>
<ol>
{chr(10).join(toc_items)}
</ol>

{chr(10).join(sections)}

<h2 id="spelling-traps" style="color:{BRAND};margin-top:1.8rem">Spelling traps — বাংলাভাষীরা যেখানে বেশি ভুল করেন</h2>
<p>নিচের শব্দগুলো Listening answer sheet-এ বেশি marks কাটায়। উপরে পূর্ণ তালিকায়ও আছে — এখানে আলাদা করে drill করুন।</p>
{rows_html(traps)}
{tip_box(
    "Memory trick",
    "<strong>accommodation</strong> = ২টি <em>c</em> + ২টি <em>m</em> (cc + mm)। "
    "<strong>necessary</strong> = ১টি <em>c</em> + ২টি <em>s</em>। একবার ছন্দে মুখস্থ করুন।"
)}

<h2 style="color:{BRAND};margin-top:1.6rem">কীভাবে আমাদের সাইটে প্র্যাকটিস করবেন</h2>
<ol>
  <li><a href="/p/vocabulary.html">Vocabulary</a> → Target list: <strong>IELTS Listening · 1600 Words</strong></li>
  <li>প্রতিদিন ১৫–২০টি কার্ড (বাংলা অর্থ + উদাহরণ)</li>
  <li><a href="/p/spelling-practice.html">Spelling Practice</a> → একই লিস্ট → শুনে লেখো</li>
  <li>ভুল → Mistake Bank / Review due</li>
  <li><a href="/p/daily-challenge.html">Daily Challenge</a> দিয়ে streak ধরে রাখুন</li>
</ol>

<p>
  <a href="/p/spelling-practice.html" style="display:inline-block;margin:6px 6px 6px 0;background:{BRAND};color:#fff;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700;max-width:100%;box-sizing:border-box">এখনই Spelling Practice শুরু করুন →</a>
  <a href="/p/vocabulary.html" style="display:inline-block;margin:6px 6px 6px 0;background:#fff;color:{BRAND};padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700;border:2px solid {BRAND};max-width:100%;box-sizing:border-box">Vocabulary List খুলুন →</a>
</p>

<h2 style="color:{BRAND};margin-top:1.6rem">FAQ</h2>
<p><strong>প্রশ্ন: সব {total} শব্দ কি একদিনে মুখস্থ করতে হবে?</strong><br>
উত্তর: না। থিম অনুযায়ী ছোট ব্যাচে শিখুন। আগে Education / Travel / Health, তারপর বাকি।</p>
<p><strong>প্রশ্ন: এটা কি অফিসিয়াল Cambridge লিস্ট?</strong><br>
উত্তর: না — IELTS Listening-এ বহুল দেখা যায় এমন শব্দের <em>unofficial practice list</em>।
IELTS® British Council / IDP / Cambridge-এর সাথে affiliated নয়।</p>
<p><strong>প্রশ্ন: বাংলা অর্থ কি Listening-এ সাহায্য করে?</strong><br>
উত্তর: হ্যাঁ। অর্থ পরিষ্কার থাকলে অডিওর situation দ্রুত বোঝেন, ফাঁকা জায়গায় সঠিক শব্দ predict করতে পারেন।</p>

<hr style="border:none;border-top:1px solid {BORDER};margin:24px 0">
<p style="font-size:0.95rem;color:#5c6b64"><em>English for Bengalis</em> — সম্পূর্ণ {total}-শব্দের তালিকা এই পোস্টে।
Interactive practice: Vocabulary + Spelling + Progress Tracking।
Don't just study English. Know exactly what you have mastered.</p>

</div>
"""
    return html.strip() + "\n"


def safe_print(*args):
    msg = " ".join(str(a) for a in args)
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", "replace").decode("ascii"))


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
    body = {
        "title": title,
        "content": content,
        "labels": labels,
    }
    if existing:
        safe_print("Updating post id:", existing.get("id"))
        return (
            service.posts()
            .update(blogId=blog_id, postId=existing["id"], body={**existing, **body})
            .execute()
        )
    safe_print("Creating post...", "[DRAFT]" if draft else "[LIVE]")
    return service.posts().insert(blogId=blog_id, body=body, isDraft=draft).execute()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()

    words = json.loads(SRC.read_text(encoding="utf-8"))
    if not isinstance(words, list) or not words:
        raise SystemExit("Source JSON empty or invalid")

    html = build_article(words)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html, encoding="utf-8")
    OUT_META.write_text(
        json.dumps(
            {
                "title": TITLE,
                "labels": LABELS,
                "file": str(OUT_HTML.relative_to(ROOT)),
                "word_count": len(words),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    safe_print("Wrote", OUT_HTML, "bytes=", OUT_HTML.stat().st_size, "words=", len(words))

    if args.build_only:
        return

    cfg = load_config()
    service = build_service()
    blog = get_blog(service, cfg["blog_url"])
    last = None
    for attempt in range(1, 5):
        try:
            result = upsert_post(service, blog["id"], TITLE, html, LABELS, draft=args.draft)
            safe_print("Post URL:", result.get("url") or result.get("id"))
            return
        except Exception as e:
            last = e
            safe_print(f"Upload attempt {attempt} failed:", e)
            time.sleep(15 * attempt)
    raise last


if __name__ == "__main__":
    main()
