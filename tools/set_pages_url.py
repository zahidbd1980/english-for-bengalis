#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper: print suggested GitHub Pages URL and optionally patch blogger_config.json asset_base_url.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
CONFIG = TOOLS / "blogger_config.json"
ROOT = TOOLS.parent


def pages_url(user: str, repo: str) -> str:
    user = user.strip().strip("/")
    repo = repo.strip().strip("/")
    return f"https://{user}.github.io/{repo}"


def patch_config(url: str) -> None:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    data["asset_base_url"] = url.rstrip("/")
    CONFIG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Updated tools/blogger_config.json asset_base_url =", data["asset_base_url"])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--user", required=True, help="GitHub username")
    p.add_argument("--repo", required=True, help="Repository name")
    p.add_argument("--write-config", action="store_true", help="Write asset_base_url into blogger_config.json")
    args = p.parse_args()
    url = pages_url(args.user, args.repo)
    print("GitHub Pages URL (after Pages is enabled):")
    print(" ", url + "/")
    print("Asset base for Blogger:")
    print(" ", url)
    if args.write_config:
        patch_config(url)


if __name__ == "__main__":
    main()
