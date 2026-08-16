# -*- coding: utf-8 -*-
"""Publish batch-3 SEO articles (TFNG, paraphrase, AWL, PTE WFD)."""
from __future__ import annotations

import argparse
import html as html_lib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from blogger_upload import build_service, get_blog, load_config  # noqa: E402

VOCAB = ROOT / "data" / "vocabulary.json"
VLISTS = ROOT / "data" / "vocabulary-lists.json"
OUT = ROOT / "content" / "posts"
BRAND, WASH, BORDER, INK = "#217a66", "#dceee6", "#cfe0d7", "#1e2b26"


def esc(s):
    return html_lib.escape(str(s or ""), quote=True)


def safe_print(*args):
    msg = " ".join(str(a) for a in args)
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", "replace").decode("ascii"))


def tip(t, b):
    return (
        f'<div style="padding:14px 16px;margin:16px 0;background:{WASH};'
        f'border-left:4px solid {BRAND};border-radius:8px"><strong>{t}</strong><br>{b}</div>'
    )


def table(items):
    parts = [
        '<div class="efb-table-wrap"><table style="width:100%;border-collapse:collapse;font-size:15px;min-width:460px">',
        f"<thead><tr><th style='text-align:left;border-bottom:2px solid {BRAND};padding:8px'>Word</th>"
        f"<th style='text-align:left;border-bottom:2px solid {BRAND};padding:8px'>বাংলা</th>"
        f"<th style='text-align:left;border-bottom:2px solid {BRAND};padding:8px'>Example</th></tr></thead><tbody>",
    ]
    for i, w in enumerate(items):
        bg = "#f2faf6" if i % 2 == 0 else "#fff"
        parts.append(
            f"<tr style='background:{bg}'><td style='padding:8px;border-bottom:1px solid {BORDER};font-weight:700'>{esc(w.get('word'))}</td>"
            f"<td style='padding:8px;border-bottom:1px solid {BORDER}'>{esc(w.get('meaning_bn'))}</td>"
            f"<td style='padding:8px;border-bottom:1px solid {BORDER}'><em>{esc(w.get('example'))}</em></td></tr>"
        )
    parts.append("</tbody></table></div>")
    return "\n".join(parts)


def load_list(list_id):
    vmeta = json.loads(VLISTS.read_text(encoding="utf-8"))
    bank = {w["id"]: w for w in json.loads(VOCAB.read_text(encoding="utf-8"))}
    for L in vmeta.get("lists") or []:
        if L.get("id") == list_id:
            return [bank[i] for i in L.get("word_ids") or [] if i in bank]
    return []


def find_post(service, blog_id, title):
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
    return None


def upsert(service, blog_id, title, html, labels, draft):
    existing = find_post(service, blog_id, title)
    body = {"title": title, "content": html, "labels": labels}
    if existing:
        safe_print("Updating:", title)
        return service.posts().update(blogId=blog_id, postId=existing["id"], body={**existing, **body}).execute()
    safe_print("Creating:", title)
    return service.posts().insert(blogId=blog_id, body=body, isDraft=draft).execute()


def art_tfng():
    title = "IELTS Reading True False Not Given — বাংলায় সহজ নিয়ম"
    labels = ["IELTS", "Reading", "Strategy", "বাংলা"]
    html = f"""
<div class="efb-seo-article" style="color:{INK};line-height:1.65">
<p>IELTS Reading-এ <strong>True / False / Not Given</strong> বাংলা শিক্ষার্থীদের জন্য সবচেয়ে confusing প্রশ্ন।
নিচে সহজ নিয়ম — মুখস্থ নয়, logic।</p>
{tip("এক লাইনে", "True = passage-এর সঙ্গে মিলে · False = passage বিপরীত বলে · Not Given = passage কিছুই বলে না (আপনি জানলেও)।")}
<h2 style="color:{BRAND}">৩টি নিয়ম</h2>
<ol>
<li><strong>True:</strong> Statement-এর অর্থ passage-এ <em>স্পষ্টভাবে</em> আছে (synonym থাকতে পারে)।</li>
<li><strong>False:</strong> Passage সরাসরি <em>উল্টো</em> কথা বলে।</li>
<li><strong>Not Given:</strong> Passage-এ তথ্য নেই — বাইরের জ্ঞান দিয়ে True বলবেন না।</li>
</ol>
<h2 style="color:{BRAND}">Common traps</h2>
<ul>
<li>Absolute words: <em>always / never / only / all</em> — প্রায়ই False বা NG</li>
<li>Names, dates, numbers — line-by-line মিলান</li>
<li>Paraphrase চিনতে synonym জানা জরুরি</li>
</ul>
<h2 style="color:{BRAND}">প্র্যাকটিস লিংক</h2>
<ol>
<li><a href="/p/vocabulary.html">Vocabulary</a> → <strong>Paraphrase Synonyms</strong> + <strong>Academic Reading Verbs</strong></li>
<li><a href="/p/vocabulary.html">Reading Theme Pack</strong> — climate / cities / health</li>
</ol>
<p><a href="/p/vocabulary.html" style="display:inline-block;background:{BRAND};color:#fff;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700">Vocabulary →</a></p>
<p style="font-size:0.95rem;color:#5c6b64">Unofficial tip guide — IELTS® bodies-এর সাথে affiliated নয়।</p>
</div>
""".strip()
    return title, html + "\n", labels, "ielts-reading-tfng-bn.html"


def art_para(items):
    title = "IELTS Paraphrasing Practice — 30 Synonym Swaps (বাংলা)"
    labels = ["IELTS", "Vocabulary", "Writing", "Reading", "বাংলা"]
    html = f"""
<div class="efb-seo-article" style="color:{INK};line-height:1.65">
<p>Reading ও Writing দুটোতেই <strong>paraphrase</strong> দরকার। নিচে <strong>{len(items)}</strong>টি high-value word —
বাংলা অর্থ + exam synonym mindset (unofficial)।</p>
{tip("Trick", "important → crucial/significant · show → indicate/illustrate · people → citizens/individuals · because → due to/since")}
{table(items)}
<p><a href="/p/vocabulary.html" style="display:inline-block;background:{BRAND};color:#fff;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700">Paraphrase list →</a></p>
</div>
""".strip()
    return title, html + "\n", labels, "ielts-paraphrase-synonyms-bn.html"


def art_awl(items):
    title = "Academic Word List Starter — IELTS TOEFL PTE (বাংলা অর্থ)"
    labels = ["IELTS", "TOEFL", "PTE", "AWL", "Vocabulary", "বাংলা"]
    html = f"""
<div class="efb-seo-article" style="color:{INK};line-height:1.65">
<p><strong>Academic Word List (AWL)</strong>-স্টাইল শব্দ Reading/Listening/Writing সব exam-এ ফিরে আসে।
এই starter pack-এ <strong>{len(items)}</strong>টি high-frequency word বাংলায় (unofficial, full AWL নয়)।</p>
{tip("Study plan", "প্রতিদিন ৮–১০টি · Vocabulary card + Spelling · নিজের essay-এ ২টি ব্যবহার")}
{table(items)}
<ol>
<li><a href="/p/vocabulary.html">Vocabulary</a> → <strong>Academic Word List · Starter</strong></li>
<li><a href="/p/spelling-practice.html">Spelling</a> → <strong>AWL Starter Spellings</strong></li>
</ol>
<p><a href="/p/vocabulary.html" style="display:inline-block;background:{BRAND};color:#fff;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700">AWL Starter →</a></p>
</div>
""".strip()
    return title, html + "\n", labels, "awl-starter-bn.html"


def art_pte():
    title = "PTE Write From Dictation — Spelling Habits যেগুলো নম্বর বাঁচায়"
    labels = ["PTE", "Spelling", "Listening", "বাংলা"]
    html = f"""
<div class="efb-seo-article" style="color:{INK};line-height:1.65">
<p>PTE <strong>Write From Dictation</strong>-এ প্রতিটি সঠিক শব্দ নম্বর দেয় — বানান ভুল = নম্বর কাটা।
বাংলা learners-এর জন্য practical habits:</p>
{tip("Golden rule", "শুনে পুরো sentence মনে রাখুন → লিখুন → articles (a/an/the) ও plural -s চেক করুন।")}
<h2 style="color:{BRAND}">৫টি অভ্যাস</h2>
<ol>
<li>প্রতিদিন ১০–১৫টি academic word Spelling Practice-এ শুনে লিখুন</li>
<li>Common traps: accommodation, necessary, environment, government</li>
<li>Capital letter শুধু sentence start / proper noun</li>
<li>Punctuation শেষে full stop দিন</li>
<li>IELTS Listening Form Traps list দিয়ে overlap practice</li>
</ol>
<h2 style="color:{BRAND}">সাইট লিংক</h2>
<ul>
<li><a href="/p/spelling-practice.html">Spelling Practice</a> → PTE Spellings / Listening Form Traps / AWL</li>
<li><a href="/p/vocabulary.html">Vocabulary</a> → PTE Academic Core</li>
</ul>
<p><a href="/p/spelling-practice.html" style="display:inline-block;background:{BRAND};color:#fff;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700">Spelling Practice →</a></p>
<p style="font-size:0.95rem;color:#5c6b64">Unofficial PTE tips — Pearson-এর সাথে affiliated নয়।</p>
</div>
""".strip()
    return title, html + "\n", labels, "pte-write-from-dictation-bn.html"


def art_false(items):
    title = "English False Friends for Bangla Speakers — ভুল অর্থ এড়ান"
    labels = ["Vocabulary", "Common Mistakes", "বাংলা", "IELTS"]
    html = f"""
<div class="efb-seo-article" style="color:{INK};line-height:1.65">
<p>কিছু ইংরেজি শব্দ বাংলা অর্থের সঙ্গে <strong>মিথ্যা মিল</strong> দেখায় — exam-এ বিপদ।
নিচে <strong>{len(items)}</strong>টি false friend (unofficial)।</p>
{table(items)}
<p><a href="/p/vocabulary.html" style="display:inline-block;background:{BRAND};color:#fff;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700">False Friends list →</a>
<a href="/p/common-mistakes.html" style="display:inline-block;margin-left:8px;border:2px solid {BRAND};color:{BRAND};padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:700">Common Mistakes →</a></p>
</div>
""".strip()
    return title, html + "\n", labels, "false-friends-bn-article.html"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    built = []
    for builder, list_id in (
        (art_tfng, None),
        (lambda: art_para(load_list("paraphrase-synonyms")), None),
        (lambda: art_awl(load_list("awl-starter")), None),
        (art_pte, None),
        (lambda: art_false(load_list("false-friends-bn")), None),
    ):
        title, html, labels, fname = builder()
        path = OUT / fname
        path.write_text(html, encoding="utf-8")
        path.with_suffix(".meta.json").write_text(
            json.dumps({"title": title, "labels": labels, "file": str(path.relative_to(ROOT))}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        built.append((title, html, labels))
        safe_print("Wrote", fname)

    if args.build_only:
        return

    cfg = load_config()
    service = build_service()
    blog = get_blog(service, cfg["blog_url"])
    for title, html, labels in built:
        last = None
        for attempt in range(1, 4):
            try:
                r = upsert(service, blog["id"], title, html, labels, args.draft)
                safe_print("URL:", r.get("url") or r.get("id"))
                break
            except Exception as e:
                last = e
                safe_print("fail", attempt, e)
                time.sleep(8 * attempt)
        else:
            raise last


if __name__ == "__main__":
    main()
