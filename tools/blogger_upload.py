#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload English for Bengalis pages/posts to Blogger via official Blogger API v3.

Usage (from project root or tools/):
  python tools/blogger_upload.py --auth
  python tools/blogger_upload.py --list
  python tools/blogger_upload.py --upload-pages
  python tools/blogger_upload.py --upload-welcome
  python tools/blogger_upload.py --all
  python tools/blogger_upload.py --draft   # create as drafts first (safer)

Requirements:
  1) Google Cloud OAuth Desktop client → tools/client_secret.json
  2) pip install -r tools/requirements-blogger.txt
  3) Optional: set asset_base_url in blogger_config.json (GitHub Pages URL for css/js/data)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
CONFIG_PATH = TOOLS / "blogger_config.json"
SECRET_PATH = TOOLS / "client_secret.json"
TOKEN_PATH = TOOLS / "token.json"
SCOPES = ["https://www.googleapis.com/auth/blogger"]

WELCOME_HTML = """
<div style="font-family:Georgia,serif;line-height:1.6;max-width:720px">
  <p><strong>English for Bengalis</strong> এ আপনাকে স্বাগতম।</p>
  <p>এখানে আপনি শুধু আর্টিকেল পড়বেন না — <em>শিখবেন, অনুশীলন করবেন, আর প্রোগ্রেস ট্র্যাক করবেন</em>।</p>
  <h3>শুরু করুন</h3>
  <ul>
    <li><a href="/p/learn.html">Learn · শিখুন</a></li>
    <li><a href="/p/spelling-practice.html">Spelling Practice · শুনে লেখো</a></li>
    <li><a href="/p/daily-challenge.html">Daily Challenge</a></li>
    <li><a href="/p/common-mistakes.html">Common Mistakes · সাধারণ ভুল</a></li>
    <li><a href="/p/quizzes.html">Quizzes</a></li>
    <li><a href="/p/level-test.html">Level Test</a></li>
    <li><a href="/p/my-progress.html">My Progress</a></li>
  </ul>
  <p><em>Don't just study English. Know exactly what you have mastered.</em></p>
  <p style="font-size:0.9em;color:#555">IELTS-style materials on this site are unofficial and not affiliated with British Council, IDP, or Cambridge.</p>
</div>
"""


def die(msg: str, code: int = 1) -> None:
    print("ERROR:", msg)
    sys.exit(code)


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        die(f"Config missing: {CONFIG_PATH}")
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def ensure_deps():
    try:
        import google.auth  # noqa: F401
        import google_auth_oauthlib  # noqa: F401
        import googleapiclient  # noqa: F401
    except ImportError:
        die(
            "Google libraries missing.\n"
            "Run:  pip install -r tools/requirements-blogger.txt"
        )


def get_credentials():
    ensure_deps()
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        if not creds or not creds.valid:
            if not SECRET_PATH.exists():
                die(
                    f"Missing {SECRET_PATH.name}\n"
                    "1) Google Cloud Console → Create OAuth Desktop client\n"
                    "2) Download JSON and save as tools/client_secret.json\n"
                    "See docs/BLOGGER_CMD_UPLOAD.md"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(SECRET_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
        print("Saved login token ->", TOKEN_PATH)
    return creds


def build_service():
    from googleapiclient.discovery import build

    return build("blogger", "v3", credentials=get_credentials(), cache_discovery=False)


def get_blog(service, blog_url: str) -> dict:
    blog = service.blogs().getByUrl(url=blog_url).execute()
    print(f"Blog: {blog.get('name')}  |  id={blog.get('id')}  |  {blog.get('url')}")
    return blog


def extract_main_html(raw: str) -> str:
    m = re.search(r"<main[^>]*>(.*?)</main>", raw, flags=re.I | re.S)
    if m:
        return m.group(1).strip()
    # fallback: body
    m = re.search(r"<body[^>]*>(.*?)</body>", raw, flags=re.I | re.S)
    return (m.group(1) if m else raw).strip()


def rewrite_for_blogger(html: str, asset_base: str, page_file: str) -> str:
    """Rewrite local asset/page links so Blogger can load them."""
    base = (asset_base or "").rstrip("/")
    out = html

    # Remove sticky header/footer chrome placeholders (Blogger theme has its own)
    out = re.sub(r'<header class="site-header"[^>]*>.*?</header>', "", out, flags=re.I | re.S)
    out = re.sub(r'<div class="nav-drawer"[^>]*>.*?</div>', "", out, flags=re.I | re.S)
    out = re.sub(r'<footer class="site-footer"[^>]*>.*?</footer>', "", out, flags=re.I | re.S)
    out = re.sub(r'<a class="skip-link"[^>]*>.*?</a>', "", out, flags=re.I | re.S)

    if base:
        # CSS / JS / data from pages/*
        out = out.replace("../css/learning.css", f"{base}/css/learning.css?v=20260820b")
        out = out.replace('href="../css/', f'href="{base}/css/')
        out = out.replace("href='../css/", f"href='{base}/css/")
        out = out.replace('src="../js/', f'src="{base}/js/')
        out = out.replace("src='../js/", f"src='{base}/js/")
        out = out.replace('href="css/', f'href="{base}/css/')
        out = out.replace('src="js/', f'src="{base}/js/')
        # inject stylesheet + fonts if main-only content
        head_inject = (
            f'<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;700'
            f'&family=Hind+Siliguri:wght@400;600;700&family=Noto+Sans+Bengali:wght@400;600;700'
            f'&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet"/>'
            f'<link rel="stylesheet" href="{base}/css/learning.css?v=20260820b"/>'
        )
        scripts = (
            f'<script src="{base}/js/storage.js"></script>'
            f'<script src="{base}/js/progress.js?v=20260818c"></script>'
            f'<script src="{base}/js/learning-path.js"></script>'
            f'<script src="{base}/js/quiz-engine.js?v=20260818d"></script>'
            f'<script src="{base}/js/daily-challenge.js?v=20260818d"></script>'
            f'<script src="{base}/js/spelling-practice.js"></script>'
            f'<script src="{base}/js/vocabulary.js?v=20260818d"></script>'
            f'<script src="{base}/js/review-session.js?v=20260818c"></script>'
            f'<script src="{base}/js/app.js?v=20260818d"></script>'
            f'<script src="{base}/js/home-v2.js?v=20260818d"></script>'
        )
        # Blogger turns Bangla inside inline <script> into &#NNNN; codes. Decode before
        # textContent / HTML-escape. Works even if GitHub Pages is still on old app.js.
        entity_polyfill = """
<script>
(function(){
  function decodeHtml(s) {
    s = String(s == null ? "" : s);
    if (s.indexOf("&") === -1) return s;
    var t = document.createElement("textarea");
    t.innerHTML = s;
    return t.value;
  }
  function escHtml(s) {
    return decodeHtml(s).replace(/[&<>"]/g, function (c) {
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];
    });
  }
  function setText(el, s) {
    if (typeof el === "string") el = document.getElementById(el);
    if (el) el.textContent = decodeHtml(s);
  }
  window.EFBApp = window.EFBApp || {};
  if (!EFBApp.decodeHtml) EFBApp.decodeHtml = decodeHtml;
  if (!EFBApp.escHtml) EFBApp.escHtml = escHtml;
  if (!EFBApp.setText) EFBApp.setText = setText;
})();
</script>
"""
        # Fix fetch root: MUST run before page scripts that call loadJSON
        wrapper_open = f'<div class="efb-blogger" data-efb-asset="{base}">'
        bootstrap = f"""
<script>
window.EFB_ASSET_BASE = "{base}";
(function(){{
  var oldFetch = window.fetch.bind(window);
  window.fetch = function(url, opts) {{
    try {{
      var u = String(url);
      if (u.indexOf("data/") !== -1 && u.indexOf("http") !== 0) {{
        var name = u.split("data/").pop();
        return oldFetch("{base}/data/" + name, opts);
      }}
    }} catch (e) {{}}
    return oldFetch(url, opts);
  }};
}})();
</script>
"""
        # Strip original relative script tags; we reload absolute copies after bootstrap
        out = re.sub(
            r"<script[^>]+src=[\"'][^\"']+[\"'][^>]*>\s*</script>",
            "",
            out,
            flags=re.I,
        )
        # Keep inline page scripts, but move them after libraries
        inline_scripts = re.findall(r"(<script(?![^>]*src=)[^>]*>.*?</script>)", out, flags=re.I | re.S)
        out_no_inline = re.sub(r"<script(?![^>]*src=)[^>]*>.*?</script>", "", out, flags=re.I | re.S)
        inline_joined = "\n".join(inline_scripts)
        out = (
            head_inject
            + bootstrap
            + wrapper_open
            + out_no_inline
            + scripts
            + entity_polyfill
            + inline_joined
            + "</div>"
        )
    else:
        notice = (
            '<div style="padding:12px;margin:0 0 16px;background:#fff7e8;border:1px solid #f0d9a8;'
            'border-radius:8px;font-family:sans-serif">'
            "<strong>Note:</strong> Interactive quiz/data needs <code>asset_base_url</code> "
            "(GitHub Pages). Text content below still works. "
            "See <code>docs/BLOGGER_CMD_UPLOAD.md</code>."
            "</div>"
        )
        # Strip script tags that will 404 on Blogger
        out = re.sub(r"<script[^>]+src=[\"'][^\"']+[\"'][^>]*>\s*</script>", "", out, flags=re.I)
        out = re.sub(r"<script\b[^>]*>.*?</script>", "", out, flags=re.I | re.S)
        out = notice + out

    # Local page links → Blogger-ish /p/ slugs (best effort)
    out = out.replace('href="../index.html"', 'href="/"')
    out = out.replace('href="index.html"', 'href="/"')
    out = re.sub(
        r'href="([a-z0-9\-]+)\.html"',
        lambda m: f'href="/p/{m.group(1)}.html"',
        out,
        flags=re.I,
    )
    out = out.replace('href="../pages/', 'href="/p/')
    out = out.replace('href="pages/', 'href="/p/')

    # Keep a marker
    out += f"\n<!-- efb-source:{page_file} -->\n"
    return out


def build_page_content(file_rel: str, asset_base: str) -> str:
    path = ROOT / file_rel
    if not path.exists():
        die(f"File not found: {path}")
    raw = path.read_text(encoding="utf-8")
    main = extract_main_html(raw)
    # Also keep page-level scripts that are inline after main (for tools)
    # Re-read full body content for interactive pages
    body_m = re.search(r"<body[^>]*>(.*?)</body>", raw, flags=re.I | re.S)
    body = body_m.group(1) if body_m else main
    # Prefer body so inline <script> blocks remain
    content_src = body if "<script>" in body else main
    return rewrite_for_blogger(content_src, asset_base, file_rel)


def upsert_page(service, blog_id: str, title: str, content: str, draft: bool) -> dict:
    existing = find_existing_page(service, blog_id, title)
    body = {"title": title, "content": content}
    last_err = None
    for attempt in range(1, 6):
        try:
            if existing:
                print(f"  Updating page: {title} ({existing['id']})")
                return (
                    service.pages()
                    .update(blogId=blog_id, pageId=existing["id"], body={**existing, **body})
                    .execute()
                )
            print(f"  Creating page: {title}" + (" [DRAFT]" if draft else ""))
            return service.pages().insert(blogId=blog_id, body=body, isDraft=draft).execute()
        except Exception as e:
            last_err = e
            msg = str(e)
            if "rateLimitExceeded" in msg or "Quota" in msg or "429" in msg:
                wait = 20 * attempt
                print(f"  Rate limit. Waiting {wait}s then retry {attempt}/5...")
                time.sleep(wait)
                continue
            raise
    raise last_err


def find_existing_page(service, blog_id: str, title: str):
    # pages.list may paginate
    token = None
    title_l = title.strip().lower()
    while True:
        kwargs = {"blogId": blog_id, "view": "ADMIN", "maxResults": 50}
        if token:
            kwargs["pageToken"] = token
        resp = service.pages().list(**kwargs).execute()
        for item in resp.get("items", []) or []:
            if item.get("title", "").strip().lower() == title_l:
                return item
        token = resp.get("nextPageToken")
        if not token:
            break
    return None


def find_welcome_post(service, blog_id: str, title: str):
    resp = service.posts().list(blogId=blog_id, maxResults=20).execute()
    for item in resp.get("items", []) or []:
        if item.get("title", "").strip().lower() == title.strip().lower():
            return item
    return None


def upsert_welcome(service, blog_id: str, cfg: dict, draft: bool) -> dict:
    wp = cfg.get("welcome_post") or {}
    title = wp.get("title") or "Welcome"
    labels = wp.get("labels") or ["welcome"]
    content = WELCOME_HTML
    if wp.get("file"):
        content = build_page_content(wp["file"], cfg.get("asset_base_url") or "")

    existing = find_welcome_post(service, blog_id, title)
    body = {"title": title, "content": content, "labels": labels}
    if existing:
        print(f"  Updating post: {title}")
        return (
            service.posts()
            .update(blogId=blog_id, postId=existing["id"], body={**existing, **body})
            .execute()
        )
    print(f"  Creating post: {title}" + (" [DRAFT]" if draft else ""))
    return service.posts().insert(blogId=blog_id, body=body, isDraft=draft).execute()


def find_post_by_title_substr(service, blog_id: str, needle: str):
    needle_l = needle.strip().lower()
    token = None
    while True:
        kwargs = {"blogId": blog_id, "maxResults": 50, "status": "LIVE"}
        if token:
            kwargs["pageToken"] = token
        resp = service.posts().list(**kwargs).execute()
        for item in resp.get("items", []) or []:
            title = (item.get("title") or "").strip().lower()
            if needle_l in title:
                return item
        token = resp.get("nextPageToken")
        if not token:
            break
    return None


def cmd_upload_seo_post(draft: bool = False):
    """Update the IELTS Listening SEO article from content/posts/."""
    cfg = load_config()
    service = build_service()
    blog = get_blog(service, cfg["blog_url"])
    path = ROOT / "content" / "posts" / "ielts-listening-1600-words-bn.html"
    html = path.read_text(encoding="utf-8")
    title = "IELTS Listening Vocabulary 1600 Words — বাংলায় শিখুন (Spelling + Meaning)"
    existing = find_post_by_title_substr(service, blog["id"], "IELTS Listening Vocabulary 1600")
    body = {
        "title": title,
        "content": html,
        "labels": ["IELTS", "Vocabulary", "Listening", "Spelling"],
    }
    if existing:
        print("  Updating SEO post:", existing.get("id"))
        result = (
            service.posts()
            .update(blogId=blog["id"], postId=existing["id"], body={**existing, **body})
            .execute()
        )
    else:
        print("  Creating SEO post" + (" [DRAFT]" if draft else ""))
        result = service.posts().insert(blogId=blog["id"], body=body, isDraft=draft).execute()
    print("SEO post ->", result.get("url") or result.get("id"))


def cmd_auth():
    get_credentials()
    print("Auth OK. You can run --list or --upload-pages next.")


def cmd_list():
    cfg = load_config()
    service = build_service()
    blog = get_blog(service, cfg["blog_url"])
    pages = service.pages().list(blogId=blog["id"], view="ADMIN").execute()
    posts = service.posts().list(blogId=blog["id"], maxResults=10).execute()
    print("\nPages:")
    for p in pages.get("items") or []:
        print(f"  - {p.get('title')}  [{p.get('status')}]  {p.get('url')}")
    print("\nRecent posts:")
    for p in posts.get("items") or []:
        print(f"  - {p.get('title')}  {p.get('url')}")
    if not (posts.get("items") or []):
        print("  (none yet)")


def cmd_upload_pages(draft: bool):
    cfg = load_config()
    asset = (cfg.get("asset_base_url") or "").strip()
    if not asset:
        print(
            "WARNING: asset_base_url empty - quizzes/JSON may not work on Blogger.\n"
            "Set GitHub Pages URL in tools/blogger_config.json then re-run.\n"
        )
    service = build_service()
    blog = get_blog(service, cfg["blog_url"])
    for item in cfg.get("pages") or []:
        title = item["title"]
        if title.strip().lower() == "home":
            print("SKIP: refusing to upload a Page titled 'Home' (home is blog root URL).")
            continue
        file_rel = item["file"]
        print(f"Preparing: {title} <- {file_rel}")
        content = build_page_content(file_rel, asset)
        result = upsert_page(service, blog["id"], title, content, draft=draft)
        print(f"    -> {result.get('url') or result.get('id')}")
        time.sleep(3)  # gentle pacing to avoid Blogger quota spikes
    # Enforce root-URL home model every pages upload
    if delete_page_by_title(service, blog["id"], "Home"):
        print("Removed leftover Page 'Home' after pages upload.")
    print("\nDone. Add pages to the Blogger menu under Pages.")
    print("Site:", cfg["blog_url"])
    print("Home = blog root URL only (no /p/home.html).")


def delete_page_by_title(service, blog_id: str, title: str) -> bool:
    """Delete a Blogger Page by exact title. Returns True if deleted."""
    existing = find_existing_page(service, blog_id, title)
    if not existing:
        return False
    page_id = existing["id"]
    url = existing.get("url") or ""
    print(f"  Deleting page: {title} ({page_id}) {url}")
    service.pages().delete(blogId=blog_id, pageId=page_id).execute()
    return True


def cmd_upload_welcome(draft: bool):
    cfg = load_config()
    service = build_service()
    blog = get_blog(service, cfg["blog_url"])
    result = upsert_welcome(service, blog["id"], cfg, draft=draft)
    print("Welcome post ->", result.get("url") or result.get("id"))

    # Home = blog root URL only. Never keep a Page titled "Home".
    if delete_page_by_title(service, blog["id"], "Home"):
        print(
            "Removed leftover Page 'Home' (/p/home.html).\n"
            "Canonical home is blog root: "
            + str(cfg.get("blog_url") or "/")
            + " (Featured Welcome post)."
        )
    else:
        print("OK: no Page titled 'Home' (correct - home is root URL).")


def cmd_fix_home(draft: bool = False):
    """Delete leftover Home Page + refresh Featured Welcome landing."""
    cfg = load_config()
    service = build_service()
    blog = get_blog(service, cfg["blog_url"])
    print("Fixing home model: root URL only (no /p/home.html Page).")
    deleted = delete_page_by_title(service, blog["id"], "Home")
    if not deleted:
        print("No Page titled 'Home' found.")
    result = upsert_welcome(service, blog["id"], cfg, draft=draft)
    print("Welcome post refreshed ->", result.get("url") or result.get("id"))
    print("Done. Menu Home should point to / (blog root), not /p/home.html")


def main():
    parser = argparse.ArgumentParser(description="Upload site content to Blogger via API")
    parser.add_argument("--auth", action="store_true", help="Login with Google (browser)")
    parser.add_argument("--list", action="store_true", help="List pages/posts")
    parser.add_argument("--upload-pages", action="store_true", help="Create/update Pages")
    parser.add_argument("--upload-welcome", action="store_true", help="Create/update welcome Post")
    parser.add_argument(
        "--upload-seo-post",
        action="store_true",
        help="Create/update IELTS Listening 1600 SEO article post",
    )
    parser.add_argument(
        "--fix-home",
        action="store_true",
        help="Delete leftover Home Page + refresh Welcome on blog root",
    )
    parser.add_argument("--all", action="store_true", help="Auth check + welcome + pages")
    parser.add_argument("--draft", action="store_true", help="Create new items as drafts")
    args = parser.parse_args()

    if not any(
        [
            args.auth,
            args.list,
            args.upload_pages,
            args.upload_welcome,
            args.upload_seo_post,
            args.fix_home,
            args.all,
        ]
    ):
        parser.print_help()
        print("\nQuick start:  upload-to-blogger.bat")
        return

    if args.auth:
        cmd_auth()
    if args.list:
        cmd_list()
    if args.fix_home:
        cmd_fix_home(draft=args.draft)
    if args.upload_welcome or args.all:
        if args.all:
            cmd_auth()
        cmd_upload_welcome(draft=args.draft)
    if args.upload_seo_post:
        cmd_upload_seo_post(draft=args.draft)
    if args.upload_pages or args.all:
        cmd_upload_pages(draft=args.draft)


if __name__ == "__main__":
    main()
