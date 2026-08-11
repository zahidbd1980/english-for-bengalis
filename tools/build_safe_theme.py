#!/usr/bin/env python3
"""Build a Blogger-safe Indie theme from original backup with minimal edits."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"H:/project/English_Learning_Platform")
SRC = ROOT / "backup" / "theme-indie-original-backup.xml"
OUT = ROOT / "themeCode.txt"
OUT_MIN = ROOT / "themeCode-SAFE.txt"


def main() -> None:
    t = SRC.read_text(encoding="utf-8")
    assert "<b:skin" in t and "</b:skin>" in t
    assert t.count("<![CDATA[") == t.count("]]>")

    # 1) Safe color tweaks only (keep Roboto fonts, keep height rules)
    replacements = {
        'name="keycolor" description="Main Color" type="color" default="#2196f3"  value="#2196f3"/>':
            'name="keycolor" description="Main Color" type="color" default="#0f6b5c"  value="#0f6b5c"/>',
        'default="#2196f3"  value="#2196f3"/>\n  <Variable name="body.link.visited.color"':
            'default="#0f6b5c"  value="#0f6b5c"/>\n  <Variable name="body.link.visited.color"',
        # visited/hover still reference $(body.link.color) in defaults - update explicit values
        'name="body.link.visited.color" description="Visited link color"\n      type="color"\n      default="$(body.link.color)"  value="#2196f3"/>':
            'name="body.link.visited.color" description="Visited link color"\n      type="color"\n      default="$(body.link.color)"  value="#0a5246"/>',
        'name="body.link.hover.color" description="Link Hover Color"\n      type="color"\n      default="$(body.link.color)"  value="#2196f3"/>':
            'name="body.link.hover.color" description="Link Hover Color"\n      type="color"\n      default="$(body.link.color)"  value="#c45c26"/>',
        # body text / post title colors
        'name="body.text.color" description="Color"\n      type="color"\n      default="#757575"  value="#757575"/>':
            'name="body.text.color" description="Color"\n      type="color"\n      default="#757575"  value="#5b6573"/>',
        'name="posts.title.color" description="Post title color"\n      type="color"\n      default="#212121"  value="#212121"/>':
            'name="posts.title.color" description="Post title color"\n      type="color"\n      default="#212121"  value="#1c2430"/>',
        # softer page bg under content (not hero) - careful: Indie uses body.background.color for hero too
        # Keep hero image from original to avoid layout validation issues.
    }

    for old, new in replacements.items():
        if old not in t:
            print("WARN missing pattern:\n", old[:120])
        else:
            t = t.replace(old, new, 1)

    # 2) Enable PageList (was hidden) - keep original pageListJson (Home only)
    old_pl = "<b:widget cond='!data:view.isPost' id='PageList1' locked='true' title='' type='PageList' visible='false'>"
    new_pl = "<b:widget cond='!data:view.isPost' id='PageList1' locked='true' title='' type='PageList' visible='true'>"
    if old_pl not in t:
        raise SystemExit("PageList widget tag not found as expected")
    t = t.replace(old_pl, new_pl, 1)

    # 3) Minimal CSS append before skin close (no @import, no external links)
    custom_css = """
/* EFB safe customizations */
.blog-name .PageList ul.tabs{
display:flex;
flex-wrap:wrap;
justify-content:center;
gap:2px;
}
.blog-name .PageList ul.tabs li a{
padding:8px 12px !important;
border-radius:8px;
font-weight:700;
}
.blog-name .PageList ul.tabs li.selected a,
.blog-name .PageList ul.tabs li a:hover{
background:rgba(255,255,255,0.16);
}
.sticky .PageList ul.tabs li a{
color:#0f6b5c !important;
}
.post-body a{
color:#0f6b5c;
}
"""
    marker = "]]></b:skin>"
    if marker not in t:
        raise SystemExit("skin close marker missing")
    # only once
    t = t.replace(marker, custom_css + marker, 1)

    # validate balance
    if t.count("<![CDATA[") != t.count("]]>"):
        raise SystemExit("CDATA imbalance after edit")
    if t.count("<b:skin") != t.count("</b:skin>"):
        raise SystemExit("b:skin imbalance")

    OUT.write_text(t, encoding="utf-8", newline="\n")
    OUT_MIN.write_text(t, encoding="utf-8", newline="\n")
    print("Wrote", OUT)
    print("Wrote", OUT_MIN)
    print("size", len(t))
    print("DONE - safe theme ready")


if __name__ == "__main__":
    main()
