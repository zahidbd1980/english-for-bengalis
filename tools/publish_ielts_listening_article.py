# -*- coding: utf-8 -*-
"""Build + publish SEO article: IELTS Listening 1600 words for Bengali learners."""
from __future__ import annotations

import argparse
import json
import sys
import time
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


def pick(by_word: dict, names: list[str]) -> list[dict]:
    out = []
    for n in names:
        w = by_word.get(n.lower())
        if w:
            out.append(w)
    return out


def rows_html(items: list[dict], limit: int = 12) -> str:
    parts = [
        '<table style="width:100%;border-collapse:collapse;margin:12px 0;font-size:15px">',
        "<thead><tr>"
        '<th style="text-align:left;border-bottom:2px solid #0f6b5c;padding:8px">Word</th>'
        '<th style="text-align:left;border-bottom:2px solid #0f6b5c;padding:8px">Meaning (EN)</th>'
        '<th style="text-align:left;border-bottom:2px solid #0f6b5c;padding:8px">বাংলা অর্থ</th>'
        "</tr></thead><tbody>",
    ]
    for i, w in enumerate(items[:limit]):
        bg = "#f7fbf9" if i % 2 == 0 else "#ffffff"
        parts.append(
            f'<tr style="background:{bg}">'
            f'<td style="padding:8px;border-bottom:1px solid #e2eeea"><strong>{w["word"]}</strong></td>'
            f'<td style="padding:8px;border-bottom:1px solid #e2eeea">{w.get("meaning_en") or ""}</td>'
            f'<td style="padding:8px;border-bottom:1px solid #e2eeea">{w.get("meaning_bn") or ""}</td>'
            "</tr>"
        )
    parts.append("</tbody></table>")
    return "\n".join(parts)


def tip_box(title: str, body: str) -> str:
    return (
        '<div style="padding:14px 16px;margin:16px 0;background:#eef8f5;border-left:4px solid #0f6b5c;'
        'border-radius:8px">'
        f"<strong>{title}</strong><br>{body}</div>"
    )


def build_article(words: list[dict]) -> str:
    by = {w["word"].lower(): w for w in words}

    campus = pick(
        by,
        [
            "library", "lecture", "seminar", "assignment", "deadline", "tuition",
            "campus", "faculty", "curriculum", "scholarship", "tutorial", "professor",
            "laboratory", "enrol", "enroll", "dissertation",
        ],
    )
    travel = pick(
        by,
        [
            "airport", "luggage", "passport", "boarding", "departure", "arrival",
            "reservation", "itinerary", "destination", "accommodation", "hostel",
            "timetable", "platform", "baggage", "terminal",
        ],
    )
    money = pick(
        by,
        [
            "account", "deposit", "withdraw", "interest", "loan", "mortgage",
            "budget", "invoice", "receipt", "overdraft", "currency", "exchange",
            "cash", "credit card",
        ],
    )
    health = pick(
        by,
        [
            "appointment", "prescription", "symptom", "allergy", "treatment",
            "surgery", "pharmacy", "ambulance", "nutrition", "obesity",
            "medicine", "disease", "regular exercise",
        ],
    )
    traps = pick(
        by,
        [
            "accommodation", "necessary", "environment", "separate", "definitely",
            "committee", "questionnaire", "rhythm", "conscious", "guarantee",
            "colleague", "fascinating", "occurrence", "embarrassed", "recommend",
        ],
    )

    # Extra high-frequency from list if clusters thin
    def fill(cluster: list[dict], n: int = 10) -> list[dict]:
        if len(cluster) >= 8:
            return cluster
        for w in words:
            if w not in cluster:
                cluster.append(w)
            if len(cluster) >= n:
                break
        return cluster

    campus, travel, money, health, traps = map(fill, [campus, travel, money, health, traps])

    html = f"""
<div style="font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;line-height:1.7;color:#1a2e2a;max-width:820px">

<p style="font-size:1.05rem"><strong>IELTS Listening</strong>-এ অনেক শিক্ষার্থী শব্দ বোঝেন, কিন্তু <em>বানান</em> ভুল লেখেন — আর Band score কমে যায়।
আজ আমি IELTS টিচার হিসেবে বাংলাভাষী শিক্ষার্থীদের জন্য দেখাব কীভাবে
<strong>IELTS Listening Vocabulary 1600 Words</strong> তালিকাটা আসলে কাজে লাগাবেন।</p>

{tip_box(
    "এই পোস্টে যা শিখবেন",
    "১৬০০ শব্দের মধ্যে কোন গ্রুপ আগে পড়বেন, ক্যাম্পাস/ট্রাভেল/ব্যাংক/স্বাস্থ্য থিম, "
    "বাংলাভাষীদের সাধারণ spelling traps, আর আমাদের সাইটে বিনামূল্যে Practice লিঙ্ক।"
)}

<h2 style="color:#0f6b5c;margin-top:1.6rem">কেন IELTS Listening-এ Vocabulary এত জরুরি?</h2>
<p>Listening টেস্টে আপনি শুধু “শুনবেন” না — <strong>Form / Note / Table completion</strong>-এ সঠিক বানান লিখতে হবে।
এক অক্ষর ভুল হলেও উত্তর ভুল ধরা হয়। তাই এই ১৬০০ শব্দ আসলে “মুখস্থ তালিকা” নয় —
এটা <strong>শোনা → বোঝা → সঠিক বানানে লেখা</strong>র প্রশিক্ষণ।</p>

<ul>
  <li><strong>Section 1–2:</strong> daily life — booking, shopping, travel, address</li>
  <li><strong>Section 3–4:</strong> study / academic — lecture, research, campus life</li>
</ul>

<p>আমাদের প্ল্যাটফর্মে পুরো তালিকা ইতিমধ্যে আছে:</p>
<p>
  <a href="/p/vocabulary.html" style="color:#0f6b5c;font-weight:700">Vocabulary → IELTS Listening · 1600 Words</a><br>
  <a href="/p/spelling-practice.html" style="color:#0f6b5c;font-weight:700">Spelling Practice → IELTS Listening · 1600 Spellings</a>
</p>

<h2 style="color:#0f6b5c;margin-top:1.6rem">টিচারের ৭ দিনের প্ল্যান (বাংলা শিক্ষার্থীদের জন্য)</h2>
<ol>
  <li><strong>Day 1–2:</strong> Campus / Study words + Spelling Practice ২০টি</li>
  <li><strong>Day 3:</strong> Travel &amp; Accommodation</li>
  <li><strong>Day 4:</strong> Money / Banking / Shopping</li>
  <li><strong>Day 5:</strong> Health &amp; Appointments</li>
  <li><strong>Day 6:</strong> Spelling traps (accommodation, necessary…)</li>
  <li><strong>Day 7:</strong> Mixed review + Mistake Bank</li>
</ol>
<p>প্রতিদিন মাত্র <strong>২০–২৫ মিনিট</strong> যথেষ্ট — বড় তালিকা একবারে শেষ করার দরকার নেই।</p>

<h2 style="color:#0f6b5c;margin-top:1.6rem">১) Campus &amp; Study words (Section 3–4)</h2>
<p>বাংলাভাষী শিক্ষার্থীরা প্রায়ই <em>lecture / seminar / assignment</em> গুলিয়ে ফেলেন।
শুনলে অর্থ মনে আসুক, লিখলে বানান ঠিক থাকুক — দুটোই দরকার।</p>
{rows_html(campus, 12)}
{tip_box(
    "Classroom tip",
    "শব্দটা জোরে বলুন → ২ সেকেন্ড চোখ বন্ধ করে বানান কল্পনা করুন → তারপর লিখুন। "
    "এভাবে ‘passive দেখা’ থেকে ‘active recall’ এ চলে আসবেন।"
)}

<h2 style="color:#0f6b5c;margin-top:1.6rem">২) Travel &amp; Accommodation</h2>
<p>Section 1-এ booking ফর্মে এই শব্দগুলো বারবার আসে। বিশেষ করে
<strong>accommodation</strong>, <strong>luggage</strong>, <strong>itinerary</strong> — বানান খেয়াল রাখুন।</p>
{rows_html(travel, 12)}

<h2 style="color:#0f6b5c;margin-top:1.6rem">৩) Money, Banking &amp; Shopping</h2>
<p>সংখ্যা শোনার পাশাপাশি <em>deposit / withdraw / receipt</em> ঠিকমতো লিখতে হয়।
বাংলায় “রসিদ/রিসিট” বললেও ইংরেজিতে <strong>receipt</strong> লিখবেন — <em>reciept</em> নয়।</p>
{rows_html(money, 12)}

<h2 style="color:#0f6b5c;margin-top:1.6rem">৪) Health &amp; Appointments</h2>
<p>Clinic বা hospital dialogue-এ <strong>appointment</strong>, <strong>prescription</strong>, <strong>symptom</strong> খুব কমন।
শব্দের বাংলা অর্থ জানলে অডিওর context ধরতে সুবিধা হয়।</p>
{rows_html(health, 10)}

<h2 style="color:#0f6b5c;margin-top:1.6rem">৫) Spelling traps — বাংলাভাষীরা যেখানে বেশি ভুল করেন</h2>
<p>নিচের শব্দগুলো Listening answer sheet-এ সবচেয়ে বেশি marks কাটায়। আগে থেকে drill করুন।</p>
{rows_html(traps, 12)}
{tip_box(
    "Memory trick",
    "<strong>accommodation</strong> = ২টি <em>c</em> + ২টি <em>m</em> (cc + mm)। "
    "<strong>necessary</strong> = ১টি <em>c</em> + ২টি <em>s</em>। একবার ছন্দে মুখস্থ করুন।"
)}

<h2 style="color:#0f6b5c;margin-top:1.6rem">কীভাবে আমাদের সাইটে প্র্যাকটিস করবেন</h2>
<ol>
  <li><a href="/p/vocabulary.html">Vocabulary</a> খুলে Target list থেকে <strong>IELTS Listening · 1600 Words</strong> সিলেক্ট করুন।</li>
  <li>প্রতিদিন ১৫–২০টি কার্ড পড়ুন (বাংলা অর্থ + উদাহরণ)।</li>
  <li><a href="/p/spelling-practice.html">Spelling Practice</a>-এ একই লিস্ট সিলেক্ট করে <strong>শুনে লেখো</strong>।</li>
  <li>ভুল হলে Mistake Bank / Review due দিয়ে আবার করুন।</li>
  <li><a href="/p/daily-challenge.html">Daily Challenge</a> দিয়ে streak ধরে রাখুন।</li>
</ol>

<p>
  <a href="/p/spelling-practice.html" style="display:inline-block;background:#0f6b5c;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:700">এখনই Spelling Practice শুরু করুন →</a>
  &nbsp;
  <a href="/p/vocabulary.html" style="display:inline-block;background:#fff;color:#0f6b5c;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:700;border:2px solid #0f6b5c">Vocabulary List খুলুন →</a>
</p>

<h2 style="color:#0f6b5c;margin-top:1.6rem">FAQ</h2>
<p><strong>প্রশ্ন: ১৬০০ শব্দ কি সব মুখস্থ করতে হবে?</strong><br>
উত্তর: না। থিম অনুযায়ী ছোট ব্যাচে শিখুন। আগে high-frequency + spelling traps।</p>
<p><strong>প্রশ্ন: এটা কি অফিসিয়াল Cambridge লিস্ট?</strong><br>
উত্তর: না — এটা IELTS Listening-এ বহুল দেখা যায় এমন শব্দের <em>unofficial practice list</em>।
IELTS® British Council / IDP / Cambridge-এর সাথে affiliated নয়।</p>
<p><strong>প্রশ্ন: বাংলা অর্থ কি Listening-এ সাহায্য করে?</strong><br>
উত্তর: হ্যাঁ। অর্থ পরিষ্কার থাকলে অডিওর situation দ্রুত বোঝেন, ফাঁকা জায়গায় সঠিক শব্দ predict করতে পারেন।</p>

<hr style="border:none;border-top:1px solid #d7e8e2;margin:24px 0">
<p style="font-size:0.95rem;color:#456"><em>English for Bengalis</em> — শুধু আর্টিকেল নয়, Vocabulary + Spelling Practice + Progress Tracking এক জায়গায়।
আজই ২০টি শব্দ দিয়ে শুরু করুন। Don't just study English. Know exactly what you have mastered.</p>

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
    # also check drafts
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
    html = build_article(words)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html, encoding="utf-8")
    OUT_META.write_text(
        json.dumps({"title": TITLE, "labels": LABELS, "file": str(OUT_HTML.relative_to(ROOT))}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    safe_print("Wrote", OUT_HTML)

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
