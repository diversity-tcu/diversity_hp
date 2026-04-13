#!/usr/bin/env python3
"""Sync frontmatter slug to filename for all content, and re-extract
SiteOrigin page content from the mirror HTML."""
from __future__ import annotations
import os, re, sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path("/home/sekiguchi/GitHub/diversity_hp")
CONTENT = ROOT / "src/content"
MIRROR = ROOT / "mirror/www.diversity.tcu.ac.jp"

FM_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
SLUG_RE = re.compile(r'^slug:\s*"(.*?)"\s*$', re.M)


def read_md(p: Path):
    text = p.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return None, text, text
    return m.group(1), m.group(2), text


def write_md(p: Path, fm: str, body: str):
    p.write_text(f"---\n{fm}\n---\n{body}", encoding="utf-8")


def sync_slugs():
    n = 0
    for coll in ("pages", "news", "events"):
        for p in (CONTENT / coll).glob("*.md"):
            fm, body, _ = read_md(p)
            if fm is None:
                continue
            slug_val = p.stem
            if SLUG_RE.search(fm):
                new_fm = SLUG_RE.sub(f'slug: "{slug_val}"', fm)
            else:
                new_fm = fm + f'\nslug: "{slug_val}"'
            if new_fm != fm:
                write_md(p, new_fm, body)
                n += 1
    print(f"synced slug frontmatter in {n} files")


def mirror_path_for(slug: str, original_url: str | None):
    # Try original_url first
    candidates = []
    if original_url:
        m = re.match(r"https?://www\.diversity\.tcu\.ac\.jp/(.*)", original_url)
        if m:
            path = m.group(1).strip("/")
            if path:
                candidates.append(MIRROR / path / "index.html")
                candidates.append(MIRROR / (path + ".html"))
            else:
                candidates.append(MIRROR / "index.html")
    candidates.append(MIRROR / slug / "index.html")
    candidates.append(MIRROR / (slug + ".html"))
    for c in candidates:
        if c.exists():
            return c
    return None


def rewrite_urls(html: str) -> str:
    html = html.replace("https://www.diversity.tcu.ac.jp/wp-content/uploads/", "/uploads/")
    html = html.replace("http://www.diversity.tcu.ac.jp/wp-content/uploads/", "/uploads/")
    # internal links
    html = re.sub(r'https?://www\.diversity\.tcu\.ac\.jp/', '/', html)
    return html


def extract_content(html_path: Path) -> str | None:
    html = html_path.read_text(encoding="utf-8", errors="replace")
    s = BeautifulSoup(html, "html.parser")
    # Prefer the entry-body (contains panel-layout)
    el = s.select_one("div.entry-body")
    if not el:
        # fallback: .mainSection
        el = s.select_one(".mainSection .post, .mainSection")
    if not el:
        el = s.select_one("main") or s.select_one("article")
    if not el:
        return None
    # remove script tags
    for t in el.find_all(["script"]):
        t.decompose()
    out = str(el)
    return rewrite_urls(out)


def extract_siteorigin_pages():
    success, fail, failed = 0, 0, []
    for p in sorted((CONTENT / "pages").glob("*.md")):
        fm, body, _ = read_md(p)
        if fm is None or "siteorigin" not in body:
            continue
        m = re.search(r'^original_url:\s*"(.*?)"', fm, re.M)
        orig = m.group(1) if m else None
        mp = mirror_path_for(p.stem, orig)
        if not mp:
            fail += 1
            failed.append((p.name, "no mirror"))
            continue
        content = extract_content(mp)
        if not content:
            fail += 1
            failed.append((p.name, f"no entry-body in {mp}"))
            continue
        write_md(p, fm, "\n" + content + "\n")
        success += 1
    print(f"re-extracted: {success} success, {fail} failed")
    for f in failed:
        print("  FAIL:", f)


if __name__ == "__main__":
    sync_slugs()
    extract_siteorigin_pages()
